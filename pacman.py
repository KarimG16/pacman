"""
Pacman character class
"""

import pygame
import math
from constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, YELLOW, BLACK


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
        self.power_mode = False
        self.power_timer = 0
        self.power_duration = 5.0  # Power mode lasts 5 seconds
        self.ghosts_eaten = 0  # Track how many ghosts have been eaten
        
    def update(self, dt, walls):
        # Update power mode timer
        if self.power_mode:
            self.power_timer += dt
            if self.power_timer >= self.power_duration:
                self.power_mode = False
                self.power_timer = 0
        
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
        # Draw Pacman body - change color when in power mode
        color = YELLOW if not self.power_mode else (255, 255, 100)  # Slightly different yellow when powered
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        
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
