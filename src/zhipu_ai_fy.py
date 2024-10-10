import datetime
import importlib
import json
import logging
import logging.config
import os
import re
import sys
from typing import Dict

from json_repair import repair_json
from zhipuai import ZhipuAI  # type: ignore

from jzhipu_ai_json import try_parse_json_object
from rsnm_log import setup_logging
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

        # 访问配置信息
        model = self.config["model"]
        system_content = self.config["system_content"]
        top_p = self.config["top_p"]
        temperature = self.config["temperature"]
        max_tokens = self.config["max_tokens"]

        # 打印配置信息
        logger.info(f"Model: {model}")
        logger.info(f"System Content (truncated): {system_content}")
        logger.info(f"Top P: {top_p}")
        logger.info(f"Temperature: {temperature}")
        logger.info(f"Max Tokens: {max_tokens}")

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
            # 显示当前工作目录
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

    def translate(self, user_input, from_language, to_language, sleep_time):
        try:
            response = self.client.chat.completions.create(
                model=self.config.get("model", "glm-4-plus"),
                messages=[
                    {
                        "role": "system",
                        "content": self.config.get(
                            "system_content",
                            "你是电视剧对话翻译家，你会结合上下文并结合剧情完成翻译。",
                        ),
                    },
                    {"role": "user", "content": "要翻译的内容如下：\n" + user_input},
                ],
                top_p=self.config.get("top_p", 0.7),
                temperature=self.config.get("temperature", 0.95),
                max_tokens=self.config.get("max_tokens", 4095),
                stream=False,
            )
            result = ""

            logger.info("\033[1;32m" + f"client: {response}" + "\033[0m")

            action_match = PATTERN.search(response.choices[0].message.content)
            if action_match is not None:
                json_text, json_object = try_parse_json_object(
                    action_match.group(1).strip()
                )

                result = json.dumps(json_object)

                self.tokens_usage["prompt_tokens"] += response.usage.prompt_tokens
                self.tokens_usage["completion_tokens"] += (
                    response.usage.completion_tokens
                )
                self.tokens_usage["total_tokens"] += response.usage.total_tokens

                return result, self.tokens_usage["total_tokens"]
            else:
                logger.info("Error: response.choices[0].message.content")
                return None
        except Exception as e:
            logger.info(f"发生错误: {e}")
            logger.info(f"{user_input} 翻译失败,请修改，修改内容要和原文字数一样。")

            return None

    def make_fanyi_dict(self, zhipu_result) -> Dict[str, str]:
        """
        翻译词典

        :param zhipu_result: zhipu翻译结果

        :return: dict[str,str],原文，译文
        """
        line_dict: Dict[str, str] = {}

        try:
            # 将字符串解析为JSON对象

            data = json.loads(zhipu_result)

            # 提取剧情总结
            summary = data.get("剧情总结", "")

            # 提取翻译风格
            style = data.get("翻译风格", {})

            # 提取翻译结果
            translations = data.get("翻译结果", [])

            # 提取翻译结果
            translations = data.get("翻译结果", [])

            logger.info(summary)
            logger.info(style)

            # 创建一个空字典来存储原文和译文的对应关系
            original_to_translation_dict = {}

            # 遍历翻译结果列表，将原文和译文添加到字典中
            for item in translations:
                original_text = item.get("原文", "")
                translation_text = item.get("译文", "")
                if len(translation_text) > 5 and not re.search(
                    r"[\u4e00-\u9fa5]", translation_text
                ):
                    logger.info(f"The line {translation_text} \
                            does not contain Chinese characters.")
                else:
                    original_to_translation_dict[original_text] = translation_text

            for (
                original_text,
                translation_text,
            ) in original_to_translation_dict.items():
                line_dict[original_text] = translation_text

            # 打印结果
        except json.JSONDecodeError as e:
            logger.info(f"JSON解析错误: {e}")

        return line_dict

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


if __name__ == "__main__":
    pass
