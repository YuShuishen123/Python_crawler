import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from datetime import datetime


def get_fund_data(url):
    # 发送HTTP GET请求
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    # 定位到所需数据的标签，根据实际情况更新选择器
    data_elements = soup.select("your-data-selector")  # 请替换 `your-data-selector`

    # 初始化数据列表
    fund_data = []
    for element in data_elements:
        # 按实际情况提取每项的数据
        data_item = {
            "基金代码": element.select_one("your-fund-code-selector").text,
            "基金名称": element.select_one("your-fund-name-selector").text,
            "基金类型": element.select_one("your-fund-type-selector").text,
            "最新净值": element.select_one("your-nav-selector").text,
            "收益率": element.select_one("your-return-selector").text
            # 更多字段按需添加
        }
        fund_data.append(data_item)
    return fund_data


def save_to_csv(fund_data, fund_type, year, quarterly):
    # 创建输出路径
    base_dir = '基金数据分析/数据清洗前/'
    os.makedirs(base_dir, exist_ok=True)

    # 构建文件路径
    rate_return_path = f"{base_dir}{year}年{fund_type}型基金近一年高收益率基金的收益详情-{quarterly}.csv"
    position_top_path = f"{base_dir}{year}年{fund_type}型基金近一年高收益率基金的前十大持仓-{quarterly}.csv"

    # 保存收益率数据
    df_rate_return = pd.DataFrame(fund_data)
    df_rate_return.to_csv(rate_return_path, index=False, encoding='utf-8-sig')

    # 假设十大持仓数据是 fund_data 中的子集，这里仅为示例
    top_position_data = [data for data in fund_data if float(data["收益率"].strip('%')) > 10]  # 根据实际规则筛选
    df_position_top = pd.DataFrame(top_position_data)
    df_position_top.to_csv(position_top_path, index=False, encoding='utf-8-sig')


# 设置参数
url = 'https://fundapi.eastmoney.com/fundtradenew.aspx'
fund_type = '股票'  # 按实际情况设置
year = str(datetime.now().year)
quarterly = 'Q4'  # 按实际情况设置

# 获取数据并保存到CSV
fund_data = get_fund_data(url)
save_to_csv(fund_data, fund_type, year, quarterly)
