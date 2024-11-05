import requests
import re

url = 'https://movie.douban.com/chart'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

response = requests.get(url, headers=headers)  # 发送请求

# print(response.text)  # 输出响应的文本内容
pattern = r'<a.*?title="(.*?)".*?>'



movie_names = re.findall(pattern, response.text)  # 提取电影名称

print(movie_names)  # 输出电影名称