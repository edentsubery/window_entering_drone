import cv2
import time
import numpy as np
from djitellopy import Tello
from ultralytics import YOLO

WIDTH=720
HEIGHT=960

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
    print("searching direction for dest: ", window_bbox)
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

    print("in get direction- getting: ", direction)
    return direction

lower = np.array([50, 50, 50])
upper = np.array([150, 150, 150])

def enter(window_bbox):
    print("searching direction for dest: ", window_bbox)
    direction = "UNKNOWN"
    # get the center coordinates of the window bbox
    x_center = (window_bbox[0] + window_bbox[2]) // 2
    y_center = (window_bbox[1] + window_bbox[3]) // 2

    # Update the Kalman filter with the object's position
    kalman_filter.update(np.array([[center_x], [center_y]]))

    # Get the estimated position from the Kalman filter
    estimated_position = kalman_filter.x[:2].flatten()
    est_x, est_y = estimated_position

    # Draw the estimated position on the frame
    cv2.circle(picker.frame, (int(est_x), int(est_y)), 5, (0, 255, 0), -1)

