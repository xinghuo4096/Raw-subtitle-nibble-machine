import requests
import json
import os


class BaiduceTranslator:
    def __init__(self, keypath="config/keys.json"):

        self.txt = None
        """原文"""
        self.dst = None
        """翻译后的文本"""

        self.response = None

        self.keypath = keypath
        self.api_key = None
        self.secret_key = None

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

    def translate(self, text):
        url = f"https://aip.baidubce.com/rpc/2.0/mt/texttrans/v1?access_token={self.get_access_token()}"
        payload = json.dumps({"from": "en", "to": "zh", "q": text})
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raises HTTPError for bad responses

            rjson = response.json()
            trans_result = rjson["result"]["trans_result"][0]
            self.dst = trans_result["dst"]
            self.src = trans_result["src"]
            return self.dst
        except KeyError as e:
            print(f"Error extracting dst and src: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error during translation: {e}")
            return None


if __name__ == "__main__":
    translator = BaiduceTranslator(keypath="config/mykeys.json")
    text_to_translate = "When tomorrow turns in today, yesterday, and someday that no more important in your memory, we suddenly realize that we r pushed forward by time. This is not a train in still in which you may feel forward when another train goes by. It is the truth that we've all grown up. And we become different."
    print("Translating...")
    translator.translate(text_to_translate)

    if translator.dst:
        print("Translation result:")
        print(translator.dst)
    else:
        print("Failed to translate.")
