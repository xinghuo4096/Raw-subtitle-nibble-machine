import json
import os
from typing import Dict


def split_list_into_chunks(str_list, max_count):
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


# 示例使用
str_list = ["hello", "world", "this", "is", "a", "test"]
max_count = 10
result = split_list_into_chunks(str_list, max_count)
print(result)


movie_filepath = "c:/test/d/Sloborn.S01E01.1080p.BluRay.x264-JustWatch.en.srt"

# 获取文件名
file_name = os.path.basename(movie_filepath)

# 去掉文件扩展名
file_name_without_extension = os.path.splitext(file_name)[0]

# 提取最后一个点之前的文件名部分
result = file_name_without_extension.rsplit(".", 1)[0]
print(result)


from itertools import zip_longest

a = ["key1", "key2"]
b = ["value1", "value2", "value3", "value4"]

a1 = ["key1", "key2", "key3", "key4"]
b1 = ["value1", "value2"]


def zip_sub1_sub2(sub1, sub2) -> Dict[str, str]:
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
                merged_dict[key] = f"None_{i+1}"
        else:
            # 如果 key 是 None，创建一个新的键
            merged_dict[f"key_{i+1}"] = str(value)
    return merged_dict


print(str(None))
print(zip_sub1_sub2(a, b))
print(zip_sub1_sub2(a1, b1))


result_dict = {"key1": "value1", "key2": "value2"}
result_str = str(result_dict)
print(result_str)


result_dict = {'key1': 'value1', 'key2': 'value2'}
result_str = json.dumps(result_dict)
print(result_str)
