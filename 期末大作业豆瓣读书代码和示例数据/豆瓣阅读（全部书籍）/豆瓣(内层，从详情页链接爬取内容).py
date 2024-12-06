import requests
import pandas as pd
from lxml import etree
import csv
import time

# 请求的基本URL，指向豆瓣阅读的类别页面（书籍列表）
url = "https://read.douban.com/j/kind/"

# 设置请求头，模拟浏览器访问，避免被封禁
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://read.douban.com',
    'Referer': 'https://read.douban.com/kind/100',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'cookie' : 'll="118339"; bid=s-TFXtf1GW8; _vwo_uuid_v2=D538D93FC7BB13242D936A4358F40E0B3|efbddd0fcdf788dee0ce92f7d3663e23; uaid="75557fc885c90f56b0c62010b6b326692c3bfd70"; _ga=GA1.3.131592604.1733226815; _ga=GA1.1.131592604.1733226815; _pk_id.100001.a7dd=457c1b6b4f0d61fc.1733226894.; ct=y; _pk_ref.100001.a7dd=%5B%22%22%2C%22%22%2C1733411154%2C%22https%3A%2F%2Fbook.douban.com%2F%22%5D; _pk_ses.100001.a7dd=1; _gid=GA1.3.588965574.1733411154; ap_v=0,6.0; __utmc=30149280; __utmz=30149280.1733411615.3.2.utmcsr=read.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=30149280.131592604.1733226815.1733411615.1733413687.4; viewed="26877746_30136042_35219185_36929195"; __utmb=30149280.3.10.1733413687; refer_url=https://read.douban.com/ebook/36570625/; dbcl2="285221866:fHVffZJK+Q4"; ck=77PY; _gat=1; _ga_RXNMP372GL=GS1.1.1733411154.5.1.1733416048.48.0.0'
}

# 从之前保存的CSV文件读取书籍的详情页链接
data = pd.read_csv("./douban_readingfrom286.csv")
urls = data['详情页链接'].values  # 获取“详情页链接”这一列中的所有链接

# 打开一个新的CSV文件用于存储爬取的评论人数、评分等信息
fd = open("./从详情页爬取评论人数和分数.csv", 'a', encoding='utf-8', newline='')
csv_write = csv.writer(fd)

# 写入CSV文件的表头
csv_head = ["name", "score", "amount", "label", "publisher", "publishDate"]
csv_write.writerow(csv_head)

counts = 0  # 统计已爬取的书籍数量

# 遍历每个书籍的详情页链接
for url in urls:
    time.sleep(1)  # 每次请求后等待1秒，避免过于频繁的请求被封禁

    # 发送GET请求访问详情页
    rep = requests.get(url, headers=headers)
    html = etree.HTML(rep.text)  # 使用lxml解析HTML

    try:
        # 使用XPath提取页面中的书籍信息
        name = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/h1/text()")[0]  # 获取书名
        score = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[2]/a/span[1]/text()")[0]  # 获取评分
        amount = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[2]/a/span[2]/text()")[0]  # 获取评论人数
        label = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[1]/p[3]/span[2]/span/text()")[0]  # 获取标签
        publisher = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[1]/p[4]/span[2]/span[1]/text()")[0]  # 获取出版社
        publishDate = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[1]/p[4]/span[2]/span[2]/text()")[0]  # 获取出版日期
    except Exception as e:
        print(e, url)  # 如果出错，打印错误信息和URL，跳过该书籍
        continue

    # 将提取的数据写入CSV文件
    data = [name, score, amount, label, publisher, publishDate]
    csv_write.writerow(data)
    fd.flush()  # 确保数据立即写入文件
    counts += 1  # 更新已爬取的书籍数量
    print(f"已经爬取{counts}本")  # 输出当前已爬取的书籍数量

# 关闭文件
fd.close()
