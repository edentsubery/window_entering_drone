import cv2
import numpy as np

def is_building_corner(left_color, right_color):
   if is_in_building_color(left_color) and not is_in_building_color(right_color):
       return True, RIGHT
   if is_in_building_color(right_color) and not is_in_building_color(left_color):
       return True, LEFT
   return False,

def is_in_building_color(color):
   print(color)
   if np.all(np.logical_and(color >= lower_color, color <= upper_color)):
       return True
   return False
# Define the color range for the building
upper_color = np.array([241,232,226])
lower_color = np.array([137,132,128])

# Read image
image = cv2.imread(r'C:\Users\amirs\Downloads\noCorner.jpeg')
image= cv2.resize(image, None, fx=0.3, fy=0.3)

def find_building_corner(image, building_color):

# Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray = cv2.GaussianBlur(gray, (9,9), 0)
    gray= cv2.bilateralFilter(gray,9, 150, 150)

# Apply bilateral filter with a small kernel size
#blurred = cv2.bilateralFilter(image, 9, 75, 75)


# Use canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply HoughLinesP method to
# to directly obtain line end points
    lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi/180 ,  # Angle resolution in radians
        threshold=100,  # Min number of votes for valid line
        minLineLength=20,  # Min allowed length of line
        maxLineGap=10  # Max allowed gap between line for joining them
    )

# Iterate over points
    for points in lines:
   # Extracted points nested in the list
        x1, y1, x2, y2 = points[0]
   # Draw the lines joing the points
   # On the original image
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
   # Maintain a simples lookup list for points
        lines_list.append([(x1, y1), (x2, y2)])

# Save the result image

    for line in lines:
        x1, y1, x2, y2 = line[0]
   # if abs(x1 - x2) < abs(y1 - y2):
   #     continue
        ys = np.arange(image.shape[0])
        xs = (ys - y1) * (x2 - x1) / (y2 - y1) + x1

   # Calculate the average color values for each side
        left_colors = image[ys, :int(np.round(xs.min()))]
        right_colors = image[ys, int(np.round(xs.min())):]
        left_color = np.mean(left_colors.reshape(-1, left_colors.shape[-1]), axis=0)
        right_color = np.mean(right_colors.reshape(-1, right_colors.shape[-1]), axis=0)
        print(f"Left side: ", left_color)
        print(f"Right side: ", right_color)
        if is_building_corner(left_color, right_color)[0]:
            # Print the results
            cv2.imshow('detectedLines.png', image)
            cv2.waitKey(0)
            return is_building_corner(left_color, right_color), x1, y1, x2, y2

   return false



