import tkinter as tk
from tkinter import messagebox
import cv2
import numpy as np
import time
import colorsys
from PIL import Image, ImageTk
from djitellopy import Tello
from ultralytics import YOLO
from corner import find_building_corner
from window import get_direction
from rectangle_detection import detect_rectangles

WIDTH=720
HEIGHT=960
BUILDING_COLOR=[0,0,0]
LIGHT_COLOR=[0,0,0]
DARK_COLOR=[0,0,0]

class ColorPicker:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=960, height=720)
        self.canvas.place(x=20, y=20)
        self.canvas.bind("<Button-1>", self.get_color)

        self.cap = tello.get_frame_read()
        self.frame = self.cap.frame
        self.results=[]
        self.unmarked=self.frame
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def get_color(self, event):
        x, y = event.x, event.y
        rgb = self.frame[y, x]
        expand_colors(rgb)


def expand_colors(rgb):
    global BUILDING_COLOR, LIGHT_COLOR, DARK_COLOR
    r,b,g=rgb
    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)

    # Compute dark color (20% darker)
    dark_l = max(0, l - 0.2)
    dark_r, dark_g, dark_b = colorsys.hls_to_rgb(h, dark_l, s)
    dark_color = (int(dark_r * 255), int(dark_g * 255), int(dark_b * 255))

    # Compute direct light color (20% brighter)
    light_l = min(1, l + 0.2)
    light_r, light_g, light_b = colorsys.hls_to_rgb(h, light_l, s)
    light_color = (int(light_r * 255), int(light_g * 255), int(light_b * 255))

    print(f"RGB color: ({r}, {g}, {b})")
    print(f"Shade color: {dark_color}")
    print(f"Direct light color: {light_color}")
    BUILDING_COLOR=rgb
    LIGHT_COLOR=light_color
    DARK_COLOR=dark_color

def update():
    global ON
    picker.frame = picker.cap.frame
    if ON:
        results = model(picker.frame)
        picker.unmarked=picker.frame
        picker.frame = results[0].plot()
        picker.results=results
#         picker.unmarked=picker.frame
#        picker.frame, picker.results = detect_rectangles(picker.frame)

    picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
    picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)
    picker.master.after(10, update)

def handle_edge():
    x1,y1,x2,y2= WIDTH,HEIGHT,WIDTH,HEIGHT
    is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    while x1 >= WIDTH//2 or x2>= WIDTH//2:
        tello.move_right(step)
        img = picker.unmarked
        is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    tello.move_right(7*step)
    img = picker.unmarked
    tello.rotate_counter_clockwise(90)
    is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    while(not is_edge or direction!= LEFT):
         tello.move_right(step)
         img = picker.unmarked
         is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    return

def find_window():
    global ON
    print("trying to find")
    if not ON:
          root.after(1000, find_window)
          return[]
    try:
        while True:
            if(len(picker.results[0].boxes)): #found window, syntax of model
                print("detected window")
            #   return picker.results[0].boxes[0]
                root.after(1000, enter_window)
                return picker.results[0].boxes[0]
            else :
                tello.move_right(step)
                print("moving right")
#             else:
#                results= find_building_corner(picker.unmarked, BUILDING_COLOR)
#                if(results[0] and results[1]==RIGHT):
#                     handle_edge()
#                     break
#                else:
#                     tello.move_right(20)
#                     break
    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        exit(1)


def ask_for_confirmation(x1,y1,x2,y2):
    original_image = Image.fromarray(picker.frame)
    dialog_box = tk.Toplevel()
    canvas = tk.Canvas(dialog_box, width=580, height=360)
    pad=10
    crop_region = (x1-pad, y1-pad, x2+pad, y2+pad)

    cropped = original_image.crop(crop_region)


# Create a canvas widget to display the image
    canvas = tk.Canvas(dialog_box, width=cropped.width, height=cropped.height)
    canvas.pack()

# Convert the cropped image to a Tkinter PhotoImage
    tk_image = ImageTk.PhotoImage(cropped)

# Add the image to the canvas
    canvas.create_image(0, 0, anchor="nw", image=tk_image)
    label=tk.Label(dialog_box, text="Enter marked window?")
    label.pack()
    # Create a function to handle the user's button click
    def on_button_click():
        # If the user clicks the "Yes" button, do something
        # ...
        dialog_box.destroy() # Close the dialog box

    # Create a "Yes" button using a Tkinter Button widget
    yes_button = up_button = tk.Button(dialog_box,activebackground="#d9d9d9",  image=accept_img, borderwidth=0,command=on_button_click)
    yes_button.pack(side="left", padx=10, pady=10)

    # Create a "No" button using a Tkinter Button widget
    no_button = tk.Button(dialog_box,activebackground="#d9d9d9",  image=reject_img, borderwidth=0,command=dialog_box.destroy)
    no_button.pack(side="right", padx=10, pady=10)

    # Run the Tkinter event loop to display the dialog box and wait for user input
    dialog_box.mainloop()
    #dialog_box.after(1000, ask_for_confirmation)


def enter_window():
#     global ON
#     if not ON: return
    direction=False
    while direction!="CENTER":
        #move to direction
        if(len(picker.results[0].boxes)): #found window
            print("saw window in enter")
            direction=get_direction(picker.results[0].boxes.xyxy)
            print(direction)
        else:
            print("couldnt see, trying to search")
            root.after(1000, find_window)
            return
    while picker.results[0].boxes!=0 and direction=="CENTER":
        tello.move_forward(step)
        if(len(picker.results[0].boxes)): #found window
            direction=get_direction(picker.results[0].boxes.xyxy)
            print(direction)

#     tello.move_forward(3*step)
#     tello.land()

def engine():
    #ask_for_confirmation(100,100,200,200)
    global ON
    if ON:
        tello.land()
        ON=False
    else:
        tello.takeoff()
        tello.move_up(100)
        ON=True

#create a Tello object to control the drone
step=20
ON=False
model = YOLO("window_detector.pt")
tello = Tello()
#
# # set up the video stream from the Tello drone
tello.connect()
tello.streamon()

# set up the GUI
root = tk.Tk()
root.title("Tello Control GUI")
root.geometry("1000x1000")


picker = ColorPicker(root)
picker.canvas_image = picker.canvas.create_image(0, 0, anchor=tk.NW, image=picker.photo)
root.after(10, update)


click_btn= tk.PhotoImage(file="buttons/left.png")
forward_img=tk.PhotoImage(file="buttons/forward.png")
back_img=tk.PhotoImage(file="buttons/back.png")
left_img=tk.PhotoImage(file="buttons/left.png")
right_img=tk.PhotoImage(file="buttons/right.png")
engine_img=tk.PhotoImage(file="buttons/engine.png")
clock_img=tk.PhotoImage(file="buttons/clockwise.png")
counterClock_img=tk.PhotoImage(file="buttons/counter.png")
up_img=tk.PhotoImage(file="buttons/up.png")
down_img=tk.PhotoImage(file="buttons/down.png")
reject_img=tk.PhotoImage(file="buttons/reject.png")
accept_img=tk.PhotoImage(file="buttons/accept.png")

left_button = tk.Button(root, activebackground="#d9d9d9", image=left_img, borderwidth=0, command=lambda: tello.move_left(step))
left_button.place(x=200, y=830)
right_button = tk.Button(root, activebackground="#d9d9d9", image=right_img, borderwidth=0,command=lambda: tello.move_right(step))
right_button.place(x=320, y=830)
forward_button = tk.Button(root, activebackground="#d9d9d9", image=forward_img, borderwidth=0,command=lambda: tello.move_forward(step))
forward_button.place(x=260, y=770)
back_button = tk.Button(root, activebackground="#d9d9d9", image=back_img, borderwidth=0, command=lambda: tello.move_back(step))
back_button.place(x=260, y=890)

up_button = tk.Button(root,activebackground="#d9d9d9",  image=up_img, borderwidth=0,command=lambda: tello.move_up(step))
up_button.place(x=650, y=770)
down_button = tk.Button(root, activebackground="#d9d9d9", image=down_img, borderwidth=0,command=lambda: tello.move_down(step))
down_button.place(x=650, y=890)
label=tk.Label(root, text="ADJUST HEIGHT")
label.place(x=650, y=850)

land_button = tk.Button(root, activebackground="#d9d9d9", image=engine_img, borderwidth=0, command=engine )
land_button.place(x=400, y=750)

clock_button = tk.Button(root, activebackground="#d9d9d9", image=clock_img, borderwidth=0,command=lambda: tello.rotate_clockwise(30))
clock_button.place(x=840, y=770)
counterclock_button = tk.Button(root, activebackground="#d9d9d9", image=counterClock_img, borderwidth=0, command=lambda:  tello.rotate_counter_clockwise(30))
counterclock_button.place(x=60, y=770)


#find_window()
#ask_for_confirmation()
#enter_window()

root.mainloop()
