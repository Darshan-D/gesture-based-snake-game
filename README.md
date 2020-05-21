# gesture-based-snake-game
We use OpenCV to track the motion of an object and then control the snake accordingly.

In this project we control snake from the classic snake game using the gesture of an object of specific color.
If the centre of the object moves left relative to the prevous centre position the snake will also move left.

## Pipeline
1. Detect the object on the basis of color
2. Find the centre of the object
3. Compare this centre with previous centre to find the change in direction
4. Change the direction of the snake accordingly


### Dependencies
1. OpenCV
2. Pygame
3. Numpy


### Note
- As of now it by default works with blue color, you can change which color it detects by changing the code
- The snake can't eat itself. This is made like this because the centre co-ordinates won't be steady due to noise.
