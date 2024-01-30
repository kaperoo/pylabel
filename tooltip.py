import tkinter as tk


class Tooltip(tk.Toplevel):
    def __init__(self, x, y):
        super().__init__()
        self.title("Tooltip")
        self.resizable(False, False)
        self.geometry(f"300x400+{x}+{y}")

        # TODO: remove hardcoded classes
        self.classes = [
            "0: class1",
            "1: class2",
            "2: class3",
            "3: class4",
            "4: class5",
            "5: class6",
            "6: class7",
            "7: class8",
            "8: class9",
            "9: class10",
            "10: class11",
            "11: class12",
            "12: class13",
            "13: class14",
            "14: class15",
            "15: class16",
            "16: class17",
            "17: class18",
            "18: class19",
            "19: class20",
            "20: class21",
            "21: class22",
            "22: class23",
            "23: class24",
            "24: class25",
            "25: class26",
            "26: class27",
            "27: class28",
            "28: class29",
            "29: class30",
            "30: class31",
        ]

        self.listbox = tk.Listbox(self)

        for i in self.classes:
            self.listbox.insert(tk.END, i)

        self.listbox.pack(expand=True, fill=tk.BOTH)

        self.listbox.bind("<<ListboxSelect>>", self.select_class)

    def update_text(self, text):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.see(int(text))
        self.listbox.selection_set(int(text))

    def select_class(self, event):
        pass
