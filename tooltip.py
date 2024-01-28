import tkinter as tk


class Tooltip(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Tooltip")
        self.resizable(False, False)
        self.geometry("300x400")

        self.class_text = tk.StringVar()
        self.label = tk.Label(self, text=self.class_text).pack()
