"""
翻译引擎

Author: xinghuo
"""

from typing import Dict


class TranslationEngine:
    """
    翻译引擎
    """

    def __init__(
        self,
    ):
        pass

    def translate(
        self, text, from_language, to_language, sleep_time=0
    ) -> Dict[str, str] | None:
        """
        抽象函数,不用abc.abstractmethod
        """
        raise Exception("translation().call.")
        return "error"

    def make_fanyi_dict(self, source: str, fanyi_text: str):
        """
        抽象函数 制作翻译词典

        Returns:
            dict: _description_
        """
        raise Exception("translation().call.")

    # 给出输出结果的json的结构
    def make_output_json(self, result_json) -> str:
        """
        抽象函数 制作输出json

        Returns:
            dict: _description_
        """
        raise Exception("translation().call.")
