import re
import requests
import csv
import time
import random

# 请求地址：https://book.douban.com/top250
url = 'https://book.douban.com/top250'

# 头部
headers = {
    'Cookie': 'll="118339"; bid=gvdQJaPULbM; _pk_id.100001.3ac3=ffc46278de69d4e5.1727428195.; viewed="1859140"; dbcl2="200350411:1dp+uvVrbs0"; ck=8Oo-; push_noty_num=0; push_doumail_num=0; frodotk_db="0f65554d946b54292e2fffe8bd41fc7b"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0'
}

# 分组爬取起始头
start = 0

# 创建并且打开一个csv文件用来写入爬取到的数据
with open('豆瓣读书TOP250.csv', mode="w", encoding='utf-8', newline='') as f:
    csv_write = csv.writer(f)
    csv_write.writerow(['序号', '书名', '链接', '作者', '评分', '评价人数', '简介'])
    i = 1

    # 循环爬取全部250条信息
    while start < 250:
        # 定义请求体
        ps = {'start': start}

        # 发送请求并捕获异常
        try:
            response = requests.get(url, headers=headers, params=ps)
            response.raise_for_status()  # 检查响应状态码
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            break  # 或者可以选择 continue 跳过这次请求
        
        # 文本形式的响应内容
        response_text = response.text

        # 正则表达式
        pattern = re.compile(
            r'<a.*?href="(?P<url>https://book\.douban\.com/subject/\d+/)".*?title="(?P<title>[^"]+)"'  # 匹配链接和标题
            r'.*?<p.*?>(?P<author>[^<]+)</p>'  # 匹配作者信息
            r'.*?<span class="rating_nums">(?P<rating>\d+\.\d+)</span>'  # 匹配评分
            r'.*?<span class="pl">\(\s*(?P<reviews>[\d,]+)人评价\s*\)</span>'  # 匹配评价人数
            r'(?:.*?<span class="inq">(?P<inq>[^<]+)</span>)?',  # 匹配简介
            re.S
        )
        match = pattern.finditer(response_text)

        # 计数器：统计本次请求成功抓取的书籍数量
        count = 0
        if match:
            for item in match:
                csv_write.writerow([
                    i,
                    item.group('title'),
                    item.group('author'),
                    item.group('rating'),
                    item.group('reviews'),
                    item.group('inq') if item.group('inq') else '',
                    item.group('url')
                ])
                i += 1
                count += 1
        else:
            print("No match found in this batch.")

        # 输出每次请求抓取到的数量
        print(f"爬取到 {count} 条书籍（当前页：{start + 1} 到 {start + count}）")

        # 增加爬取起始头
        start += 25
        
        # 随机延迟1到3秒，避免触发反爬虫机制
        time.sleep(random.uniform(1, 3))

        # 关闭响应内容
        response.close()

print("爬取完毕")
