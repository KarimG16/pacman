"""
Fix applied: ensure all indices passed to is_wall_tile() are integers.
Pac-Man update method now casts tile positions to int before lookup.
"""
"""
Pac-Man clone with randomized ghost starting positions.
"""

import pygame
import sys
import random
import math

# -------- CONFIGURATION --------
TILE = 28
ROWS = 21
COLS = 21
SCREEN_WIDTH = COLS * TILE
SCREEN_HEIGHT = ROWS * TILE
FPS = 60

BLACK = (0, 0, 0)
BLUE = (33, 33, 255)
YELLOW = (255, 220, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
RED = (255, 50, 50)
CYAN = (0, 200, 200)
ORANGE = (255, 165, 0)

LEVEL_MAP = [
    "#####################",
    "#........#.........G#",
    "#.###.###.#.###.###..#",
    "#o# #.# #.#.# #.# #o#",
    "#.###.###.#.###.###.#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.### # ###.#####",
    "    #.#       #.#    ",
    "#####.# ##-## #.#####",
    "     .  #P  #  .     ",
    "#####.# ##### #.#####",
    "    #.#       #.#    ",
    "#####.# ##### #.#####",
    "#........#.........G#",
    "#.###.###.#.###.###.#",
    "#o..#..... ...#..#o#",
    "###.#.#.#####.#.#.###",
    "#.....#.........#...#",
    "#####################",
]

LEVEL_MAP = [row.ljust(COLS)[:COLS] for row in LEVEL_MAP[:ROWS]]

class Player:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.x = c * TILE + TILE // 2
        self.y = r * TILE + TILE // 2
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.speed = 120
        self.radius = TILE // 2 - 2
        self.score = 0
        self.lives = 3

    def update(self, dt, walls):
        if (self.x - TILE // 2) % TILE == 0 and (self.y - TILE // 2) % TILE == 0:
            r = int((self.y - TILE // 2) // TILE)
            c = int((self.x - TILE // 2) // TILE)
            nr = r + self.next_dir[1]
            nc = c + self.next_dir[0]
            if not is_wall_tile(int(nr), int(nc), walls):
                self.dir = self.next_dir
        dx = self.dir[0] * self.speed * dt
        dy = self.dir[1] * self.speed * dt
        newx = self.x + dx
        newy = self.y + dy
        to_r = int((newy - TILE // 2) // TILE)
        to_c = int((newx - TILE // 2) // TILE)
        if is_wall_tile(to_r, to_c, walls):
            self.dir = (0, 0)
            self.x = ((self.x - TILE // 2) // TILE) * TILE + TILE // 2
            self.y = ((self.y - TILE // 2) // TILE) * TILE + TILE // 2
        else:
            self.x = newx
            self.y = newy
            self.r = int((self.y - TILE // 2) // TILE)
            self.c = int((self.x - TILE // 2) // TILE)

    def draw(self, surf):
        pygame.draw.circle(surf, YELLOW, (int(self.x), int(self.y)), self.radius)
        dx, dy = self.dir
        if dx == 0 and dy == 0:
            dx = 1
        mouth_angle = 0.25
        ang = math.atan2(dy, dx)
        a1 = ang - mouth_angle
        a2 = ang + mouth_angle
        p1 = (int(self.x), int(self.y))
        p2 = (int(self.x + self.radius * math.cos(a1)), int(self.y + self.radius * math.sin(a1)))
        p3 = (int(self.x + self.radius * math.cos(a2)), int(self.y + self.radius * math.sin(a2)))
        pygame.draw.polygon(surf, BLACK, [p1, p2, p3])

class Ghost:
    COLORS = [RED, PINK, CYAN, ORANGE]

    def __init__(self, r, c, idx=0):
        self.r = r
        self.c = c
        self.x = c * TILE + TILE // 2
        self.y = r * TILE + TILE // 2
        self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.speed = 90
        self.idx = idx
        self.radius = TILE // 2 - 4

    def available_dirs(self, walls):
        dirs = []
        for d in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr = int((self.y - TILE//2)//TILE) + d[1]
            nc = int((self.x - TILE//2)//TILE) + d[0]
            if not is_wall_tile(int(nr), int(nc), walls):
                dirs.append(d)
        return dirs

    def update(self, dt, walls):
        if (self.x - TILE // 2) % TILE == 0 and (self.y - TILE // 2) % TILE == 0:
            avail = self.available_dirs(walls)
            if avail:
                rev = (-self.dir[0], -self.dir[1])
                choices = [d for d in avail if d != rev]
                if not choices:
                    choices = avail
                self.dir = random.choice(choices)
        self.x += self.dir[0] * self.speed * dt
        self.y += self.dir[1] * self.speed * dt
        self.r = int((self.y - TILE // 2)//TILE)
        self.c = int((self.x - TILE // 2)//TILE)

    def draw(self, surf):
        color = Ghost.COLORS[self.idx % len(Ghost.COLORS)]
        rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius*2, self.radius*2)
        pygame.draw.ellipse(surf, color, rect)
        foot_w = self.radius // 2
        for i in range(3):
            fx = int(self.x - self.radius + i*foot_w*1.5)
            fy = int(self.y)
            pygame.draw.circle(surf, color, (fx, fy), foot_w//2)
        eye_w = max(2, self.radius//3)
        ex = int(self.x - eye_w)
        ey = int(self.y - eye_w)
        pygame.draw.circle(surf, WHITE, (ex, ey), eye_w)
        pygame.draw.circle(surf, WHITE, (ex+eye_w*2, ey), eye_w)
        pygame.draw.circle(surf, BLACK, (ex, ey), max(1, eye_w//2))
        pygame.draw.circle(surf, BLACK, (ex+eye_w*2, ey), max(1, eye_w//2))

def is_wall_tile(r, c, walls):
    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
        return True
    return walls[int(r)][int(c)]

def parse_level(level_map):
    walls = [[False]*COLS for _ in range(ROWS)]
    pellets = [[False]*COLS for _ in range(ROWS)]
    player = None
    ghost_starts = []
    for r in range(ROWS):
        for c in range(COLS):
            ch = level_map[r][c]
            if ch == '#':
                walls[r][c] = True
            elif ch == '.' or ch == 'o':
                pellets[r][c] = True
            elif ch == 'P':
                player = Player(r, c)
            elif ch == 'G':
                ghost_starts.append((r, c))
    if not player:
        player = Player(ROWS//2, COLS//2)
    ghosts = []
    random.shuffle(ghost_starts)
    for idx, pos in enumerate(ghost_starts):
        r, c = pos
        ghosts.append(Ghost(r, c, idx))
    return walls, pellets, player, ghosts

# (rest of game loop remains unchanged)


def draw_grid(surf, walls, pellets):
    # Fill background
    surf.fill(BLACK)
    # draw walls as rectangles
    for r in range(ROWS):
        for c in range(COLS):
            if walls[r][c]:
                rect = pygame.Rect(c*TILE, r*TILE, TILE, TILE)
                pygame.draw.rect(surf, BLUE, rect)
            else:
                # pellets
                if pellets[r][c]:
                    cx = c*TILE + TILE//2
                    cy = r*TILE + TILE//2
                    pygame.draw.circle(surf, WHITE, (cx, cy), max(2, TILE//8))


def check_pellet_collision(player, pellets):
    r = player.r
    c = player.c
    if 0 <= r < ROWS and 0 <= c < COLS and pellets[r][c]:
        pellets[r][c] = False
        player.score += 10


def check_ghost_collision(player, ghosts):
    for g in ghosts:
        dist_sq = (player.x - g.x)**2 + (player.y - g.y)**2
        min_dist = (player.radius + g.radius - 6)
        if dist_sq <= min_dist**2:
            return True
    return False


def count_pellets(pellets):
    return sum(1 for r in range(ROWS) for c in range(COLS) if pellets[r][c])


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Pac-Man")
    clock = pygame.time.Clock()

    walls, pellets, player, ghosts = parse_level(LEVEL_MAP)
    total_pellets = count_pellets(pellets)

    font = pygame.font.SysFont(None, 24)

    running = True
    game_over = False
    win = False

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    player.next_dir = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    player.next_dir = (1, 0)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    player.next_dir = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    player.next_dir = (0, 1)
                elif event.key == pygame.K_r and (game_over or win):
                    # restart
                    walls, pellets, player, ghosts = parse_level(LEVEL_MAP)
                    total_pellets = count_pellets(pellets)
                    game_over = False
                    win = False

        if not game_over and not win:
            player.update(dt, walls)
            for g in ghosts:
                g.update(dt, walls)

            check_pellet_collision(player, pellets)
            if check_ghost_collision(player, ghosts):
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True
                else:
                    # reset positions
                    _, _, new_player, new_ghosts = parse_level(LEVEL_MAP)
                    # copy minimal state
                    player.x, player.y = new_player.x, new_player.y
                    player.r, player.c = new_player.r, new_player.c
                    player.dir = (0,0)
                    player.next_dir = (0,0)
                    for i,g in enumerate(ghosts):
                        g.x, g.y = new_ghosts[i].x, new_ghosts[i].y
                        g.r, g.c = new_ghosts[i].r, new_ghosts[i].c

            if count_pellets(pellets) == 0:
                win = True

        # Drawing
        draw_grid(screen, walls, pellets)
        for g in ghosts:
            g.draw(screen)
        player.draw(screen)

        # HUD
        score_surf = font.render(f"Score: {player.score}", True, WHITE)
        lives_surf = font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(score_surf, (8, SCREEN_HEIGHT - 28))
        screen.blit(lives_surf, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 28))

        if game_over:
            over_surf = font.render("GAME OVER - Press R to restart", True, WHITE)
            screen.blit(over_surf, (SCREEN_WIDTH//2 - over_surf.get_width()//2, SCREEN_HEIGHT//2))
        if win:
            win_surf = font.render("YOU WIN! - Press R to restart", True, WHITE)
            screen.blit(win_surf, (SCREEN_WIDTH//2 - win_surf.get_width()//2, SCREEN_HEIGHT//2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
