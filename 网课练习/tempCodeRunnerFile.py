import requests
import json

url = 'https://qianwen.biz.aliyun.com/dialog/conversation'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Content-Type': 'application/json',  # 这里将 Content-Type 加入 headers
    "cookie": "login_current_pk=1329281571547653; _abfpc=eead243ae57610bda7850e11da76daaed57de12d_2.0; yunpk=1329281571547653; cna=j+2bHrVqp10CAXW75G/ATJ1W; t=b1c38426830f00eacdfa91af41610cf2; tongyi_guest_ticket=g2fVQCulf6BO53u2yQcQcUoDW8u8_y$Em4u_DmdbPybTeyD5T89SntFjRNmYFsIYpSecze20sAxn0; login_tongyi_ticket=A5msOW2_QhATHwJQKYPQaSb6tUAhcdVmyoiWM6JcbN3uNZ6QrsUUaHrrXUaI5WML0; tongyi_sso_ticket=_vsLhJf7nX*yNuRcvRDN2ycLwlNwHOb8LY7F70eaFulf1En_treMU*Ent6AHvLFF0; aliyun_site=CN; cnaui=1329281571547653; aui=1329281571547653; aliyun_country=CN; aliyun_site=CN; aliyun_lang=zh; acw_tc=77907886-8f0c-9feb-b616-8e5be724cbb4d6ad467328af5b45ba687f16fd6510e1; atpsida=5f4301dd38e90522fe925eea_1730859253_1; sca=53fd16a2; _samesite_flag_=true; cookie2=157e18ba31d0c4e95481f675f1a92577; _tb_token_=3b8efee386363; isg=BNnZ9IVT2mL3_IR-5ef4lQbv6MWzZs0YNMQK_PuOVYB_AvmUQ7bd6EcABkZ0oWVQ; tfstk=cwd5BysgYuq5imzqf6gVCj80M8WCaKHVJb76PqbDoUEL4VLADsm8_GT09hEUxDQf."
}

# 假设 `data` 是您想要发送的 JSON 数据
data = {
  "model": "",
  "action": "next",
  "mode": "chat",
  "userAction": "probe",
  "requestId": "39052ac9461742d5b6ac5aa14fed84c4",
  "sessionId": "f250331744e543d390a57c7ef2004d72",
  "sessionType": "text_chat",
  "parentMsgId": "478498164b6646dea1b3eede1bf27116",
  "params": {
    "agentId": "",
    "searchType": "",
    "pptGenerate": False
  },
  "contents": [
    {
      "content": "科技",
      "contentType": "text",
      "role": "user",
      "ext": {
        "searchType": "",
        "pptGenerate": False
      }
    }
  ]
}

# 发送请求
response = requests.post(url, data=json.dumps(data), headers=headers)

# 输出响应状态
print(response.status_code)

# 处理响应文本
response_text = response.text

# 提取各个 data: 开头的部分
if response_text:
    data_chunks = response_text.split('data: ')
    extracted_jsons = []

    for chunk in data_chunks:
        json_str = chunk.strip()
        if json_str and json_str != '[DONE]':
            try:
                json_data = json.loads(json_str)
                extracted_jsons.append(json_data)
            except json.JSONDecodeError:
                print("解析JSON时出错:", json_str)

    # 仅显示最后一个数据块的中文回答部分
    if extracted_jsons:
        last_json = extracted_jsons[-1]  # 获取最后一个JSON对象
        if 'contents' in last_json and last_json['contents']:
            last_content = last_json['contents'][0]['content']
            print("最后一个回答的中文部分：", last_content)
        else:
            print("最后一个数据块没有内容")
else:
    print("响应内容为空")