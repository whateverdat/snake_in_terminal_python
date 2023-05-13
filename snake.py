import sys
from random import randint, choice
from pytimedinput import timedKey
from time import sleep


board_width = 8
board_height = 8
game = False
current_direction = choice(['w', 'a', 's', 'd'])
food_location = [{'row': randint(4, board_width - 4), 'col': randint(4, board_height - 4)}]
snake_head = {'row': randint(4, board_width - 4), 'col': randint(4, board_height - 4)} 
snake_tail = []
obstacles = []
INCORRECT_TURN = {
    'w': 's',
    'a': 'd',
    's': 'w',
    'd': 'a'
}


def main():
    print("\033[H\033[J")
    inpt = timedKey('Simple Snake clone in Terminal, press any key to continue.', timeout=-1)
    if inpt:
        game()


def draw_board():
    print("\033[H\033[J")
    for col in range(board_height):
        for row in range(board_width):
            if snake_head == {'row': row, 'col': col} and snake_head in food_location:
                print('0', end='')
            elif {'row': row, 'col': col} in snake_tail:
                print('x', end='')
            elif {'row': row, 'col': col} in food_location:
                print('$', end='')
            elif {'row': row, 'col': col} in obstacles:
                print('#', end='')
            elif snake_head and col == snake_head['col'] and row == snake_head['row']:
                print('O', end='')
            elif col == 0:
                if row == board_width -1:
                    if col == 0:
                        print(f'#    Score: {len(snake_tail)}')
                    else:
                        print('#')
                else:
                    print('#', end='')
            elif row == board_width -1:
                print('#') 
            elif row == 0 or col == board_height -1:
                print('#', end='')
            else:    
                print(' ', end='')
            

def game():
    while game:
        movement()
        draw_board()
        if snake_head in food_location:
            add_tail()
            calculate_food(food_location.index(snake_head))
            calculate_obstacles()
        elif detect_collision():
            end_game()
        delay = float(0.5 - len(snake_tail) / 100)
        if delay < 0.20 : delay = 0.20
        direction, timed_out = timedKey('', timeout=delay)
        if direction in ['w', 'a', 's', 'd']:
            if direction != INCORRECT_TURN[globals()['current_direction']]:
                globals()['current_direction'] = direction


def movement():
    locations = []
    locations.append(snake_head)
    for tail in snake_tail:
        locations.append(tail)
    for idx, location in enumerate(locations):
        if idx == 0:
            store1 = location.copy()
            if current_direction == 'w':
                snake_head['col'] -= 1;
            elif current_direction == 's':
                snake_head['col'] += 1;
            elif current_direction == 'a':
                snake_head['row'] -= 1;
            elif current_direction == 'd':
                snake_head['row'] += 1;
        else:
            store2 = location
            snake_tail[idx-1] = store1.copy()
            store1 = store2


def calculate_food(idx):
    food_location.pop(idx)
    if len(snake_tail) != 0: 
        if len(snake_tail) % 5 == 0:
            enlarge_board()
        if len(snake_tail) % 10 == 0:
            for _ in range(((len(snake_tail) // 10)) + 1):
                while True:
                    new = {'row' : randint(1, board_width - 2), 'col' :randint(1, board_height -2)}
                    if new not in snake_tail and new != snake_head:
                        food_location.append(new)
                        break
            return
    while True:
        new = {'row' : randint(1, board_width - 2), 'col' :randint(1, board_height -2)}
        if new not in snake_tail and new != snake_head:
            food_location.append(new)
            break


def calculate_obstacles():
    if len(snake_tail) >= 20 and len(snake_tail) % 2 == 0:
        while True:
            new = {'row' : randint(1, board_width - 2), 'col' :randint(1, board_height -2)}
            if new not in snake_tail and new != snake_head:
                obstacles.append(new)
                break


def enlarge_board():
    if globals()['board_height'] < 24:  
        globals()['board_height'] += 4  
    if globals()['board_width'] < 64:
        globals()['board_width'] += 4 


def add_tail():
    snake_tail.append(food_location.copy())


def detect_collision():
    if snake_head in snake_tail or snake_head in obstacles or snake_head['col'] in [0, board_height -1] or snake_head['row'] in [0, board_width -1]:
        return True
    return False


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
