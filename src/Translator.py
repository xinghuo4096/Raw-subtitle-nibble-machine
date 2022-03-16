'''
翻译

Raises:
    Exception: _description_
    Exception: _description_

Returns:
    _type_: _description_
'''
import copy
import json
import re
from urllib.parse import quote
from urllib.request import Request, urlopen
from Srt import Srt, load_srt_fromfile
import chardet
#TODO 继续修改doc2
SENCTENCE_END_MARK = (r'[\w ]+[?.!]')
RE_FIND = re.compile(SENCTENCE_END_MARK)
CLEAR_MARK = r'[!?.]?\s+'
RE_CLEAR = re.compile(CLEAR_MARK)
CHINESE_MARK = r'[\w ]+[，。？]'
RE_CHINESE_MARK = re.compile(CHINESE_MARK)
languages = dict({
    'auto': 'auto',
    'af': 'Afrikaans',
    'sq': 'Albanian',
    'am': 'Amharic',
    'ar': 'Arabic',
    'hy': 'Armenian',
    'az': 'Azerbaijani',
    'eu': 'Basque',
    'be': 'Belarusian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'ceb': 'Cebuano',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'co': 'Corsican',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'fy': 'Frisian',
    'gl': 'Galician',
    'ka': 'Georgian',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'ht': 'Haitian Creole',
    'ha': 'Hausa',
    'haw': 'Hawaiian',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hmn': 'Hmong',
    'hu': 'Hungarian',
    'is': 'Icelandic',
    'ig': 'Igbo',
    'id': 'Indonesian',
    'ga': 'Irish',
    'it': 'Italian',
    'ja': 'Japanese',
    'jv': 'Javanese',
    'kn': 'Kannada',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'rw': 'Kinyarwanda',
    'ko': 'Korean',
    'ku': 'Kurdish',
    'ky': 'Kyrgyz',
    'lo': 'Lao',
    'la': 'Latin',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'lb': 'Luxembourgish',
    'mk': 'Macedonian',
    'mg': 'Malagasy',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mt': 'Maltese',
    'mi': 'Maori',
    'mr': 'Marathi',
    'mn': 'Mongolian',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'no': 'Norwegian',
    'ny': 'Nyanja (Chichewa)',
    'or': 'Odia (Oriya)',
    'ps': 'Pashto',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese (Portugal, Brazil)',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sm': 'Samoan',
    'gd': 'Scots Gaelic',
    'sr': 'Serbian',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'Sindhi',
    'si': 'Sinhala (Sinhalese)',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'so': 'Somali',
    'es': 'Spanish',
    'su': 'Sundanese',
    'sw': 'Swahili',
    'sv': 'Swedish',
    'tl': 'Tagalog (Filipino)',
    'tg': 'Tajik',
    'ta': 'Tamil',
    'tt': 'Tatar',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'tk': 'Turkmen',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'ug': 'Uyghur',
    'uz': 'Uzbek',
    'vi': 'Vietnamese',
    'cy': 'Welsh',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'zu': 'Zulu'
})


class Translator:
    '''
    翻译
    '''

    def __init__(self):
        pass

    @staticmethod
    def make_fanyi_packge(full_sentences: list):
        '''
        make_fanyi_packge 短句子打包为翻译引擎一次可以识别的最大量包
        一行不能超过5000字符，超过报错。

        google是少于5000字符

        Arguments:
            full_sentences -- list，短句子列表list(str)，单句如果超过4988则报错。

        Returns:
            list，打好包的文本
        '''
        fanyitexts = []
        length = 0
        full_sentence = []
        size_limite = 4988
        for item in full_sentences:
            text = quote(item + '\n', 'utf-8')
            if len(text) > 4988:
                raise Exception('error:to long.' + item.text)
            if (length + len(text)) < size_limite:
                length += len(text)
                full_sentence.append(text)
            else:
                fanyitexts.append(''.join(full_sentence))
                length = len(text)
                full_sentence = []
                full_sentence.append(text)
        if full_sentence:
            fanyitexts.append(''.join(full_sentence))

        return fanyitexts

    @staticmethod
    def make_fanyi_dict(google_fanyi_json) -> dict:
        '''
        制作字典

        Args:
            google_fanyi_json (_type_): _description_

        Returns:
            dict: _description_
        '''
        fanyijson = json.loads(google_fanyi_json)
        fanyi_dict = dict(
            zip([x[1].strip('\n') for x in fanyijson[0]],
                [x[0].strip('\n') for x in fanyijson[0]]))

        return fanyi_dict

    @staticmethod
    def translate_byte_dict(subcnen, fdict) -> list:
        '''
        查字典的方法翻译

        Args:
            subcnen (_type_): _description_
            fdict (_type_): _description_

        Returns:
            list: _description_
        '''
        err_text = []
        for item in subcnen.subblocks:
            for st1 in item.sentences:
                if st1.text:
                    fanyi_text = fdict.get(st1.text, '')
                    if fanyi_text:
                        if isinstance(st1, NormalSentence):
                            item.text = fanyi_text
                        if isinstance(st1, SpliteSentence):
                            item.text = fanyi_text
                        if isinstance(st1, MergeSentence):
                            st1.splite_fanyi(fanyi_text)
                    else:
                        err_text.append("fanyi error." + st1.text)
        return err_text


class Media:
    '''
    影视剧集
    '''

    def __init__(self, detail: str):
        self.detail = detail
        self.subtitles = list()

    def add_subtitle(self, language: str, subtitle_fname: str):
        '''
        增加一个语言的字幕

        Args:
            language (str): _description_
            subtitle_fname (str): _description_

        Returns:
            _type_: _description_
        '''
        sub = Subtitle(language, subtitle_fname)
        self.subtitles.append(sub)
        return sub

    def add_language_subtitle(self, language: str, index=0):
        '''
        增加一种语言的字幕，其他部分从旧字幕deepcopy。

        Args:
            language (str): _description_
            index (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        '''
        sub = copy.deepcopy(self.subtitles[index])
        sub.language = language
        self.subtitles.append(sub)
        return sub


class Subtitle:
    '''
    字幕。比如英语en，或者中文zh-cn
    '''

    def __init__(self, language: str, subtitle_fname: str):
        self.subtitle_fname = subtitle_fname
        self.language = language

        subs = list()
        subs = load_srt_fromfile(self.subtitle_fname)
        self.subblocks = [SubBlock(x) for x in subs]

    def get_sentences_text(self) -> list:
        '''
        得到字幕中所有句子文本

        Returns:
            list: _description_
        '''
        slist = [x.get_sentences_text() for x in self.subblocks]
        slist = list(filter(None, slist))
        return slist

    def make_sentence(self):
        '''
         解析字幕中的句子。
        '''
        merge_strs = list()
        merge_subblocks = list()
        for item in self.subblocks:
            assert isinstance(item, SubBlock)

            if merge_strs:
                char_end = merge_strs[-1][-1]
                char_start = item.text[0]
                assert isinstance(char_end, str)
                if char_end.isalnum() and char_start.isalnum():
                    item.text = ' ' + item.text

            merge_strs.append(item.text)

            find = re.findall(RE_FIND, item.text)

            if (len(find)) == 0:
                #没有结束，需要merge
                st1 = MergeSentence()
                st1.object_link(merge_subblocks)

                merge_subblocks.append(item)
                item.sentences = [st1]
            elif len(find) == 1:
                if len(merge_strs) == 1:
                    st1 = NormalSentence(merge_strs[0])

                    #sentence object link
                    st1.object_link([item])
                    #subblock object link
                    item.sentences = [st1]
                elif len(merge_strs) > 1:
                    st1 = MergeSentence(''.join(merge_strs))
                    #sentence object link
                    merge_subblocks.append(item)
                    st1.object_link(merge_subblocks)
                    #subblock object link
                    item.sentences = [st1]

                merge_strs = list()
                merge_subblocks = list()
            elif len(find) > 1:
                if len(merge_strs) == 1:
                    st1 = NormalSentence(merge_strs[0])

                    #sentence object link
                    st1.object_link([item])
                    #subblock object link
                    item.sentences = [st1]
                else:
                    st1 = MergeSentence(''.join(merge_strs))

                    #sentence object link
                    merge_subblocks.append(item)
                    st1.object_link(merge_subblocks)
                    #subblock object link
                    item.sentences = [st1]

                merge_strs = list()
                merge_subblocks = list()
        # 最后一句。
        item = self.subblocks[-1]
        if len(merge_strs) > 0:
            if len(merge_strs) == 1:
                st1 = NormalSentence(merge_strs[0])
                #sentence object link
                st1.object_link([item])
                #subblock object link
                item.sentences = [st1]
            else:
                st1 = MergeSentence(''.join(merge_strs))

                #sentence object link
                merge_subblocks.append(item)
                st1.object_link(merge_subblocks)
                #subblock object link
                item.sentences = [st1]

            merge_strs = list()
            merge_subblocks = list()


class SubBlock(Srt):
    '''
    字幕块类似

    ```text
    1
    0:1:45,380 --> 0:1:48,880
    -测试-1-测试-0:1:45,380-0:1:48,880
    ```
    Args:
        Srt (_type_): _description_
    '''

    def __init__(self, srt: Srt):
        '''
        从传入的srt对象，初始化。

        Args:
            srt (Srt): _description_
        '''
        Srt.__init__(self, srt.index, '0:1:45,380 --> 0:1:48,880', srt.text)
        self.index = srt.index
        self.start_time = srt.start_time
        self.end_time = srt.end_time
        self.text = self.clear_subtitle_text(srt.text)

        self.sentences = list()

    def get_sentences_text(self):
        '''
        得到包含句子的文本

        Returns:
            _type_: _description_
        '''
        assert isinstance(self.sentences, list)
        tlist = [x.text for x in self.sentences if x.text.strip()]
        if len(tlist) > 0:
            return '\n'.join(tlist)
        else:
            return ''

    def clear_subtitle_text(self, str1):
        '''
        去除字幕文本中句子结尾符号后带空白符的情况。
        如:'? ','! ','. '

        _extended_summary_

        Args:
            srt (_type_): _description_

        Returns:
            _type_: _description_
        '''
        return re.sub(RE_CLEAR, SubBlock.match_clear, str1)

    @staticmethod
    def match_clear(match):
        assert isinstance(match, re.Match)
        return (match.group()[0])


class Sentence(object):
    '''
    抽象类
    '''

    def __init__(self, text=''):
        self.text = text
        self.subblocks = list()

    def object_link(self, subblocks: list):
        '''
        设置对象链接UML

        Args:
            subblocks (list): _description_
        '''
        self.subblocks = subblocks


class MergeSentence(Sentence):
    '''
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
    '''

    def splite_fanyi(self, text: str, mode='splite'):
        '''
         MergeSentence合并的句，翻译后，需要给没有结尾符号的subblock的text赋值。
         1个MergeSentence实例对应多个subblock实例，都要赋值。
        Args:
            mode (str, optional): 拆分模式，默认是splite，其他模式就直接复制. Defaults to 'splite'.
        '''

        blk_count = len(self.subblocks)
        find = re.findall(RE_CHINESE_MARK, text)
        split_text = [text] * blk_count
        if mode.lower() == 'splite':
            if len(find) == blk_count:
                split_text = find

        subs = self.subblocks
        for i in range(blk_count):
            subs[i].text = split_text[i]
        return


class SpliteSentence(Sentence):
    '''
    可以分开的句子。如 Okay. I gotta go.

    Args:
        Sentence (_type_): _description_
    '''


class NormalSentence(Sentence):
    pass


class TranslationEngine:

    def __init__(self, ):
        pass

    @staticmethod
    def detect_code(detect_str: str) -> tuple:
        s = chardet.detect(detect_str)
        str1 = ''
        if s['confidence'] > 0.9:
            str1 = detect_str.decode(s['encoding'], 'ignore')
        else:
            raise Exception(detect_str[0:10] + '... error.' + s['confidence'])
        return str1, s['encoding']

    @staticmethod
    def fanyi_google(
            qtext=quote('test', 'utf-8'), from_language='en',
            to_language='zh-CN'):
        '''
        用谷歌翻译

        用的是免费的版本，5000字符限制。

        Args:
            str1 (str, optional): 待翻译文本，应该quote(text, 'utf-8'). Defaults to 'test'.]
            from_language (str, optional): 字幕原始语言. Defaults to 'en'.
            to_language (str, optional): 翻译后的语言. Defaults to 'zh-CN'.

        Returns:
            str: 翻译后语言
        '''

        if len(qtext) < 1:
            qtext = quote('test', 'utf-8')
        url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl={language1}&tl={language2}&dt=t&q={text}'.format(
            language1=from_language, language2=to_language, text=qtext)

        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/"
        }
        request = Request(url, headers=headers)
        request.add_header("Connection", "keep-alive")
        request.encoding = 'utf-8'
        response = urlopen(request, timeout=30)
        rawdata = response.read()
        strlist = TranslationEngine.detect_code(rawdata)
        return strlist


class Gooogle(TranslationEngine):

    def __init__(self, ):
        pass


class TranslationDict:

    def __init__(self):
        pass


def save_file(fname, savestr: str):
    ff1 = open(file=fname, mode='w', buffering=1000, encoding='utf-8')
    ff1.write(savestr)
    ff1.close()