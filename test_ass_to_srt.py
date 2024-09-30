import re

def convert_time_to_srt(time_str):
    # 将ASS时间戳格式转换为SRT时间戳格式
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split('.')
    return f"{hours}:{minutes}:{seconds},{milliseconds.zfill(3)}"  # 补足三位毫秒数

def asstosrt(ass_content):
    # 正则表达式匹配ASS文件中的对话事件，Layer字段可能缺失
    dialog_pattern = re.compile(r'Dialogue: *(?:\d+,)?(.*?),(.*?),(.*?),Default,,0,0,0,,(.*)')
    srt_content = ""
    index = 1

    for match in dialog_pattern.finditer(ass_content):
        start_time = convert_time_to_srt(match.group(2))
        end_time = convert_time_to_srt(match.group(3))
        text = match.group(4).strip().replace('\n', ' ')

        # 构建SRT格式的对话
        srt_content += f"{index}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{text}\n\n"
        index += 1

    return srt_content.strip()  # 移除最后的额外换行

# 测试数据
test_data = """
Dialogue: ,0:01:02.00,0:01:05.24,Default,,0,0,0,,ENTRANCE ONLY FOR STAFF!
Dialogue: ,0:01:44.92,0:01:48.00,Default,,0,0,0,,CAN IT GET ANY WORSE?
Dialogue: ,0:02:55.12,0:02:56.00,Default,,0,0,0,,PLACENTA DISFUNCTION...
Dialogue: ,0:03:36.00,0:03:37.00,Default,,0,0,0,,Damn it!
"""

# 执行转换并打印结果
converted_srt = asstosrt(test_data)
print(converted_srt)
