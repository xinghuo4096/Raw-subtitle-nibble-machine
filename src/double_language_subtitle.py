import datetime

from Srt import save_srt

from translator import Media, Subtitle, TranslationDict, Translator, save_file
from translation_engine import TranslationEngine
from baidu_ce_fy import BaiduceEngine


def subtitle_message(message: str, **text):
    '''
    消息回调

    Args:
        message (str): _description_
    '''
    time1 = datetime.datetime.now() + datetime.timedelta(seconds=int(message))

    text1 = f'total time: {message} sec,endtime:{ time1.strftime("%Y-%m-%d %H:%M:%S")}'
    print(text1)
    return


def make_double_lanague_subtitle(
    media: str,
    from_sub: str,
    to_sub: str,
    err_text: str,
    dict_text: str,
    from_language: str = "en",
    to_language: str = "zh",
    glossary_file: str = "",
    messagefun=subtitle_message,
    use_dict: bool = False,
    translate_engner: TranslationEngine = None,
    sleep_time=30,
) -> str:
    '''
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

    Returns:
        str: _description_
    '''

    assert isinstance(translate_engner, TranslationEngine)

    tengine = translate_engner
    movie1 = Media(media)
    movie1.add_subtitle(from_language, from_sub)

    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)
    sub.make_sentence()
    textlist = sub.get_sentences_text()

    # TODO 增加短句子凑成翻译包大小的选择，为了AI翻译，需要将翻译包大小设置为2000
    textpack = Translator.make_fanyi_packge(textlist)

    fdict = dict()
    if use_dict:
        dict1 = TranslationDict()
        dict1.dict_load(dict_text)
        fdict = dict1.dict
    else:
        # 这里是一组包，需要一个一个的翻译。
        timecount = 0
        for item in textpack:
            messagefun(f'{(len(textpack)-timecount)*sleep_time}')
            timecount += 1
            fanyiret = tengine.translate(item, from_language, to_language,
                                         sleep_time)
            fanyi_text, _ = fanyiret
            dict1 = tengine.make_fanyi_dict(fanyi_text)
            fdict.update(dict1)

    subcn = movie1.add_language_subtitle("zh-CN")
    assert subcn == movie1.subtitles[1]
    assert isinstance(subcn, Subtitle)

    err_texts = Translator.translate_byte_dict(subcn, fdict)
    if len(err_texts) > 0:
        save_file(err_text, '\n'.join(err_texts))

    save_srt(to_sub, subcn.subblocks)
    # pylint:disable=consider-using-f-string
    strlist = ['{0}\n{1}'.format(x, fdict[x]) for x in list(fdict)]

    save_file(dict_text, '\n'.join(strlist))
