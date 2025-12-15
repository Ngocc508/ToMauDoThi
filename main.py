import tkinter as tk
from gui_app import GraphColoringApp

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    app = GraphColoringApp(root)
    root.mainloop()