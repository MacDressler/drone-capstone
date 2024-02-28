"""
I bit this code from geeksforgeeks.com
https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
"""


# Python program to illustrate HoughLine
# method for line detection
import cv2
import numpy as np
 

"""I need to make this into a function so that I can call it from the drone. Eventually, I need to make it so that it can see the centre of the main line.""" 
img = cv2.imread('testimage.png')
points = []

def line_detection(img):
    # Reading the required image in
    # which operations are to be done.
    # Make sure that the image is in the same
    # directory in which this python program is    
    
    # Convert the img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection method on the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # This returns an array of r and theta values
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    
    
    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    for r_theta in lines:
        
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)
    
        # Stores the value of sin(theta) in b
        b = np.sin(theta)
    
        # x0 stores the value rcos(theta)
        x0 = a*r
    
        # y0 stores the value rsin(theta)
        y0 = b*r
    
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))
    
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))
    
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b))
    
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))
        points.extend([x1, y1, x2, y2])
        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
     
    
    # All the changes made in the input image are finally
    # written on a new image houghlines.jpg
    cv2.imwrite('linesDetected.jpg', img)
    return print("success")
"""Now I need to find the largest line"""

def widths(points):
    """The strategy is to determine if each line is horizontal or vertical"""
    d = len(points)
    print(d)
    e = d/8
    print(e)
    print(int(e))
    f = int(e)
    width = []
    for i in range (f):
        """1 is horizontal, 2 is vertical. I am mostly looking for vertical lines, but I need the direction"""
        direction = 2
        print(i)
        if points[i * 8] == -1000:
            direction = 1

        else:
            direction = 2
        print(direction)
        width.append(direction)
        if direction == 1:
            width.append(abs(points[int((i * 8) + 1)] - points[int((i * 8) + 5)]))
        else:
            width.append(abs(points[(i * 8)] - points[(i * 8) + 4]))


    return width



line_detection(img)
print(points)
print(abs(points[(0 * 8) + 1] - points[(0 * 8) + 5]))
width = widths(points)
print(width)

def calculate_average(lst):
    if not lst:
        return None  # Return None for an empty list

    return sum(lst) / len(lst)

def middle(points, width):
    max_value = max(points)
    index_of_max = points.index(max_value) - 1
    line = []

    #Index of the max corresponds to the line in the order that they were solved. It needs to be multiplied by 8 to find the position of the line.

    if width[index_of_max % 8 - 1 ] == 1:
        #horizontal so y value is the average of the two extents of the line
        line = [ points[index_of_max * 8], calculate_average([points[index_of_max], points[index_of_max + 4]]),points[index_of_max + 2] , calculate_average([points[index_of_max + 2], points[index_of_max + 6]])]

    else:
        #vertical
        line = [calculate_average([points[index_of_max ], points[index_of_max + 4]]), points[index_of_max + 1], calculate_average([points[index_of_max + 2], points[index_of_max + 6]]), points[index_of_max + 3], ]
    
    res = []
    for item in line:
        res.append(round(item))

    # I need to return two touples
        
    

    print((res[0], res[1]), (res[2], res[3]))
    return (res[0], res[1]), (res[2], res[3])
pt1, pt2 = middle(points, width)

cv2.line(img, pt1, pt2, (0, 0, 255), 2)
cv2.line(img, (1000, 500), (-1000, 500), (0, 0, 255), 2)
cv2.imwrite('linesDetected.jpg', img)