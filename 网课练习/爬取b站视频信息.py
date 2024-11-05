import json
import requests
import time

url = 'https://api.bilibili.com/x/web-show/wbi/res/locs'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 生成动态时间戳
def fetch_data():
    # 使用当前时间戳
    wts = int(time.time())
    
    params = {
        "pf": 0,
        "ids": 3449,
        "w_rid": "ce4451866eb67041f94008a185489e17",  # 如果你了解加密方式，可动态生成
        "wts": wts
    }

    # 发送请求
    response = requests.get(url, params=params, headers=headers)

    # 检查响应状态
    if response.status_code == 200:
        response.encoding = 'utf-8'
        
        # 获取响应文本并解析 JSON 数据
        data = json.loads(response.text)
        
        # 从响应数据中提取内容
        news_list = data.get('data', {}).get('3449', [])
        
        # 输出前 10 条内容
        for i, item in enumerate(news_list[:10], start=1):
            print("第", i, "条") 
            print("标题:", item['name'])
            
            # 获取房间信息
            room_info = item.get('room', {})
            if room_info and room_info.get('room_id'):
                print("房间信息:", room_info['room_id'])   
                print("房间名称:", room_info['show']['title'])    
            
            print("链接:", item['url'])
            print("-" * 40)

    else:
        print("请求失败，状态码:", response.status_code)

    # 关闭请求
    response.close()

# 调用爬取函数
fetch_data()
