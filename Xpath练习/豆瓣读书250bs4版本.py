import requests
from lxml import etree
import time
import random
import csv

url = 'https://book.douban.com/top250'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Referer': 'https://book.douban.com/',
    'Cookie': 'll="118339"; bid=gvdQJaPULbM; _pk_id.100001.3ac3=ffc46278de69d4e5.1727428195.; viewed="1859140"; dbcl2="200350411:1dp+uvVrbs0"; push_noty_num=0; push_doumail_num=0; ck=8Oo-; ap_v=0,6.0;'
}

with open('douban_books完整.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '书名', '简介','作者', '评分', '评分人数', '链接'])
    rank = 1

    with requests.Session() as session:
        session.headers.update(headers)
        start = 0
        while start < 250:
            try:
                resp = session.get(url, params={'start': start})
                resp.encoding = 'utf-8'
                resp.raise_for_status()

                if resp.status_code == 200:
                    main_page = etree.HTML(resp.text)
                    book_name = main_page.xpath('//div[@class="pl2"]/a/@title')
                    book_link = main_page.xpath('//div[@class="pl2"]/a/@href')
                    book_author = main_page.xpath('//p[@class="pl"]/text()')
                    book_rating = main_page.xpath('//span[@class="rating_nums"]/text()')
                    book_rating_num = main_page.xpath('//div[@class="star clearfix"]/span[@class="pl"]/text()')
                    
                    book_introduction = []   # 该列表用于存放该页面所有书籍的简介
                    books = main_page.xpath('//tr[@class="item"]')  # 获取并且切割所有书籍元素
                    for book in books:  # 遍历每一本书，去判断该本书是否有简介
                        intro = book.xpath('.//span[@class="inq"]/text()')  # .//的方法使其只获取当前这本书的简介，有简介的话写入该本书独自的introl列表，也就是intro[0],否则的话列表为空
                        book_introduction.append(intro[0] if intro else "无简介")  # 如果简介为空，则置为"无简介"，如果intro[0]存在,则添加到该页全部书籍简介列表中
                        # 这样可以准确判断每一本书是否简介为空，并且确保该页全部书籍简介列表中简介的准确性，不会错位

                    # 数据完整性检查（不包括简介）
                    if not (len(book_name) == len(book_link) == len(book_author) == len(book_rating) == len(book_rating_num)):
                        print(f"页面 {start} 数据不完整")
                        print(f"书名: {len(book_name)}, 链接: {len(book_link)}, "
                              f"作者: {len(book_author)}, 评分: {len(book_rating)}, "
                              f"评分人数: {len(book_rating_num)}")
                        continue

                    # 处理数据
                    for i in range(len(book_name)):
                        clean_author = book_author[i].strip().replace('\n', '').replace('\r', '')
                        clean_rating_num = book_rating_num[i].strip('()').strip()
                        
                        writer.writerow([
                            rank,
                            book_name[i],
                            book_introduction[i],
                            clean_author,
                            book_rating[i],
                            clean_rating_num,
                            book_link[i]
                        ])
                        print(f"已写入第 {rank} 条数据")
                        rank += 1

                start += 25
                time.sleep(random.randint(1, 3))

            except requests.RequestException as e:
                print(f"请求错误: {e}")
                time.sleep(5)
            except Exception as e:
                print(f"其他错误: {e}")
                print(f"错误发生时的start值: {start}")
                continue

print("数据爬取完成")
resp.close()
