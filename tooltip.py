import tkinter as tk


class Tooltip(tk.Toplevel):
    def __init__(self, x, y, master, get_classes):
        super().__init__()
        self.title("Tooltip")
        self.resizable(False, False)
        self.geometry(f"300x400+{x}+{y}")
        self.master = master

        # TODO: remove hardcoded classes
        self.classes = get_classes()
        self.listbox = tk.Listbox(self)

        for i, v in self.classes.items():
            self.listbox.insert(tk.END, f"{i}: {v}")

        self.listbox.pack(expand=True, fill=tk.BOTH)

        self.listbox.bind("<<ListboxSelect>>", self.select_class)

    def update_text(self, text):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.see(int(text))
        self.listbox.selection_set(int(text))

    def select_class(self, event):
        pass
