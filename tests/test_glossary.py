

import json
from translator import glossary_do1, glossary_do2


def test_glossary1():
    string = "TEST22.TEST1.TEST22.We have to test now and minimize TEST1's losses.We have to test now and minimize TeSt1's losses."
    string2 = "测试22组.测试1组.测试22组.We have to test now and minimize 测试1组's losses.We have to test now and minimize TeSt1's losses."

    glossary_file = "indata\\glossary.txt"
    glossary_json = '{}'
    with open(glossary_file, mode='r', encoding='utf-8') as file1:
        glossary_json = json.load(file1)
    str1 = glossary_do1(string, glossary_json)
    str2 = glossary_do2(str1, glossary_json)
    assert str2 == string2
