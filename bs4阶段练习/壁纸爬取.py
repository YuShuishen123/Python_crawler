import requests
from bs4 import BeautifulSoup
import time
import random
import os

# 定义url
url = 'https://www.umeituku.com/bizhitupian/weimeibizhi/'

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
}

# 创建保存图片的文件夹
if not os.path.exists("wallpapers"):
    os.mkdir("wallpapers")
    
# 定义请求
resp = requests.get(url,headers=headers)
# 转换编码
resp.encoding = 'utf-8'

# 把源码交给bs处理,声明类型
main_page = BeautifulSoup(resp.text,'html.parser')

# 从源码中提取到div板块,再从中提取出a标签
a_list = main_page.find("div",class_="TypeList").find_all("a")

# 输出
for i in a_list:
  print(i.text)
  # print(i.get('href'))
  # 爬取图片详情页内的图片下载连接
  inner_resp = requests.get(url=i.get('href',),headers=headers)
  inner_resp.encoding='utf-8'

  # 详情页交给bs处理
  inner_page = BeautifulSoup(inner_resp.text,'html.parser')
  
  # 提取要的内容
  try:
      # 提取要的内容
      p_tag = inner_page.find("p", align="center")
      if p_tag:
          div = p_tag.find("img")
          if div and div.get('src'):
              img_url = div.get('src')
              print(f"找到图片: {img_url}")
              
              # 下载图片
              img_name = img_url.split('/')[-1]
              img_resp = requests.get(img_url, headers=headers)
              with open(f"wallpapers/{img_name}", 'wb') as f:
                  f.write(img_resp.content)
              print(f"已保存图片: {img_name}")
          else:
              print(f"在页面 {i.get('href')} 中未找到图片链接")
      else:
          print(f"在页面 {i.get('href')} 中未找到指定的p标签")
      
      inner_resp.close()
      time.sleep(random.randint(2,3))
  except Exception as e:
      print(f"处理页面时出错: {e}")
      continue
  



# 关闭请求
resp.close()
