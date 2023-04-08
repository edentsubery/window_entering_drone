
import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry('300x300')

canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()
img = Image.open("/home/eden/Downloads/index.jpeg")
img = ImageTk.PhotoImage(img)
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Function to retrieve color at mouse click position
def get_color(event):
    # Get mouse click position
    x, y = event.x, event.y
    img = Image.open("/home/eden/Downloads/index.jpeg") # replace with your image
    # Retrieve pixel value at mouse click position
    pixel = img.getpixel((x, y))

    # Convert pixel value to color
    color = "#%02x%02x%02x" % pixel

    # Print color to console
    print("Color at position ({}, {}): {}".format(x, y, color))


# Bind mouse click event to canvas
canvas.bind("<Button-1>", get_color)

root.mainloop()





#
# # create tkinter window and canvas
# window = tkinter.Tk()
# canvas = tkinter.Canvas(window, width=720, height=480)
# canvas.pack()
#
# def update_image():
#     frame = tello.get_frame_read().frame
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     image = Image.fromarray(frame)
#     photo = ImageTk.PhotoImage(image)
#     canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
#     canvas.image = photo  # keep a reference to the photo to prevent garbage collection
#
#     window.after(30, update_image)  # update every 30 milliseconds
#
# update_image()
# window.mainloop()




#
# import tkinter as tk
# from PIL import ImageTk, Image
# import cv2
# from tello import Tello
#
# tello = Tello()
#
class ColorPicker:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=720, height=480)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.get_color)

        self.cap = tello.get_frame_read()
        self.frame = self.cap.frame
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def get_color(self, event):
        x, y = event.x, event.y
        rgb = self.frame[y, x]
        print("RGB:", rgb)

def update():
    picker.frame = picker.cap.frame
    picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
    picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)
    picker.master.after(10, update)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Color Picker")
    picker = ColorPicker(root)
    picker.canvas_image = picker.canvas.create_image(0, 0, anchor=tk.NW, image=picker.photo)
    root.after(10, update)
    root.mainloop()
