import json

from zhipuai import ZhipuAI  # type: ignore

from translation_engine import TranslationEngine


class ZhipuEngine(TranslationEngine):
    def __init__(self, api_key, config):
        self.api_key = self.load_api_key(api_key)
        self.client = ZhipuAI(api_key=self.api_key)
        self.token_usage = 0
        self.save_token_usage_file = (
            "token_usage.json"  # 初始化save_token_usage的文件名
        )
        self.config = self.load_config(config)  # 从配置文件加载参数

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

    def load_config(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                config = json.load(file)
                return config
        except FileNotFoundError:
            print("配置文件未找到，请确保存在config.json文件。")
            raise Exception("配置文件未找到，请确保存在config.json文件。")
        except json.JSONDecodeError:
            print("配置文件格式错误，请确保config.json文件是一个有效的JSON文件。")
            raise Exception(
                "配置文件格式错误，请确保config.json文件是一个有效的JSON文件。"
            )

    def translate(self, user_input):
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
            self.tokens_usage["completion_tokens"] +=\
                response.usage.completion_tokens
            self.tokens_usage["total_tokens"] += response.usage.total_tokens
            return result
        except Exception as e:
            print(f"发生错误: {e}")
            return None

    def save_token_usage(self, file_path=None):
        if file_path is None:
            file_path = self.save_token_usage_file  # 使用初始化的文件名
        try:
            with open(file_path, "w") as file:
                json.dump({"total_tokens": self.tokens_usage}, file)
            print(f"Token使用统计已保存到 {file_path}")
        except Exception as e:
            print(f"保存Token使用统计时发生错误: {file_path},{e}")
