

import json
from translator import glossary_do1, glossary_do2


def test_glossary1():
    string = "We have to sell now and minimize NYL's losses.We have to sell now and minimize nyl's losses."
    string2 = "We have to sell now and minimize 纽约投行's losses.We have to sell now and minimize nyl's losses."

    glossary_file = "indata\\glossary.txt"
    glossary_json = '{}'
    with open(glossary_file, mode='r', encoding='utf-8') as file1:
        glossary_json = json.load(file1)
    str1 = glossary_do1(string, glossary_json)
    str1 = glossary_do2(str1, glossary_json)
    assert str1 == string2
