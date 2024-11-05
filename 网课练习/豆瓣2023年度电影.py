import json
import requests

url = 'https://movie.douban.com/j/neu/page/22/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}


    # 发送请求
response = requests.get(url, headers=headers)

    # 检查响应状态
if response.status_code == 200:
        
        # 获取响应文本并解析 JSON 数据
        data = json.loads(response.text)
        # print(data)
        
        # 从响应数据中提取音乐
        news_list = data.get('bgms', [])
        # print(news_list)
        i = 0
        for item in news_list:
          print(news_list[i]['name'])
          print(news_list[i]['url'])
          print("-" * 40)
          i = i + 1
          
        # 提取电影名称
        for i in range(1,4):
          title_name = data.get('widgets', [])[i]
          movies = data.get('widgets', [])[i].get('source_data', {}).get('subject_collection_items', [])
          print("第",i,"批")
          print(title_name['title'])
          print("-" * 40)
          
          j = 0
          for movie in movies:
            print(movies[j]['title'])
            print(movies[j]['card_subtitle'])
            print(movies[j]['url'])
            print("-" * 40)
            j = j + 1
          
        
        
        # movies = data.get('widgets', [])[1].get('source_data', {}).get('subject_collection_items', [])
        # j = 0
        # for movie in movies:
        #   print(movies[j]['title'])
        #   print(movies[j]['card_subtitle'])
        #   print(movies[j]['url'])
        #   print("-" * 40)
        #   j = j + 1
        
          

    # 关闭请求
response.close()
