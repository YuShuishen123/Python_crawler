import json
import requests

url = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/news_1.jsonp?cb=news'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 发送请求
response = requests.get(url, headers=headers)

# 设置响应编码为 UTF-8
response.encoding = 'utf-8' # 设置响应编码

# 检查响应状态
if response.status_code == 200:
    # 获取响应文本
    news = response.text

    # 转换 JSONP 为 JSON
    json_str = news[news.index('(') + 1 : news.rindex(')')]  # 提取 JSON 数据
    
    # 解析 JSON
    data = json.loads(json_str)
    
    # 获取新闻列表
    news_list = data.get('data', {}).get('list', [])
    for i, item in enumerate(news_list, start=1):
        # 打印新闻信息
        print("新闻标题:", item['title'])
        print("概括:", item['brief'])
        print("发布日期:", item['focus_date'])
        print("链接:", item['url'])
        print("-" * 40)
        
        # 只显示前 3 条新闻
        if i >= 3:
            break

# 关闭请求
response.close()
