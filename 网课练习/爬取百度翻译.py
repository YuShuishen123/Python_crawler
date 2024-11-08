import requests
url = 'https://fanyi.baidu.com/sug'

# 将kw的内容改为你想要翻译的内容,只支持单词翻译

def getkw():
    kw = input('请输入你想要翻译的内容(输入q退出)：')
    return kw

def translate(kw):
    dat = {
        'kw': kw
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
    }
    response = requests.post(url,data=dat,headers=headers)  # 发送请求

    # 处理响应数据
    data = response.json()
    if 'data' in data:  # 检查 'data' 键是否存在
        translations = [item['v'] for item in data['data']]  # 从 'data' 中提取 'v' 值
        i = 1
        for translation in translations:
            print("翻译结果",i,translation)
            i += 1
    else:
        print("没有找到翻译结果。")

def main():
    while True:
        kw = getkw()
        if kw.lower() == 'q':
            print("感谢使用,再见!")
            break
        translate(kw)
        print("-" * 50)

if __name__ == "__main__":
    main()