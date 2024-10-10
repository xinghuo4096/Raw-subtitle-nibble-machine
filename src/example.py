"""
翻译目录下所有srt文件。
它读取一个目录中的所有`.srt`文件，并执行一系列操作，包括清理字幕、生成双语字幕、合并字幕等。以下是代码的用法和必需的文件：

### 翻译目录下所有srt文件：

1. **定义工作目录**：设置`mpath`变量为你想要处理字幕文件的目录路径。

2. **读取目录中的文件**：使用`os.listdir(".")`获取当前目录下的所有文件。

3. **循环处理每个文件**：对于每个文件，检查是否是`.srt`文件，并且扩展名是否符合要求。

4. **清理字幕**：调用`clear_subtile_fun1`和`clear_subtile_fun2`函数来清理字幕文件。

5. **生成字幕词汇表**：调用`make_subtile_glossary_fun1`和`make_subtile_glossary_fun2`函数来处理字幕文件，可能涉及添加词汇表或术语。

6. **翻译字幕**：使用`BaiduceEngine`（百度翻译API）来翻译英文字幕为中文。

7. **生成双语字幕**：调用`make_double_lanague_subtitle`函数来生成双语字幕。

8. **合并字幕**：调用`merge_ass_tofile`函数来合并中文和英文字幕为一个`.ass`文件。

### 必需的文件：

- **字幕模板文件**：`../indata/ass_template_cn_en_1280.txt`，用于定义合并后的字幕样式。**从SrtMergeBox里找**
- **字幕头部信息文件**：`../indata/ass_info_head_cn_en_1280.txt`，包含字幕文件的头部信息。**从SrtMergeBox里找**

- **词汇表文件**：`../indata/glossary.txt`，包含需要处理的词汇或术语列表。
- **百度翻译API配置文件**：`c:/test/config/mykeys.json`，包含百度翻译API的密钥。

### 注意事项：

- 确保所有必需的文件都在正确的路径上，并且文件路径使用的是正确的斜杠（`/`或`\`）。
- 确保`BaiduceEngine`类正确实现，并且能够使用提供的API密钥进行翻译。
- 代码中的`print`语句用于输出处理进度，你可以根据需要修改或删除这些语句。

### 示例：

假设你的工作目录是`c:/test/a/`，并且目录中有一些`.srt`字幕文件，你可以将这段代码保存为一个Python脚本，然后在命令行中运行它。脚本会自动处理目录中的所有`.srt`文件，并生成相应的双语字幕文件。

请确保你已经安装了所有必要的Python模块，并且正确配置了百度翻译API的密钥。此外，你还需要确保`Srt`、`clear_subtitle`和`double_language_subtitle`等模块是可用的，并且它们包含所需的函数。

### 例子
单个和多字幕处理的例子

会出错的情况

1. 句子太长，多数是歌词，
需要手动修字幕，把歌词结尾加句号“.”

2. 字幕文字部分，以数字开头
比如，如下：
```
........year
2000
```
需要修改srt文件里对于内容
如修复为：
`........year 2000`

"""

import os

from Srt import Srt, merge_ass_tofile

from baidu_ce_fy import BaiduceEngine
from clear_subtitle import (
    clear_subtile_fun1,
    clear_subtile_fun2,
    make_subtile_glossary_fun1,
    make_subtile_glossary_fun2,
)
from double_language_subtitle import make_double_lanague_subtitle


def main_batch2():
    """
    文件格式如下：

    文件名.en.srt
     fname = item[:-7]
     sub_ext = item[-6:-4]
     fext = item[-3:]


    文件名.sdh.srt
     fname = item[:-8]
     sub_ext = item[-7:-4]
     fext = item[-3:]
    """
    mpath = "c:/test/b/"
    sub_type = "en"
    os.chdir(mpath)

    flist = os.listdir(".")
    i = 1
    for item in flist:

        if os.path.isfile(item):

            fname = item[: -(3 + 2 + len(sub_type))]
            sub_ext = item[-(4 + len(sub_type)): -4]
            fext = item[-3:]

            if fext == "srt" and sub_ext == sub_type:
                clear_subtile_fun1(
                    f"{fname}.{sub_type}.srt", f"{fname}.en.2.srt")
                clear_subtile_fun2(f"{fname}.en.2.srt", f"{fname}.en.3.srt")
                make_subtile_glossary_fun1(
                    f"{fname}.en.3.srt", f"{fname}.en.4.srt",
                    "../indata/glossary.txt"
                )

                baiducd_fy = BaiduceEngine("../config/mykeys.json")

                make_double_lanague_subtitle(
                    media=f"movie {fname}",
                    from_sub=f"{fname}.en.4.srt",
                    to_sub=f"{fname}.cn.1.srt",
                    err_text=f"{fname}.err.txt",
                    dict_text=f"{fname}.dict.txt",
                    translate_engner=baiducd_fy,
                    use_dict=False,
                )
                make_subtile_glossary_fun2(
                    f"{fname}.cn.1.srt", f"{fname}.cn.2.srt",
                      "../indata/glossary.txt"
                )
                merge_ass_tofile(
                    first_subtitle_fname=f"{fname}.cn.2.srt",
                    second_subtitle_fname=f"{fname}.en.3.srt",
                    new_subtitle_fname=f"{fname}.cnen.ass",
                    unalign_subtitle_fname=f"{fname}.unalgin.txt",
                    ass_template_fname=os.path.join(
                        "../indata", "ass_template_cn_en_1920.txt"),
                    ass_head_fname=("../indata" "/ass_head_cn_en_1920.txt"),
                    mark1="",
                    mark2="",
                    mini_time=Srt.MINI_MERGE_TIME,
                    max_cnsubtitle=26,
                )

                print(i, "ok.", fname)
                i = i + 1


if __name__ == "__main__":

    main_batch2()
