import datetime
import json
import os
from typing import Dict

from Srt import save_srt

from rsnm_log import setup_logging
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
    sub.make_sentence()
    textlist = sub.get_sentences_text()

    textpack = Translator.make_fanyi_packge(
        full_sentences=textlist, engine=translate_engner, string_max=max_package_size
    )

    fdict: Dict[str, str] = {}
    if use_dict:
        dict1 = TranslationDict()
        dict1.dict_load(dict_text)
        fdict = dict1.dict
    else:
        # 这里是一组包，需要一个一个的翻译。
        timecount = 0
        for item in textpack:
            savefilename = f"{media}.{len(textpack)}.{timecount}.txt"
            

            json_string = t_engine.make_output_json(item)
            fanyi_text = ""

            # 如果存在savefilename文件，则加载
            if os.path.exists(savefilename):
                # 打开savefilename文件读取内容
                with open(savefilename, "r", encoding="utf-8") as fp:
                    fanyi_text = fp.read()
            else:
                messagefun(
                    f"{len(textpack)-timecount}", len(textpack), timecount, sleep_time
                )

                json_string = t_engine.make_output_json(item)
                fanyiret = t_engine.translate(
                    json_string, from_language, to_language, sleep_time
                )
                if fanyiret is None:
                    fanyi_text = ""
                    logger.info("翻译失败")
                    logger.info(
                        f"{savefilename} 翻译失败,请修改，修改内容要和原文字数一样。"
                    )
                else:
                    fanyi_text, _ = fanyiret
                    # 保存文件savefilename
                    save_file(savefilename, fanyi_text)

            if fanyi_text:
                temp_dict = t_engine.make_fanyi_dict(fanyi_text, json_string)
                fdict.update(temp_dict)
            timecount += 1

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
