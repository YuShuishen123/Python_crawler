import json
import requests

url = 'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/news_1.jsonp?cb=news'

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
    # 获取响应文本
    news = response.text
    # print("响应内容:", news)

    # 转换 JSONP 为 JSON
    json_str = news[news.index('(') + 1 : news.rindex(')')]  # 提取 JSON 数据

    # 去掉转义字符
    byte_str = bytes(json_str, "latin1")
    
    # 解码
    try:
        decoded_str = byte_str.decode("utf-8")
        # print("解码后的中文内容:", decoded_str)
    except UnicodeDecodeError as e:
        print("解码失败:", e)

        
    data = json.loads(decoded_str)
    
    # 假设 'list' 是你需要关注的数据部分
    news_list = data.get('data', {}).get('list', [])
    
    for item in news_list:
                  # 打印新闻信息
            print("新闻标题:", item['title'])
            print("概括:", item['brief'])
            print("图片:", item['image'])  
            print("发布日期:", item['focus_date'])
            print("链接:", item['url'])
            print("-" * 40)
      
    
    
    
    
    
#     try:
#         # 解析 JSON 数据
#         data = json.loads(json_str)

#         # 假设 'list' 是你需要关注的数据部分
#         news_list = data.get('data', {}).get('list', [])

#         for item in news_list:
#             # 处理解码
#             try:
#                 # 尝试使用不同的编码方式进行解码
#                 title_bytes = bytes(item['title'], 'latin1')  # 以 latin1 编码处理title_bytes
#                 title_bytes2 = bytes(item['brief'], 'latin1')  # 以 latin1 编码处理title_bytes2
#                 item['title'] = title_bytes.decode('utf-8', errors='ignore')  # 继续尝试解码为 utf-8
#                 item['brief'] = title_bytes2.decode('utf-8', errors='ignore')  # 继续尝试解码为 utf-8
                
#             except Exception as e:
#                 print("解码错误:", e)

#             # 打印新闻信息
#             print("新闻标题:", item['title'])
#             print("概括:", item['brief'])
#             print("发布日期:", item['focus_date'])
#             print("链接:", item['url'])
#             print("-" * 40)

#     except json.JSONDecodeError as e:
#         print("JSON 解码错误:", e)
# else:
#     print("请求失败，状态码:", response.status_code)

# 关闭请求
response.close()
