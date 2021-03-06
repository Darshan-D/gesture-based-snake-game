"""
This script contains all the functions that are dependent on Open CV
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
    
    
    #Drawing the max area contour and its centre on frame along with few lines for UI
    cv2.drawContours(frame_copy, contours, maxcnt, (0,0,255), 2)
    cv2.circle(frame_copy, (cX, cY), 4, (0, 0, 255), -1)
    
    
    #Rendering centre co-ordinates on screen
    font = cv2.FONT_HERSHEY_SIMPLEX
    info = "Centre Co-ordinates"
    cv2.putText(frame_copy, info, (5,450), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
    centre = "X: " + str(cX) + "  Y: " + str(cY)
    cv2.putText(frame_copy, centre, (5,470), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
    
    
    #Rendering Contour Area on screen
    info = "Contour Area"
    cv2.putText(frame_copy, info, (530,450), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
    cntArea = str(maxcntArea)
    cv2.putText(frame_copy, cntArea, (530,470), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
    
    
    #Divided by 8th part of the width
    #Vertical Lines
    
    # ~~Disabled currently
    #cv2.line(frame_copy, (60,0), (60, 480), (0,255,0), 1)
    #cv2.line(frame_copy, (580,0), (580, 480), (0,255,0), 1)
    
    #Displaying it
    cv2.imshow("Tracked", frame_copy)
    
    return(cX, cY) 

#Experimental
def kalman_init():
#Arguments - None
#Returns - Initial Values of P_k, R, I

    P_k_prev = np.array([[4, 0], [0, 4]])
    X_k = np.array([[200], [150]])
    I = np.array([[1, 0], [0, 1]])
    
    return P_k_prev, I, X_k

#Experimental
def kalman_track(pcx, pcy, P_k_prev, I, X_k):
#Arguments - pcx, pcy, P_k_prev, R, I
#Returns - Expected centre co-ordinates of the largest contour of given color

    R = np.array([[9, 0], [0, 9]])
    Y = np.array([[pcx], [pcy]]) 
    K = (P_k_prev)/(P_k_prev - R)
    X_f = X_k + np.dot(K, (Y - X_k))
    P_k = np.dot((I - K), P_k_prev)
    P_k_prev = P_k
    X_k = X_f    
    
    return X_f, X_k

