'''
    翻译引擎

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
'''
import json
import re
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

import chardet
import requests

from baidu_fanyi_sign import baidu_fanyi_sign


class TranslationEngine:
    '''
    翻译引擎
    '''

    def __init__(self, ):
        pass

    @staticmethod
    def detect_code(detect_str: str) -> tuple:
        '''
        检测字符串编码

        Args:
            detect_str (str): _description_

        Raises:
            Exception: _description_

        Returns:
            tuple: _description_
        '''
        detect_ret = chardet.detect(detect_str)
        str1 = ''
        if detect_ret['confidence'] > 0.9:
            str1 = detect_str.decode(detect_ret['encoding'], 'ignore')
        else:
            raise Exception(detect_str[0:10] + '... error.' +
                            detect_ret['confidence'])
        return str1, detect_ret['encoding']

    def translate(self):
        '''
        抽象函数,不用abc.abstractmethod
        '''
        raise Exception(type(self) + 'translation().call.')

    def make_fanyi_dict(self) -> dict:
        '''
        抽象函数 制作翻译词典

        Returns:
            dict: _description_
        '''
        raise Exception(type(self) + 'translation().call.')


class GoogleFree(TranslationEngine):
    '''
    google free translation

    Args:
        TranslationEngine (_type_): _description_
    '''

    # pylint:disable=arguments-differ
    def translate(self,
                  qtext=quote('test', 'utf-8'),
                  from_language='en',
                  to_language='zh-CN',
                  sleeptime=30) -> tuple:
        '''
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
        '''

        if len(qtext) < 1:
            qtext = quote('test', 'utf-8')


# pylint: disable=consider-using-f-string,line-too-long
        url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl={language1}&tl={language2}&dt=t&q={text}'.format(
            language1=from_language, language2=to_language, text=qtext)

        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/"
        }
        request = Request(url, headers=headers)
        request.encoding = 'utf-8'
        response = urlopen(request, timeout=30)
        rawdata = response.read()
        strlist = TranslationEngine.detect_code(rawdata)
        time.sleep(sleeptime)
        return strlist

    def make_fanyi_dict(self, google_fanyi_json) -> dict:
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


class Baidufree(TranslationEngine):
    '''
    百度翻译引擎

    Args:
        TranslationEngine (_type_): _description_
    '''

    # pylint:disable=arguments-differ
    def translate(self,
                  qtext=quote('test', 'utf-8'),
                  from_language='en',
                  to_language='zh',
                  sleeptime=30) -> tuple:
        '''
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
        '''
        baidufanyi_url = "https://fanyi.baidu.com/"
        url_v2transapi = "https://fanyi.baidu.com/v2transapi"
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/"
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
                "token": token
            }
            url1 = f'{url_v2transapi}?from={from_language}&to={to_language}'

            response = session.post(url1, data=data)

            response_dict = response.json()

            time.sleep(sleeptime)

            return response_dict
        except Exception as err1:
            print(err1)

    def baidu_json2text(self, baidu_json):
        '''
        baidu 翻译的json转为 text

        Args:
            baidu_json (_type_): _description_

        Returns:
            _type_: _description_
        '''
        strlist = [x['dst'] for x in baidu_json["trans_result"]["data"]]
        return strlist

    def make_fanyi_dict(self, baidu_json) -> dict:
        '''
        翻译词典

        Args:
            baidu_json (_type_): _description_

        Returns:
            dict: _description_
        '''
        strlist = {
            x['src']: x['dst']
            for x in baidu_json["trans_result"]["data"]
        }
        return strlist
