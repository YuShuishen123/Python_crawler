import requests

url = 'https://fanyi.baidu.com/sug'

# 将kw的内容改为你想要翻译的内容,只支持单词翻译

def getkw():
    kw = input('请输入你想要翻译的内容：')
    return kw

kw = getkw()

dat = {
    'kw': kw
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}
response = requests.post(url,data=dat,headers=headers)  # 发送请求


print(response.json())  # 输出响应的文本内容
print(response.status_code)  # 输出响应的状态码