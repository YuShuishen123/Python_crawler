import requests
import json
import csv
import time  # 添加延时
import random  # 添加随机延时
url = 'http://www.xinfadi.com.cn/getPriceData.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 分页参数
page = 1

f = open('北京新发地市场菜价.csv','w',encoding='utf-8')
csv_write = csv.writer(f)

# 添加表头
csv_write.writerow(['菜名','最低价','平均价','最高价','规格','单位','发布日期'])

while page <= 10:
    try:
        ps = {
            'limit': 20,
            'current': page
        }
        
        response = requests.get(url, headers=headers, params=ps)
        
        # 检查响应状态
        if response.status_code != 200:
            print(f"第{page}页请求失败,状态码: {response.status_code}")
            continue
            
        data = response.json()
        price_list = data.get('list', [])
        
        if not price_list:  # 如果没有数据了就退出
            print("没有更多数据了")
            break
            
        for price in price_list:
            csv_write.writerow([
                price.get('prodName'),
                price.get('lowPrice'),
                price.get('avgPrice'),
                price.get('highPrice'),
                price.get('specInfo'),
                price.get('unitInfo'),
                price.get('pubDate')
            ])
            
        print(f"已完成第{page}页的爬取")
        page += 1
        
        # 添加随机延时
        time.sleep(random.uniform(1, 3))
        
    except json.JSONDecodeError as e:
        print(f"第{page}页解析失败: {e}")
        time.sleep(5)  # 遇到错误时等待更长时间
        continue
        
    except Exception as e:
        print(f"发生错误: {e}")
        time.sleep(5)
        continue
        
    finally:
        response.close()

f.close()
