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

    def translate(self, text, from_language, to_language,
                  sleep_time=0.5) -> tuple[str, str]:
        """
        抽象函数,不用abc.abstractmethod
        """
        raise Exception("translation().call.")
        return "error"

    def make_fanyi_dict(self, fanyi_text) -> Dict[str, str]:
        """
        抽象函数 制作翻译词典

        Returns:
            dict: _description_
        """
        raise Exception("translation().call.")
