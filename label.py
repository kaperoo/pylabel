import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tooltip import Tooltip
from utils import *
import os, sys


class LabelingApp:
    def __init__(self, dataset_path):
        if dataset_path is None:
            self.dataset_path = self.load_folder()
        else:
            self.dataset_path = dataset_path

        check_dir_tree(self.dataset_path, level=1)

        self.root = tk.Tk()
        self.root.title("Labeling Tool")

        # self.root.resizable(True, False)
        # TODO: fix resizing
        self.root.resizable(False, False)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.image_ratio = 1

        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_height * 0.75 * self.image_ratio,
            height=self.screen_height * 0.75,
        )
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.image = None
        self.tk_image = None
        self.image_item = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.tk_image
        )

        self.classes = get_classes(os.path.join(self.dataset_path, "dataset.yaml"))
        self.class_name = 0
        self.file_name = ""
        self.lines = []
        self.hover_line = None
        self.coords = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}
        self.rect = self.canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)
        self.str_var = tk.StringVar()
        self.displayed_label = tk.Label(
            self.root, textvariable=self.str_var, bg="red", fg="white"
        )

        self.tog_tool = False
        self.tool_window = None

        self.new_class_window = None

        self.next_image(None)

        self.canvas.bind("<Configure>", self.fit_image)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Motion>", self.hover)
        self.root.bind("a", self.undo)
        self.root.bind("u", self.toggle_tooltip)
        self.root.bind("n", self.new_class)
        self.root.bind("<space>", self.save)
        for i in range(10):
            self.root.bind(str(i), self.select_class)

    def load_folder(self):
        # TODO: figure out a way to get relative path
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            return folder_selected
        else:
            sys.exit()

    # TODO: improve this implementation
    def next_image(self, event):
        for file in os.listdir(self.dataset_path):
            if file.endswith(".jpg"):
                self.canvas.coords(self.rect, 0, 0, 0, 0)
                for i in self.lines:
                    self.canvas.delete(i)
                self.lines = []
                self.coords = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}

                self.displayed_label.place_forget()

                self.file_name = file[:-4]
                self.image = Image.open(
                    os.path.join(self.dataset_path, self.file_name + ".jpg")
                )
                self.image_ratio = self.image.width / self.image.height

                scaling_factor = self.screen_height * 0.75 / self.image.height

                new_width = int(self.image.width * scaling_factor)
                new_height = int(self.image.height * scaling_factor)

                resized_image = self.image.resize((new_width, new_height))

                self.tk_image = ImageTk.PhotoImage(resized_image)

                self.canvas.itemconfig(self.image_item, image=self.tk_image)

                self.canvas.config(
                    width=self.screen_height * 0.75 * self.image_ratio,
                    height=self.screen_height * 0.75,
                )
                self.root.geometry(f"{int(new_width)}x{int(new_height)}")

                return

    def fit_image(self, event):
        canvas_width = event.width
        canvas_height = int(canvas_width / self.image_ratio)
        scaling_factor = canvas_width / self.image.width
        self.root.geometry(f"{canvas_width}x{canvas_height}")

        resized_image = self.image.resize(
            (
                int(self.image.width * scaling_factor),
                int(self.image.height * scaling_factor),
            )
        )
        self.tk_image = ImageTk.PhotoImage(resized_image)

        self.canvas.itemconfig(self.image_item, image=self.tk_image)

    def hover(self, event):
        if self.hover_line:
            self.canvas.delete(self.hover_line)
        if len(self.lines) != 4:
            if len(self.lines) % 2 == 0:
                self.hover_line = self.canvas.create_line(
                    0,
                    event.y,
                    self.canvas.winfo_width(),
                    event.y,
                    fill="lawn green",
                    width=2,
                    stipple="gray25",
                )
            else:
                self.hover_line = self.canvas.create_line(
                    event.x,
                    0,
                    event.x,
                    self.canvas.winfo_height(),
                    fill="lawn green",
                    width=2,
                    stipple="gray25",
                )

    def click(self, event):
        self.coords["x1"] = event.x
        self.coords["y1"] = event.y

        if self.hover_line:
            self.canvas.delete(self.hover_line)

        if len(self.lines) != 4:
            if len(self.lines) % 2 == 0:
                self.lines.append(
                    self.canvas.create_line(
                        0,
                        self.coords["y1"],
                        self.canvas.winfo_width(),
                        self.coords["y1"],
                        fill="lawn green",
                        width=2,
                    )
                )
            else:
                self.lines.append(
                    self.canvas.create_line(
                        self.coords["x1"],
                        0,
                        self.coords["x1"],
                        self.canvas.winfo_height(),
                        fill="lawn green",
                        width=2,
                    )
                )

        if len(self.lines) == 4:
            self.canvas.coords(self.rect, self.rect_coords())
            self.canvas.tag_raise(self.rect)
            # show label below rectangle
            self.displayed_label.place(
                x=self.canvas.coords(self.rect)[0],
                y=self.canvas.coords(self.rect)[3],
                anchor=tk.NW,
            )

    def drag(self, event):
        self.coords["x2"] = event.x
        self.coords["y2"] = event.y

        if len(self.lines) % 2 != 0:
            self.canvas.coords(
                self.lines[-1],
                0,
                self.coords["y2"],
                self.canvas.winfo_width(),
                self.coords["y2"],
            )
        else:
            self.canvas.coords(
                self.lines[-1],
                self.coords["x2"],
                0,
                self.coords["x2"],
                self.canvas.winfo_height(),
            )

        if len(self.lines) == 4:
            self.canvas.coords(self.rect, self.rect_coords())
            self.canvas.tag_raise(self.rect)
            self.displayed_label.place(
                x=self.canvas.coords(self.rect)[0],
                y=self.canvas.coords(self.rect)[3],
                anchor=tk.NW,
            )

    def undo(self, event):
        if len(self.lines) == 4:
            self.canvas.coords(self.rect, 0, 0, 0, 0)
        if len(self.lines) > 0:
            self.canvas.delete(self.lines[-1])
            self.lines.pop()

    def rect_coords(self):
        y1 = self.canvas.coords(self.lines[0])[1]
        x1 = self.canvas.coords(self.lines[1])[2]
        y2 = self.canvas.coords(self.lines[2])[1]
        x2 = self.canvas.coords(self.lines[3])[2]
        return x1, y1, x2, y2

    def xywh_rect_coords(self):
        n_coords = []
        x1, y1, x2, y2 = self.rect_coords()
        n_coords.append((x1 + x2) / (2 * self.canvas.winfo_width()))
        n_coords.append((y1 + y2) / (2 * self.canvas.winfo_height()))
        n_coords.append(abs(x1 - x2) / self.canvas.winfo_width())
        n_coords.append(abs(y1 - y2) / self.canvas.winfo_height())
        return n_coords

    # TODO: implement class selection
    def select_class(self, event):
        self.class_name = int(event.char)
        if len(self.classes) > self.class_name:
            if self.tool_window:
                self.tool_window.update_text(self.class_name)
            self.str_var.set(self.classes[self.class_name])

    # TODO: implement new class creation
    def new_class(self, event):
        pass

    def get_classes(self):
        return self.classes

    def save(self, event):
        if len(self.lines) == 4:
            path = os.path.join(self.dataset_path, "labels", self.file_name + ".txt")
            with open(path, "w") as f:
                f.write(
                    f"{self.class_name} {' '.join(str(c) for c in self.xywh_rect_coords())}\n"
                )
                f.close()

            # move image to 'images' folder
            os.rename(
                os.path.join(self.dataset_path, self.file_name + ".jpg"),
                os.path.join(self.dataset_path, "images", self.file_name + ".jpg"),
            )
            self.next_image(event)

    def toggle_tooltip(self, event):
        if self.tog_tool:
            self.tool_window.destroy()
            self.tog_tool = False
        else:
            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()
            self.tool_window = Tooltip(
                x, y, self.root, self.get_classes, self.select_class
            )
            self.tog_tool = True

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        DATASET_PATH = sys.argv[1]
    else:
        DATASET_PATH = None

    app = LabelingApp(DATASET_PATH)
    app.run()
