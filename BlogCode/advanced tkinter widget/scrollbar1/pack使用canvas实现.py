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
            if self.cget("orient") == tk.HORIZONTAL:
                self.pack(fill=tk.X, side=tk.BOTTOM)
            else:
                self.pack(fill=tk.Y, side=tk.RIGHT)
        ttk.Scrollbar.set(self,upper,lower)
        
    def grid(self, **kw): #
        raise AttributeError("{} has no attribute {}".format(AutoHideScrollbar.__name__, "'grid'"))
    def place(self, **kw):
        raise AttributeError("{} has no attribute {}".format(AutoHideScrollbar.__name__, "'place'"))


if __name__ == '__main__':
    
    root = tk.Tk()
    vscrollbar = AutoHideScrollbar(root)
    canvas = tk.Canvas(root, yscrollcommand=vscrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    vscrollbar.config(command=canvas.yview)
    
    #Creating the frame its contents
    frame = tk.Frame(canvas)
    test_text = tk.Text(frame, wrap=tk.NONE)
    test_text.pack(fill=tk.BOTH, expand=True)
    test_text.insert(tk.END, "This is tkinter or Tkinter!\n"*26)
    # label = tk.Label(frame, text="text", font=("Arial", "512"))
    # label.pack()
    
    #Stuff that I don't quite understand
    canvas.create_window(0, 0, anchor=tk.NW, window=frame)
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    root.mainloop()