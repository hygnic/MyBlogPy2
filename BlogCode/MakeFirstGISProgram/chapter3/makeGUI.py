# -*- coding:utf-8 -*-

import Tkinter as tk

class MyGUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("450x600+800+200") # 设置程序窗口大小和打开位置
        self.root.title("GIS") # 设置程序名称
        self.create_widget()
        self.create_run_button()
        self.root.mainloop() # 执行循环

    def create_widget(self):
        self.frame1 = tk.Frame(self.root, relief="raised", bd=3)
        self.frame1.pack(fill="x")
        self.entry = tk.Entry(self.frame1)
        self.entry.pack(side="left",expand=True, fill="x", pady=8, padx=10)
        self.but = tk.Button(
            self.frame1, text=u"输入线要素", relief="groove", width=10)
        self.but.pack(side="right", pady=8)
        
    def create_run_button(self):
        # 生成下方的“运行”按钮
        self.bottom_frame = tk.Frame(self.root,relief="raised",bd=3)
        self.bottom_frame.pack(side="bottom",fill="x",anchor="s")
        self.ok_button =tk.Button(
            self.bottom_frame,text=u"运行",relief="groove", width=10)
        self.ok_button.pack(side="right", pady=8)
        
        
if __name__ == '__main__':
    MyGUI()