import tkinter as tk
import cv2
import numpy as np
import time
from PIL import Image, ImageTk
from djitellopy import Tello
from ultralytics import YOLO



def set_buttons(root):
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
    left_button = tk.Button(root, image=left_img, borderwidth=0, command=lambda: tello.send_rc_control(-step, 0, 0, 0))
    left_button.config(activebackground=left_button.cget('background'))
    left_button.place(x=200, y=740)
    right_button = tk.Button(root, image=right_img, borderwidth=0,command=lambda: tello.send_rc_control(step, 0, 0, 0))
    right_button.place(x=320, y=740)
    right_button.config(activebackground=left_button.cget('background'))
    up_button = tk.Button(root, image=up_img, borderwidth=0,command=lambda: tello.send_rc_control(0, step, 0, 0))
    up_button.place(x=500, y=650)
    up_button.config(activebackground=left_button.cget('background'))
    down_button = tk.Button(root, image=down_img, borderwidth=0,command=lambda: tello.send_rc_control(0, -step, 0, 0))
    down_button.place(x=500, y=750)
    down_button.config(activebackground=left_button.cget('background'))
    forward_button = tk.Button(root, image=forward_img, borderwidth=0,command=lambda: tello.send_rc_control(0, 0, step, 0))
    forward_button.place(x=260, y=680)
    forward_button.config(activebackground=left_button.cget('background'))
    back_button = tk.Button(root, image=back_img, borderwidth=0, command=lambda: tello.send_rc_control(0, 0, -step, 0))
    back_button.place(x=260, y=800)
    back_button.config(activebackground=left_button.cget('background'))
    land_button = tk.Button(root, image=engine_img, borderwidth=0, command=engine )
    land_button.place(x=40, y=750)
    land_button.config(activebackground=left_button.cget('background'))
    clock_button = tk.Button(root, image=clock_img, borderwidth=0,command=lambda: tello.rotate_clockwise(30))
    clock_button.place(x=400, y=680)
    clock_button.config(activebackground=left_button.cget('background'))
    counterclock_button = tk.Button(root, image=counterClock_img, borderwidth=0, command=lambda:  tello.rotate_counter_clockwise(30))
    counterclock_button.place(x=400, y=800)
    counterclock_button.config(activebackground=left_button.cget('background'))


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



step=20
ON=False
BUILDING_COLOR=[0,0,0]
model = YOLO("window_detector.pt")
def engine():
    if ON:
        tello.land()
        ON=False
    else:
        tello.takeoff()
        ON=True

# create a Tello object to control the drone

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
forward_img=tk.PhotoImage(file="buttons/up.png")
back_img=tk.PhotoImage(file="buttons/down.png")
left_img=tk.PhotoImage(file="buttons/left.png")
right_img=tk.PhotoImage(file="buttons/right.png")
engine_img=tk.PhotoImage(file="buttons/engine.png")
clock_img=tk.PhotoImage(file="buttons/clockwise.png")
counterClock_img=tk.PhotoImage(file="buttons/counterClockwise.png")
up_img=tk.PhotoImage(file="buttons/plus.png")
down_img=tk.PhotoImage(file="buttons/minus.png")
left_button = tk.Button(root, image=left_img, borderwidth=0, command=lambda: tello.send_rc_control(-step, 0, 0, 0))
left_button.config(activebackground=left_button.cget('background'))
left_button.place(x=200, y=740)
right_button = tk.Button(root, image=right_img, borderwidth=0,command=lambda: tello.send_rc_control(step, 0, 0, 0))
right_button.place(x=320, y=740)
right_button.config(activebackground=left_button.cget('background'))
up_button = tk.Button(root, image=up_img, borderwidth=0,command=lambda: tello.send_rc_control(0, step, 0, 0))
up_button.place(x=500, y=650)
up_button.config(activebackground=left_button.cget('background'))
down_button = tk.Button(root, image=down_img, borderwidth=0,command=lambda: tello.send_rc_control(0, -step, 0, 0))
down_button.place(x=500, y=750)
down_button.config(activebackground=left_button.cget('background'))
forward_button = tk.Button(root, image=forward_img, borderwidth=0,command=lambda: tello.send_rc_control(0, 0, step, 0))
forward_button.place(x=260, y=680)
forward_button.config(activebackground=left_button.cget('background'))
back_button = tk.Button(root, image=back_img, borderwidth=0, command=lambda: tello.send_rc_control(0, 0, -step, 0))
back_button.place(x=260, y=800)
back_button.config(activebackground=left_button.cget('background'))
land_button = tk.Button(root, image=engine_img, borderwidth=0, command=engine )
land_button.place(x=40, y=750)
land_button.config(activebackground=left_button.cget('background'))
clock_button = tk.Button(root, image=clock_img, borderwidth=0,command=lambda: tello.rotate_clockwise(30))
clock_button.place(x=400, y=680)
clock_button.config(activebackground=left_button.cget('background'))
counterclock_button = tk.Button(root, image=counterClock_img, borderwidth=0, command=lambda:  tello.rotate_counter_clockwise(30))
counterclock_button.place(x=400, y=800)
counterclock_button.config(activebackground=left_button.cget('background'))

# create buttons for manual control of the drone


# create an entry box for the command
# command_entry = tk.Entry(root, width=50)
# command_entry.place(x=10, y=10)

# create a canvas to display the video stream
# canvas = tk.Canvas(root, width=640, height=480)
# canvas.place(x=300, y=10)


# Define the initial scanning direction
# direction = 1
# update_video_stream()
# try:
#    while True:
#        #update_video_stream()
#        frame = tello.get_frame_read().frame
#        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#        #     window_bbox = detect_window(frame) # assuming you have a function that detects the window in the frame
#        #     if window_bbox is not None:
#        #         # draw the bounding box around the window
#        #         x, y, w, h = window_bbox
#        #         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
#        canvas.create_image(0, 0, image=photo, anchor=tk.NW)
#        root.after(10, update_video_stream)
#        img = tello.get_frame_read().frame
#        img = model(img)
#        if(len(img[0].boxes)):
#             #ask user for permission to enter, if many windows let select
#             #while not in the center:
#                 direction=get_direction(img[0].boxes.xyxy[selected])
#                 print(direction)
                #move in that direction
                #get a frame
                #detect in new image
                #get direction
                #move in that direction
            #now need to go to the front while remaining centered

       #else
            #if there is an edge (building from left)
            #move right 100
            #rotate 90 degrees counter clockwise
            #start moving write until you see the edge (building from right)
#        plotted=img[0].plot()
#        cv2.imshow('frame', plotted)
#        cv2.waitKey(1)
#        if(back):
#            tello.move_back(20)
#            time.sleep(2)
#        else:
#            tello.move_forward(20)
#            time.sleep(2)
#        back=not back
# except KeyboardInterrupt:
#    tello.streamoff()
#    time.sleep(2)
#    tello.land()
#    time.sleep(2)
#    tello.disconnect()
#    exit(1)
# finally:
#    print("fin")
find_window()
ask_for_confirmation()
enter_window()

root.mainloop()

# function to execute the command entered by the user
def execute_command():
    command = command_entry.get()
    if command.lower() == "enter":
        enter_window() # assuming you have a function that controls the drone to enter the window
    else:
        tello.send_command(command)
