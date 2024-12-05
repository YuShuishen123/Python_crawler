from fileinput import close
from http.client import responses
from idlelib.iomenu import encoding
from operator import index
from pydoc import resolve
import requests
import pandas as pd
from get_ua import get_ua
import re
import time
import random
import numpy as np
from collections import OrderedDict
from bs4 import BeautifulSoup
import csv
from pyecharts import options as opts
from pyecharts.charts import wordCloud,Page,Line

# 获得基金的原始数据
def get_rank_data(url, page_index, max_rank, max_page, fund_type):
    # 根据当前起始页获取当前页面所有基金的情况
    try_cnt = 1
    rank_data = []
    while page_index < max_page and try_cnt < 3:
        # 根据每页数据条数确定起始下标
        new_url = url + '?ft=' + fund_type + '&sc=1n&st=desc&pi=' + str(page_index) + '&pn=100&fl=0&isab=1'
        print("正在爬取第{0}页数据：{1}".format(page_index, new_url))
        # 爬取当前页码数据
        response = requests.get(url=new_url, headers={'User-Agent': get_ua()}, timeout=10)
        if len(response.text) > 100:
            # 匹配数据并解析
            res_data = re.findall(r'\[{1}\S+]{1}', response.text)[0]
            # 解析单页数据
            rank_pages_data = resolve_rank_info(res_data)
            # 追加写入每一条基金的详细数据
            rank_data.extend(rank_page_data for rank_page_data in rank_pages_data)
            page_index += 1
        else:
            try_cnt += 1
        # 随机休眠3 - 5秒
        time.sleep(random.randint(3, 5))
    df_rank_data = pd.DataFrame(rank_data)
    print("爬取基金的总数据=" + str(len(df_rank_data)))
    return df_rank_data


# 解析排名考前的基金的详细数据
def resolve_rank_detail_info(fund_code, response):
    rank_detail_info = OrderedDict()
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_detail_info['基金代码'] = 'd' + fund_code
    soup_div = soup.find_all('div', class_='bs_gl')[0]
    rank_detail_info['成立日期'] = soup_div.find_all('label')[0].find_all('span')[0].get_text()
    rank_detail_info['基金经理'] = soup_div.find_all('label')[1].find_all('a')[0].get_text()
    rank_detail_info['类型'] = soup_div.find_all('label')[2].find_all('span')[0].get_text()
    rank_detail_info['管理人'] = soup_div.find_all('label')[3].find_all('a')[0].get_text()
    rank_detail_info['资产规模'] = soup_div.find_all('label')[4].find_all('span')[0].get_text().replace("\r\n", "").replace(" ", "")
    return rank_detail_info


# 解析排名靠前的基金的详细数据（收益数据）
def resolve_rank_info(data):
    # 解析每一页的所有基金的收益
    rank_pages_data = []
    data = data.replace("[", "").replace("]", "").replace('"', "")
    for data_row in data.split(","):
        rank_info = OrderedDict()
        row_arr = data_row.split("|")
        if len(row_arr) > 16:
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
        # 保存当前 rank 信息
        rank_pages_data.append(rank_info)
    return rank_pages_data


# 解析基金十大持仓数据
def resolve_position_info(fund_code, text):
    fund_positions_data = []
    res_data = re.findall(r'\"(.*)\"', text)[0]
    soup = BeautifulSoup(res_data, 'html.parser')
    updata_data = soup.find_all('label', class_='right lab2 xq505')[0].find_all('font')[0].get_text()
    soup_tbody = soup.find_all('table', class_='w782 comm tzxq')[0].find_all('tbody')[0]
    for soup_tr in soup_tbody.find_all('tr'):
        position_info = OrderedDict()
        position_info['基金代码'] = 'd' + fund_code
        position_info['持仓股票代码'] = 'd' + soup_tr.find_all('td')[1].find_all('a')[0].get_text()
        position_info['持仓股票名称'] = soup_tr.find_all('td')[2].find_all('a')[0].get_text()
        position_info['持仓股票占比'] = soup_tr.find_all('td')[4].get_text()
        position_info['持仓股票持股数'] = soup_tr.find_all('td')[5].get_text()
        position_info['持仓股票持股市值'] = soup_tr.find_all('td')[6].get_text().replace(",", "")
        position_info['更新日期'] = updata_data
        fund_positions_data.append(position_info)
    return fund_positions_data


# 尝试爬取失败基金数据
def try_craw_info(fund_code, try_cnt):
    if try_cnt > 3:
        return None, None
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
    except:
        time.sleep(random.randint(2 * try_cnt, 4 * try_cnt))
        print("{0}基金数据爬取失败，请注意！".format(str(fund_code[1:])))
        rank_detail_info, fund_position_data = try_craw_info(fund_code, try_cnt + 1)
    return rank_detail_info, fund_position_data


# 获取基金的详细持仓数据
def get_position_data(data, rank):
    # 清洗基金数据
    data = data.replace('', np.nan, regex=True)
    data_nona = data.dropna(subset=['近1年'])
    data_nona = data_nona.reset_index(drop=True)
    data_nona['近1年'] = data_nona['近1年'].astype(float)
    data_sort = data_nona.sort_values(by='近1年', ascending=False)
    data_sort.reset_index(inplace=True)
    data_rank = data_sort.loc[0:rank - 1, :]

    # 爬取每个基金的详细数据
    rank_detail_data = []
    position_data = []
    error_funds_list = []
    count = 1
    for row_index, data_row in data_rank.iterrows():
        fund_code = str(data_row['基金代码'])
        try:
            # 爬取页面，获取该基金的持仓数据
            position_title_url = "http://fundf10.eastmoney.com/ccmx_" + str(fund_code[1:]) + ".html"
            print('正在爬取第 {0}/{1} 个基金 {2} 的详细数据中...'.format(row_index + 1, len(data_rank), fund_code[1:]))
            response_title = requests.get(url=position_title_url, headers={'User-Agent': get_ua()}, timeout=10)
            # 解析基金的详细数据
            rank_detail_info = resolve_rank_detail_info(fund_code[1:], response_title)
            rank_detail_data.append(rank_detail_info)
            # 爬取页面，获取该基金的持仓数据
            position_data_url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=" + \
                                str(fund_code[1:]) + "&topline=10&year=2024&month=&rt=" + str(random.uniform(0, 1))
            print('正在爬取第 {0}/{1} 个基金 {2} 的持仓情况中...'.format(row_index + 1, len(data_rank), fund_code[1:]))
            # 解析基金的持仓情况
            print('持仓数据地址' + position_data_url)
            response_data = requests.get(url=position_data_url, headers={'User-Agent': get_ua()}, timeout=10)
            fund_positions_data = resolve_position_info(fund_code[1:], response_data.text)
            # 保存数据
            position_data.extend(fund_positions_data for fund_positions_data in fund_positions_data)
        except:
            error_funds_list.append(fund_code)
            print("{0}的持仓数据爬取失败，稍后再试！".format(str(fund_code[1:])))
    # 进行休眠
    time.sleep(random.randint(2, 4))

    # 爬取失败的进行重试
    for fund_info in error_funds_list:
        rank_detail_data_try, position_data_try = try_craw_info(fund_info, 1)
        if rank_detail_data_try is not None:
            # 保存数据
            rank_detail_data.append(rank_detail_data_try)
            position_data.extend(fund_position_data for fund_position_data in position_data_try)
    df_rank_detail_data = pd.DataFrame(rank_detail_data)
    df_position_data = pd.DataFrame(position_data)
    return df_rank_detail_data, df_position_data


# 爬取数据
def Get_Data(url, page_index, max_page, fund_type, max_rank, Year, Quarterly):
    Rate_return_Origin_Data_Path = '基金数据分析/数据清洗前/' + Year + '年' + fund_type + '型基金近一年高收益率基金的收益详情-' + Quarterly + '.csv'
    Position_Top_Origin_Data_Path = '基金数据分析/数据清洗前/' + Year + '年' + fund_type + '型基金近一年高收益率基金的高收益率基金的前十大持仓-' + Quarterly + '.csv'

    # 获得详细季度、年的收益情况
    df_rank_data = get_rank_data(url, page_index, max_rank, max_page, fund_type)

    # 获得 top 的基金数量
    max_rank = 300 if int(len(df_rank_data) / 100) > 3 else 100

    # 获得基金详细信息和持仓情况
    df_rank_detail_data, df_position_data = get_position_data(df_rank_data, max_rank)

    # 合并收益数据和持仓详情数据
    df_rank_data = df_rank_data.merge(df_rank_detail_data, on='基金代码', how='outer')
    df_rank_data = df_rank_data.fillna('--')

    # 保存数据到 csv 文件
    df_rank_data.to_csv(Rate_return_Origin_Data_Path, encoding='utf_8_sig', index=False)
    df_position_data.to_csv(str(Position_Top_Origin_Data_Path), encoding='utf_8_sig', index=False)

    print("数据爬取结束！")
    return max_rank

#数据清洗
def Clean_data(Year,fund_type,max_rank,Quarterly,Rate_return_top_number):
    Position_Top_Origin_Data_Path = '基金数据分析/数据清洗前/' + Year + '年' + fund_type + '型基金近一年高收益率基金的高收益率基金的' + '前十大持仓-' + Quarterly + '.csv'
    Position_Top_Clean_Data_Path = '基金数据分析/数据清洗后/' + Year + '年' + fund_type + '型基金近一年高收益率基金的高收益率基金的' + '前十大持仓-' + Quarterly + '.csv'
    Rate_return_Origin_Data_Path = '基金数据分析/数据清洗前/' + Year + '年' + fund_type + '型基金近一年高收益率基金的收益详情-' + Quarterly + '.csv'
    Rate_return_Clean_Data_Path = '基金数据分析/数据清洗后/' + Year + '年' + fund_type + '型基金近一年高收益率基金的收益详情-' + Quarterly + '.csv'
    Rate_return_Top_Data_Path =f'基金数据分析/数据清洗后/' + Year + '年' + '近一年偏股型收益率Top' + Quarterly + '.csv'

    df_gp=pd.read_csv(Position_Top_Origin_Data_Path)
    df_gp.head(10)
    df_gpl=df_gp.drop('持仓股票最新价格',axis=1)
    df_gp.to_csv(Position_Top_Clean_Data_Path,',',index=False,header=True,encoding='utf_8_sig')

    #因为要分析近一年的收益率，故将成立不到一年的收益率为空的数据清洗
    df=pd.read.csv(Rate_return_Origin_Data_Path)
    df1=df.dropna(axis=0,subset=['近一年'])

    #将资产规模中的数据提取出来
    df1['size']=df1['资产规模'].apply(lambda x:x.spilt('亿')[0])
    df1.head(Rate_return_top_number)

    #删除基金经理为空的行
    df_pg=df1.drop(index=[4,5])
    df_pg.to_csv(Rate_return_Clean_Data_Path, sep=',', index=False, header=True, encoding='utf_8_sig')

    df_pg10 = df_pg.head(Rate_return_top_number)
    df_pg10.to_csv(Rate_return_Top_Data_Path, sep=',', index=False, header=True, encoding='utf_8_sig')


#数据清洗

def Data_Process_Mutilt_Quarterly(Year1, Year2, Position_Area):
    wd1 = Data_Process_Single_Quarterly(Year2,Quarterly2,Position_Area)
    wd2 = Data_Process_Single_Quarterly(Year2, Quarterly3, Position_Area)

    Quarterly2_Stock_name_and_Position_number = pd.read_csv(
        '基金数据分析/处理数据/' + Year2 + '年' + Quarterly2 + '重仓前10股票基金持有家数统计.csv')
    Quarterly3_Stock_name_and_Position_number = pd.read_csv(
        '基金数据分析/处理数据/' + Year2 + '年' + Quarterly3 + '重仓前10股票基金持有家数统计.csv')


    #合并季度之间持有重仓股票的基金总数
    Compare_Quarterlys_Position_number = pd.DataFrame(
        columns=['股票名称', Quarterly2 + '基金持有家数', Quarterly3 + '基金持有家数'])

    Compare_Quarterlys_Position_number.to_csv(
        '基金数据分析/处理数据/' + '连续二季度股票持有的基金持有家数' + Position_Area + '-' + Quarterly2 + '与' + Quarterly3+ '.csv',
        encoding='utf-8-sig', index=False)

    Quarterly2_Stock_name=[]
    for i in range(len(Quarterly2_Stock_name_and_Position_number)):
        Quarterly2_Stock_name.append(Quarterly2_Stock_name_and_Position_number.iloc[i,0])
    Quarterly3_Stock_name = []
    for i in range(len(Quarterly3_Stock_name_and_Position_number)):
        Quarterly3_Stock_name.append(Quarterly3_Stock_name_and_Position_number.iloc[i, 0])

    #连续季度的股票名称取并集
    Compare_Quarterlys_Position_number_Stock_name_all=Quarterly2_Stock_name+Quarterly3_Stock_name
    #Compare_Quarterlys_Position_number_Stock_name=Compare_Quarterlys_Position_number_Stock_name_all.set()
    Compare_Quarterlys_Position_number_Stock_name=np.unique(Compare_Quarterlys_Position_number_Stock_name_all)
    # 连续季度的股票名称取并集

    for i in range(len(Compare_Quarterlys_Position_number_Stock_name)):
        Compare_Quarterlys_Position_number.loc[Compare_Quarterlys_Position_number.shape[0] + 1] = {
            '股票名称': Compare_Quarterlys_Position_number_Stock_name[i], Quarterly2 + '基金持有家数': 0,
            Quarterly3 + '基金持有家数': 0}
    for i in range(len(Compare_Quarterlys_Position_number)):
        for j in range(len(Quarterly2_Stock_name_and_Position_number)):
            if (Compare_Quarterlys_Position_number.iloc[i, 0] == Quarterly2_Stock_name_and_Position_number.iloc[j, 0]):
                Compare_Quarterlys_Position_number.iloc[i, 1] = Quarterly2_Stock_name_and_Position_number.iloc[j, 1]
                break
        j = 0
        for j in range(len(Quarterly3_Stock_name_and_Position_number)):
            if (Compare_Quarterlys_Position_number.iloc[i, 0] == Quarterly3_Stock_name_and_Position_number.iloc[j, 0]):
                Compare_Quarterlys_Position_number.iloc[i, 2] = Quarterly3_Stock_name_and_Position_number.iloc[j, 1]
                break

    #建立连续季度合并之间的csv文件
    Compare_Quarterlys_Position_number.sort_values(Quarterly2+'基金持有家数',inplace=True)
    Compare_Quarterlys_Position_number.to_csv(
        '基金数据分析/处理数据/' + '连续二季度股票持有的基金持有家数' + Position_Area + '-' + Quarterly2 + '与' + Quarterly3+'.csv',
        encoding='utf-8-sig', index=False)
    # 建立连续季度合并之间的csv文件
    # 合并季度之间持有重仓股票的基金总数


# 合并季度之间的各个基金持仓股票持股总市值
    Quarterly2_Stock_name_and_market_value = pd.read_csv(
        '基金数据分析/处理数据/' + Year2 + '年' + Quarterly2 + '各个基金持仓股票持股总市值.csv')
    Quarterly3_Stock_name_and_market_value = pd.read_csv(
        '基金数据分析/处理数据/' + Year2 + '年' + Quarterly3 + '各个基金持仓股票持股总市值.csv')

    Compare_Quarterlys_market_value = pd.DataFrame(
        columns=['股票名称', Quarterly2 + '各个基金持仓股票持股总市值',Quarterly3 + '各个基金持仓股票持股总市值'])

    Quarterly2_Stock_name = []
    for i in range(len(Quarterly2_Stock_name_and_market_value)):
        Quarterly2_Stock_name.append(Quarterly2_Stock_name_and_market_value.iloc[i, 0])
    Quarterly3_Stock_name = []
    for i in range(len(Quarterly3_Stock_name_and_market_value)):
        Quarterly3_Stock_name.append(Quarterly3_Stock_name_and_market_value.iloc[i, 0])

    # 相邻季度的股票名称取并集
    # 删除列表中重复的元素
    Quarterly2_Stock_name_set = Deleter(Quarterly2_Stock_name)
    Quarterly3_Stock_name_set = Deleter(Quarterly3_Stock_name)
    # 删除列表中重复的元素

    Compare_Quarterlys_market_value_Stock_name = Deleter(
        Quarterly2_Stock_name_set + Quarterly3_Stock_name_set)
    # 写相邻季度比较文件的“股票名称”字段
    for i in range(len(Compare_Quarterlys_market_value_Stock_name)):
        Compare_Quarterlys_market_value.loc[Compare_Quarterlys_market_value.shape[0] + 1] = {
            '股票名称': Compare_Quarterlys_market_value_Stock_name[i], Quarterly2 + '各个基金持仓股票持股总市值': 0,
            Quarterly3 + '各个基金持仓股票持股总市值': 0}

    for i in range(len(Compare_Quarterlys_market_value)):
        for j in range(len(Quarterly2_Stock_name_and_market_value)):
            if (Compare_Quarterlys_market_value.iloc[i, 0] == Quarterly2_Stock_name_and_market_value.iloc[j, 0]):
                Compare_Quarterlys_market_value.iloc[i, 1] = round(
                    Quarterly2_Stock_name_and_market_value.iloc[j, 1])
                break
        j=0
        for j in range(len(Quarterly3_Stock_name_and_market_value)):
            if (Compare_Quarterlys_market_value.iloc[i, 0] == Quarterly3_Stock_name_and_market_value.iloc[j, 0]):
                Compare_Quarterlys_market_value.iloc[i, 2] = round(
                    Quarterly3_Stock_name_and_market_value.iloc[j, 1])
                break

    # 建立季度之间比较数据的csv文件
    Compare_Quarterlys_market_value.sort_values(Quarterly2 + '各个基金持仓股票持股总市值', inplace=True)  # 按照第一季度各个基金持仓股票持股总市值
    Compare_Quarterlys_market_value.to_csv(
        '基金数据分析/处理数据/' + '连续二季度各个基金持仓股票持股总市值' + Position_Area + '-' + Quarterly2 + '与' + Quarterly3 + '.csv',
        encoding='utf-8-sig', index=False)
    # 合并季度之间的各个基金持仓股票持股总市值


# 合并季度之间的基金收益率
    Rate_return_Quarterly2 = pd.read_csv(
        '基金数据分析/处理数据/' + Year2 + '年' + Quarterly2 + '基金收益率前200.csv')
    Rate_return_Quarterly3 = pd.read_csv(
        '基金数据分析/处理数据/' + Year2 + '年' + Quarterly3 + '基金收益率前200.csv')
    Compare_Quarterlys_Rate_return = pd.DataFrame(
        columns=['基金名称', Quarterly2 + '收益率', Quarterly3 + '收益率'])

    Quarterly2_Fund_name = []
    for i in range(len(Rate_return_Quarterly2)):
        Quarterly2_Fund_name.append(Rate_return_Quarterly2.iloc[i, 0])
    Quarterly3_Fund_name = []
    for i in range(len(Rate_return_Quarterly3)):
        Quarterly3_Fund_name.append(Rate_return_Quarterly3.iloc[i, 0])

    # 基金名称没有重复，所以直接连接使用
    Compare_Quarterlys_Rate_return_Fund_name = Quarterly2_Fund_name + Quarterly3_Fund_name

    # 写相邻季度比较文件的“基金名称”字段
    for i in range(len(Compare_Quarterlys_Rate_return_Fund_name)):
        Compare_Quarterlys_Rate_return.loc[Compare_Quarterlys_Rate_return.shape[0] + 1] = {
            '基金名称': Compare_Quarterlys_Rate_return_Fund_name[i], Quarterly2 + '收益率': 0, Quarterly3 + '收益率': 0}

    for i in range(len(Compare_Quarterlys_Rate_return)):
        for j in range(len(Rate_return_Quarterly2)):
            if (Compare_Quarterlys_Rate_return.iloc[i, 0] == Rate_return_Quarterly2.iloc[j, 0]):
                Compare_Quarterlys_Rate_return.iloc[i, 1] = Rate_return_Quarterly2.iloc[j, 1]
                break
        j=0
        for j in range(len(Rate_return_Quarterly3)):
            if (Compare_Quarterlys_Rate_return.iloc[i, 0] == Rate_return_Quarterly3.iloc[j, 0]):
                Compare_Quarterlys_Rate_return.iloc[i, 2] = Rate_return_Quarterly3.iloc[j, 1]
                break

    # 建立季度之间收益率比较数据的csv文件
    Compare_Quarterlys_Rate_return.sort_values(Quarterly2 + '收益率', inplace=True)  # 按照第一季度各个基金的基金收益率
    Compare_Quarterlys_Rate_return.to_csv(
        '基金数据分析/处理数据/' + '连续二季度基金收益率前200' + Position_Area + '-' + Quarterly2 + '与' + Quarterly3 + '.csv',
        encoding='utf_8_sig', index=False)
    # 合并季度之间的基金收益率
    return wd1,wd2



# 处理数据
def Data_Process_Single_Quarterly(Year,Quarterly,Position_Area):
    Position_Top_Clean_Data_Path = '基金数据分析/数据清洗后/' + Year + '年' + fund_type + '型基金近一年高收益率基金的' + '前十大持仓-' + Quarterly + '.csv'
    Rate_Return_Top_Data_Path = '基金数据分析/数据清洗后/' + Year + '年' + '近一年偏股型收益率Top' + '.csv'

    #获取基金代码
    Fund_code=[]
    with open (Rate_Return_Top_Data_Path,ending='utf_8_sig') as f:
        #创建一个阅读器，将f传给csv_reader
        reader=csv.reader(f)
        #使用csv的next的函数，将文件逐行独处
        header_row=next(reader)
        for row in reader:
            Fund_code.append(row [0])
    f.close()
    Stock_name=[]
    Stock_name_and_Position_Number=[]

    with open(Position_Top_Clean_Data_Path, encoding='utf_8_sig') as f:
        # 创建一个阅读器：将f传给csv.reader
        reader = csv.reader(f)
        # 使用csv的next函数，将reader传给next，将返回文件的下一行
        header_row = next(reader)
        for row in reader:
            # 选出股票收益率前10的基金的前十大持仓的排位3,4,5,6,7的股票且持仓占比在[3%-7%]
            if (row[0] in Fund_code):
                Stock_name.append(row[4])
    f.close()

    #删除重复的股票名称
    Stock_name_set=Deleter(Stock_name)
    #删除重复的股票名称

    Stock_cloud=[]
    Finally_Stock_name=[]
    for item in Stock_name_set:
        #股票持有的基金家数满足一定的数量，才将股票放入数据分析
        Stock_cloud.append({item,Stock_name.count(item)})
        temp={'股票名称':str(item),'基金持有家数':Stock_name.count(item)}
        Stock_name_and_Position_Number.append(temp)
        Finally_Stock_name.append(item)#为了按季度些持仓市值

    #按季度获取股票的持有家数以及云数据
    wd=wordCloud(Stock_cloud,Rate_return_top_number,Year,Quarterly,Position_Area)
    wd.render('基金数据分析/可视化结果/' + Year + '年' + '收益率前' + str(Rate_return_top_number)
              + '大基金的' + Position_Area + '持仓-' + Quarterly + '.html')

    # 按季度计算基金持仓前10大股票持股总市值
    Stock_market_value = []
    Position_Top_Clean_Data = pd.read_csv(Position_Top_Clean_Data_Path)  # 收益率排名靠前的基金10大持仓

    for i in range(len(Finally_Stock_name)):
        Stock_market_value_temp = 0
        for j in range(len(Position_Top_Clean_Data)):
            if (Finally_Stock_name[i] == Position_Top_Clean_Data.iloc[j, 4]):
                Stock_market_value_temp = Stock_market_value_temp + (
                    float(str(Position_Top_Clean_Data.iloc[j, 9]).replace(',', '')))

        temp = {'股票名称': Finally_Stock_name[i], '各个基金持仓股票持股总市值': Stock_market_value_temp}
        Stock_market_value.append(temp)
    # 按季度计算基金持仓前10大股票持股总市值

        # 获取收益率
        Rate_return_top_data = pd.read_csv(Rate_Return_Top_Data_Path)  # 收率靠前的基金
        Rate_return_top_and_front_data = Rate_return_top_data.head(40)  # 进一步的减小范围
        Rate_return_top_and_front_data_only = []
        for i in range(len(Rate_return_top_and_front_data)):
            temp = {'基金名称': Rate_return_top_and_front_data.iloc[i, 1], '收益率': Rate_return_top_and_front_data.iloc[i, 9]}
            Rate_return_top_and_front_data_only.append(temp)
        # 获取收益率

    # 按季度写十大重仓股票的基金数量
    header = ['股票名称', '基金持有家数']  #
    with open('基金数据分析/处理数据/' + Year + '年' + Quarterly + '重仓前10股票基金持有家数统计.csv', 'w',
              newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        writer.writerows(Stock_name_and_Position_Number)
    f.close()
    # 按季度写十大重仓股票的基金数量

    # 按季度写十大重仓股票的持仓市值
    header = ['股票名称', '各个基金持仓股票持股总市值']  # 数据列名
    with open('基金数据分析/处理数据/' + Year + '年' + Quarterly + '各个基金持仓股票持股总市值.csv', 'w',
              newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        writer.writerows(Stock_market_value)
    f.close()
    # 按季度写十大重仓股票的持仓市值

    # 按季度写收益排名200名的基金
    header = ['基金名称', '收益率']  # 数据列名
    with open('基金数据分析/处理数据/' + Year + '年' + Quarterly + '基金收益率前200.csv', 'w',
              newline='',encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        writer.writerows(Rate_return_top_and_front_data_only)
    f.close()
    # 按季度写收益排名200名的基金
    return wd

    #删除列表中重复的元素
    def Deleter(list):
        temp_list=[]
        for one in list:
            if one not in temp_list:
                temp_list.append(one)
        return temp_list
    # 删除列表中重复的元素

    #数据词云可视化
    def wordcloud_base(words,Rate_return_top_number,Position_Area,Year,Quarterly) -> WordCloud:
        c = (
            wordCloud()
            .add("", words, word_size_range=[10, 60])
            .set_global_opts(title_opts=opts.TitleOpts(title=Year+"年收益率前"+str(Rate_return_top_number)+'大基金的'+Position_Area+'持仓-'+Quarterly))
        )
        return c
    #数据词云可视化


    #获取基金代码
    Fund_code=[]

def Data_Process_Mutilt_Quarterly(Year1,Year2,Position_Area):
    wd1=Data_Process_Single_Quarterly(Year2,Quarterly2,Position_Area)
    wd2=Data_Process_Single_Quarterly(Year2,Quarterly3,Position_Area)

# 处理数据


for k in range(3):
    if Predict_accuracy_score_all_sort[k][0] == 'Tree':
        Predict_accuracy_score_temp.append(clf_Tree.predict(Test_temp))
    if Predict_accuracy_score_all_sort[k][0] == 'KNN':
        Predict_accuracy_score_temp.append(clf_KNN.predict(Test_temp))
    if Predict_accuracy_score_all_sort[k][0] == 'SVM':
        Predict_accuracy_score_temp.append(clf_SVM.predict(Test_temp))
    if Predict_accuracy_score_all_sort[k][0] == 'CNN':
        Predict_accuracy_score_temp.append(clf_CNN.predict(Test_temp))
print(Predict_accuracy_score_temp[0][0], Predict_accuracy_score_temp[1][0], Predict_accuracy_score_temp[2][0])

#KNN方法
    KNN = KNeighborsClassifier()
    clf_KNN = KNN.fit(Train_X, Train_y)
    Predict_Result_KNN = clf_KNN.predict(Verify_X)
    print('KNN方法训练完毕！')
    # KNN方法

    #SVM方法
    SVM = SVC(kernel='linear')
    clf_SVM = SVM.fit(Train_X, Train_y)
    Predict_Result_SVM = clf_SVM.predict(Verify_X)
    print('SVM方法训练完毕！')
    # SVM方法

#CNN方法
    mlp = neural_network.MLPClassifier(hidden_layer_sizes=(10, 20),
                                       # 隐藏层,（10,20）指的是隐藏层层数+每层单元数,（10,20）:测试准确率 0.6470588235294118,该值相对较好，当然这个与数据划分方式也有关系,也就是说结果会发生变化
                                       activation='relu',  # 激活函数
                                       solver='adam',
                                       alpha=0.0001,  # 正则化项系数
                                       batch_size='auto',
                                       learning_rate='constant',  # 学习率
                                       learning_rate_init=0.001,
                                       power_t=0.5,
                                       max_iter=200,  # 迭代次数
                                       tol=1e-4)
    clf_CNN = mlp.fit(Train_X, Train_y)
    Predict_Result_CNN = clf_CNN.predict(Verify_X)
    print('CNN方法训练完毕！')
    # CNN方法





# 主函数
if __name__ == '__main__':
    url = 'https://fundapi.eastmoney.com/fundtradenew.aspx'
    Year = '2024'
    Quarterly2 = '第二季度'
    Quarterly3 = '第三季度'
    page_index = 1
    Rate_return_top_number = 200
    max_page = 2
    max_rank = 300
    fund_type = 'gp'
    Position_Area = '重仓股票前10名'
    # 爬取基金数据
    # max_rank = Get_Data(url, page_index, max_page, fund_type, max_rank, Year, Quarterly1)
    # 爬取基金数据

    # 爬取数据,每季度分别爬取，因为每个季度的具体持仓网地址不一样（主要是年份），还有不同季度的class也不一样，具体在resolve_position_info函数中,可以作为作业进行修改
    # max_rank = Get_Data(url, page_index, max_page, fund_type, max_rank, Year, Quarterly1)
    # 爬取数据,每季度分别爬取，因为每个季度的具体持仓网地址不一样（主要是年份），还有不同季度的class也不一样，具体在resolve _position_info函数中，可以作为作业进行修改



    #处理数据
    wd1,wd2 = Data_Process_Mutilt_Quarterly(Year,Year,Position_Area,)
    #处理数据


#主函数