# 比较翻译前和翻译后的原文是否一致
import json
import re


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


def compare_original_text(original_text, translation_text):
    differences = []

    dict1 = json.loads(original_text)
    dict2 = json.loads(translation_text)

    # 获取两个JSON对象中的“翻译结果”数组
    results1 = dict1.get("翻译结果", [])
    results2 = dict2.get("翻译结果", [])

    results1 = [normalize_punctuation(clean_text(x.get("原文"))) for x in results1]
    results2 = [normalize_punctuation(clean_text(x.get("原文"))) for x in results2]
    print(results1)
    print(results2)
    if len(results1) != len(results2):
        print(
            f"两个JSON对象中的“翻译结果”数组长度不一致"
            f"{len(results1)}-{len(results2)}"
        )

    # 确保两个数组长度相同
    max_len = max(len(results1), len(results2))
    for i in range(max_len):
        result1 = results1[i] if i < len(results1) else None
        result2 = results2[i] if i < len(results2) else None

        if result1 and result2:
            if result1 != result2:
                differences.append(f"Difference at index {i+1}: {result1} != {result2}")
        elif result1:
            differences.append(f"Item {i+1} is missing in second dictionary: {result1}")
        elif result2:
            differences.append(f"Item {i+1} is missing in first dictionary: {result2}")

    return differences


if __name__ == "__main__":
    original_text = (
        '{"翻译结果": [{"原文": "你好，世 界。"}, {"原文": "这 是一个测试。"}]}'
    )
    translation_text = (
        '{"翻译结果": [{"原文": "你好，世 界。"}, {"原文": "这是一 个测试!"}]}'
    )
    differences = compare_original_text(original_text, translation_text)
    if differences:
        print("原文不一致的地方：")
        for diff in differences:
            print(diff)
    else:
        print("原文一致")
