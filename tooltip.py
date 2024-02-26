import tkinter as tk


class Tooltip(tk.Toplevel):
    def __init__(self, x, y, master, get_classes, set_class):
        super().__init__()
        self.title("Tooltip")
        self.resizable(False, False)
        self.geometry(f"300x400+{x}+{y}")
        self.master = master

        self.set_class = set_class

        self.search_entry = tk.Entry(self)
        self.search_entry.pack(fill=tk.X)

        self.classes = get_classes()
        self.listbox = tk.Listbox(self)

        for i, v in self.classes.items():
            self.listbox.insert(tk.END, f"{i}: {v}")

        self.listbox.pack(expand=True, fill=tk.BOTH)

        self.listbox.bind("<<ListboxSelect>>", self.select_class)

        # self.new_class_button = tk.Button(self, text="Add a New Class", command=self.new_class)

    def update_text(self, text):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.see(int(text))
        self.listbox.selection_set(int(text))

    def select_class(self, event):
        if event.widget.curselection():
            self.set_class(event.widget.curselection()[0])
            print(event.widget.curselection()[0])

    def search(self, event):
        pass
