"""
    翻译引擎

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
"""
import json
import re
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

import chardet
import requests

from baidu_fanyi_sign import baidu_fanyi_sign


class TranslationEngine:
    """
    翻译引擎
    """

    def __init__(
        self,
    ):
        pass

    @staticmethod
    def detect_code(detect_str: str) -> tuple:
        """
        检测字符串编码

        Args:
            detect_str (str): _description_

        Raises:
            Exception: _description_

        Returns:
            tuple: _description_
        """
        detect_ret = chardet.detect(detect_str)
        str1 = ""
        if detect_ret["confidence"] > 0.9:
            str1 = detect_str.decode(detect_ret["encoding"], "ignore")
        else:
            raise Exception(detect_str[0:10] +
                            "... error." + detect_ret["confidence"])
        return str1, detect_ret["encoding"]

    def translate(self):
        """
        抽象函数,不用abc.abstractmethod
        """
        raise Exception(type(self) + "translation().call.")

    def make_fanyi_dict(self) -> dict:
        """
        抽象函数 制作翻译词典

        Returns:
            dict: _description_
        """
        raise Exception(type(self) + "translation().call.")


class GoogleFree(TranslationEngine):
    """
    google free translation

    Args:
        TranslationEngine (_type_): _description_
    """

    # pylint:disable=arguments-differ
    def translate(
        self,
        qtext=quote("test", "utf-8"),
        from_language="en",
        to_language="zh-CN",
        sleeptime=30,
    ) -> tuple:
        """
        用谷歌翻译

        用的是免费的版本，5000字符限制。

        Args:
            str1 (str, optional): 待翻译文本，应该quote(text, 'utf-8').
            Defaults to 'test'.]
            from_language (str, optional): 字幕原始语言. Defaults to 'en'.
            to_language (str, optional): 翻译后的语言. Defaults to 'zh-CN'.
            sleeeptimne:休眠时间默认30秒，默认每30秒调用一次谷歌翻译。

        Returns:
              tuple:googlejson,翻译后语言
        """

        if len(qtext) < 1:
            qtext = quote("test", "utf-8")
        else:
            qtext = quote(qtext, "utf-8")

        # pylint: disable=consider-using-f-string,line-too-long
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={language1}&tl={language2}&dt=t&q={text}".format(
            language1=from_language, language2=to_language, text=qtext
        )

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/"
        }
        request = Request(url, headers=headers)
        request.encoding = "utf-8"
        response = urlopen(request, timeout=60)
        rawdata = response.read()
        strlist = TranslationEngine.detect_code(rawdata)
        time.sleep(sleeptime)
        return strlist

    def make_fanyi_dict(self, google_fanyi_json) -> dict:
        """
        制作字典

        Args:
            google_fanyi_json (_type_): _description_

        Returns:
            dict: _description_
        """
        fanyijson = json.loads(google_fanyi_json)
        fanyi_dict = dict(
            zip(
                [x[1].strip("\n") for x in fanyijson[0]],
                [x[0].strip("\n") for x in fanyijson[0]],
            )
        )

        return fanyi_dict


class Baidufree(TranslationEngine):
    """
    百度翻译引擎

    Args:
        TranslationEngine (_type_): _description_
    """

    baidu_langList = {
        "zh": "中文",
        "jp": "日语",
        "jpka": "日语假名",
        "th": "泰语",
        "fra": "法语",
        "en": "英语",
        "spa": "西班牙语",
        "kor": "韩语",
        "tr": "土耳其语",
        "vie": "越南语",
        "ms": "马来语",
        "de": "德语",
        "ru": "俄语",
        "ir": "伊朗语",
        "ara": "阿拉伯语",
        "est": "爱沙尼亚语",
        "be": "白俄罗斯语",
        "bul": "保加利亚语",
        "hi": "印地语",
        "is": "冰岛语",
        "pl": "波兰语",
        "fa": "波斯语",
        "dan": "丹麦语",
        "tl": "菲律宾语",
        "fin": "芬兰语",
        "nl": "荷兰语",
        "ca": "加泰罗尼亚语",
        "cs": "捷克语",
        "hr": "克罗地亚语",
        "lv": "拉脱维亚语",
        "lt": "立陶宛语",
        "rom": "罗马尼亚语",
        "af": "南非语",
        "no": "挪威语",
        "pt_BR": "巴西语",
        "pt": "葡萄牙语",
        "swe": "瑞典语",
        "sr": "塞尔维亚语",
        "eo": "世界语",
        "sk": "斯洛伐克语",
        "slo": "斯洛文尼亚语",
        "sw": "斯瓦希里语",
        "uk": "乌克兰语",
        "iw": "希伯来语",
        "el": "希腊语",
        "hu": "匈牙利语",
        "hy": "亚美尼亚语",
        "it": "意大利语",
        "id": "印尼语",
        "sq": "阿尔巴尼亚语",
        "am": "阿姆哈拉语",
        "as": "阿萨姆语",
        "az": "阿塞拜疆语",
        "eu": "巴斯克语",
        "bn": "孟加拉语",
        "bs": "波斯尼亚语",
        "gl": "加利西亚语",
        "ka": "格鲁吉亚语",
        "gu": "古吉拉特语",
        "ha": "豪萨语",
        "ig": "伊博语",
        "iu": "因纽特语",
        "ga": "爱尔兰语",
        "zu": "祖鲁语",
        "kn": "卡纳达语",
        "kk": "哈萨克语",
        "ky": "吉尔吉斯语",
        "lb": "卢森堡语",
        "mk": "马其顿语",
        "mt": "马耳他语",
        "mi": "毛利语",
        "mr": "马拉提语",
        "ne": "尼泊尔语",
        "or": "奥利亚语",
        "pa": "旁遮普语",
        "qu": "凯楚亚语",
        "tn": "塞茨瓦纳语",
        "si": "僧加罗语",
        "ta": "泰米尔语",
        "tt": "塔塔尔语",
        "te": "泰卢固语",
        "ur": "乌尔都语",
        "uz": "乌兹别克语",
        "cy": "威尔士语",
        "yo": "约鲁巴语",
        "yue": "粤语",
        "wyw": "文言文",
        "cht": "中文繁体",
    }

    # pylint:disable=arguments-differ
    def translate(
        self,
        qtext=quote("test", "utf-8"),
        from_language="en",
        to_language="zh",
        sleeptime=30,
    ) -> tuple:
        """
        用百度翻译

        用的是免费的版本，5000字符限制。

        Args:
            str1 (str, optional): 待翻译文本，应该quote(text, 'utf-8').
            Defaults to 'test'.]
            from_language (str, optional): 字幕原始语言. Defaults to 'en'.
            to_language (str, optional): 翻译后的语言. Defaults to 'zh-CN'.
            sleeeptimne:休眠时间默认30秒，默认每30秒调用一次谷歌翻译。

        Returns:
              tuple:googlejson,翻译后语言
        """
        baidufanyi_url = "https://fanyi.baidu.com/"
        url_v2transapi = "https://fanyi.baidu.com/v2transapi"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/",
            "Acs-Token": "1661410972047_1668449431845_PuH6yxM4fr5fh13uzM6gX+pOyw85ZvjktITNFUcI+5F4Irx8SS+nzFeWP60g2jDM3g5WBsNy+4nEqBMPYF9D9Q/+H32BBgtQavbsTulNd9kmg9rBJya28ESweddKga0xeF03ZztY7OCIq0Mth+vOrxXXaAYorT/6No8kFIJlL0DpXlHLK30HvAcOKcuvWBmSQ8z5ZV9KOJ0x3r8qpkgyKCxpwcvt6OxAG2Uzm5MNaX+laVtQKIXxsCqx2CKXIJ7uE1jZB4xxURKNkdKged8lRqG97TehTYgf0SCjHlLenUeZUiLWmTDBi4qaKeUnQOT7FsF5gd+hGJQup+HUod9/uptg7AO8XLs9C6Lf+wqQQKM=",

        }

        session = requests.Session()
        session.headers = headers

        response = session.get(baidufanyi_url)
        response = session.get(baidufanyi_url)
        baidufanyi_homepage = response.content.decode()

        match1 = r"token:\s*'(\S*)'"
        match2 = r'window.gtk\s*=\s*"(\S*)"'

        find1 = re.findall(match1, baidufanyi_homepage)
        find2 = re.findall(match2, baidufanyi_homepage)

        token = find1[0]
        gtk = find2[0]

        sign = baidu_fanyi_sign.baidu_sign(qtext, gtk)

        try:
            data = {
                "from": from_language,
                "to": to_language,
                "query": qtext,
                "transtype": "translang",
                "domain": "common",
                "simple_means_flag": 3,
                "sign": sign,
                "token": token,
            }
            url1 = f"{url_v2transapi}?from={from_language}&to={to_language}"

            response = session.post(url1, data=data)

            response_dict = response.json()

        except Exception as err1:
            print(err1)

        if 'errno' in response_dict:
            raise ValueError(
                (response_dict['errno'], response_dict['errmsg']))

        time.sleep(sleeptime)
        return response_dict, ""

    def baidu_json2text(self, baidu_json):
        """
        baidu 翻译的json转为 text

        Args:
            baidu_json (_type_): _description_

        Returns:
            _type_: _description_
        """
        strlist = [x["dst"] for x in baidu_json["trans_result"]["data"]]
        return strlist

    def make_fanyi_dict(self, baidu_json) -> dict:
        """
        翻译词典

        Args:
            baidu_json (_type_): _description_

        Returns:
            dict: _description_
        """

        strlist = {x["src"]: x["dst"]
                   for x in baidu_json["trans_result"]["data"]}
        return strlist
