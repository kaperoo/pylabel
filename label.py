import tkinter as tk
from PIL import Image, ImageTk


def fit_image(event):
    global new_image
    canvas_width = event.width
    canvas_height = int(canvas_width / image_ratio)
    scaling_factor = canvas_width / image.width
    root.geometry(f"{canvas_width}x{canvas_height}")

    # Resize the image
    new_width = int(image.width * scaling_factor)
    new_height = int(image.height * scaling_factor)
    resized_image = image.resize((new_width, new_height))
    new_image = ImageTk.PhotoImage(resized_image)

    # update the canvas image
    canvas.itemconfig(image_item, image=new_image)


def click(event):
    coords["x1"] = event.x
    coords["y1"] = event.y

    if len(lines) != 4:
        if len(lines) % 2 == 0:
            lines.append(
                canvas.create_line(
                    0,
                    coords["y1"],
                    canvas.winfo_width(),
                    coords["y1"],
                    fill="lawn green",
                    width=2,
                )
            )
        else:
            lines.append(
                canvas.create_line(
                    coords["x1"],
                    0,
                    coords["x1"],
                    canvas.winfo_height(),
                    fill="lawn green",
                    width=2,
                )
            )

    if len(lines) == 4:
        canvas.coords(rect, rect_coords())
        canvas.tag_raise(rect)


def drag(event):
    coords["x2"] = event.x
    coords["y2"] = event.y

    if len(lines) % 2 != 0:
        canvas.coords(lines[-1], 0, coords["y2"], canvas.winfo_width(), coords["y2"])
    else:
        canvas.coords(lines[-1], coords["x2"], 0, coords["x2"], canvas.winfo_height())

    if len(lines) == 4:
        canvas.coords(rect, rect_coords())
        canvas.tag_raise(rect)
        print(normalised_rect_coords())


def undo(event):
    if len(lines) == 4:
        canvas.coords(rect, 0, 0, 0, 0)
    if len(lines) > 0:
        canvas.delete(lines[-1])
        lines.pop()


def rect_coords():
    # get the 4 intersection points
    y1 = canvas.coords(lines[0])[1]
    x1 = canvas.coords(lines[1])[2]
    y2 = canvas.coords(lines[2])[1]
    x2 = canvas.coords(lines[3])[2]
    return x1, y1, x2, y2


def normalised_rect_coords():
    n_coords = []
    for i, c in enumerate(rect_coords()):
        if i % 2 == 0:
            n_coords.append(c / canvas.winfo_width())
        else:
            n_coords.append(c / canvas.winfo_height())
    return n_coords


def save(event):
    if len(lines) == 4:
        with open("labels.csv", "a") as f:
            f.write(f"test_name,{','.join(str(c) for c in normalised_rect_coords())}\n")
            f.close()


# Main window
root = tk.Tk()
root.title("Labeling Tool")

root.resizable(True, False)

# screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# load image
image = Image.open("20230828_155817.jpg")
image_ratio = image.width / image.height

tk_image = ImageTk.PhotoImage(image)

# canvas
canvas = tk.Canvas(
    root, width=screen_height * 0.75 * image_ratio, height=screen_height * 0.75
)
canvas.pack(expand=tk.YES, fill=tk.BOTH)

# canvas image
image_item = canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)

lines = []
coords = {"x1": 0, "y1": 0, "x2": 0, "y2": 0}

# rectangle
rect = canvas.create_rectangle(0, 0, 0, 0, outline="red", width=2)

new_image = None

# bind events
canvas.bind("<Configure>", fit_image)
canvas.bind("<Button-1>", click)
canvas.bind("<B1-Motion>", drag)
root.bind("a", undo)
root.bind("<space>", save)

root.mainloop()
