import requests
import json
import time

def translate_text(text, from_lang="en", to_lang="zh"):
    url = "https://fanyi.baidu.com/ait/text/translate"
    
    headers = {
        'Accept': 'text/event-stream',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/json',
        'Origin': 'https://fanyi.baidu.com',
        'Referer': 'https://fanyi.baidu.com/mtpe-individual/multimodal',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    }
    
    data = {
        "query": text,
        "from": from_lang,
        "to": to_lang,
        "domain": "common",
        "milliTimestamp": int(time.time() * 1000)
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            translations = []
            events = response.text.strip().split('\n\n')
            
            for event in events:
                if not event:
                    continue
                    
                for line in event.split('\n'):
                    if line.startswith('data: '):
                        try:
                            event_data = json.loads(line[6:])
                            
                            # 检查是否是翻译事件
                            if (event_data.get('errno') == 0 and 
                                event_data.get('data', {}).get('event') == 'Translating'):
                                # 获取翻译结果列表
                                trans_list = event_data['data'].get('list', [])
                                for trans in trans_list:
                                    if trans.get('dst'):
                                        translations.append(trans['dst'])
                            
                        except json.JSONDecodeError:
                            continue
            
            return translations if translations else None
            
    except Exception as e:
        print(f"翻译出错: {str(e)}")
    
    return None

if __name__ == "__main__":
    while True:
        text = input("\n请输入要翻译的文本(输入q退出): ")
        if text.lower() == 'q':
            break
            
        results = translate_text(text)
        if results:
            print("\n翻译结果:")
            for i, result in enumerate(results, 1):
                if len(results) > 1:
                    print(f"{i}. {result}")
                else:
                    print(result)
        else:
            print("\n翻译失败，请重试")
