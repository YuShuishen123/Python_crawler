import re
pattern = re.compile('\w+')
text = 'ABC#123中文好456def'
print(pattern.search(text))

matches = pattern.findall(text)

if pattern.search(text):
    print("匹配到的字符串为：",matches) # 匹配到的字符串为： ['中', '文', '好']
else:
    print("没有匹配到字符串") # 没有匹配到字符串