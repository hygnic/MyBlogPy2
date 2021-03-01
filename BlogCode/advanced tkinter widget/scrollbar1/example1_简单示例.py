# -*- coding:utf-8 -*-
# Date: 2020/3/13

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    import ttk
except ImportError:
    import tkinter.ttk as ttk
    
root = tk.Tk()
root.geometry("200x300+500+600")

hscrollbar = ttk.Scrollbar(root)
hscrollbar.pack(side=tk.RIGHT, fill="y")
test_text = tk.Text(root, wrap=tk.NONE, yscrollcommand=hscrollbar.set)
test_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
test_text.insert(tk.END, "This is tkinter or Tkinter!\n"*50)
hscrollbar.config(command=test_text.yview)

root.mainloop()