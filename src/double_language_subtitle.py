import datetime
import re

from Srt import reidnex, save_srt

from translator import (GoogleFree, Media,  Subtitle, Translator, save_file)


def subtitle_message(message: str, **text):
    '''
    消息回调

    Args:
        message (str): _description_
    '''
    text = f'total time:{message},endtime:{datetime.datetime.now()+datetime.timedelta(seconds= int(message))}'
    print(text)
    return


def make_double_lanague_subtitle(media: str,
                                 from_sub: str,
                                 to_sub: str,
                                 err_text: str,
                                 dict_text: str,
                                 from_language: str = 'en',
                                 to_language: str = 'zh-CN',
                                 messagefun=subtitle_message) -> str:
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
        messagefun:消息回调

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
    timecount = 0
    for item in textpack:
        sleeptime = 3
        messagefun(f'{(len(textpack)-timecount)*sleeptime}')
        timecount += 1
        fanyiret = translate1.translate(item, 'auto', 'zh-CN', sleeptime)
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


def clear_subtitle():
    '''
    清除字幕里的特殊字符。
    '''
    CLEAR_TEXT_MARK1 = r'\[[^\]]+?\]'

    CLEAR_TEXT_MARK4 = r'<i>.+?music.+?</i>'
    str1 = re.search(CLEAR_TEXT_MARK4, '<i> upbeat music playing </i>')

    for i in range(1, 11):
        srtname = f'z:/tests/1/The.Man.Who.Fell.to.Earth.S01E{i:0>2}.1080p.WEBRip.x265-RARBG.srt'
        srtname_en = f'z:/tests/1/The.Man.Who.Fell.to.Earth.S01E{i:0>2}.1080p.WEBRip.x265-RARBG.en.srt'
        movie1 = Media(f'movie {i}')
        movie1.add_subtitle('en', srtname)
        sub = movie1.subtitles[0]
        assert isinstance(sub, Subtitle)

        for item in sub.subblocks:
            str1 = item.text
            str1 = re.sub(CLEAR_TEXT_MARK1, '', str1)
            str1 = re.sub(CLEAR_TEXT_MARK4, '', str1)
            str1 = str1.replace(r'{\an8}', '')
            str1 = str1.replace('<i>', '')
            str1 = str1.replace('</i>', '')
            str1 = str1.strip()
            if not re.search(r'\w+', str1):
                str1 = ''
            item.text = str1

        sub2 = list()
        for item in sub.subblocks:
            if item.text:
                sub2.append(item)
        reidnex(sub2)

        save_srt(srtname_en, sub2)


def main_batch():
    '''
    批处理
    '''
    for i in range(1, 9):
        print(i)
        fname = f'z:/tests/a/test.S01E{i:0>2}.'

        make_double_lanague_subtitle(media=f'movie {i}',
                                     from_sub=f'{fname}.en.srt',
                                     to_sub=f'{fname}.cn.srt',
                                     err_text=f'{fname}.err.txt',
                                     dict_text=f'{fname}.dict.txt')


def mymain():
    '''
    单个处理
    '''
    fname = 'z:/tests/a/test'
    make_double_lanague_subtitle(media=f'movie {fname}',
                                 from_sub=f'{fname}.en.srt',
                                 to_sub=f'{fname}.cn.srt',
                                 err_text=f'{fname}.err.txt',
                                 dict_text=f'{fname}.dict.txt')


main_batch()
