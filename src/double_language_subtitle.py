from Srt import save_srt
from translator import GoogleFree
from translator import (Media, MergeSentence, NormalSentence, Sentence,
                        SubBlock, Subtitle, Translator, save_file, languages)


def make_double_lanague_subtitle(media: str,
                                 from_sub: str,
                                 to_sub: str,
                                 err_text: str,
                                 dict_text: str,
                                 from_language: str = 'en',
                                 to_language: str = 'zh-CN') -> str:
    '''
    _summary_

    Args:
        media (_type_): _description_
        from_sub (_type_): _description_
        to_sub (_type_): _description_
        err_text (_type_): _description_
        dict_text (_type_): _description_
        from_language (str, optional): _description_. Defaults to 'en'.
        to_language (str, optional): _description_. Defaults to 'zh-CN'.

    Returns:
        str: _description_
    '''
    movie1 = Media(media)
    movie1.add_subtitle(from_language, from_sub)

    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)
    sub.make_sentence()
    textlist = sub.get_sentences_text()
    textpack = Translator.make_fanyi_packge(textlist)

    fdict = dict()
    translate1 = GoogleFree()
    # 这里是一组包，需要一个一个的翻译。
    for item in textpack:
        fanyiret = translate1.translate(item, 'auto')
        fanyi_text, _ = fanyiret
        dict1 = Translator.make_fanyi_dict(fanyi_text)
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


make_double_lanague_subtitle(media='movie a12', from_sub='indata/a12.en.srt',
                             to_sub='outdata/a12.cn.srt', err_text='outdata/a12.err.txt',
                             dict_text='outdata/a12.dict.txt')
