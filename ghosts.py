"""
Ghost characters class
"""

import pygame
import math
import random
from constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, BLUE, WHITE


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
        self.vulnerable = False
        self.eaten = False
        self.original_color = color
        
    def update(self, dt, walls, pacman_pos, pacman_power_mode):
        # Update vulnerability based on Pacman's power mode
        self.vulnerable = pacman_power_mode
        
        # If eaten, don't move
        if self.eaten:
            return
        
        # Update direction change timer
        self.direction_timer += dt
        
        # Change direction periodically or when hitting a wall
        if (self.direction_timer - self.last_direction_change > self.direction_change_interval or 
            self.check_wall_collision(self.x + self.direction[0] * self.speed * dt, 
                                    self.y + self.direction[1] * self.speed * dt, walls)):
            self.choose_new_direction(walls, pacman_pos, pacman_power_mode)
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
            self.choose_new_direction(walls, pacman_pos, pacman_power_mode)
            # Snap to grid
            self.x = round(self.x / TILE_SIZE) * TILE_SIZE
            self.y = round(self.y / TILE_SIZE) * TILE_SIZE
    
    def choose_new_direction(self, walls, pacman_pos, pacman_power_mode):
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
        
        # Simple AI: behavior changes based on vulnerability
        pacman_grid_x, pacman_grid_y = pacman_pos
        distance_to_pacman = math.sqrt((grid_x - pacman_grid_x)**2 + (grid_y - pacman_grid_y)**2)
        
        if self.vulnerable:
            # When vulnerable, try to run away from Pacman
            best_direction = None
            best_distance = 0
            
            for dx, dy in valid_directions:
                new_x = grid_x + dx
                new_y = grid_y + dy
                distance = math.sqrt((new_x - pacman_grid_x)**2 + (new_y - pacman_grid_y)**2)
                if distance > best_distance:
                    best_distance = distance
                    best_direction = (dx, dy)
            
            if best_direction:
                self.direction = best_direction
            else:
                self.direction = random.choice(valid_directions)
        else:
            # Normal behavior: sometimes move towards Pacman, sometimes random
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
        # Don't draw if eaten
        if self.eaten:
            return
            
        # Choose color based on vulnerability
        if self.vulnerable:
            # Flash between blue and white when vulnerable
            flash_color = BLUE if int(pygame.time.get_ticks() / 200) % 2 == 0 else WHITE
            ghost_color = flash_color
        else:
            ghost_color = self.original_color
        
        # Draw ghost body (slightly different shape than Pacman)
        pygame.draw.circle(screen, ghost_color, (int(self.x), int(self.y)), self.radius)
        
        # Draw ghost bottom (wavy bottom)
        bottom_y = int(self.y) + self.radius
        wave_points = []
        for i in range(0, self.radius * 2, 4):
            x_offset = i - self.radius
            wave_y = bottom_y + math.sin(i * 0.5) * 3
            wave_points.append((int(self.x) + x_offset, int(wave_y)))
        
        if wave_points:
            pygame.draw.polygon(screen, ghost_color, wave_points)
        
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
