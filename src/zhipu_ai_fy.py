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

    def call_zhipu_ai(self, user_input, from_language, to_language):
        messages = []
        fanyi_dict = None
        fanyi_dict2 = None
        have_match = False
        summary_text = ""
        style_text = ""
        try:
            messages = self.generate_story_summary_prompt(user_input, messages)
            summary_text = self.get_story_summary(messages)

            if summary_text is not None:
                messages = self.generate_translation_style_prompt(
                    messages, summary_text
                )
                style_text = self.get_translation_style(messages)
                if style_text is not None:
                    messages = self.generate_translation_prompt(
                        user_input=user_input,
                        from_language=from_language,
                        to_language=to_language,
                        summary_text=summary_text,
                        style_text=style_text,
                    )
                    fanyi_dict, have_match = self.get_translation_dict(
                        user_input, messages
                    )

                    if fanyi_dict is not None:
                        fanyi_dict2 = fanyi_dict
                        if not have_match:
                            logger.info(
                                f"{ LogColors.INFO.value}"
                                f"发现不匹配，开始修复"
                                f"{LogColors.RESET_COLOR.value}"
                            )
                            messages = []
                            messages = self.generate_match_translation_prompt(
                                messages, user_input, fanyi_dict
                            )
                            fanyi_dict2 = self.get_match_translation_dict(
                                user_input, messages
                            )

        except Exception as e:
            logger.error(
                f"{LogColors.ERROR.value}"
                f"翻译失败，请检查输入内容是否正确，错误信息：{e}\n"
                f"traceback:{traceback.format_exc()}\n"
                f"{LogColors.RESET_COLOR.value}"
            )
        return fanyi_dict2

    def get_match_translation_dict(self, user_input, messages):
        action_match = self.call_zhipu_action(messages)
        result_json = None
        fanyi_dict = None
        if action_match is not None:
            json_text, json_object = try_parse_json_object(
                action_match.group(1).strip()
            )
            if json_object is not None:
                result_json = json_object["s配s对s结s果s"]
                result_txts = "\n".join(list(result_json.values()))
                fanyi_dict, have_match = self.make_fanyi_dict(user_input, result_txts)
                if not have_match:
                    logger.warning(
                        f"{ LogColors.WARNING.value}"
                        f"修复失败，原文行数和译文行数不一致。"
                        f"{LogColors.RESET_COLOR.value}"
                    )

        return fanyi_dict

    def generate_match_translation_prompt(self, messages, user_input, result_dict):
        user4 = self.config.get("user_content_4")
        text = json.dumps(
            result_dict, ensure_ascii=False, indent=None, separators=(",", ":")
        )
        keys = []
        values = []

        # 遍历字典并将键和值分别添加到对应的数组中
        for key, value in result_dict.items():
            keys.append(key)
            values.append(value)
        user_lines = user_input.split("\n")

        fanyi_dict = {line: "译文" for line in user_lines}

        user_json = json.dumps(
            fanyi_dict, ensure_ascii=False, indent=None, separators=(",", ":")
        )
        values_json = json.dumps(
            values, ensure_ascii=False, indent=None, separators=(",", ":")
        )
        user4 = user4.replace("[需要配对的内容的原文]", user_json)
        user4 = user4.replace("[参考译文]", values_json)

        messages.append(
            {
                "role": "user",
                "content": user4,
            }
        )

        return messages

    def get_translation_dict(self, user_input, messages):
        fanyi_dict = None
        action_match = self.call_zhipu_action(messages)
        result_text = None
        if action_match is not None:
            json_text, json_object = try_parse_json_object(
                action_match.group(1).strip()
            )
            if json_object is not None:
                result_text = json_object["s翻s译s结s果s"].split("\n")
                if result_text is not None:
                    fanyi_dict, have_match = self.make_fanyi_dict(
                        user_input, result_text
                    )
        return fanyi_dict, have_match

    def generate_translation_prompt(
        self, user_input, from_language, to_language, summary_text, style_text
    ):
        messages = []
        system_content = self.config.get("system_content")
        messages.append(
            {
                "role": "system",
                "content": system_content,
            }
        )

        user3 = self.config.get("user_content_5")
        user3 = user3.replace("[翻译风格]", style_text)
        user3 = user3.replace("[源语言]", from_language)
        user3 = user3.replace("[目标语言]", to_language)
        user3 = user3.replace("[待翻译影视字幕]", user_input)

        messages.append(
            {
                "role": "user",
                "content": user3,
            }
        )

        return messages

    def get_translation_style(self, messages):
        action_match = self.call_zhipu_action(messages)

        style_text = None
        if action_match is not None:
            json_text, json_object = try_parse_json_object(
                action_match.group(1).strip()
            )
            # 定义 变量：翻译风格
            style_text = json.dumps(
                # TODO 修改为字符串
                json_object["翻译风格"],
                ensure_ascii=False,
                indent=None,
                separators=(",", ":"),
            )

        return style_text

    def generate_translation_style_prompt(self, messages, summary_text):
        messages.append({"role": "assistant", "content": summary_text})
        user2 = self.config.get("user_content_2")
        messages.append(
            {
                "role": "user",
                "content": user2,
            }
        )
        return messages

    def get_story_summary(self, messages):
        action_match = self.call_zhipu_action(messages)
        summary_text = None
        if action_match is not None:
            json_text, json_object = try_parse_json_object(
                action_match.group(1).strip()
            )
            # 定义 变量：剧情总结
            summary_text = json_object["总结"]
        return summary_text

    def generate_story_summary_prompt(self, user_input, messages):
        messages.append(
            {
                "role": "system",
                "content": self.config.get("system_content"),
            }
        )

        user1 = self.config.get("user_content_1")
        user1 = user1.replace("srt剧情", user_input)
        messages.append(
            {
                "role": "user",
                "content": user1,
            }
        )
        return messages

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

        action_match = PATTERN.search(response.choices[0].message.content)
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

    def make_output_json(self, inputText):
        # 将字符串按行拆分，并去除空行
        lines = [line.strip() for line in inputText.split("\n") if line.strip()]

        # 组装成包含 'id', '原文', '译文' 的JSON格式
        json_data = json.loads(self.config["output_json"])

        t_result = json_data["翻译结果"]
        for index, line in enumerate(lines, start=1):
            t_result.append({"id": index, "原文": line, "译文": ""})

        # 将字典转换为JSON字符串
        json_string = json.dumps(json_data)
        return json_string

    def make_fanyi_dict(self, origina, translation) -> tuple[dict[str, str], bool]:
        """
        翻译词典

        :param zhipu_result: zhipu翻译结果

        :return: dict[str,str],原文，译文
        """
        sub_dict: Dict[str, str] = {}
        have_match = True

        # 执行比较
        source_lines = origina.split("\n")
        translation_lines = translation
        if len(translation_lines) != len(source_lines):
            have_match = False
            logger.warning(
                f"{ LogColors.WARNING.value}"
                f"原文行数和译文行数不一致，请检查翻译结果 {len(source_lines)}!={len(translation_lines)}"
                f"{LogColors.RESET_COLOR.value}"
            )

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

    def clean_text(text):
        # 去除多余空格
        text = re.sub(r"\s+", "", text)
        # 去除特殊字符
        text = re.sub(r"[^\w\s]", "", text)
        # 转换为小写
        text = text.lower()
        return text

    def normalize_punctuation(text):
        # 标准化标点符号（这里简单地移除了它们）
        text = re.sub(r"[.,!?;:]", "", text)
        return text

    # 比较翻译前和翻译后的原文是否一致
    def compare_original_text(self, original_text, translation_text):
        differences = []

        dict1 = json.loads(original_text)
        dict2 = json.loads(translation_text)

        # 获取两个JSON对象中的“翻译结果”数组
        results1 = dict1.get("翻译结果", [])
        results2 = dict2.get("翻译结果", [])

        results1 = [
            ZhipuEngine.normalize_punctuation(ZhipuEngine.clean_text(x.get("原文")))
            for x in results1
        ]
        results2 = [
            ZhipuEngine.normalize_punctuation(ZhipuEngine.clean_text(x.get("原文")))
            for x in results2
        ]

        if len(results1) != len(results2):
            logger.warning(
                f"{LogColors.WARRING.value}"
                f"两个JSON对象中的“翻译结果”数组长度不一致"
                f"{len(results1)}-{len(results2)}"
                f"{LogColors.RESET_COLOR.value}"
            )

        # 确保两个数组长度相同
        max_len = max(len(results1), len(results2))
        for i in range(max_len):
            result1 = results1[i] if i < len(results1) else None
            result2 = results2[i] if i < len(results2) else None

            if result1 and result2:
                if result1 != result2:
                    differences.append(
                        f"Difference at index {i+1}: {result1} != {result2}"
                    )
            elif result1:
                differences.append(
                    f"Item {i+1} is missing in second dictionary: {result1}"
                )
            elif result2:
                differences.append(
                    f"Item {i+1} is missing in first dictionary: {result2}"
                )

        return differences

    def split_list_into_chunks(self, str_list, max_count):
        chunks = []
        current_chunk = []
        current_length = 0

        for s in str_list:
            # 计算当前字符串的长度
            str_length = len(s)
            # 如果当前子列表加上新字符串后长度会超过max_count，则开始一个新的子列表
            if current_length + str_length > max_count:
                chunks.append(current_chunk)
                current_chunk = []
                current_length = 0
            # 将字符串添加到当前子列表，并更新当前子列表的长度
            current_chunk.append(s)
            current_length += str_length

        # 添加最后一个子列表（如果有）
        if current_chunk:
            chunks.append(current_chunk)

        return chunks

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
