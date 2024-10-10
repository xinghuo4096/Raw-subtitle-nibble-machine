def clear_str(content):
    lines = content.split("\n")
    lines = [line for line in lines if line.strip()]
    retstr = "\n".join(lines)
    return retstr


# 假设content是包含上述文本的变量
content = ""
ff1 = open("c:/test/a/zhipu_test2.txt", "r", encoding="utf-8")
str1 = ff1.read()
ff1.close()
content = str1
a1 = clear_str(content)
# 每次显示两行，a1的内容
lines = a1.split("\n")
print(lines[0])
print(lines[1])
print("---")
print(lines[2])
print(lines[3])
print("---")
print(lines[4])
print("********")

for i in range(5, len(lines), 2):
    print(lines[i])
    print(lines[i + 1])
    print("---")
