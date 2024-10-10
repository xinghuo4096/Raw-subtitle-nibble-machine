"""

### 使用指南
翻译目录下所有srt文件。
它读取一个目录中的所有`.srt`文件，并执行一系列操作，包括清理字幕、生成双语字幕、合并字幕等。以下是代码的用法和必需的文件：

### 翻译目录下所有srt文件：

1. **定义工作目录**：设置`mpath`变量为你想要处理字幕文件的目录路径。

2. **读取目录中的文件**：使用`os.listdir(".")`获取当前目录下的所有文件。

3. **循环处理每个文件**：对于每个文件，检查是否是`.srt`文件，并且扩展名是否符合要求。

4. **清理字幕**：调用`clear_subtile_fun1`和`clear_subtile_fun2`函数来清理字幕文件。

5. **生成字幕词汇表**：调用`make_subtile_glossary_fun1`和`make_subtile_glossary_fun2`函数来处理字幕文件，可能涉及添加词汇表或术语。

6. **翻译字幕**：使用`智谱AI`来翻译英文字幕为中文。

7. **生成双语字幕**：调用`make_double_lanague_subtitle`函数来生成双语字幕。

8. **合并字幕**：调用`merge_ass_tofile`函数来合并中文和英文字幕为一个`.ass`文件。
其他参考 example4.py
#### 需要配置的文件
- **翻译引擎**:
  - `zhipu_api_key.json`: 包含智谱AI的API的密钥信息。
    类似：
    {
      "api_key": "your_api_key"
    }
  -'zhipu_fy.config.json':包含智谱AI的API的配置信息。
    类似：
    {
      "model": "glm-4-plus",
      "system_content": "你是电视剧对话翻译专家，你会结合上下文，结合剧情，完成翻译。\n-\n-s输出内容，第一行为“******”就一行不要换行；第二行为“******”包含“***”，“***”，“***”，就一行不要换行；之后是翻译结果，结果第一行是原文，第二行是译文，以此类推，译文内容格式和原内容保持一样，不要按句子换行。",
      "top_p": 0.7,
      "temperature": 0.95,
      "max_tokens": 4095
    }

  - `ZhipuEngine`: 智谱AI API的封装类，用于翻译字幕内容。
- **字幕文件**:
  - `test.movie.en.srt`: 原始英文字幕文件。
  - `test.movie.en.2.srt`: 经过第一次清理后的英文字幕文件。
  - `test.movie.en.3.srt`: 经过第二次清理后的英文字幕文件。
  - `test.movie.cn.srt`: 最终生成的中文字幕文件。
  - `test.movie.cnen.ass`: 合并后的双语字幕文件。
  - `test.movie.unalgin.txt`: 未对齐的字幕文件。

- **错误和字典文件**:
  - `test.movie.err.txt`: 错误信息文件。
  - `test.movie.dict.txt`: 字典文件，用于双语字幕生成。

- **模板文件**:
  - `ass_template_cn_en_1280.txt`: ASS字幕模板文件。
  - `ass_info_head_cn_en_1280.txt`: ASS字幕头部信息文件。

#### 详细步骤
1. **清除字幕**:
   - `clear_subtile_fun1`: 清除第一次字幕中的多余内容。
   - `clear_subtile_fun2`: 清除第二次字幕中的多余内容。

2. **生成双语字幕**:
   - `make_double_lanague_subtitle`: 根据英文字幕生成双语字幕。
   - 参数:
     - `media`: 媒体文件名。
     - `from_sub`: 源字幕文件。
     - `to_sub`: 目标字幕文件。
     - `err_text`: 错误信息文件。
     - `dict_text`: 字典文件。
     - `sleep_time`: 等待时间。

3. **合并字幕**:
   - `merge_ass_tofile`: 合并双语字幕文件。
   - 参数:
     - `first_subtitle_fname`: 第一个字幕文件（中文）。
     - `second_subtitle_fname`: 第二个字幕文件（英文）。
     - `new_subtitle_fname`: 新的合并字幕文件。
     - `unalign_subtitle_fname`: 未对齐的字幕文件。
     - `ass_template_fname`: ASS字幕模板文件路径。
     - `ass_head_fname`: ASS字幕头部信息文件路径。
     - `mark1`: 第一个字幕标记。
     - `mark2`: 第二个字幕标记。
     - `mini_time`: 最小合并时间。
     - `max_cnsubtitle`: 最大中文字幕行数。

#### 注意事项
- 确保所有文件路径正确无误。
- 确保模板文件和头部信息文件的格式正确。
- 根据需要调整 `sleep_time`、`mark1`、`mark2`、`mini_time` 和 `max_cnsubtitle` 参数。

确保所有依赖的函数（如 `clear_subtile_fun1`、`clear_subtile_fun2`、`make_double_lanague_subtitle` 和 `merge_ass_tofile`）都已定义且可用。

#### 用到SrtMergeBox的文件
ass_template_cn_en_1280.txt 和 ass_info_head_cn_en_1280.txt 是ASS字幕的模板文件，它们通常用于定义字幕的样式和头部信息。这些文件可以在SrtMergeBox项目中找到。

SrtMergeBox是一个用于合并两个SRT格式字幕为SRT或ASS格式字幕的工具，目的是制作双语字幕。这些模板文件通常位于项目的 indata 文件夹中。

要获得这些文件，你可以访问SrtMergeBox的Gitee仓库，网址是：https://gitee.com/xinghuo4096/SrtMergeBox 。在这个仓库中，你可以找到项目的所有源代码以及相关的文件，包括字幕模板文件。

在使用这些模板文件之前，你可能需要根据你的需求对它们进行一些自定义修改。例如，你可以修改字体名称、大小、颜色等参数来满足你的字幕样式需求。这些文件的修改通常涉及到ASS字幕的样式代码，比如 Style: 和 Format: 部分。

请注意，使用这些文件时，你需要确保你的字幕文件时间轴是对齐的，并且你可能需要安装一些额外的库，比如 chardet，来处理字幕文件的编码问题。安装这个库的命令是 pip install chardet
。

最后，合并后的字幕文件和未对齐的字幕部分将被存储在 outdata 文件夹中。
"""

import os

from Srt import Srt, merge_ass_tofile

from clear_subtitle import (
    clear_subtile_fun1,
    clear_subtile_fun2,
    make_subtile_glossary_fun1,
    make_subtile_glossary_fun2,
)
from double_language_subtitle import make_double_lanague_subtitle
from zhipu_ai_fy import ZhipuEngine


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

    # 注意工作目录
    translator = ZhipuEngine(
        api_key="config/my_zhipu_api_key.json",
        config="my_zhipu_fy",
        lib_path="config"
    )
    translator.save_token_usage_file = "token_usage.json"

    mpath = "c:/test/d/"
    sub_type = "en"
    os.chdir(mpath)
    # 配置翻译引擎

    
    flist = os.listdir(".")
    i = 1
    for item in flist:
        if os.path.isfile(item):
            fname = item[: -(3 + 2 + len(sub_type))]
            sub_ext = item[-(4 + len(sub_type)) : -4]
            fext = item[-3:]

            if fext == "srt" and sub_ext == sub_type:
                clear_subtile_fun1(f"{fname}.{sub_type}.srt", f"{fname}.en.2.srt")
                clear_subtile_fun2(f"{fname}.en.2.srt", f"{fname}.en.3.srt")
                make_subtile_glossary_fun1(
                    f"{fname}.en.3.srt", f"{fname}.en.4.srt", "../indata/glossary.txt"
                )

                make_double_lanague_subtitle(
                    media=f"movie {fname}",
                    from_sub=f"{fname}.en.4.srt",
                    to_sub=f"{fname}.cn.1.srt",
                    err_text=f"{fname}.err.txt",
                    dict_text=f"{fname}.dict.txt",
                    translate_engner=translator,
                    messagefun=translator.zhipuai_subtitle_message,
                    use_dict=False,
                )
                make_subtile_glossary_fun2(
                    f"{fname}.cn.1.srt", f"{fname}.cn.2.srt", "../indata/glossary.txt"
                )
                merge_ass_tofile(
                    first_subtitle_fname=f"{fname}.cn.2.srt",
                    second_subtitle_fname=f"{fname}.en.3.srt",
                    new_subtitle_fname=f"{fname}.cnen.ass",
                    unalign_subtitle_fname=f"{fname}.unalgin.txt",
                    ass_template_fname=os.path.join(
                        "../indata", "ass_template_cn_en_1920.txt"
                    ),
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
