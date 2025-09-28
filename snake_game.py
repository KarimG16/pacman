"""
Snake Game
A classic Snake game implementation using Pygame.
Control the snake with arrow keys or WASD to eat food and grow longer.
"""

import pygame
import sys
import random

# Constants
GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE
FPS = 10  # Snake games typically run at 10 FPS for good gameplay

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)

class Snake:
    def __init__(self):
        # Start the snake in the center of the screen
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = (1, 0)  # Moving right initially
        self.grow = False
        
    def move(self):
        """Move the snake in the current direction"""
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        """Change the snake's direction (prevent 180-degree turns)"""
        # Prevent the snake from going backwards into itself
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self):
        """Check if the snake has collided with walls or itself"""
        head_x, head_y = self.body[0]
        
        # Check wall collision
        if (head_x < 0 or head_x >= GRID_WIDTH or 
            head_y < 0 or head_y >= GRID_HEIGHT):
            return True
        
        # Check self collision
        if (head_x, head_y) in self.body[1:]:
            return True
        
        return False
    
    def eat_food(self, food_pos):
        """Check if the snake has eaten food"""
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False
    
    def draw(self, screen):
        """Draw the snake on the screen"""
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:  # Head
                pygame.draw.rect(screen, DARK_GREEN, rect)
                pygame.draw.rect(screen, WHITE, rect, 2)
            else:  # Body
                pygame.draw.rect(screen, GREEN, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        """Generate a random position for the food"""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def respawn(self, snake_body):
        """Respawn food at a new position (avoiding snake body)"""
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
    
    def draw(self, screen):
        """Draw the food on the screen"""
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, WHITE, rect, 2)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.high_score = 0
        
    def update(self):
        """Update the game state"""
        if not self.game_over:
            # Move the snake
            self.snake.move()
            
            # Check for food collision
            if self.snake.eat_food(self.food.position):
                self.score += 10
                self.food.respawn(self.snake.body)
            
            # Check for collisions
            if self.snake.check_collision():
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
    
    def restart(self):
        """Restart the game"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def draw(self, screen):
        """Draw the game on the screen"""
        # Clear screen
        screen.fill(BLACK)
        
        # Draw grid lines (optional, for visual reference)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
        
        # Draw snake and food
        self.snake.draw(screen)
        self.food.draw(screen)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        screen.blit(high_score_text, (10, 50))
        
        # Draw game over message
        if self.game_over:
            game_over_font = pygame.font.Font(None, 48)
            game_over_text = game_over_font.render("GAME OVER!", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
            screen.blit(game_over_text, text_rect)
            
            restart_text = font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            screen.blit(restart_text, restart_rect)
        
        # Draw instructions
        if not self.game_over:
            instruction_font = pygame.font.Font(None, 24)
            instruction_text = instruction_font.render("Use Arrow Keys or WASD to move", True, WHITE)
            screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and game.game_over:
                    game.restart()
                elif not game.game_over:
                    # Movement controls
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game.snake.change_direction((1, 0))
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        game.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game.snake.change_direction((0, 1))
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

