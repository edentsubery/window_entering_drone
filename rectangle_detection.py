import cv2
import numpy as np
from ultralytics import YOLO
#
# # Load image, grayscale, median blur, sharpen image
# image = cv2.imread('images.png')
# # image= cv2.resize(image, None, fx=0.5, fy=0.5)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur= cv2.bilateralFilter(gray,3, 100, 100)
# sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
# sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
#
# # Threshold and morph close
# thresh = cv2.threshold(sharpen, 120, 255, cv2.THRESH_BINARY_INV)[1]
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# open = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
#
# # Find contours and filter using threshold area
# cnts = cv2.findContours(open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#
# min_height=0
# min_width=0
# image_number = 0
# returned=[]
# for c in cnts:
#     x,y,w,h = cv2.boundingRect(c)
#     if h>min_height and w>min_width:
#         area = cv2.contourArea(c)
#
#         #cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
#         cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
#         image_number += 1
#         returned.append([x,y,x+w,y+h])
#
# cv2.imwrite('sharpen.jpg', sharpen)
# cv2.imwrite('open.jpg', open)
# cv2.imwrite('thresh.jpg', thresh)
# cv2.imwrite('image.jpg', image)

def check_rectangle_condition(x, y, w, h, returned):
    return any(rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3] for rect in returned)
def detect_rectangles(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   # blur=cv2.GaussianBlur(gray,(5,5),0)
    blur=cv2.bilateralFilter(gray,3, 100, 100)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    # Threshold and morph close
    thresh = cv2.threshold(sharpen, 120, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Find contours and filter using threshold area
    cnts = cv2.findContours(open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_height=20
    min_width=20
    image_number = 0
    returned=[]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if h>min_height and w>min_width:
            area = cv2.contourArea(c)

            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
            image_number += 1
            returned.append([x,y,x+w,y+h])
    return image, returned


def detect_and_check_rectangles(image, yolo_results):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.bilateralFilter(gray, 3, 100, 100)
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    # Threshold and morph close
    thresh = cv2.threshold(sharpen, 120, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Find contours and filter using threshold area
    cnts = cv2.findContours(open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    min_height = 20
    min_width = 20
    image_number = 0
    returned = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h > min_height and w > min_width:
            returned.append([x, y, x + w, y + h])

  #  Check if the YOLO results are within the detected rectangles
    is_within_rectangles = []
    windows=[]
    for yolo_result in yolo_results:
        x, y, w, h = yolo_result[0], yolo_result[1], yolo_result[2], yolo_result[3]
        yolo_rect = [x, y, x + w, y + h]
        is_within = any(rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3] for rect in returned)
        is_within_rectangles.append(is_within)
        if is_within:
                box = yolo_result.cpu().numpy()  # Convert tensor to NumPy array

                (centerX, centerY, width, height) = box.astype("int")  # Convert NumPy array to int

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                windows.append([x, y, int(width), int(height)])
                print(x,y,w,h)
                cv2.rectangle(image, (x, y), (x + int(width), y + int(height)), (0, 0, 255), 5)
                # update our list of bounding box coor

    return image, windows, is_within_rectangles

#how to test it
image = cv2.imread('images.jpg')
model=YOLO("window_detector.pt")
result=model(image)
print(result[0].boxes.xywh)
cv2.imwrite("model.png", result[0].plot())
