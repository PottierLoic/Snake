# Snake
# Author : Loïc Pottier
# Creation date : 14/12/2022

# IMPORTS
from tkinter import *
import random

# CONSTANTS
GAME_WIDTH = 1400
GAME_HEIGHT = 800
SPEED = 50
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00CCCC"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self):
        self.bodySize = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE-1)) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE-1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def nextTurn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1

        label.config(text="Score : {}".format(score))
    
        canvas.delete("food")
    
        food = Food()

        # foodOk = False

        # while not foodOk:
        #     food = Food()
        #     for body_part in snake.coordinates:
        #         if food.coordinates[0] == body_part[0] and food.coordinates[1] == body_part[1]:
        #             canvas.delete("food")
        #     if food!=None:
        #         foodOk=True

    else:

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if checkCollisions(snake):
        gameOver()
    else:
        window.after(SPEED, nextTurn, snake, food)

def changeDirection(newDirection):
    global direction

    if newDirection == "left" and direction!="right":
        direction=newDirection
    elif newDirection == "right" and direction!="left":
        direction=newDirection
    elif newDirection == "up" and direction!="down":
        direction=newDirection
    elif newDirection == "down" and direction!="up":
        direction=newDirection

def checkCollisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    
    return False

def gameOver():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("consolas", 70), text="GAME OVER", fill="red", tag="gameover")

# Main window creation
window = Tk()
window.title("Snake AI")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text="Score : {}".format(score), font=("consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Key bindings
window.bind("<Left>", lambda event: changeDirection("left"))
window.bind("<Right>", lambda event: changeDirection("right"))
window.bind("<Up>", lambda event: changeDirection("up"))
window.bind("<Down>", lambda event: changeDirection("down"))

snake = Snake()
food = Food()

nextTurn(snake, food)

window.mainloop()