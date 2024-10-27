import datetime
import glob
import json
import os
import re
import traceback
from typing import Dict

import zhipuai
from Srt import by_start_time, load_srt_from_str, load_srt_fromfile, reidnex, save_srt

from rsnm_log import LogColors, setup_logging
from translation_engine import TranslationEngine
from translator import Media, Subtitle, Translator, save_file
from zhipu_ai_fy import ZhipuEngine

logger = setup_logging()


def subtitle_message(
    message: str, textpack: int = 0, timecount: int = 0, sleep_time: int = 0, **text
):
    """
    消息回调

    Args:
        message (str): _description_
    """
    time1 = datetime.datetime.now() + datetime.timedelta(seconds=int(message))

    text1 = f'total time: {message} sec,endtime:{
        time1.strftime("%Y-%m-%d %H:%M:%S")}'
    print(text1)
    return


def extract_number(filename):
    match = re.search(r"pack\.(\d{3})\.txt", filename)
    if match:
        return int(match.group(1))  # 返回数字部分作为整数
    else:
        raise ValueError(f"No valid number found in filename: {filename}")


def make_packs(sub: Subtitle, max_package_size: int):
    # packs处理也需要存盘，原因是ai有时候会因为分句而串行，需要修正

    # 初始化一个空列表来存储结果
    result = []
    # 初始化一个临时字符串来存储当前段落的总长度
    current_length = 0
    # 初始化一个临时列表来存储当前段落
    current_segment = []

    # 原始文件名
    filename = sub.subtitle_fname
    # 获取文件的基本名称（不包括扩展名）
    base_name = os.path.splitext(filename)[0]
    base_00_file = f"{base_name}.pack.000.txt"
    if os.path.exists(base_00_file):
        # 使用glob模块获取当前目录下所有匹配的文件

        pattern = f"{base_name}.pack.[0-9][0-9][0-9].txt"
        files = glob.glob(pattern)
        # 使用正则表达式提取文件名中的数字部分

        # 根据提取的数字对文件列表进行排序
        try:
            sorted_files = sorted(files, key=extract_number)
            # 加载到result中
            for file in sorted_files:
                with open(file, "r", encoding="utf-8") as f:
                    result.append(f.read())
        except Exception as e:
            logger.error(
                f"{LogColors.ERROR.value}"
                f"加载pack字幕文件{filename}错误，{e}\n"
                f"traceback:{traceback.format_exc()}\n"
                f"{LogColors.RESET_COLOR.value}"
            )
            result = []
    else:
        # 遍历subblocks中的每个subblock
        for subblock in sub.subblocks:
            # 将subblock转换为字符串并计算其长度
            subblock_str = str(subblock)
            subblock_str_length = len(subblock_str)
            # 如果当前段落加上这个subblock的字符串长度不会超过max_count，则添加到当前段落
            if current_length + subblock_str_length + 1 <= max_package_size:
                current_segment.append(subblock_str)
                current_length += subblock_str_length + 1
            else:
                # 否则，将当前段落添加到结果列表，并开始一个新的段落
                result.append("\n".join(current_segment))
                current_segment = []
                current_segment.append(subblock_str)
                current_length = subblock_str_length
                # 重置当前长度，并加上分隔符的长度

        # 不要忘记添加最后一个段落，如果它不为空
        if current_segment:
            result.append("\n".join(current_segment))
        result = [x.strip() for x in result if x.strip()]

        # 将结果写入新的文件中
        for index, item in enumerate(result):
            newfilename = f"{base_name}.pack.{index:03d}.txt"
            with open(newfilename, "w", encoding="utf-8") as f:
                f.write(item)

    return result


def make_double_lanague_subtitle(
    media: str,
    from_sub: str,
    to_sub: str,
    translate_engner: TranslationEngine,
    from_language: str = "en",
    to_language: str = "zh",
    messagefun=subtitle_message,
    sleep_time=30,
    max_package_size=1024,
) -> str:
    """
    制作双语字幕

    Args:
        media (str): 电影名称
        from_sub (str): 源字幕
        to_sub (str): 目的字幕
        err_text (str): 翻译中错误存储文件
        dict_text (str): 词典文件
        from_language (str, optional):源语言 Defaults to 'en'.
        to_language (str, optional): 目的语言 Defaults to 'zh'.
        messagefun (_type_, optional): 翻译过程中回调函数，提供翻译进度  Defaults to subtitle_message.
        translate_engner (_type_, optional): 翻译引擎 Defaults to Baidufree.
        sleep_time (int, optional): 每用一次引擎，休眠时间，防止引擎拒绝 Defaults to 30.
        max_package_size (int, optional): 翻译包的大小，是把每个小句子组合为大的数据包后大小， Defaults to 1024.

    Returns:
        str: _description_
    """

    assert isinstance(translate_engner, TranslationEngine)

    movie1 = Media(media)
    movie1.add_subtitle(from_language, from_sub)
    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)

    textpack = []
    srt_list = []
    err_list = []

    match translate_engner.__class__.__name__:
        case "BaiduEngine":
            sub.make_sentence()
            textlist = sub.get_sentences_text()

            textpack = Translator.make_fanyi_packge(
                full_sentences=textlist,
                engine=translate_engner,
                string_max=max_package_size,
            )
            textpack = [s.strip() for s in textpack if s.strip()]
        case "ZhipuEngine":
            t_engine: ZhipuEngine
            assert isinstance(translate_engner, ZhipuEngine)
            t_engine = translate_engner
            # 分段处理也需要存盘，原因是ai有时候会因为分句而串行，需要修正，
            textpack = make_packs(sub=sub, max_package_size=max_package_size)

            # 这里是一组包，需要一个一个的翻译。
            pack_count = 0
            for item in textpack:
                savefilename = f"{media}.{len(textpack):03d}.{pack_count:03d}.txt"
                err_savefilename = (
                    f"{media}.{len(textpack):03d}.{pack_count:03d}.err.txt"
                )
                logger.info(
                    f"{LogColors.INFO.value}{media},翻译第{pack_count}组，共{len(textpack)}组{LogColors.RESET_COLOR.value}"
                )

                # 如果不存在savefilename文件，则翻译
                if not os.path.exists(savefilename):
                    messagefun(
                        f"{len(textpack)-pack_count}",
                        len(textpack),
                        pack_count,
                        sleep_time,
                    )

                    fanyiret = t_engine.translate(
                        item, from_language, to_language, sleep_time
                    )

                    if fanyiret:
                        # 有结果，保存文件savefilename
                        save_file(savefilename, fanyiret)
                    else:
                        logger.error(
                            f"{LogColors.ERROR.value}"
                            f"翻译失败，{media},翻译第{pack_count}组，共{len(textpack)}组"
                            f"{LogColors.RESET_COLOR.value}"
                        )
                        save_file(err_savefilename, item)
                        err_list.append(err_savefilename)

                # 如果存在savefilename文件，则加载
                if os.path.exists(savefilename):
                    # 打开savefilename文件读取内容
                    user_srt = load_srt_from_str(str(item).encode("utf-8"))
                    result_srt = load_srt_fromfile(savefilename)

                    # 检查翻译结果是否与原文srt行数一致
                    if len(user_srt) == len(result_srt):
                        srt_list.append(result_srt)
                    else:
                        logger.error(
                            f"{LogColors.ERROR.value}"
                            f"翻译结果与原文行数不一致，{len(user_srt)}-{len(result_srt)}，请检查翻译结果文件:{savefilename}"
                            f"{LogColors.RESET_COLOR.value}"
                        )
                        err_list.append(savefilename)

                pack_count += 1

            if len(err_list) > 0:
                logger.error(
                    f"{LogColors.ERROR.value}"
                    f"翻译失败，有{len(err_list)}个错误，检查错误文件和log文件。\n{'\n'.join(err_list)}"
                    f"{LogColors.RESET_COLOR.value}"
                )

                # 要抛出异常，让调用者处理，要修复字幕文件
                raise Exception(
                    "翻译失败，有错误，请检查错误文件和log文件，需要修复字幕文件，详见readme里修复部分"
                )
            else:
                new_srts = [item for sublist in srt_list for item in sublist]
                new_srts.sort(key=by_start_time)
                reidnex(new_srts)

                save_srt(fname=to_sub, subtitles=new_srts)

    return to_sub
