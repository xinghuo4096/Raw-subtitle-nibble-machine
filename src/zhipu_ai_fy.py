import datetime
import importlib
import json
import os
import sys
from typing import Dict

from zhipuai import ZhipuAI  # type: ignore

from translation_engine import TranslationEngine


class ZhipuEngine(TranslationEngine):
    def __init__(self, api_key, config: str = "my_zhipu_fy",lib_path='config'):
        self.api_key = self.load_api_key(api_key)
        self.client = ZhipuAI(api_key=self.api_key)
        self.token_usage = 0
        self.save_token_usage_file = (
            "token_usage.json"  # 初始化save_token_usage的文件名
        )

        self.config = self.load_config(config,lib_path)

        # 访问配置信息
        model = self.config["model"]
        system_content = self.config["system_content"]
        top_p = self.config["top_p"]
        temperature = self.config["temperature"]
        max_tokens = self.config["max_tokens"]

        # 打印配置信息
        print(f"Model: {model}")
        print(f"System Content (truncated): {system_content}")
        print(f"Top P: {top_p}")
        print(f"Temperature: {temperature}")
        print(f"Max Tokens: {max_tokens}")

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
            print("API密钥文件未找到，请确保存在api_key.json文件。")
            raise Exception("API密钥文件未找到，请确保存在api_key.json文件。")
        except json.JSONDecodeError:
            print("API密钥文件格式错误，请确保api_key.json文件是一个有效的JSON文件。")
            raise Exception(
                "API密钥文件格式错误，请确保api_key.json文件是一个有效的JSON文件。"
            )

    def load_config(self, zhipu_config,lib_path='config'):
        try:
            # 动态加载 config 模块
            # 显示当前工作目录
            current_directory = os.getcwd()
            print(f"当前工作目录: {current_directory}")

            # 检查当前目录的config文件夹是否存在
            config_path = os.path.join(current_directory,lib_path )
            if os.path.exists(config_path):
                # 将config目录添加到模块搜索路径
                sys.path.append(config_path)
                print(f"'config'目录已添加到模块搜索路径：{config_path}")
            else:
                print(f"'config'目录不存在：{config_path}")

            config = importlib.import_module(zhipu_config)

            return config.config
        except ImportError as e:
            print(f"无法导入配置文件：{e}")
            raise Exception(f"无法导入配置文件：{e}")
        except Exception as e:
            print(f"加载配置文件时发生错误：{e}")
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
            result = response.choices[0].message.content
            self.tokens_usage["prompt_tokens"] += response.usage.prompt_tokens
            self.tokens_usage["completion_tokens"] += response.usage.completion_tokens
            self.tokens_usage["total_tokens"] += response.usage.total_tokens
            return result, self.tokens_usage["total_tokens"]
        except Exception as e:
            print(f"发生错误: {e}")
            return None

    def make_fanyi_dict(self, zhipu_result) -> Dict[str, str]:
        """
        翻译词典

        :param zhipu_result: zhipu翻译结果

        :return: dict[str,str],原文，译文
        """
        lines = zhipu_result.split("\n")
        lines = [line for line in lines if line.strip()]
        print(lines[0])
        print(lines[1])
        print("---")

        line_dict: Dict[str, str] = {}
        # 如果len(lines)为奇数，则删除一行，并打印一个错误提示
        if len(lines) % 2 != 0:
            print(f"{len(lines)},Error: The number of lines is not even.")
            lines.pop()

        # 遍历列表，步长为2，从索引2开始
        for i in range(2, len(lines), 2):
            # 将每对连续的行添加到字典中，其中第一行作为键，第二行作为值
            line_dict[lines[i]] = lines[i + 1]

        return line_dict

    def save_token_usage(self, file_path=None):
        if file_path is None:
            file_path = self.save_token_usage_file  # 使用初始化的文件名
        try:
            with open(file_path, "w") as file:
                json.dump({"total_tokens": self.tokens_usage}, file)
            print(f"Token使用统计已保存到 {file_path}")
        except Exception as e:
            print(f"保存Token使用统计时发生错误: {file_path},{e}")

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

        text1 = f'total time: {total_time} sec, finally time: {finally_time} sec,endtime:{
            time1.strftime("%Y-%m-%d %H:%M:%S")}'
        print(text1)
        return

if __name__ == "__main__":
    pass