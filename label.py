import tkinter as tk
from PIL import Image, ImageTk
import os, sys


class LabelingApp:
    def __init__(self, dataset_name, dataset_path, file_name, class_name):
        self.dataset_name = dataset_name
        self.dataset_path = dataset_path
        self.file_name = file_name
        self.class_name = class_name

        self.root = tk.Tk()
        self.root.title("Labeling Tool")
        self.root.resizable(True, False)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.image = Image.open(
            # os.path.join(self.dataset_path, self.file_name + ".jpg")
            "dataset\\20230828_155817.jpg"
        )
        self.image_ratio = self.image.width / self.image.height

        self.tk_image = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_height * 0.75 * self.image_ratio,
            height=self.screen_height * 0.75,
        )
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.image_item = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.tk_image
        )

        self.lines = []
        self.coords = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}

        self.rect = self.canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)

        self.new_image = None

        self.canvas.bind("<Configure>", self.fit_image)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.root.bind("a", self.undo)
        self.root.bind("<space>", self.save)

    # TODO: implement next_image
    def next_image(self, event):
        pass

    def fit_image(self, event):
        canvas_width = event.width
        canvas_height = int(canvas_width / self.image_ratio)
        scaling_factor = canvas_width / self.image.width
        self.root.geometry(f"{canvas_width}x{canvas_height}")

        new_width = int(self.image.width * scaling_factor)
        new_height = int(self.image.height * scaling_factor)
        resized_image = self.image.resize((new_width, new_height))
        self.new_image = ImageTk.PhotoImage(resized_image)

        self.canvas.itemconfig(self.image_item, image=self.new_image)

    def click(self, event):
        self.coords["x1"] = event.x
        self.coords["y1"] = event.y

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

    def save(self, event):
        if len(self.lines) == 4:
            path = os.path.join(self.dataset_path, self.file_name + ".txt")
            with open(path, "w") as f:
                f.write(
                    f"{self.class_name} {' '.join(str(c) for c in self.xywh_rect_coords())}\n"
                )
                f.close()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # TODO: remove hardcoded paths and names
    DATASET_NAME = "test"
    FILE_NAME = "test_file"
    CLASS_NAME = 0

    if len(sys.argv) < 2:
        DATASET_PATH = os.path.join(os.getcwd(), "dataset")
    else:
        DATASET_PATH = sys.argv[1]

    app = LabelingApp(DATASET_NAME, DATASET_PATH, FILE_NAME, CLASS_NAME)
    app.run()
