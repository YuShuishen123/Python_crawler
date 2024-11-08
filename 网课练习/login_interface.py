import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path
import os

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("电影数据管理系统")
        self.root.geometry("400x500")
        
        # 设置窗口背景颜色
        self.root.configure(bg="#f0f0f0")
        
        # 创建主框架
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # 添加标题
        title_label = tk.Label(
            self.main_frame,
            text="欢迎登录",
            font=("微软雅黑", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=20)
        
        # 用户名输入框
        self.username_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.username_frame.pack(fill="x", pady=10)
        
        self.username_entry = ttk.Entry(
            self.username_frame,
            font=("微软雅黑", 12),
            width=25
        )
        self.username_entry.insert(0, "用户名")
        self.username_entry.bind("<FocusIn>", lambda e: self.on_entry_click(e, "用户名"))
        self.username_entry.bind("<FocusOut>", lambda e: self.on_focus_out(e, "用户名"))
        self.username_entry.pack()
        
        # 密码输入框
        self.password_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.password_frame.pack(fill="x", pady=10)
        
        self.password_entry = ttk.Entry(
            self.password_frame,
            font=("微软雅黑", 12),
            width=25,
            show="*"
        )
        self.password_entry.insert(0, "密码")
        self.password_entry.bind("<FocusIn>", lambda e: self.on_entry_click(e, "密码"))
        self.password_entry.bind("<FocusOut>", lambda e: self.on_focus_out(e, "密码"))
        self.password_entry.pack()
        
        # 登录按钮
        style = ttk.Style()
        style.configure("Custom.TButton", 
                       padding=10, 
                       font=("微软雅黑", 12))
        
        self.login_button = ttk.Button(
            self.main_frame,
            text="登录",
            style="Custom.TButton",
            command=self.login
        )
        self.login_button.pack(pady=20)
        
        # 注册链接
        self.register_label = tk.Label(
            self.main_frame,
            text="还没有账号？点击注册",
            font=("微软雅黑", 10),
            bg="#f0f0f0",
            fg="#0066cc",
            cursor="hand2"
        )
        self.register_label.pack(pady=10)
        self.register_label.bind("<Button-1>", self.show_register)
        
        # 加载用户数据
        self.users_file = Path("users.json")
        self.load_users()
        
        self.root.mainloop()
    
    def load_users(self):
        if self.users_file.exists():
            with open(self.users_file, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        else:
            self.users = {}
            self.save_users()
    
    def save_users(self):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)
    
    def on_entry_click(self, event, default_text):
        if event.widget.get() == default_text:
            event.widget.delete(0, "end")
            if default_text == "密码":
                event.widget.config(show="*")
    
    def on_focus_out(self, event, default_text):
        if event.widget.get() == "":
            event.widget.insert(0, default_text)
            if default_text == "密码":
                event.widget.config(show="")
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in ["用户名", ""] or password in ["密码", ""]:
            messagebox.showerror("错误", "请输入用户名和密码")
            return
        
        if username in self.users and self.users[username] == password:
            messagebox.showinfo("成功", "登录成功！")
            self.root.destroy()
            # 这里可以添加登录成功后的操作
        else:
            messagebox.showerror("错误", "用户名或密码错误")
    
    def show_register(self, event=None):
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("注册新用户")
        self.register_window.geometry("300x400")
        self.register_window.configure(bg="#f0f0f0")
        
        # 注册界面的组件
        title_label = tk.Label(
            self.register_window,
            text="用户注册",
            font=("微软雅黑", 18, "bold"),
            bg="#f0f0f0"
        )
        title_label.pack(pady=20)
        
        # 用户名输入
        self.reg_username = ttk.Entry(
            self.register_window,
            font=("微软雅黑", 12),
            width=20
        )
        self.reg_username.insert(0, "用户名")
        self.reg_username.pack(pady=10)
        
        # 密码输入
        self.reg_password = ttk.Entry(
            self.register_window,
            font=("微软雅黑", 12),
            width=20,
            show="*"
        )
        self.reg_password.insert(0, "密码")
        self.reg_password.pack(pady=10)
        
        # 确认密码
        self.reg_confirm = ttk.Entry(
            self.register_window,
            font=("微软雅黑", 12),
            width=20,
            show="*"
        )
        self.reg_confirm.insert(0, "确认密码")
        self.reg_confirm.pack(pady=10)
        
        # 注册按钮
        register_button = ttk.Button(
            self.register_window,
            text="注册",
            style="Custom.TButton",
            command=self.register
        )
        register_button.pack(pady=20)
    
    def register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        
        if username in ["用户名", ""] or password in ["密码", ""] or confirm in ["确认密码", ""]:
            messagebox.showerror("错误", "请填写所有字段")
            return
        
        if password != confirm:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return
        
        if username in self.users:
            messagebox.showerror("错误", "用户名已存在")
            return
        
        self.users[username] = password
        self.save_users()
        messagebox.showinfo("成功", "注册成功！")
        self.register_window.destroy()

if __name__ == "__main__":
    LoginWindow() 