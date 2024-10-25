import datetime
import json
import os
import traceback
from typing import Dict

import zhipuai
from Srt import save_srt

from rsnm_log import LogColors, setup_logging
from translation_engine import TranslationEngine
from translator import Media, Subtitle, TranslationDict, Translator, save_file

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
    logger.info(text1)
    return


def make_double_lanague_subtitle(
    media: str,
    from_sub: str,
    to_sub: str,
    err_text: str,
    dict_text: str,
    translate_engner: TranslationEngine,
    from_language: str = "en",
    to_language: str = "zh",
    glossary_file: str = "",
    messagefun=subtitle_message,
    use_dict: bool = False,
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
        glossary_file:术语文件,
        messagefun (_type_, optional): 翻译过程中回调函数，提供翻译进度  Defaults to subtitle_message.
        use_dict (bool, optional): 是否是词典翻译 Defaults to False.
        translate_engner (_type_, optional): 翻译引擎 Defaults to Baidufree.
        sleep_time (int, optional): 每用一次引擎，休眠时间，防止引擎拒绝 Defaults to 30.
        max_package_size (int, optional): 翻译包的大小，是把每个小句子组合为大的数据包后大小， Defaults to 1024.

    Returns:
        str: _description_
    """

    assert isinstance(translate_engner, TranslationEngine)

    t_engine = translate_engner
    movie1 = Media(media)
    movie1.add_subtitle(from_language, from_sub)

    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)
    textpack = []

    match t_engine.__class__.__name__:
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
            max_count = 2048

            # 初始化一个空列表来存储结果
            result = []
            # 初始化一个临时字符串来存储当前段落的总长度
            current_length = 0
            # 初始化一个临时列表来存储当前段落
            current_segment = []

            # 遍历subblocks中的每个subblock
            for subblock in sub.subblocks:
                # 将subblock转换为字符串并计算其长度
                subblock_str = str(subblock)
                subblock_str_length = len(subblock_str)
                # 如果当前段落加上这个subblock的字符串长度不会超过max_count，则添加到当前段落
                if current_length + subblock_str_length + 1 <= max_count:
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

            textpack = result
            print(textpack)

    fdict: Dict[str, str] = {}
    if use_dict:
        dict1 = TranslationDict()
        dict1.dict_load(dict_text)
        fdict = dict1.dict
    else:
        # 这里是一组包，需要一个一个的翻译。
        pack_count = 0
        for item in textpack:
            savefilename = f"{media}.{len(textpack)}.{pack_count}.txt"
            err_savefilename = f"{media}.{len(textpack)}.{pack_count}.err.txt"
            logger.info(
                f"{LogColors.INFO.value}{media},翻译第{pack_count}组，共{len(textpack)}组{LogColors.RESET_COLOR.value}"
            )

            fanyi_dict: Dict[str, str] = {}

            # 如果存在savefilename文件，则加载
            if os.path.exists(savefilename):
                # 打开savefilename文件读取内容

                with open(savefilename, "r", encoding="utf-8") as fp:
                    fanyi_dict = json.load(fp)
            else:
                messagefun(
                    f"{len(textpack)-pack_count}", len(textpack), pack_count, sleep_time
                )

                fanyiret = t_engine.translate(
                    item, from_language, to_language, sleep_time
                )
                if fanyiret is None:
                    logger.warning(
                        f"{LogColors.WARNING.value}"
                        f"翻译失败，{LogColors.INFO.value}{media},翻译第{pack_count}组，共{len(textpack)}组{LogColors.RESET_COLOR.value}，请检查日志翻译引擎放回的错误信息：\n"
                        f"{LogColors.RESET_COLOR.value}"
                    )
                    save_file(err_savefilename, item)
                else:
                    fanyi_dict = fanyiret
                    # 保存文件savefilename
                    fanyi_json = json.dumps(fanyi_dict, ensure_ascii=False, indent=4)
                    save_file(savefilename, fanyi_json)

            if fanyi_dict:
                fdict.update(fanyi_dict)
            pack_count += 1

    subcn = movie1.add_language_subtitle("zh-CN")
    assert subcn == movie1.subtitles[1]
    assert isinstance(subcn, Subtitle)

    err_texts = Translator.translate_byte_dict(subcn, fdict)
    if len(err_texts) > 0:
        save_file(err_text, "\n".join(err_texts))

    save_srt(to_sub, subcn.subblocks)
    # pylint:disable=consider-using-f-string
    strlist = ["{0}\n{1}".format(x, fdict[x]) for x in list(fdict)]

    save_file(dict_text, "\n".join(strlist))
    return to_sub
