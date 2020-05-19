"""
This script contains all the functions that are dependent on Pygame
"""

import pygame

def draw_snake(x1, y1, snake_block, dis):
    pygame.draw.rect(dis, (255, 0, 0), [x1, y1, snake_block, snake_block])
    

def gameloop(cx, cy, snake_block, pcx, pcy, x1, y1, threshold, dis):

    #Drawing on the screen
    draw_snake(x1, y1, snake_block, dis)
    
    #Updating the screen
    pygame.display.update()
            
    #Check on which direction it moved
    #Left
    if cx < pcx and cx != pcx and abs(pcx - cx) >= threshold:
        print("Left")
        x1 -= snake_block
        y1 += 0
     
    #Right    
    if cx > pcx  and cx != pcx and abs(cx - pcx) >= threshold:
        print("Right")
        x1 += snake_block
        y1 += 0
        
     
    #Up
    if cy < pcy and cy != pcy and abs(cy - pcy) >= threshold:
        print("Up")        
        x1 += 0
        y1 -= snake_block
        
   #Down     
    if cy > pcy and cy != pcy and abs(cy - pcy) >= threshold:
        print("Down")
        x1 += 0
        y1 += snake_block
        
    return (x1, y1)