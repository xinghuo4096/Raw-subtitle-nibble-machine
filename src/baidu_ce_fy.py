import json
from datetime import time
from typing import Dict

import requests

from translation_engine import TranslationEngine


class BaiduceEngine(TranslationEngine):
    def __init__(self, keypath="config/keys.json"):

        self.rjson = None
        """翻译结果json"""

        self.response = None

        self.keypath = keypath
        """
        存储百度的key的json

        例子：
        {
        "API_KEY": "你的API_KEY",
        "SECRET_KEY": "你的SECRET_KEY"
        }
        """
        self.api_key = None
        """baidu api key"""
        self.secret_key = None
        """baidu secret key"""

        self.load_keys()

    def load_keys(self):
        try:
            with open(self.keypath, "r") as f:
                keys = json.load(f)
                self.api_key = keys["API_KEY"]
                self.secret_key = keys["SECRET_KEY"]
        except Exception as e:
            print(f"Error loading keys: {e}")
            raise

    def get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
        }
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json().get("access_token")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None

    def translate(self, text, from_language, to_language, sleep_time):
        url = f"https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token=\
        {self.get_access_token()}"
        payload = json.dumps({"from": from_language,
                              "to": to_language, "q": text})
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raises HTTPError for bad responses

            rjson = response.json()
            self.rjson = rjson

            if (
                "error_code" in rjson and rjson["error_code"]
            ):  # 检查是否存在 'error_code' 键且其值不为空
                print(
                    f"Error during translation:{rjson['error_code']},\
                    {rjson['error_msg']}"
                )
                raise Exception(
                    f"Error during translation:{rjson['error_code']},\
                    {rjson['error_msg']}"
                )

            if sleep_time > 0:
                time.sleep(sleep_time)
            return rjson, None
        except KeyError as e:
            print(f"Error extracting dst and src: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error during translation: {e}")
            return None

    def baidu_json2text(self, baidu_json):
        """
        baidu 翻译的json转为 text

        Args:
            baidu_json (_type_): _description_

        Returns:
            _type_: _description_
        """
        # 检查是否存在 'result' 键
        if "result" in baidu_json and baidu_json["result"]:

            strlist = [x["dst"] for x in baidu_json["result"]["trans_result"]]
        return strlist

    def make_fanyi_dict(self, baidu_json) -> Dict[str, str]:
        """
        翻译词典

        Args:
            baidu_json (_type_): _description_

        Returns:
            dict: _description_
        """

        strlist = {x["src"]: x["dst"] 
                   for x in baidu_json["result"]["trans_result"]}

        return strlist

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
