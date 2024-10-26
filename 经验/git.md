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

## git-crypt

git-crypt 是一个用于 git 仓库的加密工具，可以加密 git 仓库中的文件。使用 git-crypt 加密文件后，这些文件在 git 仓库中会被加密，只有知道解密密钥的人才能解密这些文件。

### 安装
git-crypt init
.git目录下config里面可能会有类似：
```ini
[filter "git-crypt"]
	smudge = \"C:\Git\\\\cmd\\\\git-crypt.exe\" smudge
	clean = \"Programs\\\\Git\\\\cmd\\\\git-crypt.exe\" clean
	required = true
[diff "git-crypt"]
	textconv = \"C:AppData\\\\Local\\\\Programs\\\\Git\\\\cmd\\\\git-crypt.exe\" diff
```

### 加密文件
.gitattributes 文件中添加类似下面的内容：
```ini
* !filter !diff
.secrets/** filter=git-crypt diff=git-crypt
config/test1.test.txt filter=git-crypt diff=git-crypt
test1.test.txt filter=git-crypt diff=git-crypt
```

### 对称加密下接受的密钥格式
git-crypt unlock /path/to/key/file
其中 /path/to/key/file 是你的密钥文件的路径。执行这个命令后，git-crypt 会使用这个密钥来解密仓库中的文件。

确认解锁成功：
 解锁成功后，你应该能够查看和编辑仓库中之前加密的文件。可以通过查看文件内容或者尝试编辑文件来确认解锁是否成功。

## git 更新子模块的远程url
比如从github.com/xxx/xxx 更新到 gitee.com/xxx/xxx
### 0.**先备份**
备份，因为可能有很多配置要变,venv，git-crypt等

### 1. 更改子模块的远程 URL
可以更改.gitmodules，也如下：

首先，你需要更改子模块的远程 URL。这可以通过 `git submodule` 命令来完成。

```bash
git submodule set-url <path_to_submodule> <new_remote_url>
```

- `<path_to_submodule>` 是子模块在主仓库中的相对路径。
- `<new_remote_url>` 是子模块的新远程仓库 URL。

### 2. 初始化和更新子模块

如果你刚刚克隆了主仓库，或者子模块目录为空，你需要初始化并更新子模块。

```bash
git submodule update --init --recursive
```

这将初始化子模块，并从其远程仓库拉取数据。

```bash
git push origin main
```

### 3. 如果不成功，强行更新本地主仓库和子模块

如果你需要强行更新本地主仓库和子模块以匹配远程分支的状态，可以使用以下命令：

```bash
git fetch origin
git reset --hard origin/main
```

这将覆盖你本地的所有更改，包括子模块的更改。

### 4. 清理本地未跟踪的文件（可选）

如果你还想要删除未跟踪的文件，可以使用 `git clean` 命令：

```bash
git clean -fd
```

### 5. 验证子模块的状态

最后，你可以验证子模块的状态，确保它指向正确的远程 URL 和提交。

```bash
git submodule status
```


