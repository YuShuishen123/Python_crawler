import requests
import json
import time
import random
from urllib.parse import quote

def search_bilibili(keyword, page=1, page_size=42):
    # 对关键词进行 URL 编码
    encoded_keyword = quote(keyword)
    
    # 使用搜索API
    base_url = "https://api.bilibili.com/x/web-interface/search/all/v2"
    
    params = {
        "keyword": keyword,
        "page": page,
        "page_size": page_size,
        "platform": "pc",
        "order": "default",
        "search_type": "video",
        "context": "",
        "duration": "",
        "tids_1": "",
        "tids_2": "",
        "__refresh__": "true",
        "_extra": "",
        "highlight": "1",
        "single_column": "0"
    }

    headers = {
        'cookie': "buvid4=A7A0254B-1DB9-582B-BC3A-D6666361E71F93552-023032710-e63QcPwqs3ejMQNxFVoRBA%3D%3D; header_theme_version=CLOSE; enable_web_push=DISABLE; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW2; buvid3=96E0DEEE-A286-573A-7897-709B16C794DE23717infoc; b_nut=1711420622; _uuid=73E1CEEF-691A-159B-AFEE-43CE5F3DB891036518infoc; is-2022-channel=1; buvid_fp=e3e7ac82edcacf5a5fa385fd4711f394; rpdid=|(um~lkR~m)J0J'u~uRYJ)k~R; LIVE_BUVID=AUTO8417194715109098; DedeUserID=323766577; DedeUserID__ckMd5=45de88ac3f3f9e97; blackside_state=0; CURRENT_BLACKGAP=0; PVID=1; hit-dyn-v2=1; CURRENT_FNVAL=4048; CURRENT_QUALITY=120; fingerprint=19d00ed93723fd1e5cffa1d40c925263; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzA5ODY0NTksImlhdCI6MTczMDcyNzE5OSwicGx0IjotMX0.5g3QVh3hF0qle-Do7VBdHAqTCALmzXRnOYqHSzYkN7s; bili_ticket_expires=1730986399; SESSDATA=27eef1f7%2C1746280614%2C4c370%2Ab2CjCNpK1tfeS0SjCKleYAXrcGV0NTRcAO3ryZHEcUsWZzWBmlUJgp8JaNNWRVAzFbBQUSVklsY2VYWjV0dWZHbnJvNTlHd01aenhUZUlzWnhwRVVSTlh0Y3U0cW02T1NfcmNOQVYwT0pmZi01emMyOUdOcmNXMi14TnhKQlFHeXhob3E5VlRuWGFBIIEC; bili_jct=9d4e37a11dae17933d48ffdb049055ca; home_feed_column=5; b_lsid=810BDCD107_19305CFF398; browser_resolution=1528-746; sid=4iabfw4r",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # 创建会话
        session = requests.Session()
        
        # 先访问搜索页面
        search_page_url = f'https://search.bilibili.com/all?keyword={encoded_keyword}'
        session.get(search_page_url, headers=headers)
        
        # 随机延迟
        time.sleep(random.uniform(1, 3))
        
        # 发起API请求
        response = session.get(base_url, params=params, headers=headers)
        
        # 检查响应状态码
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return None
            
        # 解析 JSON
        data = response.json()
        
        # 检查返回的数据结构
        if data.get('code') != 0:
            print(f"API返回错误: {data.get('message')}")
            return None

        # 提取所需数据
        videos = []
        for result_type in data['data']['result']:
            if result_type['result_type'] == 'video':
                for video in result_type['data']:
                    if isinstance(video, dict):  # 确保是视频数据
                        video_data = {
                            'title': video.get('title', '').replace('<em class="keyword">', '').replace('</em>', ''),
                            'author': video.get('author', '未知作者'),
                            'play': video.get('play', 0),
                            'arcurl': video.get('arcurl', '')
                        }
                        videos.append(video_data)
        
        # 根据播放量排序
        videos.sort(key=lambda x: x['play'] if x['play'] is not None else 0, reverse=True)
        return videos
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None
    except Exception as e:
        print(f"其他错误: {e}")
        return None

def format_number(num):
    """格式化数字显示"""
    if num >= 10000:
        return f"{num/10000:.1f}万"
    return str(num)

def print_videos(videos):
    """格式化打印视频信息"""
    print("\n" + "="*50)
    print(f"共获取到 {len(videos)} 个视频，按播放量排序如下：")
    print("="*50 + "\n")
    
    for i, video in enumerate(videos, 1):
        print(f"视频 {i}:")
        print(f"标题: {video['title']}")
        print(f"作者: {video['author']}")
        print(f"播放量: {format_number(video['play'])}")
        print(f"链接: {video['arcurl']}")
        print("-"*50)  # 分隔线

if __name__ == "__main__":
    while True:
        keyword = input("\n请输入搜索关键词(输入 q 退出): ")
        if keyword.lower() == 'q':
            break
            
        print(f"\n正在搜索: {keyword}")
        videos = search_bilibili(keyword)
        
        if videos:
            print_videos(videos)
        else:
            print("搜索失败，请重试")


