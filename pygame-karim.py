import pygame
import sys

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 480, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pac-Man")
clock = pygame.time.Clock()

# Colors
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PELLET_COLOR = (255,215,0)

# --- Simple Map (0=empty, 1=wall, 2=pellet) ---
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,2,1,0,1,2,1,0,0,0,0,0,0,0,1,0,1,1,2,1],
    [1,2,1,0,1,2,1,0,1,1,1,1,1,0,1,0,0,1,2,1],
    [1,2,2,0,0,2,2,0,0,0,0,0,0,0,2,0,0,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

TILE = WIDTH // len(MAP[0])

# --- Pac-Man ---
class Pacman:
    def __init__(self):
        self.x = TILE + TILE//2
        self.y = TILE + TILE//2
        self.speed = 2
        self.dir = (0,0)
        self.next_dir = (0,0)
        self.radius = TILE//2 - 2

    def update(self):
        dx, dy = self.next_dir
        if can_move(self.x, self.y, dx, dy):
            self.dir = self.next_dir

        dx, dy = self.dir
        if can_move(self.x, self.y, dx, dy):
            self.x += dx*self.speed
            self.y += dy*self.speed

        # Eat pellet
        tx, ty = self.x // TILE, self.y // TILE
        if MAP[int(ty)][int(tx)] == 2:
            MAP[int(ty)][int(tx)] = 0

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

def can_move(x, y, dx, dy):
    nx = x + dx*2
    ny = y + dy*2
    tx = int(nx // TILE)
    ty = int(ny // TILE)
    if ty<0 or ty>=len(MAP) or tx<0 or tx>=len(MAP[0]):
        return False
    return MAP[ty][tx] != 1

pacman = Pacman()

# --- Main Loop ---
running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: pacman.next_dir = (-1,0)
            if event.key == pygame.K_RIGHT: pacman.next_dir = (1,0)
            if event.key == pygame.K_UP: pacman.next_dir = (0,-1)
            if event.key == pygame.K_DOWN: pacman.next_dir = (0,1)

    pacman.update()

    # Draw map
    for r,row in enumerate(MAP):
        for c,cell in enumerate(row):
            x = c*TILE
            y = r*TILE
            if cell == 1:
                pygame.draw.rect(screen, BLUE, (x,y,TILE,TILE))
            elif cell == 2:
                pygame.draw.circle(screen, PELLET_COLOR, (x+TILE//2, y+TILE//2), 4)

    pacman.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
