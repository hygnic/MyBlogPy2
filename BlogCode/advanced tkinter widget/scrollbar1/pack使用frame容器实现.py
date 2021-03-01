# -*- coding:utf-8 -*-

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    import ttk
except ImportError:
    import tkinter.ttk as ttk

class AutoHideScrollbar(ttk.Scrollbar):
    def set(self,upper,lower):
        if float(upper) <= 0.0 and float(lower) >= 1.0:
            self.pack_forget()
        else:
            self.pack(side="right", fill="y")
        ttk.Scrollbar.set(self,upper,lower)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("200x300+500+600")
    
    frame = tk.Frame(root) # 用于放置scrollbar组件
    frame.pack(side="right", fill="y")

    vscrollbar = AutoHideScrollbar(frame)
    vscrollbar.pack(side=tk.RIGHT, fill="y")
    test_text = tk.Text(root, wrap=tk.NONE, yscrollcommand=vscrollbar.set)
    test_text.pack(fill=tk.BOTH, expand=True)
    vscrollbar.config(command=test_text.yview)
    test_text.insert(tk.END, "This is tkinter or Tkinter!\n"*26)
    
    
    root.mainloop()
