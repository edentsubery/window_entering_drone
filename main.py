import time
import tkinter as tk
import colorsys

import tkinter.messagebox as messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk
from djitellopy import Tello
from ultralytics import YOLO
import threading

# Globals:
change_button = None
open_button = None

is_enter_manually_running = False
should_return_to_model = False
WIDTH = 720
HEIGHT = 960
BUILDING_COLOR = [0, 0, 0]
LIGHT_COLOR = [0, 0, 0]
DARK_COLOR = [0, 0, 0]
last_no_answer_time = 0



class ColorPicker:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=720, height=540)
        self.canvas.grid(row=0, column=0, columnspan=12)
        self.canvas.bind("<Button-1>", self.get_color)

        self.cap = tello.get_frame_read()
        self.frame = self.cap.frame
        self.frame= cv2.resize(self.frame, (720, 540))
        self.results = []
        self.unmarked = self.frame
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def get_color(self, event):
        x, y = event.x, event.y
        rgb = self.frame[y, x]
        expand_colors(rgb)


def expand_colors(rgb):
    global BUILDING_COLOR, LIGHT_COLOR, DARK_COLOR
    r, b, g = rgb
    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

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
    BUILDING_COLOR = rgb
    LIGHT_COLOR = light_color
    DARK_COLOR = dark_color


def done_manual_msg_thread():
    global should_return_to_model
    pass


def stop_manual_return_model():
    global should_return_to_model
    global is_enter_manually_running
    should_return_to_model = True
    is_enter_manually_running = False
    print(f"The value of should_return_to_model was changed to {should_return_to_model}")
    print(f"The value of is_enter_manually_running was changed to {is_enter_manually_running}")
    change_button.grid_forget()
    open_button.grid_forget()


def report_detection_dialog(plotted_detection):
    dialog = tk.Toplevel(root)
    # Load and display the image
    image = Image.open("my_image.png")
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(dialog, image=photo)
    image_label.image = photo  # keep a reference to the image
    image_label.pack()

    # Add other dialog content...
    message_label = tk.Label(dialog, text="This is my custom dialog with an image.")
    message_label.pack()

    ok_button = tk.Button(dialog, text="OK", command=dialog.destroy)
    ok_button.pack()


def update():
    global ON
    global is_enter_manually_running
    global change_button, open_button
    global last_no_answer_time
    picker.frame = picker.cap.frame
    picker.frame= cv2.resize(picker.frame, (720, 540))
    picker.frametomodel = picker.frame
    picker.frametomodel = cv2.cvtColor(picker.frame, cv2.COLOR_BGR2YCrCb)
    picker.frame = cv2.cvtColor(picker.frame, cv2.COLOR_BGR2RGB)
    if ON:
        # print("still entering manually? ", is_enter_manually_running)
        if time.time() - last_no_answer_time >= 3:
            if not is_enter_manually_running:
                #picker.frametomodel = cv2.cvtColor(picker.frame, cv2.COLOR_BGR2YUV)
                results = model(picker.frametomodel)
                if results and len(results[0].boxes)>0:
                    picker.unmarked = picker.frame
                    print("plotting")
                    picker.frame = results[0].plot()
                    picker.frame = cv2.cvtColor(picker.frame, cv2.COLOR_YCrCb2RGB)
                    picker.results = results
                    picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
                    picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)

                    # if we're already navigating, don't interrupt
                    answer = messagebox.askyesno("Window is found!", "window is found in position: \n"
                                                                     "would you like to navigate in?")
                    if answer:
                        # user wants to get in - stop model
                        is_enter_manually_running = True
                        frame_copy = np.copy(picker.frame)
                        open_button = tk.Button(root, text="show window capture", command=lambda: detected_dialog(frame_copy))
                        # # open_button.pack()
                        open_button.grid(row=4, column=1)

                        #info_message = tk.Label(root,
                        #                       text="Model detection PAUSED\nModel detection will now be paused.\n you can navigate manually. ")
                        #info_message.grid(row=5, column=1)  # Adjust row and column as needed

                        new_window = tk.Toplevel(root)
                        change_button = tk.Button(new_window, text="return to model", command=stop_manual_return_model)
                        #change_button.pack()
                        change_button.grid(row=4, column=2)

                    else:
                        # user doesn't want to get it- proceed.
                        last_no_answer_time = time.time()
                        print("        update-> don't want to get it- move on.")
                else:
                    picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
                    picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)
            else:
                picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
                picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)
        else:
            picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
            picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)
    else:
        picker.photo = ImageTk.PhotoImage(image=Image.fromarray(picker.frame))
        picker.canvas.itemconfig(picker.canvas_image, image=picker.photo)
    picker.master.after(10, update)


def detected_dialog(current_plotted_frame):
    print("opening dialog")
    dialog_box = tk.Toplevel(root)
    dialog_box.geometry = ("400x400")

    # Convert the OpenCV image (BGR) to a PIL image (RGB)
    current_plotted_frame = cv2.cvtColor(current_plotted_frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(current_plotted_frame)

    # Convert the PIL image to a PhotoImage, which Tkinter can display
    photo = ImageTk.PhotoImage(image)

    # Display the image
    image_label = tk.Label(dialog_box, image=photo)
    image_label.image = photo  # keep a reference to the image
    image_label.grid(row=0, column=0)

    # Create a function to handle the user's button click
    def on_button_click():
        # If the user clicks the "Yes" button, do something
        # ...
        dialog_box.destroy()  # Close the dialog box
        return

    # Create a "Yes" button using a Tkinter Button widget
    yes_button = up_button = tk.Button(dialog_box, activebackground="#d9d9d9", image=accept_img, borderwidth=0,
                                       command=on_button_click)
    yes_button.grid(row=1, column=1)

    # Create a "No" button using a Tkinter Button widget
    no_button = tk.Button(dialog_box, activebackground="#d9d9d9", image=reject_img, borderwidth=0,
                          command=dialog_box.destroy)
    no_button.grid(row=1, column=2)

    # Run the Tkinter event loop to display the dialog box and wait for user input
    dialog_box.mainloop()
    # dialog_box.after(1000, ask_for_confirmation)


def get_tello_command(direction, inner_tello):
    # Define a dictionary that maps directions to Tello commands
    commands = {'UP': 'up 20', 'DOWN': 'down 20', 'LEFT': 'left 20', 'RIGHT': 'right 20', 'CENTER': 'forward 20',
                'backward': 'back 20'}

    # Check if the direction is in the dictionary
    if direction in commands:
        print("in tello_command, sending command: ", commands[direction])
        inner_tello.send_control_command(commands[direction])
        print("sent")
        return commands[direction]
    else:
        return


def move_in_direction(direction):
    if direction == "UNKNOWN":
        return
    if direction == "UP":
        tello.move_up(step)
        return
    if direction == "DOWN":
        tello.move_down(step)
        return
    if direction == "RIGHT":
        tello.move_right(step)
        return
    if direction == "LEFT":
        tello.move_left(step)
        return
    if direction == "CENTER":
        tello.move_forward(step)
        return


def track_window():
    pass


def engine():
    # ask_for_confirmation(100,100,200,200)
    global ON
    if ON:
        print("     engine-> drone is landing")
        tello.land()
        ON = False
    else:
        tello.takeoff()
        ON = True
        print("     engine-> drone mode is: ", ON)


# create a Tello object to control the drone
step = 35
ON = False
is_enter_manually_running = False
print("     main-> starting Model")
model = YOLO("window_detector.pt")
tello = Tello()

# set up the video stream from the Tello drone
print("     main-> connecting tello and start streaming")
tello.connect()

tello.streamon()

# set up the GUI
root = tk.Tk()
root.title("Tello Control GUI")


picker = ColorPicker(root)
picker.canvas_image = picker.canvas.create_image(0, 0, anchor=tk.NW, image=picker.photo)
root.after(10, update)

click_btn = tk.PhotoImage(file="buttons/left.png")
forward_img = tk.PhotoImage(file="buttons/forward.png")
back_img = tk.PhotoImage(file="buttons/back.png")
left_img = tk.PhotoImage(file="buttons/left.png")
right_img = tk.PhotoImage(file="buttons/right.png")
engine_img = tk.PhotoImage(file="buttons/engine.png")
clock_img = tk.PhotoImage(file="buttons/clockwise.png")
counterClock_img = tk.PhotoImage(file="buttons/counter.png")
up_img = tk.PhotoImage(file="buttons/up.png")
down_img = tk.PhotoImage(file="buttons/down.png")
reject_img = tk.PhotoImage(file="buttons/reject.png")
accept_img = tk.PhotoImage(file="buttons/accept.png")


def move_left():
    tello.send_control_command('command')  # Put the drone in command mode
    tello.move_left(step)  # Move left
    time.sleep(1)  # Wait for 5 seconds


def move_right():
    tello.send_control_command('command')  # Put the drone in command mode
    tello.move_right(step)  # Move right
    time.sleep(1)  # Wait for 5 seconds


def move_up():
    tello.send_control_command('command')  # Put the drone in command mode
    tello.move_up(step)  # Move up
    print("up from botton")
    time.sleep(1)  # Wait for 5 seconds


def move_down():
    tello.send_control_command('command')  # Put the drone in command mode
    tello.move_down(step)  # Move down
    time.sleep(1)  # Wait for 5 seconds


def move_forward():
    tello.send_control_command('command')  # Put the drone in command mode
    tello.move_forward(step)  # Move forward
    time.sleep(1)  # Wait for 5 seconds


def move_back():
    tello.send_control_command('command')  # Put the drone in command mode
    tello.move_back(step)  # Move back
    time.sleep(1)  # Wait for 5 seconds


left_button = tk.Button(root, activebackground="#d9d9d9", image=left_img, borderwidth=0,
                        command=lambda: move_left())
#left_button.place(x=200, y=430)
left_button.grid(row=2, column=0)
right_button = tk.Button(root, activebackground="#d9d9d9", image=right_img, borderwidth=0,
                         command=lambda: move_right())
#right_button.place(x=320, y=430)
right_button.grid(row=2, column=2)
forward_button = tk.Button(root, activebackground="#d9d9d9", image=forward_img, borderwidth=0,
                           command=lambda: move_forward())
#forward_button.place(x=260, y=370)
forward_button.grid(row=1, column=1)
back_button = tk.Button(root, activebackground="#d9d9d9", image=back_img, borderwidth=0,
                        command=lambda: move_back())
#back_button.place(x=260, y=490)
back_button.grid(row=3, column=1)
up_button = tk.Button(root, activebackground="#d9d9d9", image=up_img, borderwidth=0,
                      command=lambda: move_up())
#up_button.place(x=650, y=370)
up_button.grid(row=1, column=10)
down_button = tk.Button(root, activebackground="#d9d9d9", image=down_img, borderwidth=0,
                        command=lambda: move_down())
#down_button.place(x=650, y=490)
down_button.grid(row=3, column=10)
label = tk.Label(root, text="ADJUST HEIGHT")
#label.place(x=650, y=450)
label.grid(row=2,column=10)

land_button = tk.Button(root, activebackground="#d9d9d9", image=engine_img, borderwidth=0, command=engine)
land_button.grid(row=1,column=3, columnspan=6, rowspan=3)

clock_button = tk.Button(root, activebackground="#d9d9d9", image=clock_img, borderwidth=0,
                         command=lambda: tello.rotate_clockwise(30))
#clock_button.place(x=840, y=370)
clock_button.grid(row=1,column= 11)
counterclock_button = tk.Button(root, activebackground="#d9d9d9", image=counterClock_img, borderwidth=0,
                                command=lambda: tello.rotate_counter_clockwise(30))
#counterclock_button.place(x=60, y=370)
counterclock_button.grid(row=3, column=11)

root.mainloop()
