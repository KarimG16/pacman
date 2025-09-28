"""
Simple Pacman Game
A basic Pacman implementation with a consistent map and Pacman character.
Map regenerates every time you win or die.
"""

import pygame
import sys
import random
import math

# Constants
TILE_SIZE = 30
MAP_WIDTH = 21
MAP_HEIGHT = 21
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = TILE_SIZE // 2 - 3
        self.speed = 120  # pixels per second
        self.direction = (0, 0)  # (dx, dy)
        self.next_direction = (0, 0)
        self.score = 0
        self.lives = 3
        
    def update(self, dt, walls):
        # Always allow direction changes for now
        if self.next_direction != (0, 0):
            self.direction = self.next_direction
            
        # Move Pacman
        dx = self.direction[0] * self.speed * dt
        dy = self.direction[1] * self.speed * dt
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check wall collisions
        if not self.check_wall_collision(new_x, new_y, walls):
            self.x = new_x
            self.y = new_y
        else:
            # Stop movement if hitting a wall
            self.direction = (0, 0)
            # Snap to grid
            self.x = round(self.x / TILE_SIZE) * TILE_SIZE
            self.y = round(self.y / TILE_SIZE) * TILE_SIZE
    
    def can_change_direction(self, walls):
        # Check if Pacman is aligned with the grid
        grid_x = round(self.x / TILE_SIZE) * TILE_SIZE
        grid_y = round(self.y / TILE_SIZE) * TILE_SIZE
        return abs(self.x - grid_x) < 5 and abs(self.y - grid_y) < 5
    
    def check_wall_collision(self, x, y, walls):
        # Get the tile coordinates
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        # Check bounds
        if tile_x < 0 or tile_x >= MAP_WIDTH or tile_y < 0 or tile_y >= MAP_HEIGHT:
            return True
            
        # Check if it's a wall
        return walls[tile_y][tile_x]
    
    def get_grid_position(self):
        return (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
    
    def draw(self, screen):
        # Draw Pacman body
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        
        # Draw mouth
        if self.direction != (0, 0):
            dx, dy = self.direction
            if dx == 0 and dy == 0:
                dx = 1  # Default direction for mouth
            
            # Calculate mouth angle
            angle = math.atan2(dy, dx)
            mouth_angle = 0.4  # Half of mouth opening
            
            # Calculate mouth points
            p1 = (int(self.x), int(self.y))
            p2_x = int(self.x + self.radius * math.cos(angle - mouth_angle))
            p2_y = int(self.y + self.radius * math.sin(angle - mouth_angle))
            p3_x = int(self.x + self.radius * math.cos(angle + mouth_angle))
            p3_y = int(self.y + self.radius * math.sin(angle + mouth_angle))
            
            # Draw mouth triangle
            pygame.draw.polygon(screen, BLACK, [p1, (p2_x, p2_y), (p3_x, p3_y)])

class Ghost:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.radius = TILE_SIZE // 2 - 3
        self.speed = 80  # Slightly slower than Pacman
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.direction_timer = 0
        self.direction_change_interval = 1.0  # Change direction every second
        self.last_direction_change = 0
        
    def update(self, dt, walls, pacman_pos):
        # Update direction change timer
        self.direction_timer += dt
        
        # Change direction periodically or when hitting a wall
        if (self.direction_timer - self.last_direction_change > self.direction_change_interval or 
            self.check_wall_collision(self.x + self.direction[0] * self.speed * dt, 
                                    self.y + self.direction[1] * self.speed * dt, walls)):
            self.choose_new_direction(walls, pacman_pos)
            self.last_direction_change = self.direction_timer
        
        # Move ghost
        dx = self.direction[0] * self.speed * dt
        dy = self.direction[1] * self.speed * dt
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check wall collisions
        if not self.check_wall_collision(new_x, new_y, walls):
            self.x = new_x
            self.y = new_y
        else:
            # Stop movement if hitting a wall and choose new direction
            self.choose_new_direction(walls, pacman_pos)
            # Snap to grid
            self.x = round(self.x / TILE_SIZE) * TILE_SIZE
            self.y = round(self.y / TILE_SIZE) * TILE_SIZE
    
    def choose_new_direction(self, walls, pacman_pos):
        """Choose a new direction based on simple AI"""
        # Get current grid position
        grid_x = int(self.x // TILE_SIZE)
        grid_y = int(self.y // TILE_SIZE)
        
        # Available directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        valid_directions = []
        
        # Check which directions are valid (no walls)
        for dx, dy in directions:
            new_x = grid_x + dx
            new_y = grid_y + dy
            
            # Check bounds
            if (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT and 
                not walls[new_y][new_x]):
                valid_directions.append((dx, dy))
        
        # If no valid directions, don't move
        if not valid_directions:
            self.direction = (0, 0)
            return
        
        # Simple AI: sometimes move towards Pacman, sometimes random
        pacman_grid_x, pacman_grid_y = pacman_pos
        distance_to_pacman = math.sqrt((grid_x - pacman_grid_x)**2 + (grid_y - pacman_grid_y)**2)
        
        # 30% chance to move towards Pacman if close, otherwise random
        if distance_to_pacman < 5 and random.random() < 0.3:
            # Try to move towards Pacman
            best_direction = None
            best_distance = float('inf')
            
            for dx, dy in valid_directions:
                new_x = grid_x + dx
                new_y = grid_y + dy
                distance = math.sqrt((new_x - pacman_grid_x)**2 + (new_y - pacman_grid_y)**2)
                if distance < best_distance:
                    best_distance = distance
                    best_direction = (dx, dy)
            
            if best_direction:
                self.direction = best_direction
            else:
                self.direction = random.choice(valid_directions)
        else:
            # Random movement
            self.direction = random.choice(valid_directions)
    
    def check_wall_collision(self, x, y, walls):
        """Check if the ghost would collide with a wall at the given position"""
        tile_x = int(x // TILE_SIZE)
        tile_y = int(y // TILE_SIZE)
        
        # Check bounds
        if tile_x < 0 or tile_x >= MAP_WIDTH or tile_y < 0 or tile_y >= MAP_HEIGHT:
            return True
            
        # Check if it's a wall
        return walls[tile_y][tile_x]
    
    def get_grid_position(self):
        return (int(self.x // TILE_SIZE), int(self.y // TILE_SIZE))
    
    def draw(self, screen):
        # Draw ghost body (slightly different shape than Pacman)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw ghost bottom (wavy bottom)
        bottom_y = int(self.y) + self.radius
        wave_points = []
        for i in range(0, self.radius * 2, 4):
            x_offset = i - self.radius
            wave_y = bottom_y + math.sin(i * 0.5) * 3
            wave_points.append((int(self.x) + x_offset, int(wave_y)))
        
        if wave_points:
            pygame.draw.polygon(screen, self.color, wave_points)
        
        # Draw eyes
        eye_offset = self.radius // 3
        pygame.draw.circle(screen, WHITE, 
                         (int(self.x - eye_offset), int(self.y - eye_offset)), 3)
        pygame.draw.circle(screen, WHITE, 
                         (int(self.x + eye_offset), int(self.y - eye_offset)), 3)
        
        # Draw eye pupils
        pygame.draw.circle(screen, BLACK, 
                         (int(self.x - eye_offset), int(self.y - eye_offset)), 1)
        pygame.draw.circle(screen, BLACK, 
                         (int(self.x + eye_offset), int(self.y - eye_offset)), 1)

class Game:
    def __init__(self):
        self.walls = []
        self.pellets = []
        self.pacman = None
        self.ghosts = []
        self.total_pellets = 0
        self.game_over = False
        self.win = False
        self.life_lost_message = ""
        self.life_lost_timer = 0
        self.life_lost_duration = 2.0  # Show message for 2 seconds
        self.generate_map()
    
    def generate_map(self):
        """Generate a consistent map layout"""
        # Create a simple maze pattern
        self.walls = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.pellets = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        # Create border walls
        for x in range(MAP_WIDTH):
            self.walls[0][x] = True
            self.walls[MAP_HEIGHT-1][x] = True
        for y in range(MAP_HEIGHT):
            self.walls[y][0] = True
            self.walls[y][MAP_WIDTH-1] = True
        
        # Add some internal walls to create a maze
        # Horizontal walls
        for x in range(3, MAP_WIDTH-3, 4):
            for y in range(3, MAP_HEIGHT-3, 2):
                if random.random() < 0.7:  # 70% chance of wall
                    self.walls[y][x] = True
                    if x+1 < MAP_WIDTH:
                        self.walls[y][x+1] = True
        
        # Vertical walls
        for y in range(3, MAP_HEIGHT-3, 4):
            for x in range(3, MAP_WIDTH-3, 2):
                if random.random() < 0.7:  # 70% chance of wall
                    self.walls[y][x] = True
                    if y+1 < MAP_HEIGHT:
                        self.walls[y+1][x] = True
        
        # Place pellets in empty spaces
        for y in range(1, MAP_HEIGHT-1):
            for x in range(1, MAP_WIDTH-1):
                if not self.walls[y][x]:
                    self.pellets[y][x] = True
        
        # Place Pacman in the center
        center_x = MAP_WIDTH // 2
        center_y = MAP_HEIGHT // 2
        self.pacman = Pacman(center_x * TILE_SIZE + TILE_SIZE // 2, 
                            center_y * TILE_SIZE + TILE_SIZE // 2)
        
        # Create ghosts
        self.ghosts = []
        ghost_colors = [RED, PINK, CYAN, ORANGE]
        ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
        
        # Find empty positions for ghosts (avoid center area where Pacman is)
        ghost_positions = []
        for y in range(1, MAP_HEIGHT-1):
            for x in range(1, MAP_WIDTH-1):
                if (not self.walls[y][x] and 
                    abs(x - center_x) > 2 and abs(y - center_y) > 2):  # Keep ghosts away from Pacman
                    ghost_positions.append((x, y))
        
        # Create 4 ghosts at random positions
        for i in range(min(4, len(ghost_positions))):
            x, y = random.choice(ghost_positions)
            ghost_positions.remove((x, y))  # Remove to avoid duplicates
            ghost = Ghost(x * TILE_SIZE + TILE_SIZE // 2, 
                         y * TILE_SIZE + TILE_SIZE // 2,
                         ghost_colors[i], ghost_names[i])
            self.ghosts.append(ghost)
        
        # Count total pellets
        self.total_pellets = sum(sum(row) for row in self.pellets)
        
        # Reset game state
        self.game_over = False
        self.win = False
        self.life_lost_message = ""
        self.life_lost_timer = 0
    
    def update(self, dt):
        # Update life lost message timer
        if self.life_lost_message:
            self.life_lost_timer += dt
            if self.life_lost_timer >= self.life_lost_duration:
                self.life_lost_message = ""
                self.life_lost_timer = 0
        
        if not self.game_over and not self.win:
            # Update Pacman
            self.pacman.update(dt, self.walls)
            
            # Update ghosts
            pacman_grid_pos = self.pacman.get_grid_position()
            for ghost in self.ghosts:
                ghost.update(dt, self.walls, pacman_grid_pos)
            
            # Check pellet collection
            grid_x, grid_y = self.pacman.get_grid_position()
            if (0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT and 
                self.pellets[grid_y][grid_x]):
                self.pellets[grid_y][grid_x] = False
                self.pacman.score += 10
            
            # Check ghost-Pacman collision
            for ghost in self.ghosts:
                distance = math.sqrt((self.pacman.x - ghost.x)**2 + (self.pacman.y - ghost.y)**2)
                if distance < (self.pacman.radius + ghost.radius):
                    # Collision detected
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.game_over = True
                        self.life_lost_message = "GAME OVER!"
                    else:
                        # Show life lost message
                        self.life_lost_message = f"LOST A LIFE! Lives remaining: {self.pacman.lives}"
                        self.life_lost_timer = 0
                        # Reset Pacman position to center
                        center_x = MAP_WIDTH // 2
                        center_y = MAP_HEIGHT // 2
                        self.pacman.x = center_x * TILE_SIZE + TILE_SIZE // 2
                        self.pacman.y = center_y * TILE_SIZE + TILE_SIZE // 2
                        self.pacman.direction = (0, 0)
                        self.pacman.next_direction = (0, 0)
                    break  # Only handle one collision per frame
            
            # Check win condition
            remaining_pellets = sum(sum(row) for row in self.pellets)
            if remaining_pellets == 0:
                self.win = True
    
    def draw(self, screen):
        # Draw background
        screen.fill(BLACK)
        
        # Draw walls
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.walls[y][x]:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, BLUE, rect)
        
        # Draw pellets
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.pellets[y][x]:
                    center_x = x * TILE_SIZE + TILE_SIZE // 2
                    center_y = y * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, WHITE, (center_x, center_y), 3)
        
        # Draw Pacman
        if self.pacman:
            self.pacman.draw(screen)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(screen)
        
        # Draw UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        lives_text = font.render(f"Lives: {self.pacman.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        
        # Debug info
        debug_text = font.render(f"Dir: {self.pacman.direction} Next: {self.pacman.next_direction}", True, WHITE)
        screen.blit(debug_text, (10, 50))
        
        pos_text = font.render(f"Pos: ({int(self.pacman.x)}, {int(self.pacman.y)})", True, WHITE)
        screen.blit(pos_text, (10, 90))
        
        # Draw life lost message
        if self.life_lost_message:
            life_lost_text = font.render(self.life_lost_message, True, RED)
            text_rect = life_lost_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(life_lost_text, text_rect)
        
        # Draw game over/win messages
        if self.game_over:
            game_over_text = font.render("GAME OVER - Press R to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(game_over_text, text_rect)
        elif self.win:
            win_text = font.render("YOU WIN! - Press R to restart", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(win_text, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Pacman Game")
    clock = pygame.time.Clock()
    
    game = Game()
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and (game.game_over or game.win):
                    # Restart game
                    game.generate_map()
                elif not game.game_over and not game.win:
                    # Movement controls only work during gameplay
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        print("Left key pressed")
                        game.pacman.next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        print("Right key pressed")
                        game.pacman.next_direction = (1, 0)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        print("Up key pressed")
                        game.pacman.next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        print("Down key pressed")
                        game.pacman.next_direction = (0, 1)
        
        game.update(dt)
        game.draw(screen)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
