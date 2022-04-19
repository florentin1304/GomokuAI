import tkinter as tk

class OptionsWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # container = tk.Frame(self)
        # container.pack(side="top", fill="both", expand=True)

a = OptionsWindow()
a.mainloop()
