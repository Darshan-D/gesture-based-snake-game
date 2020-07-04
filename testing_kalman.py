from cameramodule import kalman_init, centre_tracked, kalman_track
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

P_k_prev, I, X_k = kalman_init()

while(cap.isOpened()):
    ret, frame=cap.read()
    if ret == True:
      cx, cy = centre_tracked(frame)
      print(cx, cy)
      X_f, X_k = kalman_track(cx, cy, P_k_prev, I, X_k)
      print(X_f)
      print(X_k)
      
      frame = cv2.flip(frame, 1)
      cv2.imshow('', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      
cap.release()
cv2.destroyAllWindows()