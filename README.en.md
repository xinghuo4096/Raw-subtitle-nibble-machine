# Raw-subtitle-nibble-machine Subtitle Translation and Bilingual Subtitle Creation Tool

A tool for translating subtitles that come with movie and TV show files in SRT format into other languages. It supports most languages, such as Chinese-English, Chinese-German, Chinese-Swedish, etc.

1. Translate SRT format subtitles of movies and TV series into other languages.
2. Merge two-language SRT format subtitles to generate bilingual subtitles in SRT or ASS format.

Current Engine:

1. Baidu Intelligent Cloud Text Translation - General Version (as of September 30, 2024)
<https://cloud.baidu.com/product/mt/text_trans>

2.Zhipu AI-GLM-4-Plus (October 17, 2024) 
https://www.zhipuai.cn/

## Install requirements.txt

This `requirements.txt` file lists several Python libraries and their specific versions, which are commonly used for web requests and character encoding processing. Here is a brief description of each library:

1. **certifi**: Provides the Mozilla trusted CA certificate package for SSL certification.
   - Version: 2024.8.30

2. **chardet**: A character encoding detection library that automatically detects the encoding of text files.
   - Version: 5.2.0

3. **charset-normalizer**: Used for handling the character encoding of web requests and files, with better performance and accuracy.
   - Version: 3.3.2

4. **idna**: A library for handling international domain names.
   - Version: 3.10

5. **requests**: A simple and easy-to-use HTTP library for sending various HTTP requests.
   - Version: 2.32.3

6. **urllib3**: An HTTP client library used for sending HTTP requests, which is the underlying library used by the `requests` library.
   - Version: 2.2.3

### Steps to Install Dependencies Using This `requirements.txt` File

1. **Open the Command Line Interface**:
   - Windows users can open the command prompt or PowerShell.
   - macOS or Linux users can open the terminal.

2. **Navigate to Your Project Directory**:
   Use the `cd` command to switch to the directory containing the `requirements.txt` file. For example:

   ```bash
   cd path/to/your/project
   ```

3. **Install Dependencies**:
   In the directory containing the `requirements.txt` file, run the following command to install all listed dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   This command will read the `requirements.txt` file and install all the dependency libraries and their specified versions.

4. **Confirm Dependency Installation**:
   After installation, you can use the following command to confirm whether all dependencies are installed correctly:

   ```bash
   pip list
   ```

   This command will list all the packages installed in the current environment, and you can check if they are consistent with those listed in the `requirements.txt` file.

5. **Use a Virtual Environment (Optional but Recommended)**:
   To keep your project dependencies separate from the system Python environment, it is recommended to use a virtual environment. Here are the steps on how to use a virtual environment:
   - Create a virtual environment:

     ```bash
     python -m venv venv
     ```

   - Activate the virtual environment:
     - Windows:

       ```bash
       .\venv\Scripts\activate
       ```

     - macOS/Linux:

       ```bash
       source venv/bin/activate
       ```

   - Install dependencies in the virtual environment:

     ```bash
     pip install -r requirements.txt
     ```

   - Exit the virtual environment:

     ```bash
     deactivate
     ```

Using a virtual environment helps to avoid dependency conflicts between different projects and makes the project more portable.

## Preparing take_mkv_subtitle.py to Extract SRT Files from MKV

Extract subtitles from MKV video files. It uses the mkvinfo and mkvextract command-line tools from the mkvtoolnix toolkit.

### Usage

1. **Set Paths**:
   - `mpath`: The directory path containing MKV files.
   - `mkv_info`: The full path to the `mkvinfo.exe` tool.
   - `mkv_extract`: The full path to the `mkvextract.exe` tool.

2. **Modify Subtitle Track Numbers**:
   - Adjust the number in the `tracks` command according to the subtitle track number displayed by `mkvinfo` to extract specific subtitles.

3. **Run the Script**:
   - Call the `mkv_subtitle_extract()` function to start extracting subtitles.

### Notes

- Ensure that the `mkvinfo.exe` and `mkvextract.exe` tools are correctly installed and the paths are provided correctly.
- Ensure that the `mpath` path is correct and contains the MKV files to be processed.
- Adjust the number in the `tracks` command according to the actual subtitle track number in the MKV file.
- This script needs to be run in a command-line environment, make sure the system allows the execution of external commands.
- Before extracting subtitles, you can run `mkv_subtitle_extract(False)` to view the output of `mkvinfo` to determine the correct subtitle track number.
- By default, the script will automatically extract subtitles; if you only need to view MKV information without extracting subtitles, set the function parameter to `False`.

## example3.py, Introduction to the Use of Subtitle Processing to Generate Bilingual Subtitles

Use it to understand the processing logic.

### User Guide

#### Overview

The `mymain` function is a script for processing subtitle files, including clearing redundant content in subtitles, generating bilingual subtitles, and merging subtitle files, etc.

#### Usage

1. **Function Call**: Directly call the `mymain()` function to execute the entire subtitle processing workflow.
2. **File Path**: The function internally defines the file path `fname`, which needs to be modified according to the actual situation.
3. **fname is a string variable that represents the basic path and name of a file, but does not include the file extension name.**: This usage allows you to refer to different versions or related files of the same file by adding different extensions after the variable.

#### Required Configuration Files

- **Subtitle Files**:
- **Translation Engine**:
  - `keys.json`: Contains the API key information for Baidu Translation API.
    - Example content:

        Similar to:
        {
        "API_KEY": "your_API_KEY",
        "SECRET_KEY": "your_SECRET_KEY"
        }

  - Engine configuration: Configure in the config directory, baidu = BaiduceEngine("../config/mykeys.json")

- `test.movie.en.srt`: **Original English subtitle file.**
- `test.movie.en.2.srt`: English subtitle file after the first cleaning.
- `test.movie.en.3.srt`: English subtitle file after the second cleaning.
- `test.movie.cn.srt`: The final generated Chinese subtitle file.
- `test.movie.cnen.ass`: Merged bilingual subtitle file.
- `test.movie.unalgin.txt`: Unaligned subtitle file.

- **Error and Dictionary Files**:
  - `test.movie.err.txt`: Error information file.
  - `test.movie.dict.txt`: Dictionary file for generating bilingual subtitles.

- **Template Files**:
  - `ass_template_cn_en_1280.txt`: ASS subtitle template file.
  - `ass_info_head_cn_en_1280.txt`: ASS subtitle header information file.

#### Detailed Steps

1. **Clear Subtitles**:
   - `clear_subtile_fun1`: Clear redundant content in the first subtitle.
   - `clear_subtile_fun2`: Clear redundant content in the second subtitle.

2. **Generate Bilingual Subtitles**:
   - `make_double_lanague_subtitle`: Generate bilingual subtitles based on English subtitles.
   - Parameters:
     - `media`: Media file name.
     - `from_sub`: Source subtitle file.
     - `to_sub`: Target subtitle file.
     - `err_text`: Error information file.
     - `dict_text`: Dictionary file.
     - `sleep_time`: Waiting time.

3. **Merge Subtitles**:
   - `merge_ass_tofile`: Merge bilingual subtitle files.
   - Parameters:
     - `first_subtitle_fname`: The first subtitle file (Chinese).
     - `second_subtitle_fname`: The second subtitle file (English).
     - `new_subtitle_fname`: The new merged subtitle file.
     - `unalign_subtitle_fname`: Unaligned subtitle file.
     - `ass_template_fname`: Path to the ASS subtitle template file.
     - `ass_head_fname`: Path to the ASS subtitle header information file.
     - `mark1`: The first subtitle mark.
     - `mark2`: The second subtitle mark.
     - `mini_time`: Minimum merge time.
     - `max_cnsubtitle`: Maximum number of Chinese subtitle lines.

#### Notes

- Ensure all file paths are correct.
- Ensure the format of the template files and header information files is correct.
- Adjust `sleep_time`, `mark1`, `mark2`, `mini_time`, and `max_cnsubtitle` parameters as needed.

Ensure all dependent functions (such as `clear_subtile_fun1`, `clear_subtile_fun2`, `make_double_lanague_subtitle`, and `merge_ass_tofile`) are defined and

available.

#### Using Files from SrtMergeBox

`ass_template_cn_en_1280.txt` and `ass_info_head_cn_en_1280.txt` are ASS subtitle template files often used to define subtitle styles and header information. These files can be found in the SrtMergeBox project.

SrtMergeBox is a tool for merging two SRT format subtitles into SRT or ASS format subtitles, with the purpose of creating bilingual subtitles. These template files are usually located in the project's `indata` folder.

To obtain these files, you can visit the SrtMergeBox Gitee repository at: <https://gitee.com/xinghuo4096/SrtMergeBox>. In this repository, you can find all the source code and related files for the project, including subtitle template files.

Before using these template files, you may need to customize them according to your needs. For example, you can modify font names, sizes, colors, and other parameters to meet your subtitle style requirements. These files often involve ASS subtitle style code, such as `Style:` and `Format:` sections.

Please note that when using these files, you need to ensure that your subtitle files are time-aligned, and you may need to install additional libraries, such as `chardet`, to handle the encoding issues of subtitle files. The command to install this library is `pip install chardet`.

Finally, the merged subtitle files and unaligned subtitle parts will be stored in the `outdata` folder.

## example1.py, Batch Processing Subtitles, Generating Bilingual Subtitles Usage Introduction

Translate all `.srt` files in the directory.

It reads all `.srt` files in a directory and performs a series of operations, including cleaning subtitles, generating bilingual subtitles, and merging subtitles. Here are the usage and required files for the code:

### Translate All SRT Files in the Directory

1. **Define the Working Directory**: Set the `mpath` variable to the directory path where you want to process subtitle files.

2. **Read the Files in the Directory**: Use `os.listdir(".")` to get all the files in the current directory.

3. **Process Each File in the Loop**: For each file, check if it is a `.srt` file and if the extension name meets the requirements.

4. **Clean Subtitles**: Call the `clear_subtile_fun1` and `clear_subtile_fun2` functions to clean subtitle files.

5. **Generate Subtitle Glossary**: Call the `make_subtile_glossary_fun1` and `make_subtile_glossary_fun2` functions to process subtitle files, which may involve adding a glossary or terminology.

6. **Translate Subtitles**: Use `BaiduceEngine` (Baidu Translation API) to translate English subtitles into Chinese.

7. **Generate Bilingual Subtitles**: Call the `make_double_lanague_subtitle` function to generate bilingual subtitles.

8. **Merge Subtitles**: Call the `merge_ass_tofile` function to merge Chinese and English subtitles into a `.ass` file.

### Required Files

- **Subtitle Template File**: `../SrtMergeBox/indata/ass_template_cn_en_1280.txt`, used to define the style of the merged subtitles.
- **Subtitle Header Information File**: `../SrtMergeBox/indata/ass_info_head_cn_en_1280.txt`, containing the header information of the subtitle file.
- **Glossary File**: `../indata/glossary.txt`, containing the vocabulary or terminology that needs to be processed.
- **Baidu Translation API Configuration File**: `c:/test/config/mykeys.json`, containing the keys for the Baidu Translation API.

### Notes

- Ensure that all required files are in the correct path and that the file paths use the correct slashes (`/` or `\`).
- Ensure that the `BaiduceEngine` class is correctly implemented and can use the provided API keys for translation.
- The `print` statements in the code are used to output processing progress, which you can modify or delete as needed.

### Example

Assume your working directory is `c:/test/a/`, and there are some `.srt` subtitle files in the directory. You can save this code as a Python script and run it in the command line. The script will automatically process all `.srt` files in the directory and generate the corresponding bilingual subtitle files.

Please make sure you have installed all the necessary Python modules and correctly configured the Baidu Translation API keys. In addition, you need to ensure that modules such as `Srt`, `clear_subtitle`, and `double_language_subtitle` are available and contain the required functions.

### Example2

An example of individual and multiple subtitle processing

Potential issues that may arise:

1. Sentences are too long, mostly lyrics,
   need to manually repair subtitles, add a period "." at the end of the lyrics.

2. The subtitle text part starts with a number
   For example, as follows:

   ```text
   ........year
   2000
   ```

   Need to modify the content in the srt file
   such as fixing to:

   ``` text
   ........year 2000
   ```
