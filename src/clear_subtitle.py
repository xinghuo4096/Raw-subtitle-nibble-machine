
import re

from Srt import reidnex, save_srt

from translator import Media, Subtitle


def clear_subtile_fun1(fname1: str, fname2: str):
    '''
    清除字幕里的[]里面的字符，一般是声音或音乐的描述。如：[ Wind blowing ][ Sighs ]
    '''
    CLEAR_TEXT_MARK1 = r'\[[^\]]+?\]'

    movie1 = Media(f'movie {fname1}')
    movie1.add_subtitle('en', fname1)
    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)

    for item in sub.subblocks:
        str1 = item.text
        str1 = re.sub(CLEAR_TEXT_MARK1, '', str1)
        str1 = str1.strip()
        if not re.search(r'\w+', str1):
            str1 = ''
        item.text = str1

    sub2 = list()
    for item in sub.subblocks:
        if item.text:
            sub2.append(item)
    reidnex(sub2)
    save_srt(fname2, sub2)


def clear_subtitle():
    '''
    清除字幕里的特殊字符。
    '''
    return

    # CLEAR_TEXT_MARK1 = r'\[[^\]]+?\]'

    # CLEAR_TEXT_MARK4 = r'<i>.+?music.+?</i>'
    # str1 = re.search(CLEAR_TEXT_MARK4, '<i> upbeat music playing </i>')

    # for i in range(1, 11):
    #     srtname = f'z:/tests/1/The.Man.Who.Fell.to.Earth.S01E{i:0>2}.1080p.WEBRip.x265-RARBG.srt'
    #     srtname_en = f'z:/tests/1/The.Man.Who.Fell.to.Earth.S01E{i:0>2}.1080p.WEBRip.x265-RARBG.en.srt'
    #     movie1 = Media(f'movie {i}')
    #     movie1.add_subtitle('en', srtname)
    #     sub = movie1.subtitles[0]
    #     assert isinstance(sub, Subtitle)

    #     for item in sub.subblocks:
    #         str1 = item.text
    #         str1 = re.sub(CLEAR_TEXT_MARK1, '', str1)
    #         str1 = re.sub(CLEAR_TEXT_MARK4, '', str1)
    #         str1 = str1.replace(r'{\an8}', '')
    #         str1 = str1.replace('<i>', '')
    #         str1 = str1.replace('</i>', '')
    #         str1 = str1.strip()
    #         if not re.search(r'\w+', str1):
    #             str1 = ''
    #         item.text = str1

    #     sub2 = list()
    #     for item in sub.subblocks:
    #         if item.text:
    #             sub2.append(item)
    #     reidnex(sub2)

    #     save_srt(srtname_en, sub2)
