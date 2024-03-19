import tkinter as tk


class Tooltip(tk.Toplevel):
    def __init__(self, x, y, get_classes, set_class, new_class):
        super().__init__()
        self.title("Tooltip")
        self.resizable(False, False)
        self.geometry(f"300x400+{x}+{y}")

        self.set_class = set_class
        self.new_class = new_class

        self.search_entry = tk.Entry(self)
        self.search_entry.pack(fill=tk.X)

        self.classes = get_classes()
        self.listbox = tk.Listbox(self)

        for i, v in self.classes.items():
            self.listbox.insert(tk.END, f"{i}: {v}")

        self.listbox.pack(expand=True, fill=tk.BOTH)

        self.listbox.bind("<<ListboxSelect>>", self.select_class)
        self.search_entry.bind("<KeyRelease>", self.search)

        self.new_class_button = tk.Button(
            self, text="New Class", command=lambda: self.new_class()
        )
        self.new_class_button.pack(fill=tk.X)

    def update_classes(self, classes):
        # TODO: see if clearing the listbox is necessary
        self.listbox.delete(0, tk.END)
        for i, v in classes.items():
            self.listbox.insert(tk.END, f"{i}: {v}")

    def update_selection(self, text):
        self.listbox.selection_clear(0, tk.END)
        self.listbox.see(int(text))
        self.listbox.selection_set(int(text))

    def select_class(self, event):
        if event.widget.curselection():
            self.set_class(event.widget.curselection()[0])

    def search(self, event):
        search = self.search_entry.get()
        if not search:
            self.listbox.selection_clear(0, tk.END)
            return
        for i, v in self.classes.items():
            if search.lower() in v.lower():
                self.listbox.selection_clear(0, tk.END)
                self.listbox.see(int(i))
                self.listbox.selection_set(int(i))
                break

    def focus_entry(self, event):
        self.search_entry.focus()
