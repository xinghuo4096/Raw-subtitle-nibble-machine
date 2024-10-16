# Raw-subtitle-nibble-machine生肉啃食机

字幕翻译和双语字幕制作工具。

1. 将电影和剧集文件附带的srt格式字幕翻译为其他语言。支持大多数语言。比如中英，中德，中瑞典。

2. 将两种语言的srt格式字幕合并，生成srt或ass格式的双语字幕。

目前引擎：

1. 百度智能云的文本翻译-通用版（2024年9月30日）
<https://cloud.baidu.com/product/mt/text_trans>

2. 智谱AI-GLM-4-Plus （2024年10月17日）
<https://www.zhipuai.cn/>


## 安装requirements.txt

这个 `requirements.txt` 文件列出了几个 Python 库及其特定版本，这些库通常用于网络请求和字符编码处理。以下是每个库的简要说明：

1. **certifi**: 提供 Mozilla 可信任的 CA 证书包，用于 SSL 认证。
   - 版本: 2024.8.30

2. **chardet**: 字符编码检测库，用于自动检测文本文件的编码。
   - 版本: 5.2.0

3. **charset-normalizer**: 用于处理网络请求和文件的字符编码，具有更好的性能和准确性。
   - 版本: 3.3.2

4. **idna**: 用于处理国际化域名的库。
   - 版本: 3.10

5. **requests**: 一个简单易用的 HTTP 库，用于发送各种 HTTP 请求。
   - 版本: 2.32.3

6. **urllib3**: HTTP客户端库，用于发送 HTTP 请求，是 `requests` 库底层使用的库。
   - 版本: 2.2.3

### 使用这个 `requirements.txt` 文件安装依赖的步骤

1. **打开命令行界面**：
   - Windows 用户可以打开命令提示符或 PowerShell。
   - macOS 或 Linux 用户可以打开终端。

2. **导航到你的项目目录**：
   使用 `cd` 命令切换到包含 `requirements.txt` 文件的目录。例如：

   ```bash
   cd path/to/your/project
   ```

3. **安装依赖**：
   在包含 `requirements.txt` 文件的目录中，运行以下命令来安装所有列出的依赖：

   ```bash
   pip install -r requirements.txt
   ```

   这个命令会读取 `requirements.txt` 文件，并安装其中列出的所有依赖库及其指定版本。

4. **确认依赖安装**：
   安装完成后，你可以使用以下命令来确认所有依赖是否正确安装：

   ```bash
   pip list
   ```

   这个命令会列出当前环境中安装的所有包，你可以检查它们是否与 `requirements.txt` 文件中列出的一致。

5. **使用虚拟环境（可选但推荐）**：
   为了保持你的项目依赖与系统 Python 环境分开，建议使用虚拟环境。以下是如何使用虚拟环境的步骤：
   - 创建虚拟环境：

     ```bash
     python -m venv venv
     ```

   - 激活虚拟环境：
     - Windows:

       ```bash
       .\venv\Scripts\activate
       ```

     - macOS/Linux:

       ```bash
       source venv/bin/activate
       ```

   - 在虚拟环境中安装依赖：

     ```bash
     pip install -r requirements.txt
     ```

   - 退出虚拟环境：

     ```bash
     deactivate
     ```

使用虚拟环境有助于避免不同项目之间的依赖冲突，并使项目更加便携。

## take_mkv_subtitle.py 准备工作，提取MKV里面的srt文件

提取MKV视频文件中的字幕。它使用mkvtoolnix工具集中的mkvinfo和mkvextract命令行工具来完

### 使用方法

1. **设置路径**：
   - `mpath`: 包含MKV文件的目录路径。
   - `mkv_info`: `mkvinfo.exe`工具的完整路径。
   - `mkv_extract`: `mkvextract.exe`工具的完整路径。

2. **修改字幕序号**：
   - 根据`mkvinfo`显示的字幕序号，修改`tracks`命令中的序号来提取特定字幕。

3. **运行脚本**：
   - 调用`mkv_subtitle_extract()`函数开始提取字幕。

### 使用注意事项

- 确保`mkvinfo.exe`和`mkvextract.exe`工具已正确安装，并提供正确的路径。
- 确保`mpath`路径正确，且包含要处理的MKV文件。
- 根据MKV文件中的实际字幕序号，调整`tracks`命令中的序号。
- 此脚本需要在命令行环境中运行，确保系统允许执行外部命令。
- 在提取字幕之前，可以先运行`mkv_subtitle_extract(False)`来查看`mkvinfo`的输出，以确定正确的字幕序号。
- 默认情况下，脚本会自动提取字幕；如果只需要查看MKV信息而不提取字幕，将函数参数设置为`False`。

### 再提醒一次

1. 确认`mpath`, `mkv_info`, `mkv_extract`路径设置正确。
2. 运行`mkv_subtitle_extract()`提取字幕。
3. 如需查看MKV信息，运行`mkv_subtitle_extract(False)`。

## example3.py，单独处理字幕，生成双语字幕的用法介绍

 用它可以理解处理逻辑

### 使用指南

#### 概述

`mymain` 函数是一个处理字幕文件的脚本，它包括清除字幕中的多余内容、生成双语字幕、合并字幕文件等步骤。

#### 用法

1. **函数调用**: 直接调用 `mymain()` 函数即可执行整个字幕处理流程。
2. **文件路径**: 函数内部定义了文件路径 `fname`，该路径需要根据实际情况进行修改。
3. **fname 是一个字符串变量，它代表了一个文件的基本路径和名称，但不包括文件扩展名。**:这种用法允许你通过在变量后添加不同的扩展名来引用同一个文件的不同版本或相关文件。

#### 需要配置的文件

- **字幕文件**:
- **翻译引擎**:
  - `keys.json`: 包含百度翻译API的密钥信息。
    - 内容示例：

        类似：
        {
        "API_KEY": "你的API_KEY",
        "SECRET_KEY": "你的SECRET_KEY"
        }

  - 配置引擎：配置到config目录下,baidu = BaiduceEngine("../config/mykeys.json")

- `test.movie.en.srt`: **原始英文字幕文件。**
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

要获得这些文件，你可以访问SrtMergeBox的Gitee仓库，网址是：<https://gitee.com/xinghuo4096/SrtMergeBox> 。在这个仓库中，你可以找到项目的所有源代码以及相关的文件，包括字幕模板文件。

在使用这些模板文件之前，你可能需要根据你的需求对它们进行一些自定义修改。例如，你可以修改字体名称、大小、颜色等参数来满足你的字幕样式需求。这些文件的修改通常涉及到ASS字幕的样式代码，比如 Style: 和 Format: 部分。

请注意，使用这些文件时，你需要确保你的字幕文件时间轴是对齐的，并且你可能需要安装一些额外的库，比如 chardet，来处理字幕文件的编码问题。安装这个库的命令是 pip install chardet
。

最后，合并后的字幕文件和未对齐的字幕部分将被存储在 outdata 文件夹中。

## example1.py，批量处理字幕，生成双语字幕的用法介绍

翻译目录下所有srt文件。
它读取一个目录中的所有`.srt`文件，并执行一系列操作，包括清理字幕、生成双语字幕、合并字幕等。以下是代码的用法和必需的文件：

### 翻译目录下所有srt文件

1. **定义工作目录**：设置`mpath`变量为你想要处理字幕文件的目录路径。

2. **读取目录中的文件**：使用`os.listdir(".")`获取当前目录下的所有文件。

3. **循环处理每个文件**：对于每个文件，检查是否是`.srt`文件，并且扩展名是否符合要求。

4. **清理字幕**：调用`clear_subtile_fun1`和`clear_subtile_fun2`函数来清理字幕文件。

5. **生成字幕词汇表**：调用`make_subtile_glossary_fun1`和`make_subtile_glossary_fun2`函数来处理字幕文件，可能涉及添加词汇表或术语。

6. **翻译字幕**：使用`BaiduceEngine`（百度翻译API）来翻译英文字幕为中文。

7. **生成双语字幕**：调用`make_double_lanague_subtitle`函数来生成双语字幕。

8. **合并字幕**：调用`merge_ass_tofile`函数来合并中文和英文字幕为一个`.ass`文件。

### 必需的文件

- **字幕模板文件**：`../SrtMergeBox/indata/ass_template_cn_en_1280.txt`，用于定义合并后的字幕样式。
- **字幕头部信息文件**：`../SrtMergeBox/indata/ass_info_head_cn_en_1280.txt`，包含字幕文件的头部信息。
- **词汇表文件**：`../indata/glossary.txt`，包含需要处理的词汇或术语列表。
- **百度翻译API配置文件**：`c:/test/config/mykeys.json`，包含百度翻译API的密钥。

### 注意事项

- 确保所有必需的文件都在正确的路径上，并且文件路径使用的是正确的斜杠（`/`或`\`）。
- 确保`BaiduceEngine`类正确实现，并且能够使用提供的API密钥进行翻译。
- 代码中的`print`语句用于输出处理进度，你可以根据需要修改或删除这些语句。

### 示例

假设你的工作目录是`c:/test/a/`，并且目录中有一些`.srt`字幕文件，你可以将这段代码保存为一个Python脚本，然后在命令行中运行它。脚本会自动处理目录中的所有`.srt`文件，并生成相应的双语字幕文件。

请确保你已经安装了所有必要的Python模块，并且正确配置了百度翻译API的密钥。此外，你还需要确保`Srt`、`clear_subtitle`和`double_language_subtitle`等模块是可用的，并且它们包含所需的函数。

### 例子

单个和多字幕处理的例子

会出错的情况

1. 句子太长，多数是歌词，
需要手动修字幕，把歌词结尾加句号“.”

2. 字幕文字部分，以数字开头
比如，如下：

```text
........year
2000
```

需要修改srt文件里对于内容
如修复为：
`........year 2000`
