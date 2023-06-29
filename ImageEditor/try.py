import tkinter as tk

def get_value(v):
    print(v)

root = tk.Tk()
root.title("Test")
slider = tk.Scale(orient='horizontal', label = 'Amount', length = 500, from_= 0, to = 1000, bg = 'white', fg = 'black', sliderlength = 20, command=get_value)
slider.pack()

root.mainloop()