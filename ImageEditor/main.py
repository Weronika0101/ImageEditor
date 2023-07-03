import tkinter as tk
from tkinter import PhotoImage, filedialog, colorchooser, Scale, messagebox
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance
from tkinter import ttk

pen_color = "black"
pen_size = 5
file_path = ""
filter_bool = False
number = 1

class App(tk.Tk):
    def __init__(self,titl,size):

        #main setup
        super().__init__()
        self.title(titl)
        self.geometry(f'{size[0]}x{size[1]}')
        self.config(bg='white')

        #widgets
        self.canvas =Canvas(self, 750, 500)
        self.left_frame = LeftFrame(self,200, 600, 'white',self.canvas)
        self.top_frame = TopFrame(self, 750, 100, 'white',self.canvas)

        self.left_frame.pack(side="left", fill="y")
        self.canvas.pack()
        self.left_frame.create_widgets()

        #run
        self.mainloop()

class LeftFrame(tk.Frame):
    def __init__(self,parent,width,height,bg,canvas):
        super().__init__(parent)
        self.width=width
        self.height=height
        self.config(bg=bg)
        self.canvas = canvas

    def add_image(self):
        global file_path
        file_path = filedialog.askopenfilename()

        image = Image.open(file_path)
        width, height = int( image.width/2), int(image.height/2)
        image = image.resize((width,height), Image.ANTIALIAS)
        self.canvas.config(width=image.width, height=image.height)
        image = ImageTk.PhotoImage(image)
        self.canvas.image = image
        self.canvas.create_image(0, 0, image=image, anchor="nw")

    def change_size(self,size):
        global pen_size
        pen_size = size

    def change_color(self):
        global pen_color
        pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

            
    def save_image_with_dialog(self):
        image = ImageTk.getimage(self.canvas.image)
        file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                    filetypes=[('PNG Image', '*.png'),
                                                ('JPEG Image', '*.jpg'),
                                                ('All Files', '*.*')])

        if file_path:
            image.save(file_path)
            print(f"Image saved as: {file_path}")
        else:
            print("Save operation canceled.")

    def apply_filter(self,filter):
        global filter_bool

        if filter_bool == False:
            self.canvas.delete("all")
            image = ImageTk.getimage(self.canvas.image)
        else:
            image = Image.open(file_path)
            width, height = int(image.width / 2), int(image.height / 2)
            image = image.resize((width, height), Image.ANTIALIAS)
            self.canvas.config(width=image.width, height=image.height)
        if filter == "Black and White":
            image = ImageOps.grayscale(image)
            filter_bool=True
        elif filter == "Blur":
            image = image.filter(ImageFilter.BLUR)
            filter_bool=True
        elif filter == "Sharpen":
            image = image.filter(ImageFilter.SHARPEN)
            filter_bool=True
        elif filter == "Smooth":
            image = image.filter(ImageFilter.SMOOTH)
            filter_bool=True
        elif filter == "Emboss":
            image = image.filter(ImageFilter.EMBOSS)
            filter_bool=True
        elif filter == "None":
            image = image
            filter_bool=False
        image = ImageTk.PhotoImage(image)
        self.canvas.image = image
        self.canvas.create_image(0, 0, image=image, anchor="nw")

    def enhance(self,type,level):
        self.canvas.delete("all")
        img = Image.open(file_path)
        width, height = int(img.width / 2), int(img.height / 2)
        img = img.resize((width, height), Image.ANTIALIAS)

        if type =='color':
            color_enhancer = ImageEnhance.Color(img)
            enhanced_img = color_enhancer.enhance(float(level))
            print(level)
        elif type == 'contrast':
            contrast_enhancer = ImageEnhance.Contrast(img)
            enhanced_img = contrast_enhancer.enhance(float(level))
        elif type == 'brightness':
            brightness_enhancer = ImageEnhance.Brightness(img)
            enhanced_img = brightness_enhancer.enhance(float(level))
        elif type == 'sharpness':
            sharpness_enhancer = ImageEnhance.Sharpness(img)
            enhanced_img = sharpness_enhancer.enhance(float(level))

        enhanced_image = ImageTk.PhotoImage(enhanced_img)
        self.canvas.image = enhanced_image
        self.canvas.create_image(0, 0, image=enhanced_image, anchor="nw")

    def get_value_color(self,v):
        self.enhance('color',v)
        print(v)

    def get_value_contrast(self,v):
        self.enhance('contrast',v)
        print(v)

    def get_value_brightness(self,v):
        self.enhance('brightness',v)
        print(v)

    def get_value_sharpness(self,v):
        self.enhance('sharpness',v)
        print(v)

    def create_widgets(self):
        image_button = tk.Button(self, text = "Add Image", command=self.add_image, bg="white")
        image_button.pack(pady=15)

        color_button = tk.Button(self, text="Change Pen Color", command=self.change_color, bg="white")
        color_button.pack(pady=5)

        pen_size_frame = tk.Frame(self, bg="white")
        pen_size_frame.pack(pady=5)

        pen_size_1 = tk.Radiobutton(
            pen_size_frame, text="Small", value=3, command=lambda: self.change_size(3), bg="white")
        pen_size_1.pack(side="left")

        pen_size_2 = tk.Radiobutton(
            pen_size_frame, text="Medium", value=5, command=lambda: self.change_size(5), bg="white")
        pen_size_2.pack(side="left")
        pen_size_2.select()

        pen_size_3 = tk.Radiobutton(
            pen_size_frame, text="Large", value=7, command=lambda: self.change_size(7), bg="white")
        pen_size_3.pack(side="left")

        filter_label = tk.Label(self, text="Select Filter", bg="white")
        filter_label.pack()
        filter_combobox = ttk.Combobox(self, values=["Black and White", "Blur",
                                                    "Emboss", "Sharpen", "Smooth","None"])
        filter_combobox.pack()

        filter_combobox.bind("<<ComboboxSelected>>",
                            lambda event: self.apply_filter(filter_combobox.get()))

        #color
        enhance_color_label = tk.Label(self, text="Color", bg="white")
        enhance_color_label.pack()
        scale_color = tk.Scale(self,from_=1, to=8, orient="horizontal", command=self.get_value_color)
        scale_color.pack()

        #contrast
        enhance_color_label = tk.Label(self, text="Contrast", bg="white")
        enhance_color_label.pack()
        scale_color = tk.Scale(self,from_=1, to=8, orient="horizontal", command=self.get_value_contrast)
        scale_color.pack()

        #brightness
        enhance_color_label = tk.Label(self, text="Brightness", bg="white")
        enhance_color_label.pack()
        scale_color = Scale(self,from_=1, to=8, orient="horizontal", command=self.get_value_brightness)
        scale_color.pack()

        #sharpness
        enhance_color_label = tk.Label(self, text="Sharpness", bg="white")
        enhance_color_label.pack()
        scale_color = Scale(self,from_=1, to=8, orient="horizontal", command=self.get_value_sharpness)
        scale_color.pack()

        save_button = tk.Button(self, text="Save image",
                                command=self.save_image_with_dialog, bg="#1de01d", pady=15)
        save_button.pack(side='bottom', pady=80)


class TopFrame(tk.Frame):
    def __init__(self,parent,width, height, bg,canvas):
        super().__init__(parent)
        self.width=width
        self.height=height
        self.config(bg=bg)
        self.image_left = Image.open(r"C:\Users\weron\Desktop\python\PythonYT\ImageEditor\rotate_left.png")
        self.image_right = Image.open(r"C:\Users\weron\Desktop\python\PythonYT\ImageEditor\rotate_right.png")
        self.canvas = canvas
        self.pack(side="top", fill="x")  
        self.create_widgets()

    def rotate_left(self):
        try:
            self.canvas.delete("all")
            img = ImageTk.getimage(self.canvas.image)
            rotated_img = img.rotate(90,expand=True)
            self.canvas.config(width=rotated_img.width, height=rotated_img.height)
            photoimage = ImageTk.PhotoImage(rotated_img)
            self.canvas.image = photoimage
            self.canvas.create_image(0, 0, image=photoimage, anchor="nw")
        except AttributeError:
            messagebox.showerror("Błąd","You have to add image first")

    def rotate_right(self):
        try:
            self.canvas.delete("all")
            img = ImageTk.getimage(self.canvas.image)
            rotated_img = img.rotate(-90,expand=True)
            self.canvas.config(width=rotated_img.width, height=rotated_img.height)
            photoimage = ImageTk.PhotoImage(rotated_img)
            self.canvas.image = photoimage
            self.canvas.create_image(0, 0, image=photoimage, anchor="nw")
        except AttributeError:
            messagebox.showerror("Błąd","You have to add image first")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")

    def create_widgets(self):
        image_left = self.image_left
        image_right = self.image_right
        width, height = 30, 30
        image_left = image_left.resize((width,height), Image.ANTIALIAS)
        width, height = 30, 30
        image_right = image_right.resize((width,height), Image.ANTIALIAS)

        icon_left = ImageTk.PhotoImage(image_left)
        icon_right = ImageTk.PhotoImage(image_right)

        rotate_left_button = tk.Button(self, image=icon_left, command=self.rotate_left, bg="white")
        rotate_left_button.image=icon_left
        rotate_left_button.pack(side="left",padx=(345,20))
        rotate_right_button = tk.Button(self, image=icon_right, command=self.rotate_right, bg="white")
        rotate_right_button.image=icon_right
        rotate_right_button.pack(side="left", padx=(0,20))

        clear_button = tk.Button(self, text="Clear changes",
                                command=self.clear_canvas, bg="#FF9797")
        clear_button.pack(side='left')

    
class Canvas(tk.Canvas):
    def __init__(self,parent, width, height):
        super().__init__(parent)
        self.width=width
        self.height=height
        self.config(width=width, height=height)
        #self.geometry(f'{width}x{height}')

        self.bind("<B1-Motion>",self.draw)

    def draw(self,event):
        global pen_color
        global pen_size
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        self.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')

app = App('Images Editor',(1000,600))
