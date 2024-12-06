import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 设置 Chrome 浏览器的无头模式（不显示浏览器窗口）
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 启动浏览器
driver = webdriver.Chrome(options=chrome_options)

# 打开豆瓣主页以获取 Cookie
driver.get("https://book.douban.com/top250")

# 手动添加你的 Cookie
cookies = [
    {'name': 'll', 'value': '118339'},
    {'name': 'bid', 'value': 'gvdQJaPULbM'},
    {'name': '_pk_id.100001.3ac3', 'value': 'ffc46278de69d4e5.1727428195.'},
    {'name': 'viewed', 'value': '1859140'},
    {'name': 'dbcl2', 'value': '200350411:1dp+uvVrbs0'},
    {'name': 'ck', 'value': '8Oo-'},
    {'name': 'push_noty_num', 'value': '0'},
    {'name': 'push_doumail_num', 'value': '0'},
    {'name': 'frodotok_db', 'value': '0f65554d946b54292e2fffe8bd41fc7b'}
]

for cookie in cookies:
    driver.add_cookie(cookie)

# 刷新页面以应用 Cookie
driver.refresh()

# 定义目标 URL
url = "https://book.douban.com/top250"

# 创建并打开一个 csv 文件用来写入爬取到的数据
with open("豆瓣读书TOP250.csv", mode="w", encoding="utf-8", newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["序号", "书名", "链接", "作者", "评分", "评价人数", "简介"])

    i = 1  # 书籍序号
    start = 0  # 起始位置

    # 循环爬取每一页，直到爬取 250 条数据
    while start < 250:
        # 构建分页 URL
        page_url = f"{url}?start={start}"
        
        # 打开页面
        driver.get(page_url)
        
        # 增加随机延迟以模拟真实用户
        time.sleep(random.uniform(2, 4))

        # 查找页面中所有的书籍信息项
        books = driver.find_elements(By.CSS_SELECTOR, ".subject-item")
        
        for book in books:
            # 提取书籍的标题、链接、作者、评分、评价人数和简介
            title_element = book.find_element(By.CSS_SELECTOR, "h2 a")
            title = title_element.get_attribute("title")
            link = title_element.get_attribute("href")
            
            # 作者信息
            author = book.find_element(By.CSS_SELECTOR, ".pub").text.split("/")[0].strip()
            
            # 评分
            try:
                rating = book.find_element(By.CSS_SELECTOR, ".rating_nums").text
            except:
                rating = "N/A"  # 如果没有评分，则标记为 N/A
            
            # 评价人数
            try:
                reviews = book.find_element(By.CSS_SELECTOR, ".pl").text
                reviews = ''.join(filter(str.isdigit, reviews))  # 只提取数字部分
            except:
                reviews = "N/A"
            
            # 简介
            try:
                inq = book.find_element(By.CSS_SELECTOR, ".inq").text
            except:
                inq = ""  # 如果没有简介，则为空
            
            # 写入 CSV 文件
            csv_writer.writerow([i, title, link, author, rating, reviews, inq])
            i += 1
        
        # 增加爬取起始头以获取下一批数据
        start += 25

print("爬取完毕")
driver.quit()
