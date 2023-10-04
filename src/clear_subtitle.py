"""字幕预处理
一些字幕有特殊字符，需要其他预处理
"""
import json
import os
import pathlib
import re

from Srt import reidnex, save_srt

from translator import Media, Subtitle, glossary_do1, glossary_do2


def clear_subtile_fun1(fname1: str, fname2: str):
    """
    清除字幕里的[]里面的字符，一般是声音或音乐的描述。如：[ Wind blowing ][ Sighs ]

    清除字幕里的<i></i>，替换为空格。

    清除字幕里的{\an8}，替换为空。
    """
    CLEAR_TEXT_MARK1 = r"\[[^\]]+?\]|\([^\)]+?\)"
    CLEAR_TEXT_MARK2 = r"</*i>"
    CLEAR_TEXT_MARK3 = r"{\\an8}"

    movie1 = Media(f"movie {fname1}")
    movie1.add_subtitle("en", fname1)
    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)

    for item in sub.subblocks:
        str1 = item.text
        str1 = re.sub(CLEAR_TEXT_MARK1, "", str1)
        str1 = re.sub(CLEAR_TEXT_MARK2, " ", str1)
        str1 = re.sub(CLEAR_TEXT_MARK3, "", str1)
        str1 = str1.strip()
        if not re.search(r"\w+", str1):
            str1 = ""
        item.text = str1

    sub2 = list()
    for item in sub.subblocks:
        if item.text:
            sub2.append(item)
    reidnex(sub2)
    save_srt(fname2, sub2)


def clear_subtile_fun2(fname1: str, fname2: str):
    """
    为字幕里包含'♪'字符时，字幕末尾加结束符'.'
    如：-♪ Don't let me hear you sighin' ♪
    处理为：-♪ Don't let me hear you sighin' ♪.

    """
    TEXT_MARK = r"♪"

    movie1 = Media(f"movie {fname1}")
    movie1.add_subtitle("en", fname1)
    sub = movie1.subtitles[0]
    assert isinstance(sub, Subtitle)

    for item in sub.subblocks:
        str1 = item.text
        if str1.find(TEXT_MARK) != -1:
            str1 = str1.strip()
            str1 = str1 + "."
        if not re.search(r"\w+", str1):
            str1 = ""
        item.text = str1

    sub2 = list()
    for item in sub.subblocks:
        if item.text:
            sub2.append(item)
    reidnex(sub2)
    save_srt(fname2, sub2)


def make_subtile_glossary_fun1(fname1: str, fname2: str, glossary_file: str):
    """
    为字幕里处理术语fun1
    """
    json_data = '{}'

    str1 = ''
    with open(file=fname1, mode="r", buffering=1000, encoding="utf-8") as ff1:
        str1 = ff1.read()

    if os.path.isfile(glossary_file):
        with open(glossary_file, encoding='utf-8') as file1:
            json_data = json.load(file1)
        str1 = glossary_do1(str1, json_data)

    with open(file=fname2, mode="w", buffering=1000, encoding="utf-8") as ff1:
        ff1.write(str1)


def make_subtile_glossary_fun2(fname1: str, fname2: str, glossary_file: str):
    """
    为字幕里处理术语fun2
    """
    json_data = '{}'

    str1 = ''
    with open(file=fname1, mode="r", buffering=1000, encoding="utf-8") as ff1:
        str1 = ff1.read()

    if os.path.isfile(glossary_file):
        with open(glossary_file, encoding='utf-8') as file1:
            json_data = json.load(file1)
        str1 = glossary_do2(str1, json_data)

    with open(file=fname2, mode="w", buffering=1000, encoding="utf-8") as ff1:
        ff1.write(str1)


def clear_subtitle():
    """
    清除字幕里的特殊字符。
    """
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
