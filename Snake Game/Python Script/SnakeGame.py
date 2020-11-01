
from pygame import *
from time import sleep,time
from random import randint
import shelve

# Window setup
init()
window = display.set_mode((775,700))
display.set_caption("Snake Game 1.9")

# Pictures load up
snake_down = image.load('icons//SnakeDown.png')
snake_up = image.load('icons//SnakeUp.png')
snake_right = image.load('icons//SnakeRight.png')
snake_left = image.load('icons//SnakeLeft.png')
body_lr = image.load('icons//Snakelf.png')
body_ud = image.load('icons//Snakeud.png')
back_ground = image.load('icons//bgSnakeGame.png')
apple_food = image.load('icons//apple.png')

# Snake head
class Snake(object):
    def __init__(self,x,y):
        ''' Creating the attributes of the Snake '''
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.direction = "stop"
        self.speed = 30

    def draw(self):
        ''' Drawing the head in the screen '''
        if self.direction ==  "up" or self.direction == "stop":
            window.blit(snake_up,(self.x,self.y))
        if self.direction ==  "down":
            window.blit(snake_down,(self.x,self.y))
        if self.direction ==  "right":
            window.blit(snake_right,(self.x,self.y))
        if self.direction ==  "left":
            window.blit(snake_left,(self.x,self.y))

    def move(self):
        ''' Makes the snake move '''
        if self.direction ==  "up":
            self.y -= self.speed
        if self.direction ==  "down":
            self.y += self.speed
        if self.direction ==  "right":
            self.x += self.speed
        if self.direction ==  "left":
            self.x -= self.speed

# Snake body parts
class Snake_part(object):
    def __init__(self,x,y,direction):
        ''' Creating the attributes of the Snake part '''
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.direction = direction

    def draw(self):
        ''' Drawing the head in the screen '''
        if self.direction == "up" or self.direction == "down":
            window.blit(body_ud,(self.x, self.y))
        else:
            window.blit(body_lr,(self.x, self.y))

# Apple
class apple(object):
    def __init__(self):
        ''' Setting some attributes and picking randomly the first posetion '''
        self.x = randint(100,400)
        self.y = randint(80,200)
        self.width = 25
        self.height = 25

    def draw(self):
        ''' Drawing the apple in the screen '''
        window.blit(apple_food ,(self.x ,self.y))

    def change(self):
        ''' Changing the cordinates randomly '''
        self.x = randint(100,500)
        self.y = randint(60,620)

# Redraw function
def redraw():
    display.update() # Reseting the screen
    score_text = font.render(f"Score = {score}", 1, (0,0,139)) # Rendering the score and the high score 
    high_score_text = font.render(f"High Score = {high_score}", 1, (0,0,139))
    window.blit(back_ground,(0,0)) # Blitting the background image
    window.blit(score_text, (580,250)) # and the score and highscore
    window.blit(high_score_text, (540,300))
    food.draw() # and the food and the snake
    for part in parts:
        part.draw()
    snake.draw()
    
# Score set up
score = 0 # Initializing the score
datafile = shelve.open("data//highscore") # Getting the highscore from an shelve file 
high_score = datafile.get("highscore",0) 
datafile.close()
font = font.SysFont("Arial", 28, True) # Creating the font for the score 

# Main Program
snake = Snake(260,350) # Creating the head of the snake
parts = [snake] # Creating the list with the parts , the first part is the head
run = True # The run fralg used in the while loop
time_from_last_move = time() # Initializes the time
food = apple() # Creating the apple

while run:
    # User Quit Decision
    for i in event.get():
        if i.type == QUIT:
            run = False

    # Snake Movement
    keys = key.get_pressed()  # Get the state of the keys
    # If an arrow is presssed then the direction changes
    if keys[K_LEFT]: 
        snake.direction = "left"
    if keys[K_RIGHT]:
        snake.direction = "right"
    if keys[K_UP]:
        snake.direction = "up"
    if keys[K_DOWN]:
        snake.direction = "down"
        
    #Snake - Food reaction
    if snake.y < food.y + food.width and snake.y + snake.width > food.y and snake.x + snake.width > food.x and snake.x < food.x + food.width:
        food.change() # Change food's position

        score += 10 # Add points
        if score > high_score: # Checks if the score is bigger than the highscore
            high_score = score
            datafile = shelve.open("data//highscore")
            if datafile.get("highscore",0) < high_score: # Writes the new highscore in the file
            	datafile["highscore"] = high_score

        part = Snake_part(parts[-1].x, parts[-1].y, parts[-1].direction) # Add a snake part to the snake
        parts.append(part)
        
    

    #Snake - Snake Body reaction
    for part in parts[2:]: # All the part of the snake minus the first and the second 
        if snake.y < part.y + part.width and snake.y + snake.width > part.y and snake.x + snake.width > part.x and snake.x < part.x + part.width:    
            score = 0 # Player loses and game resets
            del parts[1:]
            snake.x = 250
            snake.y = 350
            snake.direction = "stop"

    #Snake - Borders reaction
    if snake.x < 40 or snake.x + snake.width > 530 or snake.y < 40 or snake.y + snake.width > 650:
        score = 0
        del parts[1:]
        snake.x = 250
        snake.y = 350
        snake.direction = "stop"

    if time() - time_from_last_move > 0.1: # Moves every 0.1 seconds
        for part in range(len(parts)-1,0,-1): # The whole body from the last part to the first by index
            parts[part].x = parts[part-1].x # Updating the position and the direction of the part
            parts[part].y = parts[part-1].y
            parts[part].direction = parts[part-1].direction
        snake.move() # Snake moves
        time_from_last_move = time()
    redraw() # Redraws the screen

quit() # Closes the window after player's quit dicision
    





    
