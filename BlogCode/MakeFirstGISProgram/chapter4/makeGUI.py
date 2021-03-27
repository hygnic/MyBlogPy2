# -*- coding:utf-8 -*-

import Tkinter as tk
import tkFileDialog
import giscode ###

class MyGUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("450x600+800+200") #设置窗口大小、位置
        self.root.title("GIS") #设置程序名称
        self.var = tk.StringVar()
        
        # run function
        self.create_widget()
        self.create_run_button()
        self.root.mainloop() # 执行循环

    def create_widget(self):
        self.frame1 = tk.Frame(self.root, relief="raised", bd=3)
        self.frame1.pack(fill="x")
        self.entry = tk.Entry(self.frame1)
        self.entry.config(textvariable=self.var) #<<注释2>>
        self.entry.pack(side="left",expand=True,
                        fill="x", pady=8, padx=10)
        self.but = tk.Button(self.frame1, text=u"输入线要素",
                            relief="groove", width=10)
        self.but.config(command=self.open_dialog)
        self.but.pack(side="right", pady=8)
    
    def open_dialog(self):
        varrr = tkFileDialog.askopenfilename()
        self.var.set(varrr)
        
    def create_run_button(self):
        # 生成下方的“运行”按钮
        self.bottom_frame = tk.Frame(self.root,relief="raised",bd=3)
        self.bottom_frame.pack(side="bottom",fill="x",anchor="s")
        self.ok_button =tk.Button(
            self.bottom_frame,text=u"运行",relief="groove", width=10)
        self.ok_button.pack(side="right", pady=8)
        self.ok_button.config(command=self.run)
    
    def run(self):
        giscode.main(self.var.get())
        
        
if __name__ == '__main__':
    MyGUI()