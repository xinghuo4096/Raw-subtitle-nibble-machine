"""
翻译

Raises:
    Exception: _description_
Returns:
    _type_: _description_
"""

import copy
import re
from typing import Dict
from urllib.parse import quote

from Srt import Srt, detect_code, load_srt_fromfile

from baidu_ce_fy import BaiduceEngine
from translation_engine import TranslationEngine

SENCTENCE_END_MARK = r"[\w ]+[\[\]*()?.!♪]"
RE_FIND = re.compile(SENCTENCE_END_MARK)
CLEAR_MARK = r"[!?.]?\s+"
RE_CLEAR = re.compile(CLEAR_MARK)
CHINESE_MARK = r"[，。？]|……"
RE_CHINESE_MARK = re.compile(CHINESE_MARK)
languages = dict(
    {
        "auto": "auto",
        "af": "Afrikaans",
        "sq": "Albanian",
        "am": "Amharic",
        "ar": "Arabic",
        "hy": "Armenian",
        "az": "Azerbaijani",
        "eu": "Basque",
        "be": "Belarusian",
        "bn": "Bengali",
        "bs": "Bosnian",
        "bg": "Bulgarian",
        "ca": "Catalan",
        "ceb": "Cebuano",
        "zh-CN": "Chinese (Simplified)",
        "zh-TW": "Chinese (Traditional)",
        "co": "Corsican",
        "hr": "Croatian",
        "cs": "Czech",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "eo": "Esperanto",
        "et": "Estonian",
        "fi": "Finnish",
        "fr": "French",
        "fy": "Frisian",
        "gl": "Galician",
        "ka": "Georgian",
        "de": "German",
        "el": "Greek",
        "gu": "Gujarati",
        "ht": "Haitian Creole",
        "ha": "Hausa",
        "haw": "Hawaiian",
        "he": "Hebrew",
        "hi": "Hindi",
        "hmn": "Hmong",
        "hu": "Hungarian",
        "is": "Icelandic",
        "ig": "Igbo",
        "id": "Indonesian",
        "ga": "Irish",
        "it": "Italian",
        "ja": "Japanese",
        "jv": "Javanese",
        "kn": "Kannada",
        "kk": "Kazakh",
        "km": "Khmer",
        "rw": "Kinyarwanda",
        "ko": "Korean",
        "ku": "Kurdish",
        "ky": "Kyrgyz",
        "lo": "Lao",
        "la": "Latin",
        "lv": "Latvian",
        "lt": "Lithuanian",
        "lb": "Luxembourgish",
        "mk": "Macedonian",
        "mg": "Malagasy",
        "ms": "Malay",
        "ml": "Malayalam",
        "mt": "Maltese",
        "mi": "Maori",
        "mr": "Marathi",
        "mn": "Mongolian",
        "my": "Myanmar (Burmese)",
        "ne": "Nepali",
        "no": "Norwegian",
        "ny": "Nyanja (Chichewa)",
        "or": "Odia (Oriya)",
        "ps": "Pashto",
        "fa": "Persian",
        "pl": "Polish",
        "pt": "Portuguese (Portugal, Brazil)",
        "pa": "Punjabi",
        "ro": "Romanian",
        "ru": "Russian",
        "sm": "Samoan",
        "gd": "Scots Gaelic",
        "sr": "Serbian",
        "st": "Sesotho",
        "sn": "Shona",
        "sd": "Sindhi",
        "si": "Sinhala (Sinhalese)",
        "sk": "Slovak",
        "sl": "Slovenian",
        "so": "Somali",
        "es": "Spanish",
        "su": "Sundanese",
        "sw": "Swahili",
        "sv": "Swedish",
        "tl": "Tagalog (Filipino)",
        "tg": "Tajik",
        "ta": "Tamil",
        "tt": "Tatar",
        "te": "Telugu",
        "th": "Thai",
        "tr": "Turkish",
        "tk": "Turkmen",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "ug": "Uyghur",
        "uz": "Uzbek",
        "vi": "Vietnamese",
        "cy": "Welsh",
        "xh": "Xhosa",
        "yi": "Yiddish",
        "yo": "Yoruba",
        "zu": "Zulu",
    }
)


class Translator:
    """
    翻译
    """

    def __init__(self):
        pass

    @staticmethod
    def make_fanyi_packge(
        full_sentences: list, engine: TranslationEngine, string_max=1024
    ):
        """
        make_fanyi_packge 短句子打包为翻译引擎一次可以识别的最大量包
        比如有些翻译引擎一行不能超过5000字符，超过报错。
        ai的翻译引擎根据模型，输出token量不同，有的模型是1000，有的模型是2000，有的模型是4000。

        google是少于5000字符

        Arguments:
            full_sentences -- list，短句子列表list(str)，单句如果超过4988则报错。

        Returns:
            list，打好包的文本
        """
        fanyitexts = []
        length = 0
        full_sentence = []
        size_limite = string_max
        for item in full_sentences:
            text = item + "\n"

            if len(text) > string_max:
                raise Exception("error:to long." + item.text)
            if (length + len(text)) < size_limite:
                length += len(text)
                full_sentence.append(text)
            else:
                fanyitexts.append("".join(full_sentence))
                length = len(text)
                full_sentence = []
                full_sentence.append(text)
        if full_sentence:
            fanyitexts.append("".join(full_sentence))

        return fanyitexts

    @staticmethod
    def translate_byte_dict(subcnen, fdict, mode_="splite") -> list:
        """
        查字典的方法翻译

        如果是MergeSentence合并的句，翻译后，需要给没有结尾符号的subblock的text赋值。
        1个MergeSentence实例对应多个subblock实例，都要赋值。
        mode (str, optional): 拆分模式，默认是splite，其他模式就直接复制.
        Args:
            subcnen (_type_): _description_
            fdict (_type_): _description_
            mode (str, optional): 拆分模式，默认是splite，其他模式就直接复制.

        Returns:
            list: _description_
        """
        err_text = []
        for item in subcnen.subblocks:
            for st1 in item.sentences:
                if st1.text:
                    fanyi_text = fdict.get(st1.text, "")
                    if fanyi_text:
                        if isinstance(st1, NormalSentence):
                            item.text = fanyi_text
                        if isinstance(st1, SpliteSentence):
                            item.text = fanyi_text
                        if isinstance(st1, MergeSentence):
                            st1.splite_fanyi(fanyi_text, mode=mode_)
                    else:
                        err_text.append("fanyi error." + st1.text)
        return err_text


class Media:
    """
    影视剧集
    """

    def __init__(self, detail: str):
        self.detail = detail
        self.subtitles = list()

    def add_subtitle(self, language: str, subtitle_fname: str):
        """
        增加一个语言的字幕

        Args:
            language (str): _description_
            subtitle_fname (str): _description_

        Returns:
            _type_: _description_
        """
        sub = Subtitle(language, subtitle_fname)
        self.subtitles.append(sub)
        return sub

    def add_language_subtitle(self, language: str, index=0):
        """
        增加一种语言的字幕，其他部分从旧字幕deepcopy。

        Args:
            language (str): _description_
            index (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        sub = copy.deepcopy(self.subtitles[index])
        sub.language = language
        self.subtitles.append(sub)
        return sub


class Subtitle:
    """
    字幕。比如英语en，或者中文zh-cn
    """

    def __init__(self, language: str, subtitle_fname: str):
        self.subtitle_fname = subtitle_fname
        self.language = language
        self.language_detail = languages[language]

        subs = list()
        subs = load_srt_fromfile(self.subtitle_fname)
        self.subblocks = [SubBlock(x) for x in subs]

    def get_sentences_text(self) -> list:
        """
        得到字幕中所有句子文本

        Returns:
            list: _description_
        """
        slist = [x.get_sentences_text() for x in self.subblocks]
        slist = list(filter(None, slist))
        return slist

    def make_sentence(self):
        """
        解析字幕中的句子。
        """
        merge_strs = list()
        merge_subblocks = list()
        for item in self.subblocks:
            assert isinstance(item, SubBlock)

            if merge_strs:
                char_end = merge_strs[-1][-1]
                char_start = item.text[0]
                assert isinstance(char_end, str)
                if char_end.isalnum() and char_start.isalnum():
                    item.text = " " + item.text

            merge_strs.append(item.text)

            find = re.findall(RE_FIND, item.text)

            if (len(find)) == 0:
                # 没有结束，需要merge
                st1 = MergeSentence()
                st1.object_link(merge_subblocks)

                merge_subblocks.append(item)
                item.sentences = [st1]
            elif len(find) == 1:
                if len(merge_strs) == 1:
                    st1 = NormalSentence(merge_strs[0])

                    # sentence object link
                    st1.object_link([item])
                    # subblock object link
                    item.sentences = [st1]
                elif len(merge_strs) > 1:
                    st1 = MergeSentence("".join(merge_strs))
                    # sentence object link
                    merge_subblocks.append(item)
                    st1.object_link(merge_subblocks)
                    # subblock object link
                    item.sentences = [st1]

                merge_strs = list()
                merge_subblocks = list()
            elif len(find) > 1:
                if len(merge_strs) == 1:
                    st1 = NormalSentence(merge_strs[0])

                    # sentence object link
                    st1.object_link([item])
                    # subblock object link
                    item.sentences = [st1]
                else:
                    st1 = MergeSentence("".join(merge_strs))

                    # sentence object link
                    merge_subblocks.append(item)
                    st1.object_link(merge_subblocks)
                    # subblock object link
                    item.sentences = [st1]

                merge_strs = list()
                merge_subblocks = list()
        # 最后一句。
        item = self.subblocks[-1]
        if len(merge_strs) > 0:
            if len(merge_strs) == 1:
                st1 = NormalSentence(merge_strs[0])
                # sentence object link
                st1.object_link([item])
                # subblock object link
                item.sentences = [st1]
            else:
                st1 = MergeSentence("".join(merge_strs))

                # sentence object link
                merge_subblocks.append(item)
                st1.object_link(merge_subblocks)
                # subblock object link
                item.sentences = [st1]

            merge_strs = list()
            merge_subblocks = list()


class SubBlock(Srt):
    """
    字幕块类似

    ```text
    1
    0:1:45,380 --> 0:1:48,880
    -测试-1-测试-0:1:45,380-0:1:48,880
    ```
    Args:
        Srt (_type_): _description_
    """

    def __init__(self, srt: Srt):
        """
        从传入的srt对象，初始化。

        Args:
            srt (Srt): _description_
        """
        Srt.__init__(self, srt.index, "0:1:45,380 --> 0:1:48,880", srt.text)
        self.index = srt.index
        self.start_time = srt.start_time
        self.end_time = srt.end_time
        self.text = srt.text.strip()

        self.sentences = list()

    def get_sentences_text(self):
        """
        得到包含句子的文本

        Returns:
            _type_: _description_
        """
        assert isinstance(self.sentences, list)
        tlist = [x.text for x in self.sentences if x.text.strip()]
        if len(tlist) > 0:
            return "\n".join(tlist)
        else:
            return ""

    def clear_subtitle_text(self, str1):
        """
        去除字幕文本中句子结尾符号后带空白符的情况。
        如:'? ','! ','. '

        _extended_summary_

        Args:
            srt (_type_): _description_

        Returns:
            _type_: _description_
        """
        return re.sub(RE_CLEAR, SubBlock.match_clear, str1)

    @staticmethod
    def match_clear(match):
        """
        用于拆分subblock，的re.sub
        Args:
            match (_type_): _description_

        Returns:
            _type_: _description_
        """
        assert isinstance(match, re.Match)
        # pylint:disable=(superfluous-parens)
        return match.group()[0]


class Sentence(object):
    """
    抽象类
    """

    def __init__(self, text=""):
        self.text = text
        self.subblocks = list()

    def object_link(self, subblocks: list):
        """
        设置对象链接UML

        Args:
            subblocks (list): _description_
        """
        self.subblocks = subblocks


class MergeSentence(Sentence):
    """
    可以合并的句子。类似

        54
        00:03:01,190 --> 00:03:02,500
        After our session,

        55
        00:03:03,050 --> 00:03:05,140
        I had the sudden clarity that we were ready,

        56
        00:03:06,260 --> 00:03:07,330
        that I was ready.

    Args:
        Sentence (_type_): _description_
    """

    def splite_fanyi(self, text1: str, mode="splite"):
        """
         MergeSentence合并的句，翻译后，需要给没有结尾符号的subblock的text赋值。
         1个MergeSentence实例对应多个subblock实例，都要赋值。
        Args:
            mode (str, optional): 拆分模式，默认是splite，其他模式就直接复制.
            Defaults to 'splite'.
        """

        blk_count = len(self.subblocks)
        split_text = [text1] * blk_count

        strlist1 = []
        find = RE_CHINESE_MARK.search(text1)
        str_begin = 0

        while find:
            strlist1.append(text1[str_begin : find.end()])
            str_begin = find.end()
            find = RE_CHINESE_MARK.search(text1, str_begin)
        if str_begin < len(text1):
            strlist1.append(text1[str_begin:])

        if mode.lower() == "splite":
            if len(strlist1) == blk_count:
                split_text = strlist1

        subs = self.subblocks
        for i in range(blk_count):
            subs[i].text = split_text[i]

        return


class SpliteSentence(Sentence):
    """
    可以分开的句子。如 Okay. I gotta go.

    Args:
        Sentence (_type_): _description_
    """


class NormalSentence(Sentence):
    """
    普通句子。只有一个结束符在句子末尾。

    Args:
        Sentence (_type_): _description_
    """


class TranslationDict:
    """
    翻译词典
    """

    def __init__(self):
        self.dict: Dict[str, str] = {}
        self.glossary: Dict[str, str] = {}

    def dict_load(self, fname):
        """
        加载词典
        类似：

        hello
        你好

        Args:
            fname (_type_): _description_
        """
        file1 = open(fname, "r", encoding="utf-8")
        buffer = file1.readlines()
        file1.close()

        self.dict = {
            buffer[x].rstrip(): buffer[x + 1].rstrip()
            for x in range(0, len(buffer) - 1, 2)
        }

        return self.dict

    def glossary_load(self, fname):
        """
        加载glossary.utf-880
        类似：

        Tom Cruise
        阿汤哥

        Args:
            fname (_type_): _description_
        """
        file1 = open(fname, "rb")
        buffer = file1.read()
        file1.close()
        str1 = detect_code(buffer)[0]
        self.glossary = str1.splite["\n"]

    def glossary_after(self, texts: str) -> str:
        """
        翻译前的glossary处理.utf-8
        如:

        Tom Cruise
        阿汤哥

        Args:
            str1 (str): _description_
            fname (_type_): _description_

        Returns:
            str: _description_
        """
        return texts

    def glossary_before(self, texts: str) -> str:
        """
        翻译前的glossary处理.utf-8
        如:

        Tom Cruise
        阿汤哥

        Args:
            str1 (str): _description_
            fname (_type_): _description_

        Returns:
            str: _description_
        """
        return texts


def glossary_do1(string, glossary_json):
    """
    术语支持。在翻译前用，保证术语不会被翻译，供glossary_do2处理。

    Args:
        string (_type_): 原始文本
        glossary_json (_type_): 术语。格式为json，数组，第一个是原文，第二个是应该翻译后文本
        类似
        [
            {"old_value": "TEST1", "new_value": "测试1组"},
            {"old_value": "TEST22", "new_value": "测试22组"}
        ]

    Returns:
        _type_: 处理后的文本。
    """

    for item in glossary_json:
        old_value = item["old_value"]
        new_value = f'aa_{hex(hash(item["old_value"]))}_zz'
        string = re.sub(old_value, new_value, string)
    return string


def glossary_do2(string, glossary_json):
    """
    术语支持。在翻译后使用，将经过glossary_do1处理的后的文本里的标记翻译为术语。

    Args:
        string (_type_): 原始翻译的字符串
        glossary_json (_type_): 术语格式为json，数组，第一个是原文，第二个是应该翻译后文本
        类似
        [
            {"old_value": "TEST1", "new_value": "测试1组"},
            {"old_value": "TEST22", "new_value": "测试22组"}
        ]

    Returns:
        _type_: 处理后的文本。
    """
    for item in glossary_json:
        old_value = f'aa_{hex(hash(item["old_value"]))}_zz'
        new_value = item["new_value"]
        string = re.sub(old_value, new_value, string)
    return string


def save_file(fname, savestr: str):
    """
    保存文件。utf-8格式

    Args:
        fname (_type_): _description_
        savestr (str): _description_
    """
    ff1 = open(file=fname, mode="w", buffering=1000, encoding="utf-8")
    ff1.write(savestr)
    ff1.close()
