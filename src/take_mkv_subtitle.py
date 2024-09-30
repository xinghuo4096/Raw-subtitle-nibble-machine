"""
   查看mkv的信息和提取字幕
### 使用方法：

1. **设置路径**：
   - `mpath`: 包含MKV文件的目录路径。
   - `mkv_info`: `mkvinfo.exe`工具的完整路径。
   - `mkv_extract`: `mkvextract.exe`工具的完整路径。

2. **修改字幕序号**：
   - 根据`mkvinfo`显示的字幕序号，修改`tracks`命令中的序号来提取特定字幕。

3. **运行脚本**：
   - 调用`mkv_subtitle_extract()`函数开始提取字幕。

### 使用注意事项：

- 确保`mkvinfo.exe`和`mkvextract.exe`工具已正确安装，并提供正确的路径。
- 确保`mpath`路径正确，且包含要处理的MKV文件。
- 根据MKV文件中的实际字幕序号，调整`tracks`命令中的序号。
- 此脚本需要在命令行环境中运行，确保系统允许执行外部命令。
- 在提取字幕之前，可以先运行`mkv_subtitle_extract(False)`来查看`mkvinfo`的输出，以确定正确的字幕序号。
- 默认情况下，脚本会自动提取字幕；如果只需要查看MKV信息而不提取字幕，将函数参数设置为`False`。

### 言简意赅的使用步骤：

1. 确认`mpath`, `mkv_info`, `mkv_extract`路径设置正确。
2. 运行`mkv_subtitle_extract()`提取字幕。
3. 如需查看MKV信息，运行`mkv_subtitle_extract(False)`。

"""

import os
from os import path


def mkv_subtitle_extract(extract: bool = True):
    """
    提取mkv字幕

    - 电影路径，mkvinfo，mkvextract路径。

    mpath = 'F:/1/testdir/'
    mkv_info = r'D:/Tools/Mkv/mkvtoolnix/mkvinfo.exe'
    mkv_extract = r'D:/Tools/Mkv/mkvtoolnix/mkvextract.exe'

    - 需要根据mkvinfo显示的字幕序号修改

    `f'tracks  3:"{fname}.sdh.srt" '`

    例子：

    提取第四条，序号为3的字幕,并存储为.sdh.srt
    'tracks  3:"{fname}.sdh.srt" '

    """

    mpath = "O:/Sloborn - season 2"
    mkv_info = r"m:/Tools/Mkv/mkvtoolnix/mkvinfo.exe"
    mkv_extract = r"m:/Tools/Mkv/mkvtoolnix/mkvextract.exe"
    os.chdir(mpath)
    flist = os.listdir(".")
    for item in flist:
        if path.isfile(item):
            fname = os.path.splitext(item)[0]
            fext = os.path.splitext(item)[1]
            if fext == ".mkv":
                os.system(f'{mkv_info} "{item}"')
                if extract:
                    extract_commondline = " ".join(
                        [mkv_extract, f'"{item}"', f'tracks  2:"{fname}.en.srt"  ']
                    )
                    print(extract_commondline)
                    os.system(extract_commondline)


# mkv_subtitle_extract(False)
mkv_subtitle_extract()
