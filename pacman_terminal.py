import os
import sys

# Simple map: W = wall, . = pellet, space = empty
MAP = [
    list("WWWWWWWWWW"),
    list("W........W"),
    list("W.WWWW.W.W"),
    list("W.W....W.W"),
    list("W.WWWWWW.W"),
    list("W........W"),
    list("WWWWWWWWWW"),
]

# Pac-Man start position
pacman_x, pacman_y = 1, 1

def print_map():
    os.system('cls' if os.name == 'nt' else 'clear')
    for y, row in enumerate(MAP):
        line = ""
        for x, cell in enumerate(row):
            if x == pacman_x and y == pacman_y:
                line += "P"
            else:
                line += cell
        print(line)

def move(dx, dy):
    global pacman_x, pacman_y
    nx, ny = pacman_x + dx, pacman_y + dy
    if MAP[ny][nx] != "W":
        pacman_x, pacman_y = nx, ny
        # Eat pellet
        if MAP[ny][nx] == ".":
            MAP[ny][nx] = " "

def game_loop():
    print_map()
    while True:
        print("Move with W/A/S/D. Press Q to quit.")
        move_input = input().lower()
        if move_input == "w": move(0,-1)
        elif move_input == "s": move(0,1)
        elif move_input == "a": move(-1,0)
        elif move_input == "d": move(1,0)
        elif move_input == "q": 
            print("Bye!")
            sys.exit()
        print_map()

if __name__ == "__main__":
    game_loop()
