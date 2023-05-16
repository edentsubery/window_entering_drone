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

import cv2

def fly_through_window(window_bbox, drone):
    # Get the coordinates of the window bounding box
    window_x1, window_y1, window_x2, window_y2 = window_bbox

    # Calculate the center point of the window
    window_center_x = (window_x1 + window_x2) / 2
    window_center_y = (window_y1 + window_y2) / 2

    # Calculate the difference between the window center and the camera center
    camera_center_x = WIDTH / 2
    camera_center_y = HEIGHT / 2
    diff_x = window_center_x - camera_center_x
    diff_y = window_center_y - camera_center_y

    # Adjust the drone's yaw to center it with respect to the window
    # Here's a simple example using proportional control to adjust the drone's yaw
    k_p_yaw = 0.1
    yaw_speed = k_p_yaw * diff_x
    drone.set_yaw_speed(yaw_speed)

    # Adjust the drone's height to center it with respect to the window
    # Here's a simple example using proportional control to adjust the drone's height
    k_p_height = 0.1
    height_speed = k_p_height * diff_y
    drone.set_height(height_speed)

    # Move the drone forward to enter the window
    # Here's a simple example using a fixed forward speed
    forward_speed = 0.5
    drone.set_forward_speed(forward_speed)



def get_direction(window_bbox):
    print("window bbox " , window_bbox)
    direction = "UNKNOWN"
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
    print("x_section: ", x_section)
    print("y_section: ", y_section)


    # determine the direction in which the drone needs to move based on the grid section
    if x_section == 1 and y_section == 1:
        direction = "CENTER"
        return direction
    if x_section == 0:
        direction = "LEFT"
        return direction
    if x_section == 2:
        direction = "RIGHT"
        return direction
    if y_section == 0:
        direction = "UP"
        return direction
    if y_section == 2:
        direction = "DOWN"
        return direction
#     elif x_section == 1 and y_section == 0:
#         direction = "UP"
#     elif x_section == 0:
#         direction = "LEFT"
#     elif x_section == 2:
#         direction = "RIGHT"
#     elif x_section == 1 and y_section == 2:
#         direction = "DOWN"
    print(direction)
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


results = model("facade (copy).jpg")
window_bbox=results[0].boxes.xyxy[1]
#
print(len(results[0].boxes))
res_plotted = results[0].plot()
print(get_direction(window_bbox))

