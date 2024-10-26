import os

from Srt import load_srt_fromfile

# 定义可能的结束字符
END_CHARS = (".", "?", "!", ":", ";", ",", "—", "(", ")", '"', "'", "…")


def preprocess_and_detect_sentence_boundaries(sub_file_path):
    """
    预处理字幕文件并检测分句断句错误。

    参数:
    sub_file_path (str): 原始字幕文件的路径。
    output_correction_file (str): 用于记录需要手动修复的分句错误的输出文件路径。

    返回:
    None

    功能描述:
    - 读取并预处理字幕文件，包括清理不必要的字符和格式。
    - 检测分句断句错误，例如，过长的句子可能需要拆分，或者由于错误的分句导致的句子断裂。
    - 生成一个包含潜在分句错误的列表，并将其写入到指定的输出文件中。
    - 输出文件将包含错误的句子位置和建议的修复措施，以便进行人工审核和修复。

    注意:
    - 确保输入的字幕文件格式正确，且路径有效。
    - 输出文件将被创建在指定的路径，如果文件已存在，其内容将被覆盖。
    """
    # 预处理字幕文件
    result_srt = load_srt_fromfile(sub_file_path)
    result = []

    return result


if __name__ == "__main__":
    mpath = "c:/test/d/"
    sub_type = "en"
    os.chdir(mpath)
    # 配置翻译引擎

    flist = os.listdir(".")
    i = 1
    for item in flist:
        try:
            if os.path.isfile(item):
                fname = item[: -(3 + 2 + len(sub_type))]
                sub_ext = item[-(4 + len(sub_type)) : -4]
                fext = item[-3:]

                if fext == "srt" and sub_ext == sub_type:
                    print(f"处理文件{i}：{item}")
                    i += 1
                    result = preprocess_and_detect_sentence_boundaries(item)

                    print(result)
        except Exception as e:
            print(f"处理文件{i}：{item}出错，错误信息：{e}")
            i += 1
