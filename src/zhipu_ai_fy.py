import datetime
import importlib
import json
import os
import re
import sys
import traceback
from itertools import zip_longest
from typing import Dict, List

from json_repair import repair_json
from zhipuai import ZhipuAI  # type: ignore

from jzhipu_ai_json import try_parse_json_object
from rsnm_log import LogColors, setup_logging
from translation_engine import TranslationEngine

logger = setup_logging()

PATTERN = re.compile(r"```(?:json\s+)?(\W.*?)```", re.DOTALL)
PATTERN2 = re.compile(r"```json\s+(.*?)```", re.DOTALL)


class ZhipuEngine(TranslationEngine):
    def __init__(self, api_key, config: str = "my_zhipu_fy", lib_path="config"):
        self.api_key = self.load_api_key(api_key)
        self.client = ZhipuAI(api_key=self.api_key)
        self.token_usage = 0
        self.save_token_usage_file = (
            "token_usage.json"  # 初始化save_token_usage的文件名
        )

        self.config = self.load_config(config, lib_path)

        self.tokens_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def load_api_key(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data["api_key"]
        except FileNotFoundError:
            logger.info("API密钥文件未找到，请确保存在api_key.json文件。")
            raise Exception("API密钥文件未找到，请确保存在api_key.json文件。")
        except json.JSONDecodeError:
            logger.info(
                "API密钥文件格式错误，请确保api_key.json文件是一个有效的JSON文件。"
            )
            raise Exception(
                "API密钥文件格式错误，请确保api_key.json文件是一个有效的JSON文件。"
            )

    def load_config(self, zhipu_config, lib_path="config"):
        try:
            # 动态加载 config 模块
            current_directory = os.getcwd()
            logger.info(f"当前工作目录: {current_directory}")

            # 检查当前目录的config文件夹是否存在
            config_path = os.path.join(current_directory, lib_path)
            if os.path.exists(config_path):
                # 将config目录添加到模块搜索路径
                sys.path.append(config_path)
                logger.info(f"'config'目录已添加到模块搜索路径：{config_path}")
            else:
                logger.info(f"'config'目录不存在：{config_path}")

            config = importlib.import_module(zhipu_config)

            return config.config
        except ImportError as e:
            logger.info(f"无法导入配置文件：{e}")
            raise Exception(f"无法导入配置文件：{e}")
        except Exception as e:
            logger.info(f"加载配置文件时发生错误：{e}")
            raise Exception(f"加载配置文件时发生错误：{e}")

    def call_zhipu_ai(self, user_text, from_language, to_language):
        messages = []
        fanyi_dict = None
        have_match = False
        user_lines = user_text.split("\n")
        user_new_text = "<字幕断句>".join(user_lines)  # user_text  #
        try:
            have_match = False
            fanyi_dict = None
            messages = []
            messages = self.generate_translation_prompt(
                user_new_text, from_language, to_language
            )

            result_lines = self.generate_translation(messages)

            if result_lines is not None:
                fanyi_dict, have_match = self.make_fanyi_dict(user_lines, result_lines)

                if fanyi_dict is not None:
                    if not have_match:
                        logger.warn(
                            f"{ LogColors.WARNING.value}"
                            f"发现不匹配"
                            f"{LogColors.RESET_COLOR.value}"
                        )
        except Exception as e:
            logger.error(
                f"{LogColors.ERROR.value}"
                f"翻译失败，请检查输入内容是否正确，错误信息：{e}\n"
                f"traceback:{traceback.format_exc()}\n"
                f"{LogColors.RESET_COLOR.value}"
            )
        return fanyi_dict

    def generate_translation_prompt(self, user_text, from_language, to_language):
        messages = []
        system_content = self.config.get("system_content")
        messages.append(
            {
                "role": "system",
                "content": system_content,
            }
        )
        user_prompt = self.config.get("user_content_6")
        user_prompt = user_prompt.replace("[源语言]", from_language)
        user_prompt = user_prompt.replace("[目标语言]", to_language)
        user_prompt = user_prompt.replace("[待翻译影视字幕]", user_text)

        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        return messages

    def generate_translation(self, messages):
        result_list = None

        for i in range(3):
            try:
                action_match = self.call_zhipu_action(messages)
                text = action_match.group(1).strip()

                if action_match is not None:
                    json_text, json_object = try_parse_json_object(text)
                if json_object is not None:
                    result_list = json_object["s翻s译s结s果s"]
                    # 正确取到结果
                    break
            except Exception as e:
                logger.error(
                    f"{LogColors.ERROR.value}"
                    f"翻译失败，请检查输入内容是否正确，错误信息：{e}\n"
                    f"traceback:{traceback.format_exc()}\n"
                    f"{LogColors.RESET_COLOR.value}"
                )

        return result_list

    def call_zhipu_action(self, messages):
        logger.info(
            LogColors.INFO.value + f"messages: {messages}" + LogColors.RESET_COLOR.value
        )

        response = self.client.chat.completions.create(
            model=self.config.get("model", "glm-4-plus"),
            messages=messages,
            top_p=self.config.get("top_p", 0.7),
            temperature=self.config.get("temperature", 0.95),
            max_tokens=self.config.get("max_tokens", 4095),
            stream=False,
        )
        logger.info(
            LogColors.INFO.value + f"client: {response}" + LogColors.RESET_COLOR.value
        )

        action_match = PATTERN2.search(response.choices[0].message.content)
        return action_match

    def translate(
        self, user_input, from_language, to_language, sleep_time=5
    ) -> Dict[str, str] | None:
        result_dict = None
        try:
            if from_language == "en":
                from_language = "英文"
            if to_language == "zh-CN":
                to_language = "中文"

            result_dict = self.call_zhipu_ai(user_input, from_language, to_language)
        except Exception as e:
            # 显示出错堆栈和行号
            logger.error(
                f"{LogColors.ERROR.value}"
                f"{e}\n 堆栈信息: {traceback.format_exc()}"
                f"{LogColors.RESET_COLOR.value}"
            )
        return result_dict

    def make_fanyi_dict(
        self, source_lines: list, translation_lines: list
    ) -> tuple[dict[str, str], bool]:
        """
        翻译词典

        :param zhipu_result: zhipu翻译结果

        :return: dict[str,str],原文，译文
        """
        sub_dict: Dict[str, str] = {}
        have_match = True

        if len(translation_lines) != len(source_lines):
            have_match = False

        sub_dict = self.zip_sub1_sub2(
            source_lines,
            translation_lines,
        )

        return sub_dict, have_match

    def save_token_usage(self, file_path=None):
        if file_path is None:
            file_path = self.save_token_usage_file  # 使用初始化的文件名
        try:
            with open(file_path, "w") as file:
                json.dump({"total_tokens": self.tokens_usage}, file)
            logger.info(f"Token使用统计已保存到 {file_path}")
        except Exception as e:
            logger.info(f"保存Token使用统计时发生错误: {file_path},{e}")

    def zhipuai_subtitle_message(
        self,
        message: str,
        textpack: int = 0,
        timecount: int = 0,
        sleep_time: int = 0,
        **text,
    ):
        """
        消息回调

        Args:
            message (str): _description_
        """
        zhipu_ai_time = 20
        # 总时间
        total_time = (zhipu_ai_time + sleep_time) * textpack
        # 剩余时间
        finally_time = (zhipu_ai_time + sleep_time) * (textpack - timecount)

        time1 = datetime.datetime.now() + datetime.timedelta(seconds=finally_time)

        text1 = f'{timecount} total time: {total_time} sec, finally time: {finally_time} sec,endtime:{
            time1.strftime("%Y-%m-%d %H:%M:%S")}'
        print(text1)
        return

    def zip_sub1_sub2(self, sub1, sub2) -> Dict[str, str]:
        """
        将两个列表按照顺序合并成一个字典，如果两个列表长度不一致，则将较短的列表用 None 填充
        :param sub1: 第一个列表
        :param sub2: 第二个列表
        :return: 合并后的字典
        :example:
        >>> zip_sub1_sub2(["key1", "key2"], ["value1", "value2"])
        """
        merged_dict: Dict[str, str] = {}
        for i, (key, value) in enumerate(zip_longest(sub1, sub2, fillvalue=None)):
            # 如果 key 不是 None，直接使用 key
            if key is not None:
                if value is not None:
                    merged_dict[key] = value
                else:
                    merged_dict[key] = f"Value_None_{i+1}"
            else:
                # 如果 key 是 None，创建一个新的键
                merged_dict[f"Key_None_{i+1}"] = str(value)
        return merged_dict


if __name__ == "__main__":
    pass
