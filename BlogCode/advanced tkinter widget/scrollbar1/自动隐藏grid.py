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
    def set(self,upper,lower):  # ❶
        if float(upper) <= 0.0 and float(lower) >= 1.0:
            self.grid_remove() # ❷
        else:
            self.grid()
        ttk.Scrollbar.set(self,upper,lower)
    
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("200x300+500+600")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    yscrollbar = AutoHideScrollbar(root)
    yscrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)
    
    test_text = tk.Text(root, wrap=tk.NONE, yscrollcommand=yscrollbar.set)
    test_text.grid(row=0, column=0, sticky=tk.N + tk.E + tk.W + tk.S)
    test_text.insert(tk.END, "This is tkinter or Tkinter!\n"*26)
    yscrollbar.config(command=test_text.yview)
    root.mainloop()
