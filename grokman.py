import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PACMAN_SIZE = 40
PACMAN_SPEED = 5
DOT_SIZE = 10
BG_COLOR = (0, 0, 0)       # Black
PACMAN_COLOR = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stupid Pacman - No Ghosts, No Map")

# Pacman starting position
pacman_x = SCREEN_WIDTH // 2
pacman_y = SCREEN_HEIGHT // 2

# List of dots (random positions for stupidity)
dots = []
for _ in range(50):  # More dots, randomly placed
    x = random.randint(20, SCREEN_WIDTH - 20)
    y = random.randint(20, SCREEN_HEIGHT - 20)
    dots.append((x, y, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))  # Random color

# Score
score = 0
font = pygame.font.Font(None, 36)

# Stupid mode: Pacman changes size and color randomly sometimes
stupid_timer = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_x -= PACMAN_SPEED
    if keys[pygame.K_RIGHT]:
        pacman_x += PACMAN_SPEED
    if keys[pygame.K_UP]:
        pacman_y -= PACMAN_SPEED
    if keys[pygame.K_DOWN]:
        pacman_y += PACMAN_SPEED

    # Boundary checks
    pacman_x = max(0, min(pacman_x, SCREEN_WIDTH - PACMAN_SIZE))
    pacman_y = max(0, min(pacman_y, SCREEN_HEIGHT - PACMAN_SIZE))

    # Check for dot collection
    pacman_rect = pygame.Rect(pacman_x, pacman_y, PACMAN_SIZE, PACMAN_SIZE)
    new_dots = []
    for dot in dots:
        dot_rect = pygame.Rect(dot[0] - DOT_SIZE // 2, dot[1] - DOT_SIZE // 2, DOT_SIZE, DOT_SIZE)
        if pacman_rect.colliderect(dot_rect):
            score += random.randint(1, 50)  # Random points for stupidity
            stupid_timer = 60  # Trigger stupid mode
        else:
            new_dots.append(dot)
    dots = new_dots

    # Stupid mode logic
    if stupid_timer > 0:
        stupid_timer -= 1
        current_pacman_size = random.randint(20, 60)
        current_pacman_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        current_pacman_size = PACMAN_SIZE
        current_pacman_color = PACMAN_COLOR

    # Draw background
    screen.fill(BG_COLOR)

    # Draw Pacman (random shape sometimes: circle or rect)
    if random.random() < 0.5:  # 50% chance to be rect for stupidity
        pygame.draw.rect(screen, current_pacman_color, (pacman_x, pacman_y, current_pacman_size, current_pacman_size))
    else:
        pygame.draw.circle(screen, current_pacman_color, (pacman_x + current_pacman_size // 2, pacman_y + current_pacman_size // 2), current_pacman_size // 2)

    # Draw dots with random colors
    for dot in dots:
        pygame.draw.circle(screen, dot[2], (dot[0], dot[1]), DOT_SIZE // 2)

    # Draw score
    score_text = font.render(f"Stupid Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Stupid text overlay sometimes
    if random.random() < 0.1:  # 10% chance per frame
        stupid_text = font.render("EVERYTHING IS STUPID!", True, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        screen.blit(stupid_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    # Update display
    pygame.display.flip()

    # Cap FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()