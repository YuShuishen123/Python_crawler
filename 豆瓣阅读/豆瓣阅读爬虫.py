import requests
import json
import csv
import time
import random

url = "https://read.douban.com/j/kind/"

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://read.douban.com',
    'Referer': 'https://read.douban.com/kind/100',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

payload = {
    "sort": "hot",
    "page": 1,
    "kind": 100,
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

# 打开CSV文件以追加数据
with open('douban_readingfrom286.csv', 'a', encoding='utf-8-sig', newline='') as f, \
        open('failed_pages3.txt', 'a', encoding='utf-8') as failed_file:
    writer = csv.writer(f)

    # 只有第一次运行时，才写入表头
    if f.tell() == 0:  # 文件指针位置为0，说明文件是空的
        writer.writerow(['标题', '封面链接', '详情页链接', '作者', '简介', '字数', '价格'])

    def fetch_page(page):
        """爬取指定页的数据并写入CSV文件"""
        payload["page"] = page  # 更新payload中的页码

        try:
            # 使用session保持会话
            session = requests.Session()
            
            # 先访问主页获取cookie
            session.get('https://read.douban.com/kind/100', headers=headers)
            
            # 然后发送API请求
            response = session.post(url, headers=headers, json=payload)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                books = data.get('list', [])
                
                # 遍历每本书的信息，提取并写入CSV
                for book in books:
                    # 提取标题
                    title = book.get('title', '')
                    
                    # 提取封面链接
                    cover = book.get('cover', '')
                    
                    # 提取详情页链接
                    detail_url = f"https://read.douban.com{book.get('url', '')}"
                    
                    # 提取作者信息
                    authors = []
                    for author in book.get('author', []):
                        authors.append(author.get('name', ''))
                    for author in book.get('origAuthor', []):
                        authors.append(author.get('name', ''))
                    for translator in book.get('translator', []):
                        authors.append(f"译者: {translator.get('name', '')}")
                    author_str = ', '.join(authors) if authors else '未知'
                    
                    # 提取简介
                    abstract = book.get('abstract', '').replace('\n', ' ').replace('\r', ' ')
                    
                    # 提取字数
                    word_count = f"{book.get('wordCount', '未知')}{book.get('wordCountUnit', '')}"
                    
                    # 提取价格
                    price = '免费'
                    if 'realPrice' in book and book['realPrice']:
                        price_info = book['realPrice']
                        if price_info.get('price'):
                            price = f"{price_info['price']/100}元"
                    
                    # 将每本书的信息写入CSV文件
                    writer.writerow([title, cover, detail_url, author_str, abstract, word_count, price])
                print(f"已提取第{page}页")
            else:
                print(f"请求失败，状态码: {response.status_code}，跳过第{page}页")
                # 将失败的页码和状态码写入失败日志文件
                failed_file.write(f"第{page}页请求失败，状态码: {response.status_code}\n")

        except Exception as e:
            print(f"发生错误，在第{page}页，错误: {e}")
            # 记录失败的页码和错误信息
            failed_file.write(f"第{page}页请求失败，错误: {e}\n")

        finally:
            if 'response' in locals():
                response.close()

    def main():
        start_page = 286  # 从第128页开始爬取
        total_pages = 3142
        page_counter = 0  # 用于统计爬取的页数

        for page in range(start_page, total_pages + 1):
            fetch_page(page)
            page_counter += 1

            # 每爬取50页就休息5秒钟
            if page_counter % 50 == 0:
                print(f"已爬取{page_counter}页，休息5秒钟...")
                time.sleep(5)
            else:
                # 随机等待1-2秒，避免被封禁
                time.sleep(random.uniform(4, 5))

    if __name__ == "__main__":
        main()
