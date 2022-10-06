import re

text1 = '我aaaa，当我bbbb。上面写着……“待续”'
CHINESE_MARK2 = r'[，。？]|……'
reobj = re.compile(CHINESE_MARK2)

strlist1 = []
find = reobj.search(text1)
str_begin = 0
str_end = len(text1)

while find:
    strlist1.append(text1[str_begin:find.end()])
    str_begin = find.end()
    find = reobj.search(text1, str_begin)
if str_begin < len(text1):
    strlist1.append(text1[str_begin:])
print(strlist1)
