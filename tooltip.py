import tkinter as tk


class Tooltip(tk.Toplevel):
    def __init__(self, x, y):
        super().__init__()
        self.title("Tooltip")
        self.resizable(False, False)
        self.geometry(f"300x400+{x}+{y}")

        #TODO: remove hardcoded classes
        self.classes = ['0: class1', '1: class2', '2: class3', '3: class4', '4: class5', '5: class6', '6: class7', '7: class8', '8: class9', '9: class10', '10: class11', '11: class12', '12: class13', '13: class14', '14: class15', '15: class16', '16: class17', '17: class18', '18: class19', '19: class20', '20: class21', '21: class22', '22: class23', '23: class24', '24: class25', '25: class26', '26: class27', '27: class28', '28: class29', '29: class30', '30: class31', '31: class32', '32: class33', '33: class34', '34: class35', '35: class36', '36: class37', '37: class38', '38: class39', '39: class40', '40: class41', '41: class42', '42: class43', '43: class44', '44: class45', '45: class46', '46: class47', '47: class48', '48: class49', '49: class50', '50: class51', '51: class52', '52: class53', '53: class54', '54: class55', '55: class56', '56: class57', '57: class58', '58: class59', '59: class60', '60: class61', '61: class62', '62: class63', '63: class64', '64: class65', '65: class66', '66: class67', '67: class68', '68: class69', '69: class70', '70: class71', '71: class72', '72: class73', '73: class74', '74: class75', '75: class76', '76: class77', '77: class78', '78: class79', '79: class80', '80: class81', '81: class82', '82: class83', '83: class84', '84: class85', '85: class86']

        self.search = tk.Entry(self).pack()

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
