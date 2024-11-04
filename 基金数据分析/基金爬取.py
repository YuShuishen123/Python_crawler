import requests
# 导入BeautifulSoup库
from bs4 import BeautifulSoup
from collections import OrderedDict  # 有序字典
import random
import time

def resolve_rank_detail_info(fund_code, response):
    rank_detail_info = OrderedDict()  # 生成有序字典，保存相关信息
    soup = BeautifulSoup(response.text, 'html.parser')  # 解析HTML
    rank_detail_info['基金代码'] = 'd' + fund_code
    soup_div = soup.find_all('div', class_='bs_gl')[0] # 获取基金的详细信息
    rank_detail_info['成立日期'] = soup_div.find_all('label')[0].find_all('span')[0].get_text()
    rank_detail_info['基金经理'] = soup_div.find_all('label')[1].find_all('a')[0].get_text()
    rank_detail_info['类型'] = soup_div.find_all('label')[2].find_all('span')[0].get_text()
    rank_detail_info['管理人'] = soup_div.find_all('label')[3].find_all('a')[0].get_text()
    rank_detail_info['资产规模'] = soup_div.find_all('label')[4].find_all('span')[0].get_text().replace("\r\n", "").replace(" ", "")
    return rank_detail_info  # 返回基金的详细信息

def resolve_rank_info(row_arr): 
    rank_info = {}
    rank_info['基金代码'] = 'd' + row_arr[0]
    rank_info['基金名称'] = row_arr[1]
    rank_info['截止日期'] = row_arr[3]
    rank_info['单位净值'] = row_arr[4]
    rank_info['日增长率'] = row_arr[5]
    rank_info['近1周'] = row_arr[6]
    rank_info['近1月'] = row_arr[7]
    rank_info['近3月'] = row_arr[8]
    rank_info['近6月'] = row_arr[9]
    rank_info['近1年'] = row_arr[10]
    rank_info['近2年'] = row_arr[11]
    rank_info['近3年'] = row_arr[12]
    rank_info['今年来'] = row_arr[13]
    rank_info['成立来'] = row_arr[14]
    rank_info['起购金额'] = row_arr[-5]
    rank_info['原手续费'] = row_arr[-4]
    rank_info['现手续费'] = row_arr[-3]
    return rank_info

def resolve_position_info(fund_code, response_text):
    # 这里假设解析持仓数据的逻辑已经实现
    fund_position_data = {}  # 示例返回值
    return fund_position_data

def get_ua():
    # 这里假设有一个获取随机User-Agent的方法
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    ]
    return random.choice(user_agents)

def try_craw_info(fund_code, try_cnt=1):
    try:
        # 爬取页面，获得该基金的详细数据
        position_title_url = "http://fundf10.eastmoney.com/ccmx_" + str(fund_code[1:]) + ".html"
        print('第 {0} 次尝试，正在爬取基金 {1} 的详细数据中...'.format(try_cnt, fund_code[1:]))
        response_title = requests.get(url=position_title_url, headers={'User-Agent': get_ua()}, timeout=10)

        # 爬取页面，获取该基金的持仓数据
        position_data_url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=" + \
                            str(fund_code[1:]) + "&topline=10&year=&month=&rt=" + str(random.uniform(0, 1))
        print('第 {0} 次尝试，正在爬取基金 {1} 的持仓情况中...'.format(try_cnt, fund_code[1:]))
        response_data = requests.get(url=position_data_url, headers={'User-Agent': get_ua()}, timeout=10)

        # 解析基金的数据以及持仓数据
        rank_detail_info = resolve_rank_detail_info(fund_code[1:], response_title)
        fund_position_data = resolve_position_info(fund_code[1:], response_data.text)
        time.sleep(random.randint(2, 4))
    except Exception as e:
        print(e)
        time.sleep(random.randint(2 * try_cnt, 4 * try_cnt))
        print("{0}基金数据爬取失败，请注意！".format(str(fund_code[1:])))
        rank_detail_info, fund_position_data = try_craw_info(fund_code, try_cnt + 1)  # 递归调用
    return rank_detail_info, fund_position_data

# 示例调用
fund_code = 'd000001'
rank_detail_info, fund_position_data = try_craw_info(fund_code)
print(rank_detail_info)
print(fund_position_data)