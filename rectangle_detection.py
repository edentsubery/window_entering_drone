import cv2
import numpy as np

# # Load image, grayscale, median blur, sharpen image
# image = cv2.imread('facade (copy).jpg')
# image= cv2.resize(image, None, fx=0.5, fy=0.5)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur= cv2.bilateralFilter(gray,9, 100, 100)
# sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
# sharpen = cv2.filter2D(blur, -1, sharpen_kernel)
#
# # Threshold and morph close
# thresh = cv2.threshold(sharpen, 120, 255, cv2.THRESH_BINARY_INV)[1]
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
# open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
#
# # Find contours and filter using threshold area
# cnts = cv2.findContours(open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#
# min_height=20
# min_width=20
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

def detect_rectangles(image):

    # grayscale, median blur, sharpen image
    image = cv2.imread('facade (copy).jpg')
    image= cv2.resize(image, None, fx=0.5, fy=0.5)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur= cv2.bilateralFilter(gray,9, 100, 100)
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

        #cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
            image_number += 1
            returned.append([x,y,x+w,y+h])
    return returned
#     cv2.imwrite('sharpen.jpg', sharpen)
#     cv2.imwrite('open.jpg', open)
#     cv2.imwrite('thresh.jpg', thresh)
#     cv2.imwrite('image.jpg', image)
