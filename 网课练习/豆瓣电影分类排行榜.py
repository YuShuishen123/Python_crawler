import requests

url = 'https://movie.douban.com/j/chart/top_list'

dat = {
    'type': 13,
    'interval_id': '100:90',
    'action': '',
    'start': 0,
    'limit': 50
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}
response = requests.post(url,data=dat,headers=headers)  # 发送请求


print(response.json())  # 输出响应的文本内容
print(response.status_code)  # 输出响应的状态码

# 保存为json文本并且打开
with open('豆瓣爱情电影排行榜3.json','w',encoding='utf-8') as f:
    f.write((response.json()))  # 将json文本写入文件
    
    response.close  # 关闭请求
    




