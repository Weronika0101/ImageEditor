import tkinter as tk
from tkinter import PhotoImage, filedialog, colorchooser, Scale
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageEnhance
from tkinter import ttk

class App(tk.Tk):
    def __init__(self,title,size):

        #main setup
        super().__init__
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.config(bg='white')

        #widgets


        #run
        
