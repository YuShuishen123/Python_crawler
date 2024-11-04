import requests

url = 'https://movie.douban.com/j/chart/top_list'

dat = {
    'type': 7,
    'interval_id': '100:90',
    'action': '',
    'start': 0,
    'limit': 20
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}
response = requests.post(url,data=dat,headers=headers)  # 发送请求


# print(response.json())  # 输出响应的文本内容
# print(response.status_code)  # 输出响应的状态码

# # 保存为json文本并且打开
# with open('豆瓣爱情电影排行榜3.json','w',encoding='utf-8') as f:
#     f.write((response.json()))  # 将json文本写入文件
    
movies = response.json()  # 读取json文件
# 提取电影名称和评分
# 提取每部电影的名称和评分
for movie in movies:
    movie_title = movie['title']  # 访问每部电影的 title
    movie_score = movie['score']  # 访问每部电影的 score
    move_rank = movie['rank'] # 访问每部电影的 rank
    move_type = movie['types'] # 访问每部电影的 type
    print("第",move_rank ,"名,""电影名称:",movie_title,",评分:",movie_score,",类型:",move_type)
    
response.close  # 关闭请求
    




