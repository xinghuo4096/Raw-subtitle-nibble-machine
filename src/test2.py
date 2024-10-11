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
