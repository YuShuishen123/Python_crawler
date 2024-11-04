import json
import requests

url = 'https://military.cctv.com/data/index.json'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

dat = {
    'cb': 'news'
}

# 发送请求
response = requests.get(url, headers=headers)

# 检查响应状态
if response.status_code == 200:
    response.encoding = 'utf-8'
    
    # 获取响应文本
    news = response.text
    # print(news)
    # print("-" * 40)

        
    data = json.loads(news)   # 该步骤处理编码
    # print(data)
    # print("-" * 40)
    
    news_list = data.get('rollData', [])
    i = 1
    for item in news_list:
                  # 打印新闻信息
            print("第",i,"条新闻") 
            print("新闻标题:", item['title'])
            # print("概括:", item['brief'])
            print("图片:", item['image'])  
            # print("发布日期:", item['focus_date'])
            print("链接:", item['url'])
            print("-" * 40)
            # 只显示前3条新闻
            if i == 5:
                break
            i += 1
            
# 关闭请求
response.close()
