import cv2
import time
import numpy as np
from djitellopy import Tello
from ultralytics import YOLO

WIDTH=720
HEIGHT=960
# # Define the drone's IP address and port number
# tello = Tello()
# tello.connect()
#
# time.sleep(2)
# tello.streamon()
#
# time.sleep(2)
# tello.takeoff()
#
# time.sleep(5)
# tello.move_up(100)
#
# time.sleep(2)
model = YOLO("window_detector.pt")
back=True


# results = model("facade (copy).jpg")
# window_bbox=results[0].boxes.xyxy[1]
#
# print(len(results[0].boxes))
# res_plotted = results[0].plot()



def get_direction(window_bbox):
    # get the center coordinates of the window bbox
    x_center = (window_bbox[0] + window_bbox[2]) // 2
    y_center = (window_bbox[1] + window_bbox[3]) // 2

    # calculate the distance of the center of the window from the center of the image
    x_distance = x_center - (WIDTH // 2)
    y_distance = y_center - (HEIGHT // 2)

    # calculate the grid size
    x_grid_size = WIDTH // 3
    y_grid_size = HEIGHT // 3

    # calculate the section in which the center of the window falls
    x_section = x_center // x_grid_size
    y_section = y_center // y_grid_size

    # determine the direction in which the drone needs to move based on the grid section
    if x_section == 1 and y_section == 1:
        direction = "CENTER"
    elif x_section == 1 and y_section == 0:
        direction = "UP"
    elif x_section == 0 and y_section == 1:
        direction = "LEFT"
    elif x_section == 2 and y_section == 1:
        direction = "RIGHT"
    elif x_section == 1 and y_section == 2:
        direction = "DOWN"
    return direction


# res_plotted= cv2.resize(res_plotted, None, fx=0.5, fy=0.5)
# cv2.imshow("result", res_plotted)
# cv2.waitKey(0)
# cv2.imwrite("/home/eden/Downloads/result.jpg", res_plotted)
#
# Connect to the drone and initialize the video stream
#
#
# time.sleep(2)


# Define the color range for the building
lower = np.array([50, 50, 50])
upper = np.array([150, 150, 150])

# def enter_window(window_xyxy):
#     while direction!=CENTER:
#         #move to direction
#         captur image
#         calculate new xyxy
#         direction=get_direction(img[0].boxes.xyxy
#     while you see window:
#         move forward
#     land

# Define the initial scanning direction
# direction = 1
# try:
#    while True:
#        start = time.time()
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
#
#
