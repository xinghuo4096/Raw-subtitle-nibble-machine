

import os
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


def convert_directory_ass_to_srt(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.lower().endswith('.srt'):
                ass_file_path = os.path.join(root, file)
                with open(ass_file_path, 'r', encoding='utf-8') as ass_file:
                    ass_content = ass_file.read()

                srt_content = asstosrt(ass_content)
                srt_file_name = os.path.splitext(file)[0] + '.srt'
                srt_file_path = os.path.join(target_dir, srt_file_name)

                with open(srt_file_path, 'w', encoding='utf-8') as srt_file:
                    srt_file.write(srt_content)
                print(f"Converted: {ass_file_path} to {srt_file_path}")


# 指定包含ASS文件的目录
source_directory = 'c:/test/b'
target_directory = 'c:/test/b2'

convert_directory_ass_to_srt(source_directory, target_directory)
