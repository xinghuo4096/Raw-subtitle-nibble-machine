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
            raise Exception(detect_str[0:10] + "... error." + detect_ret["confidence"])
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
