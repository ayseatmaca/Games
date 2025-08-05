import tkinter
import random


ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE* ROWS
WINDOW_HEIGHT = TILE_SIZE* COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y




#game window
window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black", borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

#center the wındıw
witndow_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2 - witndow_width/ 2))
window_y = int((screen_height/2 - window_height/ 2))
#format the window size (width x height + x_offset + y_offset )
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}")

#initialize game
snake = Tile(5* TILE_SIZE, 5* TILE_SIZE) #single tile , snake's head
food = Tile(10* TILE_SIZE, 10* TILE_SIZE)  # food tile
snake_body = []  # List to hold snake body segments
velocity_x = 0
velocity_y = 0
game_over = False
score = 0

def reset_game():
    global snake, food, snake_body, velocity_x, velocity_y, game_over, score
    snake.x = 5 * TILE_SIZE
    snake.y = 5 * TILE_SIZE
    food.x = 10 * TILE_SIZE
    food.y = 10 * TILE_SIZE
    snake_body.clear()
    velocity_x = 0
    velocity_y = 0
    game_over = False
    score = 0

def on_key_press(event):
    global velocity_x, velocity_y, game_over
    if game_over and event.keysym == "space":
        reset_game()
        return
    if game_over:
        return
    if event.keysym == "Up" and velocity_y != 1:
        velocity_x = 0
        velocity_y = -1
    elif event.keysym == "Down" and velocity_y != -1:
        velocity_x = 0
        velocity_y = 1
    elif event.keysym == "Left" and velocity_x != 1:
        velocity_x = -1
        velocity_y = 0
    elif event.keysym == "Right" and velocity_x != -1:
        velocity_x = 1
        velocity_y = 0

def move():
    global snake,game_over, snake_body, food,score
    if game_over:
        return
    
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # collision with food
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        # Generate new food position
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1
        # Add a new segment to the snake body
        

    #uptade snake body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]   
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:  
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y 




    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE


def draw():
    global snake, snake_body, food, game_over, score
    move()  # Move the snake
    #draw snake

    canvas.delete("all")  # Clear the canvas
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")
    
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green")
    

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="lime green")

    if game_over:
        canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", fill="white", font=("Arial", 20))
        canvas.create_text(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + 30, text=f"Score: {score}", fill="red", font=("Arial", 16))
        canvas.create_text(WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) + 60, text="Press space for new game", fill="red", font=("Arial", 14))
    else:
        canvas.create_text(60, 15, font=("Arial", 14), text=f"Score: {score}", fill="white")
    window.after(100, draw)  # Redraw every 100 milliseconds


draw()  # Start the drawing loop

window.bind("<KeyPress>", on_key_press)
window.mainloop()