import os
import pandas as pd
from header_tools.get_ua import get_ua
import requests
import re
import time
import random
from collections import OrderedDict
from bs4 import BeautifulSoup

# 爬取详细季度、年的收益情况
def get_rank_data(url, page_index, max_rank, max_page, fund_type):
    rank_pages_data = []  # 存储收益数据
    # 实现数据抓取和解析逻辑
    # 示例数据
    rank_pages_data.append({'基金代码': 'd000001', '基金名称': '基金A'})
    return pd.DataFrame(rank_pages_data)

# 爬取基金详细信息和持仓情况
def get_position_data(df_rank_data, max_rank):
    df_rank_detail_data = pd.DataFrame([{'基金代码': 'd000001', '基金经理': '经理A'}])  # 示例数据
    df_position_data = pd.DataFrame()  # 存储持仓数据
    return df_rank_detail_data, df_position_data

# 解析基金的详细数据
def resolve_rank_detail_info(fund_code, response):
    rank_detail_info = OrderedDict()
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_detail_info['基金代码'] = 'd' + fund_code
    return rank_detail_info

# 解析基金的持仓数据
def resolve_position_info(fund_code, response):
    fund_positions_data = []
    soup = BeautifulSoup(response.text, 'html.parser')
    return fund_positions_data

# 爬取数据
def get_data(url, page_index, max_page, fund_type, max_rank, year, quarterly):
    Rate_return_Origin_Data_Path = f'基金数据分析/数据清洗前/{year}年{fund_type}型基金近一年高收益率基金的收益详情-{quarterly}.csv'
    Position_Top_Origin_Data_Path = f'基金数据分析/数据清洗前/{year}年{fund_type}型基金近一年高收益率基金的高收益率基金的前十大持仓-{quarterly}.csv'

    # Ensure the directory exists
    os.makedirs(os.path.dirname(Rate_return_Origin_Data_Path), exist_ok=True)

    df_rank_data = get_rank_data(url, page_index, max_rank, max_page, fund_type)

    # Debug statement to check if df_rank_data is empty
    if df_rank_data.empty:
        print("df_rank_data is empty")
        return

    max_rank = 300 if int(len(df_rank_data) / 100) > 3 else 100
    df_rank_detail_data, df_position_data = get_position_data(df_rank_data, max_rank)

    # Debug statements to check for '基金代码' column
    print("df_rank_data columns:", df_rank_data.columns)
    print("df_rank_detail_data columns:", df_rank_detail_data.columns)

    # Check if '基金代码' column exists in both DataFrames
    if '基金代码' in df_rank_data.columns and '基金代码' in df_rank_detail_data.columns:
        df_rank_data = df_rank_data.merge(df_rank_detail_data, on='基金代码', how='outer').fillna('--')
    else:
        raise KeyError("Column '基金代码' is missing in one of the DataFrames")

    df_rank_data.to_csv(Rate_return_Origin_Data_Path, encoding='utf_8_sig', index=False)
    df_position_data.to_csv(Position_Top_Origin_Data_Path, encoding='utf_8_sig', index=False)

    print("数据爬取结束！")

# 主函数
if __name__ == '__main__':
    url = 'https://fundapi.eastmoney.com/fundtradenew.aspx'
    year = '2024'
    quarterly = '第一季度'
    page_index = 1
    max_page = 2
    fund_type = 'gp'
    max_rank = 300

    get_data(url, page_index, max_page, fund_type, max_rank, year, quarterly)