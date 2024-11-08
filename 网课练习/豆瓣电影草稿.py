import re
import requests
import csv

url = 'https://movie.douban.com/top250'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

start = 0
f = open('豆瓣电影TOP250.csv', mode="w", encoding='utf-8', newline='')
csv_write = csv.writer(f)

while start <= 25:

    data = {
        'start': start,
        'filter': ''
    }
    
    # 发送请求
    response = requests.get(url, headers=headers, params=data)

    result_text = '''
<li>
    <div class="item">
        <div class="pic">
            <em class="">249</em>
            <a href="https://movie.douban.com/subject/2213597/">
                <img width="100" alt="朗读者" src="https://img1.doubanio.com/view/photo/s_ratio_poster/public/p1140984198.webp" class="">
            </a>
        </div>
        <div class="info">
            <div class="hd">
                <a href="https://movie.douban.com/subject/2213597/" class="">
                    <span class="title">朗读者</span>
                    <span class="title">&nbsp;/&nbsp;The Reader</span>
                    <span class="other">&nbsp;/&nbsp;为爱朗读(台)  /  读爱(港)</span>
                </a>
            </div>
            <div class="bd">
                <p class="">
                    导演: 史蒂芬·戴德利 Stephen Daldry&nbsp;&nbsp;&nbsp;主演: 凯特·温丝莱特 Kate Winslet ...<br>
                    2008&nbsp;/&nbsp;美国 德国&nbsp;/&nbsp;剧情 爱情
                </p>
                <div class="star">
                    <span class="rating45-t"></span>
                    <span class="rating_num" property="v:average">8.6</span>
                    <span property="v:best" content="10.0"></span>
                    <span>472693人评价</span>
                </div>
                <p class="quote">
                    <span class="inq">当爱情跨越年龄的界限，它似乎能变得更久远一点，成为一种责任，一种水到渠成的相濡以沫。</span>
                </p>
            </div>
        </div>
    </div>
</li>
'''


    # 编写正则表达式
    pattern = re.compile(r'<li>.*?<em class="">(?P<rank>.*?)</em>.*?<div class="hd".*?'
                         r'<a href="(?P<url>.*?)" class="">.*?'
                         r'<span class="title">(?P<movie_name>.*?)'
                         r'</span>.*?<div class="star">.*?'
                         r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
                         r'<span>(?P<score_num>.*?)</span>.*?'
                         r'<span class="inq">(?P<comment>.*?)</span>', re.S)

    # 匹配
    result = pattern.finditer(result_text)

    for i in result:
        print(i.group('rank'), i.group('url'), i.group('movie_name'), i.group('score'), i.group('score_num'), i.group('comment'))

    # 增加start，确保在下一个循环时能够正确获取下一页数据
    start += 25

response.close()
f.close()
print("爬取完毕")



# import requests
# from lxml import etree
 
 
# class DouBan:
#     def __init__(self, start_page=0, end_page=10):
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
#         }
#         self.base_url = 'https://movie.douban.com/top250?start={}'
#         self.url_list = [self.base_url.format(i * 25) for i in range(start_page, end_page)]
 
#     def fetch_page(self, url):
#         try:
#             response = requests.get(url, headers=self.headers)
#             response.raise_for_status()  # 将触发HTTPError，如果状态码不是200
#             return response.content
#         except requests.exceptions.RequestException as e:
#             print(f"请求错误: {e}")
#             return None
 
#     def parse_page(self, html_content):
#         movies = []
#         try:
#             html = etree.HTML(html_content)
#             for li in html.xpath('//ol/li'):
#                 title = li.xpath('.//span[@class="title"][1]/text()')[0]
#                 score = li.xpath('.//span[@class="rating_num"][1]/text()')[0]
#                 number = li.xpath('.//div[@class="star"]/span[last()]/text()')[0]
#                 movies.append({
#                     'title': title.strip(),
#                     'score': score.strip(),
#                     'number': number.strip()
#                 })
#         except IndexError as e:
#             print(f"解析错误: {e}")
#         return movies
 
#     def print_movies(self, movies):
#         for movie in movies:
#             print(f'[电影名称]：{movie["title"]}  [电影评分]：{movie["score"]}  [评价人数]：{movie["number"]}')
 
#     def run(self):
#         for url in self.url_list:
#             print(f"开始抓取页面：{url}")
#             html_content = self.fetch_page(url)
#             if html_content:
#                 movies = self.parse_page(html_content)
#                 self.print_movies(movies)
 
 
# if __name__ == '__main__':
#     db = DouBan()
#     db.run()