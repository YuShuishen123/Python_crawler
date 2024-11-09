# Python爬虫与GUI项目集合 🚀

这是一个包含多个Python实战项目的代码仓库，主要包括爬虫和GUI界面开发。

## 项目列表 📋

### 1. 豆瓣读书TOP250爬虫 📚

- 文件: `Xpath练习/豆瓣读书250.py`
- 功能:
  - 爬取豆瓣读书TOP250的书籍信息
  - 获取书名、作者、评分、简介等数据
  - 数据保存为CSV格式
  - 包含反爬处理和错误处理机制
  - 支持空值处理和数据清洗

### 2. 壁纸网站爬虫 🖼️

- 文件: `bs4阶段练习/壁纸爬取.py`
- 功能:
  - 爬取高清壁纸图片
  - 自动创建保存目录
  - 支持批量下载
  - 包含异常处理机制
  - 添加随机延时防反爬

### 3. B站视频搜索爬虫 🎬

- 文件: `网课练习/b站搜索推荐爬取.py`
- 功能:
  - 根据关键词搜索B站视频
  - 获取视频标题、作者、播放量、链接等信息
  - 按播放量排序展示结果
  - 支持持续搜索不同关键词

### 4. 百度翻译爬虫 🔤

- 文件: `网课练习/百度翻译.py`
- 功能:
  - 调用百度翻译API进行英汉互译
  - 支持多个翻译结果的展示
  - 提供持续翻译功能
  - 优雅的错误处理

### 5. 新发地市场菜价爬虫 🥬

- 文件: `json练习/北京新发地市场菜价爬取.py`
- 功能:
  - 爬取北京新发地市场的菜价信息
  - 支持分页获取数据
  - 将数据保存为CSV格式
  - 包含菜名、价格、规格等信息

## 技术特点 💡

- 使用多种网页解析技术:
  - XPath提取数据
  - BeautifulSoup解析HTML
  - JSON数据处理
- 数据存储:
  - CSV文件存储
  - 图片文件下载
- 反爬虫处理:
  - 随机延时
  - 请求头伪装
  - Cookie处理
- 异常处理:
  - 网络请求异常处理
  - 数据解析异常处理
  - 文件操作异常处理

## 环境要求 🔧

- Python 3.6+
- requests
- lxml
- BeautifulSoup4
- csv
