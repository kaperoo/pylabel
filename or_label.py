import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageCanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Canvas App")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.image_path = None
        self.image = None

        self.load_image_button = tk.Button(
            root, text="Load Image", command=self.load_image
        )
        self.load_image_button.pack()

    def load_image(self):
        self.image_path = filedialog.askopenfilename(
            title="Select an image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )

        if self.image_path:
            self.image = Image.open(self.image_path)
            self.display_image()

    def display_image(self):
        if self.image:
            # Resize the image to fit the canvas
            width, height = self.image.size
            self.canvas.config(width=width, height=height)

            # Convert PIL Image to Tkinter PhotoImage
            tk_image = ImageTk.PhotoImage(self.image)

            # Display the image on the canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
            self.canvas.image = tk_image  # Keep a reference to avoid garbage collection


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCanvasApp(root)
    root.mainloop()
