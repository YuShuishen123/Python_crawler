import requests
from bs4 import BeautifulSoup

# 定义url
url = 'https://www.umeituku.com/bizhitupian/weimeibizhi/'

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 定义请求
resp = requests.get(url,headers=headers)
# 转换编码
resp.encoding = 'utf-8'

# 把源码交给bs处理,声明类型
main_page = BeautifulSoup(resp.text,'html.parser')

# 从源码中提取到div板块,再从中提取出a标签
a_list = main_page.find("div",class_="TypeList").find("a")

# 输出
  # print(i.text)
print(a_list.get('href')) 
  # 爬取图片详情页内的图片下载连接
inner_resp = requests.get(url=a_list.get('href',),headers=headers)
inner_resp.encoding='utf-8'
# print(inner_resp.text)

# 详情页交给bs处理
inner_page = BeautifulSoup(inner_resp.text,'html.parser')

# # 提取要的内容
div = inner_page.find("p",align="center").find("img")
print(div.get('src'))
# resp.close()
  



# 关闭请求
resp.close()
