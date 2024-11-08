import re
import requests
import csv 

url = 'https://dytt.dytt8.net/index.htm'
base_url = 'https://dytt.dytt8.net/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 发送请求
response = requests.get(url, headers=headers)
response.encoding = 'gb2312'

# 正则表达式
pattern_out = re.compile(r'<td width="85%" height="22" class="inddline">.*?电影.*?<a href=\'(?P<url>.*?)\'>(?P<movie_name>.*?)</a><br/>.*?<font color=#FF0000>(?P<data>.*?)</font></td>', re.S)
pattern_inner = re.compile(r'target="_blank" href="(?P<dowlod_url>.*?)"><strong')

get_baseinfo = pattern_out.finditer(response.text)

# 创建 CSV 文件
with open('电影天堂主页电影.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['电影名称', '发布日期', '下载链接']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    for i in get_baseinfo:
        movie_name = i.group('movie_name')
        data = i.group('data')
        url = base_url + i.group('url')

        # 继续内层请求，获取下载链接
        inner_response = requests.get(url, headers=headers)
        inner_response.encoding = 'gb2312'
        get_dowlod_url = pattern_inner.findall(inner_response.text)

        # 将下载链接合并成字符串
        download_links = ', '.join(get_dowlod_url)

        # 写入数据到CSV文件
        writer.writerow({'电影名称': movie_name, '发布日期': data, '下载链接': download_links})

    print("爬取完毕")

# 关闭请求
response.close()
