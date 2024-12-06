import requests
import json
import csv
import time
import random
from lxml import etree

# 实现思路：
# 外层爬取书籍的基本信息，获取书籍的详情页链接。
# 每本书根据详情页链接进一步爬取出版社、出版时间、评分、评分人数等详细信息。
# 最终将这些信息整合并输出到 CSV 文件中。
# 外层 API URL：用于获取书籍列表的 API 接口地址

outer_url = "https://read.douban.com/j/kind/"

# 结果输出的 CSV 文件路径
output_csv = 'douban_books_integrated.csv'

# 通用请求头，模拟浏览器请求，避免请求被拒绝
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://read.douban.com',
    'Referer': 'https://read.douban.com/kind/100',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 定义请求的 payload 模板，包含了分页和查询类型等
payload = {
    "sort": "hot",  # 排序方式：按热度排序
    "page": 1,      # 当前页数
    "kind": 100,    # 类别，100表示当前类别
    "query": """
    query getFilterWorksList($works_ids: [ID!]) {
      worksList(worksIds: $works_ids) {
        id
        title
        cover
        url
        author {
          name
        }
        origAuthor {
          name
        }
        translator {
          name
        }
        abstract
        wordCount
        wordCountUnit
        realPrice {
          price
          priceType
        }
      }
    }
    """,
    "variables": {}
}

# 打开 CSV 文件，用于写入最终抓取的数据
with open(output_csv, 'a', encoding='utf-8-sig', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # 如果 CSV 文件为空，则写入表头
    if csv_file.tell() == 0:
        writer.writerow(['书名', '作者', '出版社', '出版时间', '字数', '价格', '评分', '评分人数'])

    # 定义函数，爬取外层书籍信息（每一页）
    def fetch_outer_page(page):
        """
        爬取外层页面的数据，获取当前页的书籍信息，并提取详情页链接。
        """
        payload["page"] = page  # 更新当前的页码
        try:
            # 向外层 API 发送请求，获取书籍信息
            response = requests.post(outer_url, headers=headers, json=payload)
            response.raise_for_status()  # 如果请求失败会抛出异常
            data = response.json()  # 解析返回的 JSON 数据
            books = data.get('list', [])  # 获取书籍列表
            return books
        except Exception as e:
            print(f"外层第{page}页请求失败: {e}")
            return []  # 如果请求失败，返回空列表

    # 定义函数，从详情页获取更详细的信息（出版社、出版时间、评分、评分人数）
    def fetch_detail_info(detail_url):
        """
        爬取详情页的数据，获取出版社、出版时间、评分和评分人数。
        """
        try:
            # 向详情页 URL 发送请求，获取页面内容
            response = requests.get(detail_url, headers=headers)
            response.raise_for_status()
            html = etree.HTML(response.text)  # 使用 lxml 解析 HTML

            # 提取各项信息，如果未找到则返回 None
            publisher = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[1]/p[4]/span[2]/span[1]/text()")
            publish_date = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[1]/p[4]/span[2]/span[2]/text()")
            score = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[2]/a/span[1]/text()")
            amount = html.xpath("/html/body/div[1]/div[5]/article/div[1]/div[2]/div[2]/a/span[2]/text()")

            # 如果没有找到对应的数据，返回 None
            return (
                publisher[0] if publisher else None,
                publish_date[0] if publish_date else None,
                score[0] if score else None,
                amount[0] if amount else None,
            )
        except Exception as e:
            print(f"详情页爬取失败 ({detail_url}): {e}")
            return None, None, None, None  # 发生错误时返回 None

    # 主函数，开始爬取所有书籍
    def main():
        total_pages = 3142  # 总页数，可以根据实际情况调整
        for page in range(1, total_pages + 1):
            # 获取当前页的书籍信息
            books = fetch_outer_page(page)

            # 遍历当前页的所有书籍
            for book in books:
                # 提取外层书籍信息
                title = book.get('title', None)
                cover = book.get('cover', None)
                detail_url = f"https://read.douban.com{book.get('url', '')}"  # 拼接详情页链接
                authors = [author.get('name', None) for author in book.get('author', [])] + \
                          [author.get('name', None) for author in book.get('origAuthor', [])]
                author_str = ', '.join(filter(None, authors)) if authors else None  # 拼接作者信息
                word_count = f"{book.get('wordCount', None)}{book.get('wordCountUnit', '')}" if book.get('wordCount') else None
                price = None if not book.get('realPrice', {}).get('price') else f"{book['realPrice']['price'] / 100}元"

                # 爬取详情页的更多信息
                publisher, publish_date, score, amount = fetch_detail_info(detail_url) # 此处详情页信息爬取定义为一个方法来进行调用

                # 将所有信息写入到 CSV 文件
                writer.writerow([title, author_str, publisher, publish_date, word_count, price, score, amount])
                csv_file.flush()  # 刷新缓冲区，确保数据及时写入文件
                print(f"完成书籍: {title}")  # 输出当前爬取的书名

            # 每爬取一页后，随机休眠 2-5 秒，避免被封禁
            time.sleep(random.uniform(2, 5))

    # 程序入口
    if __name__ == "__main__":
        main()
