"""
This script contains all the functions that are dependent on Open CV

>> More functions to be added soon
"""

import cv2
import numpy as np

def centre_tracked(frame):
#Arguments - input frame
#Returns - Centre co-ordinates of the largest contour of given color
    
    
    #Flipping the image just to make it not inverted
    frame = cv2.flip(frame, 1)
    width, height, _ = frame.shape
    
    #Bluring to remove noise
    blur_frame = cv2.GaussianBlur(frame, (5,5), cv2.BORDER_DEFAULT)

    #Converting to HSV color space
    hsv = cv2.cvtColor(blur_frame, cv2.COLOR_BGR2HSV)
    
    #Setting the range for blue color in HSV color space
    #Change this as per the color you want to track
    lower_value=np.array([100, 50, 50])
    upper_value=np.array([130, 255, 255])
    
    #Making a mask for blue color
    mask=cv2.inRange(hsv, lower_value, upper_value)
    mask=cv2.erode(mask, None, iterations=2)
    mask-cv2.dilate(mask, None, iterations=2)
    
    #Finding the contours in it
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Making a copy of the original frame to draw stuff on
    frame_copy = frame.copy()
    
    #Finding the contour with max area
    maxcntArea = 0
    maxcnt = 0

    for i,c in enumerate(contours):
        area = cv2.contourArea(c)
        if area > maxcntArea:
            maxcntArea = area
            maxcnt = i    
            
    #If blue color not found in frame
    if maxcnt < 1 :
        print("***Target not found")
        return(None, None)
    
    
    c = contours[maxcnt]
    
    print("\n\n-----------------Next Frame")
    
    
    #Finding the centre of the contour having largest area
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"]) 
    print("Cx:", cX)
    print("Cy:", cY)
    
    #Drawing the max area contour and its centre on frame along with few lines for UI
    cv2.drawContours(frame_copy, contours, maxcnt, (0,0,255), 2)
    cv2.circle(frame_copy, (cX, cY), 4, (0, 0, 255), -1)
    
    #Divided by 8th part of the width
    #Vertical Lines
    
    # ~~Disabled currently
    #cv2.line(frame_copy, (60,0), (60, 480), (0,255,0), 1)
    #cv2.line(frame_copy, (580,0), (580, 480), (0,255,0), 1)
    
    #Displaying it
    cv2.imshow("Tracked", frame_copy)
    
    return(cX, cY) 
