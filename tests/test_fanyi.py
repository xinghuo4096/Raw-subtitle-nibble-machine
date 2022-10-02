import re

match1 = r"token:\s*'(\S*)'"
match2 = r'window.gtk\s*=\s*"(\S*)"'

token = "  token: 'e55c967a31d0ce6dd63ccadbf53f703d',"
gtk = ';window.gtk = "320305.131321201";'
find1 = re.findall(match1, token)
find2 = re.findall(match2, gtk)
print(find1[0], find2[0])
print()
