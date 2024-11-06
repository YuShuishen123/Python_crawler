import requests
import json
import uuid

url = 'https://qianwen.biz.aliyun.com/dialog/conversation'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'Content-Type': 'application/json',
    "cookie": "login_current_pk=1329281571547653; _abfpc=eead243ae57610bda7850e11da76daaed57de12d_2.0; yunpk=1329281571547653; cna=j+2bHrVqp10CAXW75G/ATJ1W; t=b1c38426830f00eacdfa91af41610cf2; tongyi_guest_ticket=g2fVQCulf6BO53u2yQcQcUoDW8u8_y$Em4u_DmdbPybTeyD5T89SntFjRNmYFsIYpSecze20sAxn0; login_tongyi_ticket=A5msOW2_QhATHwJQKYPQaSb6tUAhcdVmyoiWM6JcbN3uNZ6QrsUUaHrrXUaI5WML0; tongyi_sso_ticket=_vsLhJf7nX*yNuRcvRDN2ycLwlNwHOb8LY7F70eaFulf1En_treMU*Ent6AHvLFF0; aliyun_site=CN; cnaui=1329281571547653; aui=1329281571547653; aliyun_country=CN; aliyun_site=CN; aliyun_lang=zh; acw_tc=77907886-8f0c-9feb-b616-8e5be724cbb4d6ad467328af5b45ba687f16fd6510e1; atpsida=5f4301dd38e90522fe925eea_1730859253_1; sca=53fd16a2; _samesite_flag_=true; cookie2=157e18ba31d0c4e95481f675f1a92577; _tb_token_=3b8efee386363; isg=BNnZ9IVT2mL3_IR-5ef4lQbv6MWzZs0YNMQK_PuOVYB_AvmUQ7bd6EcABkZ0oWVQ; tfstk=cwd5BysgYuq5imzqf6gVCj80M8WCaKHVJb76PqbDoUEL4VLADsm8_GT09hEUxDQf."
}

# 初始化 requestId, sessionId, sessionType, parentMsgId
request_id = str(uuid.uuid4())  # 使用 UUID 生成唯一的 requestId
session_id = "f250331744e543d390a57c7ef2004d72"  # 可初始化为固定的 sessionId，或通过请求获取动态 session
session_type = "text_chat"
parent_msg_id = "478498164b6646dea1b3eede1bf27116"

while True:
    # 用户输入提问内容
    user_content = input("请输入您的问题（输入 'exit' 退出）：")
    
    # 检查用户输入是否为 'exit'，若是则结束循环
    if user_content.lower() == "exit":
        print("结束对话。")
        break

    data = {
        "model": "",
        "action": "next",
        "mode": "chat",
        "userAction": "probe",
        "requestId": request_id,
        "sessionId": session_id,
        "sessionType": session_type,
        "parentMsgId": parent_msg_id,
        "params": {
            "agentId": "",
            "searchType": "",
            "pptGenerate": False
        },
        "contents": [
            {
                "content": user_content,
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

    # 检查响应状态
    if response.status_code == 200:
        response_text = response.text
        
    # 输出响应内容
        print(response_text)