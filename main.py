import tkinter as tk
import cv2
import numpy as np
import time
from PIL import Image, ImageTk
from djitellopy import Tello
from ultralytics import YOLO
from corner import find_building_corner
WIDTH=720
HEIGHT=960
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
        BUILDING_COLOR=rgb
        print("RGB:", rgb)


def update():
    picker.frame = picker.cap.frame
    picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
    picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)
    picker.master.after(10, update)

def handle_edge():
    img = tello.get_frame_read().frame
    x1,y1,x2,y2= WIDTH,HEIGHT,WIDTH,HEIGHT
    is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    while x1 >= WIDTH//2 or x2>= WIDTH//2:
        tello.move_right(step)
        img = tello.get_frame_read().frame
        is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    tello.move_right(7*step)
    img = tello.get_frame_read().frame
    tello.rotate_counter_clockwise(90)
    is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    while(not is_edge or direction!= LEFT):
         tello.move_right(step)
         img = tello.get_frame_read().frame
         is_edge,direction, x1,y1,x2,y2= find_building_corner(img, BUILDING_COLOR)
    return

def find_window():
    if(ON):
        try:
           while True:
               img = picker.frame
               img = model(img)
               if(len(img[0].boxes)): #found window
                    plotted=img[0].plot()
                    cv2.imshow('frame', plotted)
                    cv2.waitKey(1)
                    return img[0]
               else:
                    results= find_building_corner(img, BUILDING_COLOR)
                    if(results[0] and results[1]==RIGHT):
                        handle_edge()
                        break
                    else:
                        tello.move_right(20)
                        break
        except KeyboardInterrupt:
           tello.streamoff()
           tello.land()
           tello.disconnect()
           exit(1)
    else:
        return[]

def enter_window():
    direction=False
    while direction!=CENTER:
        #move to direction
        img = picker.frame
        img = model(img)
        if(len(img[0].boxes)): #found window
            direction=get_direction(img[0].boxes.xyxy)
    while len(img[0].boxes)!=0 and direction==CENTER:
        tello.move_forward(step)
        img = picker.frame
        img = model(img)
        if(len(img[0].boxes)): #found window
            direction=get_direction(img[0].boxes.xyxy)

    tello.move_forward(3*step)
    tello.land()



step=20
ON=False
BUILDING_COLOR=[0,0,0]
model = YOLO("window_detector.pt")
def engine():
    if ON:
        tello.land()
        tello.streamoff()
        tello.disconnect()
        ON=False
    else:
        tello.takeoff()
        ON=True

# create a Tello object to control the drone
#
# tello = Tello()
# #
# # # set up the video stream from the Tello drone
# tello.connect()
# tello.streamon()

# set up the GUI
root = tk.Tk()
root.title("Tello Control GUI")
root.geometry("1000x1000")


# picker = ColorPicker(root)
# picker.canvas_image = picker.canvas.create_image(0, 0, anchor=tk.NW, image=picker.photo)
# root.after(10, update)
#

click_btn= tk.PhotoImage(file="buttons/left.png")
forward_img=tk.PhotoImage(file="buttons/up.png")
back_img=tk.PhotoImage(file="buttons/down.png")
left_img=tk.PhotoImage(file="buttons/left.png")
right_img=tk.PhotoImage(file="buttons/right.png")
engine_img=tk.PhotoImage(file="buttons/engine.png")
clock_img=tk.PhotoImage(file="buttons/clockwise.png")
counterClock_img=tk.PhotoImage(file="buttons/counterClockwise.png")
up_img=tk.PhotoImage(file="buttons/plus.png")
down_img=tk.PhotoImage(file="buttons/minus.png")
left_button = tk.Button(root, activebackground="#d9d9d9", image=left_img, borderwidth=0, command=lambda: tello.send_rc_control(-step, 0, 0, 0))
left_button.place(x=200, y=740)
right_button = tk.Button(root, activebackground="#d9d9d9", image=right_img, borderwidth=0,command=lambda: tello.send_rc_control(step, 0, 0, 0))
right_button.place(x=320, y=740)
up_button = tk.Button(root,activebackground="#d9d9d9",  image=up_img, borderwidth=0,command=lambda: tello.send_rc_control(0, step, 0, 0))
up_button.place(x=500, y=650)
down_button = tk.Button(root, activebackground="#d9d9d9", image=down_img, borderwidth=0,command=lambda: tello.send_rc_control(0, -step, 0, 0))
down_button.place(x=500, y=750)
forward_button = tk.Button(root, activebackground="#d9d9d9", image=forward_img, borderwidth=0,command=lambda: tello.send_rc_control(0, 0, step, 0))
forward_button.place(x=260, y=680)
back_button = tk.Button(root, activebackground="#d9d9d9", image=back_img, borderwidth=0, command=lambda: tello.send_rc_control(0, 0, -step, 0))
back_button.place(x=260, y=800)
land_button = tk.Button(root, activebackground="#d9d9d9", image=engine_img, borderwidth=0, command=engine )
land_button.place(x=40, y=750)
clock_button = tk.Button(root, activebackground="#d9d9d9", image=clock_img, borderwidth=0,command=lambda: tello.rotate_clockwise(30))
clock_button.place(x=400, y=680)
counterclock_button = tk.Button(root, activebackground="#d9d9d9", image=counterClock_img, borderwidth=0, command=lambda:  tello.rotate_counter_clockwise(30))
counterclock_button.place(x=400, y=800)

# create an entry box for the command
# command_entry = tk.Entry(root, width=50)
# command_entry.place(x=10, y=10)

# create a canvas to display the video stream
# canvas = tk.Canvas(root, width=640, height=480)
# canvas.place(x=300, y=10)


# find_window()
# # ask_for_confirmation()
# enter_window()

root.mainloop()

# function to execute the command entered by the user
def execute_command():
    command = command_entry.get()
    if command.lower() == "enter":
        enter_window() # assuming you have a function that controls the drone to enter the window
    else:
        tello.send_command(command)
