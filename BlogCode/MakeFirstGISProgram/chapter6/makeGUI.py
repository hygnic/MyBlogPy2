# -*- coding:utf-8 -*-

import Tkinter as tk
import tkFileDialog
from multiprocessing import Process
from ttkthemes import ThemedTk #<<注释1>>
import ttk #<<注释2>>
import giscode


class MyGUI(object):
    def __init__(self):
        # self.root = tk.Tk()
        self.root = ThemedTk(theme="arc") #<<注释3>>
        self.root.geometry("450x600+800+200")
        self.root.title("GIS") #设置程序名称
        self.var = tk.StringVar()

        self.img1 = tk.PhotoImage(file="icon/shp2.gif")
        self.img2 = tk.PhotoImage(file="icon/ok2.gif")
        
        # run function
        self.create_widget()
        self.create_run_button()
        self.root.mainloop() # 执行循环

    def create_widget(self):
        self.frame1 = ttk.Frame(self.root)
        self.frame1.pack(fill="x")
        self.entry = ttk.Entry(self.frame1) #<<注释4>>
        self.entry.config(textvariable=self.var)
        self.entry.pack(
            side="left",expand=True, fill="x", pady=8, padx=10
        )
        self.but = tk.Button(self.frame1, relief="flat")
        # self.but = ttk.Button(self.frame1)
        self.but.config(command=self.open_dialog)
        self.but.config(image=self.img1)
        self.but.pack(side="right", pady=8, padx=6)
     
    def open_dialog(self):
        varrr = tkFileDialog.askopenfilename()
        self.var.set(varrr)
        
    def create_run_button(self):
        # 生成下方的“运行”按钮
        self.bottom_frame = ttk.Frame(self.root)
        self.bottom_frame.pack(side="bottom",fill="x",anchor="s")
        self.ok_button = tk.Button(self.bottom_frame, relief="flat")
        # self.ok_button = ttk.Button(self.bottom_frame)
        self.ok_button.pack(side="right", pady=8, padx=6)
        self.ok_button.config(image=self.img2)
        self.ok_button.config(command=self.run_multiprocessing)
    
    # def run(self):
    #     giscode.main(self.var.get())
    
    def run_multiprocessing(self):
        p = Process(target=giscode.main,
                    args=(self.var.get(),)
                    )
        p.start()
        print "PID:",p.pid
        
        
if __name__ == '__main__':
    MyGUI()