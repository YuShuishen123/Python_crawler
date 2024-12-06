import requests
import json
import csv
import time
import random

# 该脚本为第一层爬取，用于获取书本的基本信息（如书名、封面、详情页链接等）

# 外层API的请求URL，用于获取书籍的列表数据
url = "https://read.douban.com/j/kind/"

# 请求头，用来模拟浏览器行为，避免被封禁
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/json',
    'Origin': 'https://read.douban.com',
    'Referer': 'https://read.douban.com/kind/100',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 请求体的内容，指定了排序方式、页码和查询参数
payload = {
    "sort": "hot",  # 按照热度排序
    "page": 1,      # 当前的页码
    "kind": 100,    # 书籍类别编号
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

# 打开CSV文件以追加数据，并创建一个记录请求失败页面的日志文件
with open('douban_readingfrom286.csv', 'a', encoding='utf-8-sig', newline='') as f, \
        open('failed_pages3.txt', 'a', encoding='utf-8') as failed_file:
    writer = csv.writer(f)

    # 如果CSV文件是空的（即首次运行），则写入表头
    if f.tell() == 0:  # 文件指针位置为0，说明文件是空的
        writer.writerow(['标题', '封面链接', '详情页链接', '作者', '简介', '字数', '价格'])

    # 定义函数：爬取指定页的数据并写入CSV文件
    def fetch_page(page):
        """
        爬取指定页的书籍数据，提取书名、封面链接、作者、简介等信息，并将其写入CSV文件。
        """
        payload["page"] = page  # 更新请求体中的页码

        try:
            # 使用Session对象来保持会话，这样可以复用连接和cookie，减少重复请求
            session = requests.Session()
            
            # 先访问主页来获取cookie，以便后续的请求能够成功
            session.get('https://read.douban.com/kind/100', headers=headers)
            
            # 使用POST方法发送API请求，获取当前页的书籍数据
            response = session.post(url, headers=headers, json=payload)
            response.encoding = 'utf-8'  # 设置响应的编码格式

            # 如果请求成功，状态码为200
            if response.status_code == 200:
                data = response.json()  # 将返回的JSON数据解析成字典
                books = data.get('list', [])  # 获取书籍列表

                # 遍历当前页中的每本书籍，提取相关信息
                for book in books:
                    # 提取书名（如果没有则为空字符串）
                    title = book.get('title', '')
                    
                    # 提取封面链接
                    cover = book.get('cover', '')
                    
                    # 拼接详情页链接（需要前缀）
                    detail_url = f"https://read.douban.com{book.get('url', '')}"
                    
                    # 提取作者信息
                    authors = []
                    for author in book.get('author', []):
                        authors.append(author.get('name', ''))
                    for author in book.get('origAuthor', []):
                        authors.append(author.get('name', ''))
                    for translator in book.get('translator', []):
                        authors.append(f"译者: {translator.get('name', '')}")
                    author_str = ', '.join(authors) if authors else '未知'  # 合并作者信息，若没有作者则为'未知'
                    
                    # 提取简介，去除换行符，保证格式统一
                    abstract = book.get('abstract', '').replace('\n', ' ').replace('\r', ' ')
                    
                    # 提取字数信息，格式为“数字+单位”
                    word_count = f"{book.get('wordCount', '未知')}{book.get('wordCountUnit', '')}"
                    
                    # 提取价格信息，若没有价格则标记为“免费”
                    price = '免费'
                    if 'realPrice' in book and book['realPrice']:
                        price_info = book['realPrice']
                        if price_info.get('price'):
                            price = f"{price_info['price']/100}元"  # 将价格从分转为元

                    # 将每本书籍的信息写入CSV文件
                    writer.writerow([title, cover, detail_url, author_str, abstract, word_count, price])
                print(f"已提取第{page}页")
            else:
                # 如果请求失败，记录失败信息
                print(f"请求失败，状态码: {response.status_code}，跳过第{page}页")
                failed_file.write(f"第{page}页请求失败，状态码: {response.status_code}\n")

        except Exception as e:
            # 如果发生异常，记录错误信息
            print(f"发生错误，在第{page}页，错误: {e}")
            failed_file.write(f"第{page}页请求失败，错误: {e}\n")

        finally:
            if 'response' in locals():
                response.close()  # 关闭响应

    # 主函数：负责调用fetch_page()来遍历所有需要爬取的页码
    def main():
        start_page = 359  # 从第359页开始爬取
        total_pages = 3142  # 总共需要爬取的页数
        page_counter = 0  # 用于统计已爬取的页数

        # 遍历所有页码，从start_page开始，到total_pages为止
        for page in range(start_page, total_pages + 1):
            fetch_page(page)  # 爬取当前页数据
            page_counter += 1  # 计数已爬取的页数

            # 每爬取50页，休息5秒钟
            if page_counter % 50 == 0:
                print(f"已爬取{page_counter}页，休息5秒钟...")
                time.sleep(5)
            else:
                # 随机休眠1-2秒，避免请求过于频繁导致被封禁
                time.sleep(random.uniform(4, 5))

    # 程序入口：启动主函数
    if __name__ == "__main__":
        main()
