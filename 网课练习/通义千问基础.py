import requests
import json
import uuid
import tkinter as tk
from tkinter import scrolledtext
import threading

# 初始化URL和请求头
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

# 创建主窗口
root = tk.Tk()
root.title("深哥通义 AI 聊天")

# 增加窗口大小
root.geometry("800x550")  # 增加窗口宽度和高度

# 设置全局字体
default_font = ("Arial", 14)

# 创建滚动的输出框
output_text = scrolledtext.ScrolledText(root, height=20, width=70, wrap=tk.WORD, font=default_font)
output_text.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
output_text.insert(tk.END, "欢迎提问！\n\n")  

# 创建输入框
input_text = tk.Entry(root, width=50, font=default_font)
input_text.grid(row=1, column=0, padx=20, pady=10)

# 显示加载动画的标签
loading_label = tk.Label(root, text="", fg="red", font=default_font)
loading_label.grid(row=1, column=1, padx=10)

# 发送按钮点击事件
def send_message():
    global request_id, session_id, parent_msg_id  # 使用 global 关键字声明使用外部变量

    user_content = input_text.get()
    
    if user_content.lower() == "exit":
        output_text.insert(tk.END, "结束对话。\n")
        root.quit()
        return

    # 清空输入框
    input_text.delete(0, tk.END)

    # 显示"请稍等..."消息
    loading_label.config(text="请稍等...")

    # 构造请求数据
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

    # 使用线程避免阻塞
    threading.Thread(target=send_request, args=(data,)).start()

def send_request(data):
    global request_id, session_id, parent_msg_id
    
    # 发送请求
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)

        # 处理响应
        if response.status_code == 200:
            response_text = response.text
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

                # 处理提取的 JSON 数据
                if extracted_jsons:
                    last_json = extracted_jsons[-1]
                    if 'contents' in last_json and last_json['contents']:
                        for content_item in last_json['contents']:
                            if content_item['contentType'] == 'plugin':
                                plugin_result = content_item.get('content', '')
                                if plugin_result:
                                    try:
                                        plugin_data = json.loads(plugin_result)
                                        # display_response(f"插件返回数据：{plugin_data}")
                                    except json.JSONDecodeError:
                                        display_response(f"插件返回内容解析失败：{plugin_result}")
                            elif content_item['contentType'] == 'text':
                                display_response(f"AI：{content_item.get('content', '未能提取有效内容')}")
                    else:
                        display_response("返回内容结构不符合预期")
                        display_response(f"原始响应内容：{response_text}")
                    # 更新 requestId, sessionId, parentMsgId
                    request_id = str(uuid.uuid4())  # 每次生成一个新的 requestId
                    session_id = last_json.get("sessionId", session_id)
                    parent_msg_id = last_json.get("msgId", parent_msg_id)
                else:
                    display_response("响应内容为空")
            else:
                display_response("响应内容为空")
        else:
            display_response(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        display_response(f"请求失败，错误信息：{str(e)}")
    finally:
        loading_label.config(text="")  # 请求结束后清除“请稍等...”


def display_response(message):
    # 在 GUI 中显示响应
    output_text.insert(tk.END, f"{message}\n")
    output_text.yview(tk.END)

# 发送按钮
send_button = tk.Button(root, text="发送", command=send_message)
send_button.grid(row=1, column=2, padx=10)

# 按回车键发送消息
root.bind('<Return>', lambda event: send_message())

# 启动 GUI 主循环
root.mainloop()
