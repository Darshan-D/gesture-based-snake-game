"""
This script merges both cameramodule and screenmodule
"""
import cv2
import pygame


from cameramodule import centre_tracked
from screenmodule import gameloop



#Setting up input stream location
#Currently set to webcam
cap = cv2.VideoCapture(0)

#Setting up drawing screen parameters
dis_height = 480
dis_width = 480

#Initialize Display
dis = pygame.display.set_mode((dis_width, dis_height))

#Set display window  
pygame.display.set_caption("Beta !")

#Setting the thickness of drawing stroke
snake_block = 5

#Setting the sensitiviy
threshold = 5

#Initial position of cursor
x1 = 50
y1 = 100

#Previous pos of coursour
pcx = 0
pcy = 0

#Game state
game_over = False


while not game_over:
    
    #Read the frame from the feed
    _, frame = cap.read()
    
    #Find the co-ordinates of centre of largest contour
    cx, cy = centre_tracked(frame)
    print("Coordinates of previous centre:", pcx, pcy)
    print("Coordinates of centre:", cx, cy)
    
    #If blue color not detected
    if cx == None:
        cx = pcx
        cy = pcy
        continue
    
    #If user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
    #Updating the screen        
    x1, y1 = gameloop(cx, cy, snake_block, pcx, pcy, x1, y1, threshold, dis)
    
    pcx = cx
    pcy = cy
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
pygame.quit()