import sys
from random import randint, choice
from pytimedinput import timedKey
from time import sleep

# Vars
board_width = 8
board_height = 8
game = False
current_direction = choice(['w', 'a', 's', 'd'])
food_location = [{'row': randint(4, board_width - 4), 'col': randint(4, board_height - 4)}]
snake_head = {'row': randint(4, board_width - 4), 'col': randint(4, board_height - 4)} 
snake_tail = []
obstacles = []
INCORRECT_TURN = { # Constant dict to store incorrect turns
    'w': 's',      # Disallow opposite direction
    'a': 'd',
    's': 'w',
    'd': 'a'
}

# Interface 
def main():
    print("\033[H\033[J")
    inpt = timedKey('Simple Snake clone in Terminal, press any key to continue.', timeout=-1)
    if inpt:
        game()

# Nested for loops to print rows and columns
def draw_board():
    print("\033[H\033[J") # Clears terminal
    for col in range(board_height):
        for row in range(board_width):
            if snake_head == {'row': row, 'col': col} and snake_head in food_location: # Snake head eating food
                print('0', end='')
            elif {'row': row, 'col': col} in snake_tail: # Snake tail
                print('x', end='')
            elif {'row': row, 'col': col} in food_location: # Food
                print('$', end='')
            elif {'row': row, 'col': col} in obstacles: # Obstacle
                print('#', end='')
            elif snake_head and col == snake_head['col'] and row == snake_head['row']: # Snake head
                print('O', end='')
            elif col == 0: # Borders
                if row == board_width -1: 
                    print(f'#    Score: {len(snake_tail)}')
                else:
                    print('#', end='')
            elif row == board_width -1:
                print('#') 
            elif row == 0 or col == board_height -1:
                print('#', end='')
            else:    
                print(' ', end='') # Moveable area
            

def game():
    max_speed = False # Constant game speed
    while game:
        movement() # Move snake
        draw_board() # Then draw the board
        if snake_head in food_location: # Eating food
            add_tail()
            calculate_food(food_location.index(snake_head))
            calculate_obstacles()
        elif detect_collision(): # If collided
            end_game()
        if not max_speed: # Calculate speed, if max speed is not reached
            delay = float(0.5 - len(snake_tail) / 100)
            if delay < 0.25:
                max_speed = True   
        else:
            delay = 0.25 # Max speed
        direction, timed_out = timedKey('', timeout=delay) # Wait for input, continue if not provided
        if direction in ['w', 'a', 's', 'd']:
            if direction != INCORRECT_TURN[globals()['current_direction']]:
                globals()['current_direction'] = direction # Set direction when input


def movement():
    locations = [] # Store entire snake
    locations.append(snake_head)
    for tail in snake_tail:
        locations.append(tail)
    for idx, location in enumerate(locations):
        if idx == 0: # Snake head idx
            store1 = location.copy() # Store location then move snake
            if current_direction == 'w':
                snake_head['col'] -= 1;
            elif current_direction == 's':
                snake_head['col'] += 1;
            elif current_direction == 'a':
                snake_head['row'] -= 1;
            elif current_direction == 'd':
                snake_head['row'] += 1;
        else:
            store2 = location # Store location
            snake_tail[idx-1] = store1.copy() # Move tail 
            store1 = store2 # Pass the store to other iteration


def calculate_food(idx):
    food_location.pop(idx) # Remove eaten food
    length = len(snake_tail) 
    if length % 5 == 0: # Enlarge board every five food eaten
        enlarge_board()
    if length % 10 == 0 and length < 30: # Increase food count, max is 4
        for _ in range(((length // 10)) + 1):
            while True: # Loop until valid location is found
                new = {'row' : randint(1, board_width - 2), 'col' :randint(1, board_height -2)}
                if new not in snake_tail and new != snake_head and new not in obstacles and new not in food_location: # Find valid location
                    food_location.append(new)
                    break
        return
    while True: # No increase in food count
        new = {'row' : randint(1, board_width - 2), 'col' :randint(1, board_height -2)}
        if new not in snake_tail and new != snake_head and new not in obstacles and new not in food_location:
            food_location.append(new)
            break


def calculate_obstacles():
    length = len(snake_tail)
    if length >= 20 and length % 2 == 0: # Every other food eaten, after length passes 20
        while True:
            new = {'row' : randint(1, board_width - 2), 'col' :randint(1, board_height -2)}
            if new not in snake_tail and new != snake_head and new not in food_location and new not in obstacles: # Valid location
                obstacles.append(new)
                break

# Max board is 64 x 28
def enlarge_board():
    if globals()['board_height'] < 24:  
        globals()['board_height'] += 4  
    if globals()['board_width'] < 64:
        globals()['board_width'] += 4 


def add_tail():
    snake_tail.append(food_location.copy()) # Add eaten food location as new tail

# True when head collides with tail, border or obstacles
def detect_collision(): 
    if snake_head in snake_tail or snake_head in obstacles or snake_head['col'] in [0, board_height -1] or snake_head['row'] in [0, board_width -1]:
        return True
    return False

# End game animation, tail pieces disappear one by one
def end_game():
    score = len(snake_tail)
    globals()['snake_head'] = None
    draw_board()
    while snake_tail:
        snake_tail.pop(-1)
        sleep(0.1)
        draw_board()
    print(f'Game over, you scored {score} points!')
    sys.exit()


if __name__ == '__main__':
    main()
