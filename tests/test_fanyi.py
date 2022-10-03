import re
from translation_engine import GoogleFree, Baidufree


def test_token_gtk():
    '''
    token gtk
    '''
    match1 = r"token:\s*'(\S*)'"
    match2 = r'window.gtk\s*=\s*"(\S*)"'

    token = "  token: 'e55c967a31d0ce6dd63ccadbf53f703d',"
    gtk = ';window.gtk = "320305.131321201";'
    find1 = re.findall(match1, token)[0]
    find2 = re.findall(match2, gtk)[0]
    assert 'e55c967a31d0ce6dd63ccadbf53f703d' == find1
    assert '320305.131321201' == find2


def test_baidufanyi():
    '''
    baidu fanyi 引擎测试
    '''
    bd = Baidufree()
    bdjson = bd.translate('hello', 'en', 'zh', 1)
    assert bdjson
    text1 = bd.baidu_json2text(bdjson)[0]
    assert '你好' == text1

    aa = bd.make_fanyi_dict(bdjson)
    assert aa
