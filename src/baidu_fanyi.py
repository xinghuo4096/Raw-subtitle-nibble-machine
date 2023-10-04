import re
import requests
from baidu_fanyi_sign import baidu_fanyi_sign

a = baidu_fanyi_sign.baidu_sign("kkk")
print(a)

baidufanyi_url = "https://fanyi.baidu.com/"
url_langdetect = "https://fanyi.baidu.com/langdetect"
url_v2transapi = "https://fanyi.baidu.com/v2transapi"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Acs-Token": "1661410972047_1668449431845_PuH6yxM4fr5fh13uzM6gX+pOyw85ZvjktITNFUcI+5F4Irx8SS+nzFeWP60g2jDM3g5WBsNy+4nEqBMPYF9D9Q/+H32BBgtQavbsTulNd9kmg9rBJya28ESweddKga0xeF03ZztY7OCIq0Mth+vOrxXXaAYorT/6No8kFIJlL0DpXlHLK30HvAcOKcuvWBmSQ8z5ZV9KOJ0x3r8qpkgyKCxpwcvt6OxAG2Uzm5MNaX+laVtQKIXxsCqx2CKXIJ7uE1jZB4xxURKNkdKged8lRqG97TehTYgf0SCjHlLenUeZUiLWmTDBi4qaKeUnQOT7FsF5gd+hGJQup+HUod9/uptg7AO8XLs9C6Lf+wqQQKM=",
}
cookies = {}
cache = {}
conn = None

input_lang = "en"
output_lang = "zh"

session = requests.Session()
session.headers = headers

response = session.get(baidufanyi_url)
response = session.get(baidufanyi_url)
baidu_cookie = response.cookies
text1 = response.content.decode()

match1 = r"token:\s*'(\S*)'"
match2 = r'window.gtk\s*=\s*"(\S*)"'

find1 = re.findall(match1, text1)
find2 = re.findall(match2, text1)

token = find1[0]
gtk = find2[0]

text1 = "face\nfacebook\nface to face\n"
sign = baidu_fanyi_sign.baidu_sign(text1)

print(token, gtk, sign)

try:
    data = {
        "from": input_lang,
        "to": output_lang,
        "query": text1,
        "transtype": "translang",
        "domain": "common",
        "simple_means_flag": 3,
        "sign": sign,
        "token": token,
    }
    url1 = f"{url_v2transapi}?from={input_lang}&to={output_lang}"

    response = session.post(url1, data=data)

    response_dict = response.json()

    trans = [x["dst"] for x in response_dict["trans_result"]["data"]]

    print(trans)

except Exception as e:
    print(e)
