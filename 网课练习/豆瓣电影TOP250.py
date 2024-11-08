import re
import requests
import csv
import time

url = 'https://movie.douban.com/top250'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

start = 0
f = open('豆瓣电影TOP250.csv', mode="w", encoding='utf-8', newline='')
csv_write = csv.writer(f)

while start <= 225:

    data = {
        'start': start, 
        'filter': ''
    }
    
    # 发送请求
    response = requests.get(url, headers=headers, params=data) # 发送请求


    result_text = response.text

    # 编写正则表达式
    pattern = re.compile(r'<li>.*?<em class="">(?P<rank>.*?)</em>.*?<div class="hd".*?' # 排名
                         r'<a href="(?P<url>.*?)" class="">.*?' # 链接
                         r'<span class="title">(?P<movie_name>.*?)' # 电影名
                         r'</span>.*?<div class="star">.*?'
                         r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                         r'<span>(?P<score_num>.*?)</span>.*?'
                         r'<span class="inq">(?P<comment>.*?)</span>', re.S)

    # 匹配
    result = pattern.finditer(result_text)

    for i in result:
        print(i.groupdict())
        dic = i.groupdict()
        csv_write.writerow(dic.values())

    # 增加start，确保在下一个循环时能够正确获取下一页数据
    start += 25

response.close()
f.close()
print("爬取完毕")
