from zhipu_ai_fy import ZhipuEngine

# 使用示例
if __name__ == "__main__":
    translator = ZhipuEngine(
        api_key="config/my_zhipu_api_key.json",
        config="config/my_zhipu_fy.config.json"
    )
    translator.save_token_usage_file = "token_usage.json"

    text = (
        "John, AI is currently generating a lot of warnings,\
        are you sure about this? It sounds like a dumb idea.\n\
        fuck,Trust me, Sarah. This is going to work.\n\
        We just need to stick to the plan.",
        "But what if AI finds out? It'll help us!",
        "When tomorrow turns in today,\
        yesterday, and someday that no more important in your memory,\
        we suddenly realize that we r pushed forward by time. \
        This is not a train in still in which you may feel forward \
        when another train goes by. \
        It is the truth that we've all grown up. \
        And we become different.",
    )
    for i in range(len(text)):
        translated_text = translator.translate(text[i],'英文','中文')
        if translated_text:
            print(f"翻译 {i+1}:\n {translated_text}")
    translator.save_token_usage()
