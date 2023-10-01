import tkinter as tk
from tkinter import filedialog, Menu, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MarkMyPic")
        self.root.geometry("1080x1920")

        # create a menubar
        menubar = Menu(root)
        root.config(menu=menubar)
        file_menu = Menu(menubar, tearoff=False)
        file_menu.add_command(
            label='Exit',
            command=root.destroy
        )

        # add the File menu to the menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        # global variables to store the watermark options
        self.font = None
        self.font_size = None
        self.font_color = None
        self.position = None
        self.opacity = None
        self.rotation = None
        self.padding = None
        self.outline = None

        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, width=720, height=480)
        self.canvas.pack(side=tk.LEFT)

        # Create a frame for options
        self.options_frame = tk.Frame(root)
        self.options_frame.pack(side=tk.RIGHT, padx=20)

        # Load Image Button
        self.load_button = tk.Button(self.options_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        # Watermark Text Entry
        self.watermark_label = tk.Label(self.options_frame, text="Watermark Text:")
        self.watermark_label.pack()
        self.watermark_entry = tk.Entry(self.options_frame)
        self.watermark_entry.pack(pady=10)

        # open settings Button
        self.watermark_button = tk.Button(self.options_frame, text="Open Settings", command=self.open_settings)
        self.watermark_button.pack()

        # Apply Watermark Button
        self.watermark_button = tk.Button(self.options_frame, text="Apply Watermark", command=self.apply_watermark)
        self.watermark_button.pack()

        # Download Image Button
        self.download_button = tk.Button(self.options_frame, text="Download Image", command=self.download_image,
                                         state=tk.DISABLED)
        self.download_button.pack()

    def open_settings(self):
        # Create a new popup window
        popup = tk.Toplevel(self.root)
        popup.title("Watermark Settings")
        popup.geometry("200x300")

        # Create and pack the option menus
        font = tk.StringVar()
        font.set("Select the font")
        font_size = tk.StringVar()
        font_size.set("font size")
        font_color = tk.StringVar()
        font_color.set("font color")
        position = tk.StringVar()
        position.set("Select the position")
        opacity = tk.StringVar()
        opacity.set("100")
        rotation = tk.StringVar()
        rotation.set("0")
        padding = tk.StringVar()
        padding.set("0")
        outline = tk.StringVar()
        outline.set("Select the outline")

        dropdown_font = tk.OptionMenu(popup, font, "Arial", "Times New Roman", "Courier New")
        dropdown_font.pack()
        font_size_label = tk.Label(popup, text="Font Size:")
        font_size_label.pack()
        font_size_entry = tk.Entry(popup, textvariable=font_size)
        font_size_entry.pack()

        font_color_label = tk.Label(popup, text="Font Color:")
        font_color_label.pack()
        font_color_entry = tk.Entry(popup, textvariable=font_color)
        font_color_entry.pack()

        opacity_label = tk.Label(popup, text="Opacity:")
        opacity_label.pack()
        opacity_entry = tk.Entry(popup, textvariable=opacity)
        opacity_entry.pack()

        rotation_label = tk.Label(popup, text="Rotation:")
        rotation_label.pack()
        rotation_entry = tk.Entry(popup, textvariable=rotation)
        rotation_entry.pack()

        padding_label = tk.Label(popup, text="Padding:")
        padding_label.pack()
        padding_entry = tk.Entry(popup, textvariable=padding)
        padding_entry.pack()
        dropdown_position = tk.OptionMenu(popup, position, "Top Left", "Top Right", "Bottom Left", "Bottom Right")
        dropdown_position.pack()

        # Create a submit button to submit values
        submit_button = ttk.Button(popup, text="Submit",
                                   command=lambda: self.submit_settings(popup, font, font_size, font_color, position,
                                                                        opacity, rotation, padding, outline))
        submit_button.pack()

    def submit_settings(self, popup, font, font_size, font_color, position, opacity, rotation, padding, outline):
        # Retrieve the selected values and do something with them
        self.font = font.get()
        self.font_size = int(font_size.get())
        self.font_color = font_color.get()
        self.position = position.get()
        self.opacity = opacity.get()
        self.rotation = rotation.get()
        self.padding = padding.get()
        self.outline = outline.get()

        # Close the popup window
        popup.destroy()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

    def display_image(self):
        if hasattr(self, 'image'):
            img_width, img_height = self.image.size
            canvas_width, canvas_height = 720, 480  # Set your desired canvas size

            # Calculate the scaling factors for width and height
            scale_x = canvas_width / img_width
            scale_y = canvas_height / img_height

            # Choose the smaller scaling factor to fit the image within the canvas
            scale = min(scale_x, scale_y)

            # Calculate the new image size to fit within the canvas
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)

            # Resize the image
            resized_image = self.image.resize((new_width, new_height))

            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.image = self.tk_image

            # Configure canvas size to match the resized image size
            self.canvas.config(width=new_width, height=new_height)

            # Center the image on the canvas
            canvas_x = (canvas_width - new_width) // 2
            canvas_y = (canvas_height - new_height) // 2
            self.canvas.move(self.tk_image, canvas_x, canvas_y)

    def apply_watermark(self):
        """ Apply the watermark to the image """
        if hasattr(self, 'image'):
            # Create a transparent layer the size of the image and draw the watermark on it
            watermark = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(watermark)

            # Get the font and size
            font = ImageFont.truetype("arial.ttf", int(self.font_size))
            text = self.watermark_entry.get()

            # Get the bounding box of the text
            text_bbox = draw.textbbox((0, 0), text, font=font)

            # Calculate the text width and height from the bounding box
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Calculate the position for the watermark (e.g., bottom right with some padding)
            padding = int(self.padding) if self.padding else 0  # Adjust this value as needed
            position = "Center"
            if self.position == "Top Left":
                position = (0 + padding, 0 + padding)
            elif self.position == "Top Right":
                position = (self.image.size[0] - text_width - padding, 0 + padding)
            elif self.position == "Bottom Left":
                position = (0 + padding, self.image.size[1] - text_height - padding)
            elif self.position == "Bottom Right":
                position = (self.image.size[0] - text_width - padding, self.image.size[1] - text_height - padding)
            else:
                # in the center if no choice is made
                position = ((self.image.size[0] - text_width) // 2, (self.image.size[1] - text_height) // 2)

            # Draw text on the transparent layer
            draw.text(position, text, fill=self.font_color, font=font)

            # Rotate the text (you can adjust the rotation angle as needed)
            if self.rotation:
                watermark = watermark.rotate(int(self.rotation), expand=True)

            # Paste the transparent layer on the image
            self.image.paste(watermark, (0, 0), watermark)
            # Replace the image in the canvas with the watermarked image
            self.display_image()

            # Enable the download button
            self.download_button.config(state=tk.NORMAL)

    def download_image(self):
        """ Download the watermarked image """
        if hasattr(self, 'image'):
            file_path = filedialog.asksaveasfile(filetypes=[("PNG", "*.png")])
            if file_path:
                self.image.save(file_path.name + ".png", format="PNG")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
