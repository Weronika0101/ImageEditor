import tkinter as tk
from tkinter import PhotoImage, filedialog, colorchooser, Scale
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance
from tkinter import ttk


root = tk.Tk()
root.geometry("1000x600")
root.title("Images Editor")
root.config(bg="white")

pen_color = "black"
pen_size = 5
file_path = ""
filter_bool = False
number = 1

def add_image():
    global file_path
    file_path = filedialog.askopenfilename()

    image = Image.open(file_path)
    width, height = int( image.width/2), int(image.height/2)
    image = image.resize((width,height), Image.ANTIALIAS)
    canvas.config(width=image.width, height=image.height)
    image = ImageTk.PhotoImage(image)
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def rotate_left():
    canvas.delete("all")
    img = ImageTk.getimage(canvas.image)
    rotated_img = img.rotate(90,expand=True)
    canvas.config(width=rotated_img.width, height=rotated_img.height)
    photoimage = ImageTk.PhotoImage(rotated_img)
    canvas.image = photoimage
    canvas.create_image(0, 0, image=photoimage, anchor="nw")


def rotate_right():
    canvas.delete("all")
    img = ImageTk.getimage(canvas.image)
    rotated_img = img.rotate(-90,expand=True)
    canvas.config(width=rotated_img.width, height=rotated_img.height)
    photoimage = ImageTk.PhotoImage(rotated_img)
    canvas.image = photoimage
    canvas.create_image(0, 0, image=photoimage, anchor="nw")

def draw(event):
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline='')

 
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]


def change_size(size):
    global pen_size
    pen_size = size

def clear_canvas():
    canvas.delete("all")
    canvas.create_image(0, 0, image=canvas.image, anchor="nw")


def apply_filter(filter):
    global filter_bool
    #image = Image.open(file_path)
    #width, height = int(image.width / 2), int(image.height / 2)
    #image = image.resize((width, height), Image.ANTIALIAS)
    if filter_bool == False:
        canvas.delete("all")
        image = ImageTk.getimage(canvas.image)
    else:
        image = Image.open(file_path)
        width, height = int(image.width / 2), int(image.height / 2)
        image = image.resize((width, height), Image.ANTIALIAS)
        canvas.config(width=image.width, height=image.height)
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
    canvas.image = image
    canvas.create_image(0, 0, image=image, anchor="nw")

def enhance(type,level):
    canvas.delete("all")
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
    canvas.image = enhanced_image
    canvas.create_image(0, 0, image=enhanced_image, anchor="nw")

def save_image():
    global number
    image = ImageTk.getimage(canvas.image)
    image.save("edited_photo_"+number, 'jpg')

left_frame = tk.Frame(root, width=200, height=600, bg="white")
left_frame.pack(side="left", fill="y")

top_frame = tk.Frame(root, width=750, height=100, bg= "white")
top_frame.pack(side="top", fill="x")

canvas = tk.Canvas(root, width=750, height=500)
canvas.pack()
canvas.bind("<B1-Motion>",draw)


image_button = tk.Button(left_frame, text = "Add Image", command=add_image, bg="white")
image_button.pack(pady=15)

color_button = tk.Button(left_frame, text="Change Pen Color", command=change_color, bg="white")
color_button.pack(pady=5)

pen_size_frame = tk.Frame(left_frame, bg="white")
pen_size_frame.pack(pady=5)

pen_size_1 = tk.Radiobutton(
    pen_size_frame, text="Small", value=3, command=lambda: change_size(3), bg="white")
pen_size_1.pack(side="left")

pen_size_2 = tk.Radiobutton(
    pen_size_frame, text="Medium", value=5, command=lambda: change_size(5), bg="white")
pen_size_2.pack(side="left")
pen_size_2.select()

pen_size_3 = tk.Radiobutton(
    pen_size_frame, text="Large", value=7, command=lambda: change_size(7), bg="white")
pen_size_3.pack(side="left")


filter_label = tk.Label(left_frame, text="Select Filter", bg="white")
filter_label.pack()
filter_combobox = ttk.Combobox(left_frame, values=["Black and White", "Blur",
                                             "Emboss", "Sharpen", "Smooth","None"])
filter_combobox.pack()


filter_combobox.bind("<<ComboboxSelected>>",
                     lambda event: apply_filter(filter_combobox.get()))

def get_value_color(v):
    enhance('color',v)
    print(v)

def get_value_contrast(v):
    enhance('contrast',v)
    print(v)

def get_value_brightness(v):
    enhance('brightness',v)
    print(v)

def get_value_sharpness(v):
    enhance('sharpness',v)
    print(v)

#color
enhance_color_label = tk.Label(left_frame, text="Color", bg="white")
enhance_color_label.pack()
scale_color = tk.Scale(left_frame,from_=1, to=8, orient="horizontal", command=get_value_color)
scale_color.pack()

#contrast
enhance_color_label = tk.Label(left_frame, text="Contrast", bg="white")
enhance_color_label.pack()
scale_color = tk.Scale(left_frame,from_=1, to=8, orient="horizontal", command=get_value_contrast)
scale_color.pack()
#brightness
enhance_color_label = tk.Label(left_frame, text="Brightness", bg="white")
enhance_color_label.pack()
scale_color = Scale(left_frame,from_=1, to=8, orient="horizontal", command=get_value_brightness)
scale_color.pack()
#sharpness
enhance_color_label = tk.Label(left_frame, text="Sharpness", bg="white")
enhance_color_label.pack()
scale_color = Scale(left_frame,from_=1, to=8, orient="horizontal", command=get_value_sharpness)
scale_color.pack()

image_left = Image.open(r"C:\Users\weron\Desktop\python\PythonYT\ImageEditor\Icons\rotate_left.png")
width, height = 30, 30
image_left = image_left.resize((width,height), Image.ANTIALIAS)

image_right = Image.open(r"C:\Users\weron\Desktop\python\PythonYT\ImageEditor\Icons\rotate_right.png")
width, height = 30, 30
image_right = image_right.resize((width,height), Image.ANTIALIAS)

icon_left = ImageTk.PhotoImage(image_left)
icon_right = ImageTk.PhotoImage(image_right)
rotate_left_button = tk.Button(top_frame, image=icon_left, command=rotate_left, bg="white").pack(side="left",padx=(345,20))
rotate_right_button = tk.Button(top_frame, image=icon_right, command=rotate_right, bg="white").pack(side="left", padx=(0,20))

clear_button = tk.Button(top_frame, text="Clear changes",
                         command=clear_canvas, bg="#FF9797")
clear_button.pack(side='left')

save_button = tk.Button(left_frame, text="Save image",
                         command=save_image, bg="#1de01d", pady=15)
save_button.pack(side='bottom', pady=80)

root.mainloop()