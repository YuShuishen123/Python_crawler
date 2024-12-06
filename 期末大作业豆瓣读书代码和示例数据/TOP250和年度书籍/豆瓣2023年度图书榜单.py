import requests
import csv
import lxml
import time 
import random
import json
from lxml import etree

url = 'https://book.douban.com/j/neu/page/21/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Cookie': 'll="118339"; bid=gvdQJaPULbM; _pk_id.100001.3ac3=ffc46278de69d4e5.1727428195.; viewed="1859140"; dbcl2="200350411:1dp+uvVrbs0"; push_noty_num=0; push_doumail_num=0; ck=8Oo-; ap_v=0,6.0;'
}

with open('douban_books年度图书完整test.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)

    with requests.Session() as session:
        session.headers.update(headers)
        resp = session.get(url)
        resp.encoding = 'utf-8'
        resp.raise_for_status()
        data = resp.json()
        
        # 打印数据结构以便调试
        print("JSON数据结构：")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        widgets = data.get('widgets', [])
        
        for widget in widgets:
            # 打印每个widget的结构
            # print("\nWidget结构：")
            # print(json.dumps(widget, indent=2, ensure_ascii=False))
            
            try:
                # 获取类别名称
                category = widget.get('source_data', {})
                if category is None:  # 如果source_data为None
                    print(f"跳过无效数据: {widget}")
                    continue
                    
                category = category.get('subject_collection', {}).get('title', '').replace('2023年度', '').strip()
                
                # 获取该类别下的所有图书
                books = widget.get('source_data', {}).get('subject_collection_items', [])
                
                for book in books:
                    # 提取书籍详细信息
                    title = book.get('title', '')  # 书名
                    author = book.get('card_subtitle', '')  # 作者信息
                    
                    rating = book.get('rating', {}).get('value', '')  # 评分
                    rating_count = book.get('rating', {}).get('rating_count', '')  # 评分人数
                    book_url = book.get('url', '')  # 链接
                    
                    # 写入CSV文件
                    writer.writerow([category, title, author, rating, rating_count, book_url])
                    
                    # 打印提取的信息（调试用）
                    print(f"类别：{category}")
                    print(f"书名：{title}")
                    print(f"作者：{author}")
                    print(f"评分：{rating}")
                    print(f"评分人数：{rating_count}")
                    print(f"链接：{book_url}")
                    print("-" * 50)
            
            except Exception as e:
                print(f"处理数据时出错: {e}")
                continue
                
            # 添加随机延迟
            time.sleep(random.uniform(1, 2))

resp.close()
        
        
    


