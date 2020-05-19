"""
Gestured Based Snake Game 
Prototype 1.1


Further imporvements that can be made:-
> Change in the cond for dir change
> See if optical flow can help
"""

import pygame
import random
import cv2

#This module helps to track the colors and find the centre of the object
from cameramodule import centre_tracked

#Initializing the input stream
cap = cv2.VideoCapture(0)

#Sensitivity
threshold = 7

#Initializing Pygame
pygame.init()

#RGB values of colors
black = (0, 0, 0)
green = (0, 255, 0)

#Pygame window size
dis_width = 400
dis_height = 300

#Initializing pygame display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('NOT a FAce snaKe')

clock = pygame.time.Clock()

#Size of Snake and it's speed
snake_block = 10
snake_speed = 20
 
font_style = pygame.font.SysFont("bahnschrift", 15)
score_font = pygame.font.SysFont("comicsansms", 20)


flag = "start"
 
 
def Your_score(score):
    #Used to render the score on screen
    value = score_font.render("Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    #Used to draw snake on screen
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    #Used to dispaly the end screen text
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
    
    
def values(x1, y1, cx, cy):
    #Prints previous and current centre co-ordinates ~ helps in debugging
    print("x1:", x1)
    print("y1:", y1)
    print("cx:", cx)
    print("cy:", cy)
    
def pause():
    #Called when the game is paused
    paused = True
    print("Paused")
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
    
    
def gameLoop(flag):
    #Main game loop
    
    #Initialize basic parameters
    game_over = False
    game_close = False
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1

    #Choose x and y coordinate of the foood randomly
    foodx = round(random.randrange(0, dis_width - snake_block)/ 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block)/ 10.0) * 10.0

    
    while not game_over:
 
        while game_close == True:
            
            #When player gets out
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", green)
            value = score_font.render("Your Score: " + str(Length_of_snake - 1), True, green)
            dis.blit(value, [0, 0])
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:                    
                    #Check for which key is pressed
                    
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                
                    if event.key == pygame.K_c:
                        flag = "start"
                        gameLoop(flag)

        #Read from the input video stream
        _, frame = cap.read()
    
        #Get centre coordinates of largest contour of set color
        cx, cy = centre_tracked(frame)    

        #If object is not tracked then go for next iteration
        if cx == None:
            cx = x1
            cy = y1
            continue
        
        
        for event in pygame.event.get():
            
            #Check for quit or pause
            if event.type == pygame.QUIT:
                game_over = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    mesg = score_font.render("PAUSED", True, black)
                    dis.blit(mesg, [300, 275])                    
                    pygame.display.update()
                    pause()
           
         
        #Compare x  and y coordinates with previous x and y coordinates 
        #to determine the direction of the movement
        
        if cx < x1 and abs(cx - x1) >= threshold and flag != "left":
            print("Left")
            x1_change = -snake_block
            y1_change = 0
            flag = "left"
            
            
        elif cx > x1 and abs(cx - x1) >= threshold and flag != "right":
            print("Right")
            x1_change = snake_block
            y1_change = 0
            flag = "right"
            
            
        elif cy < y1 and abs(cy - y1) >= threshold and flag != "up":
            print("Up")
            y1_change = -snake_block
            x1_change = 0
            flag = "up"
            
            
        elif cy > y1 and abs(cy - y1) >= threshold and flag != "down":
            print("Down")
            y1_change = snake_block
            x1_change = 0
            flag = "down"
            
        if x1 == x1_change and y1 == y1_change:
            print("No change in dir")
            
            
        #If touched the corners of the screen
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
    
        x1 += x1_change
        y1 += y1_change
        
        dis.fill(green)
        pygame.draw.rect(dis, black, [foodx, foody, snake_block, snake_block])
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()

        #Check if the food eaten
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
        
            
        clock.tick(snake_speed)
    
    #Release the cap buffer
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()
 
#Calling the game loop function
gameLoop(flag)
