# git

## 重命名

文件或文件夹可以使用 git mv 命令。参数详解：

-v：显示信息。

-f：强制重命名或移动，会覆盖目标文件。

-k：跳过对重命名或移动出错的文件。出错的时候发生在源文件不存在，或者没有追踪的源文件，或者目标文件已经存在，但没有加-f进行覆盖。

-n：只显示信息，但不会进行实际重命名或移动操作。

    -v, --verbose         be verbose
    -n, --dry-run         dry run
    -f, --force           force move/rename even if target exists
    -k                    skip move/rename errors
    --sparse              allow updating entries outside of the sparse-checkout cone
