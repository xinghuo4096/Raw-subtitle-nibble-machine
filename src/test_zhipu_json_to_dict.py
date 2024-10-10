import json

# 假设你的字符串存储在变量str_data中
str_data = """
```json{
  "剧情总结": "这段对话发生在一个名叫Wednesday的青少年与朋友们之间。Wednesday表达了对世界末日和全球危机的无奈，同时对比了自己所在小镇Slaborn的平静生活。接着，朋友们讨论了Evelin的情况，并表现出对一些事情的困惑和不满。",
  "翻译风格": {
    "风格": "青春口语",
    "语言特色": "现代汉语",
    "模仿对象": "青春校园剧对话"
  },
  "翻译结果": [
    {
      "原文": "Wednesday Ever since I can remember, the world has been ending somewhere.",
      "译文": "Wednesday：从我记事起，世界总在某个地方走向末日。"
    },
    {
      "原文": "Species extinction, deforestation, economic crises, environmental pollution, terrorism and climate change. Thanks a lot!",
      "译文": "物种灭绝、森林砍伐、经济危机、环境污染、恐怖主义和气候变化。真是谢了！"
    },
    {
      "原文": "Pit stop?- Yes.",
      "译文": "休息一下？- 对。"
    },
    {
      "原文": "Somewhere there is always the next crisis, the next war - and mankind has but a few years left...",
      "译文": "总有个地方会发生下一场危机，下一场战争——人类只剩下几年时间……"
    },
    {
      "原文": "...to avert the apocalypse. You get used to it.",
      "译文": "……来避免末日。你习惯了就好。"
    }
  ]
}
```
"""

# 检查字符串是否以正确的JSON格式开头和结尾
str_data = str_data.strip()
if str_data.startswith("```json") and str_data.endswith("```"):
    try:
        # 将字符串解析为JSON对象
        str_data = str_data[7:-3]
        data = json.loads(str_data)

        # 提取剧情总结
        summary = data.get("剧情总结", "")

        # 提取翻译风格
        style = data.get("翻译风格", {})

        # 提取翻译结果
        translations = data.get("翻译结果", [])

        # 提取翻译结果
        translations = data.get("翻译结果", [])

        print(summary)
        print(style)

        # 创建一个空字典来存储原文和译文的对应关系
        original_to_translation_dict = {}

        # 遍历翻译结果列表，将原文和译文添加到字典中
        for item in translations:
            original_text = item.get("原文", "")
            translation_text = item.get("译文", "")
            original_to_translation_dict[original_text] = translation_text

        # 打印结果字典
        for original_text, translation_text in original_to_translation_dict.items():
            print(f"原文: {original_text}\n译文: {translation_text}\n")

        # 打印结果
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
else:
    print("字符串不是有效的JSON格式")
