"""
Main Game class that manages the game state and logic
"""

import pygame
import math
from constants import *
from pacman import Pacman
from levels import LevelGenerator


class Game:
    def __init__(self):
        self.level_generator = LevelGenerator()
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        self.pacman = None
        self.ghosts = []
        self.total_pellets = 0
        self.pellets_eaten = 0  # Track how many pellets have been eaten
        self.game_over = False
        self.win = False
        self.life_lost_message = ""
        self.life_lost_timer = 0
        self.life_lost_duration = 2.0  # Show message for 2 seconds
        self.level = 1
        self.level_complete_message = ""
        self.level_complete_timer = 0
        self.level_complete_duration = 3.0  # Show level complete message for 3 seconds
        self.generate_map()
    
    def generate_map(self):
        """Generate a map layout based on current level"""
        # Generate the map using the level generator
        self.walls, self.pellets, self.power_pellets = self.level_generator.generate_map(self.level)
        
        # Place Pacman in the center
        center_x = MAP_WIDTH // 2
        center_y = MAP_HEIGHT // 2
        self.pacman = Pacman(center_x * TILE_SIZE + TILE_SIZE // 2, 
                            center_y * TILE_SIZE + TILE_SIZE // 2)
        
        # Create ghosts based on level
        self.ghosts = self.level_generator.create_ghosts(self.level, center_x, center_y)
        
        # Count total pellets
        self.total_pellets = sum(sum(row) for row in self.pellets) + sum(sum(row) for row in self.power_pellets)
        
        # Reset game state
        self.game_over = False
        self.win = False
        self.life_lost_message = ""
        self.life_lost_timer = 0
        self.level_complete_message = ""
        self.level_complete_timer = 0
        self.pellets_eaten = 0
        if self.pacman:
            self.pacman.ghosts_eaten = 0
    
    def can_skip_level(self):
        """Check if player can skip to next level (half pellets eaten + 2 ghosts eaten)"""
        half_pellets = self.total_pellets // 2
        return self.pellets_eaten >= half_pellets and self.pacman.ghosts_eaten >= 2
    
    def skip_to_next_level(self):
        """Skip to the next level"""
        if self.level < 2:  # Only 2 levels for now
            self.level += 1
            self.level_complete_message = f"LEVEL SKIPPED! Advanced to Level {self.level}"
            self.level_complete_timer = 0
            # Generate new map after a short delay
            self.generate_map()
        else:
            # If already at max level, just win
            self.win = True
    
    def update(self, dt):
        # Update life lost message timer
        if self.life_lost_message:
            self.life_lost_timer += dt
            if self.life_lost_timer >= self.life_lost_duration:
                self.life_lost_message = ""
                self.life_lost_timer = 0
        
        # Update level complete message timer
        if self.level_complete_message:
            self.level_complete_timer += dt
            if self.level_complete_timer >= self.level_complete_duration:
                self.level_complete_message = ""
                self.level_complete_timer = 0
                # Advance to next level
                self.level += 1
                self.generate_map()
        
        if not self.game_over and not self.win:
            # Update Pacman
            self.pacman.update(dt, self.walls)
            
            # Update ghosts
            pacman_grid_pos = self.pacman.get_grid_position()
            for ghost in self.ghosts:
                ghost.update(dt, self.walls, pacman_grid_pos, self.pacman.power_mode)
            
            # Check pellet collection
            grid_x, grid_y = self.pacman.get_grid_position()
            if (0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT):
                if self.pellets[grid_y][grid_x]:
                    self.pellets[grid_y][grid_x] = False
                    self.pacman.score += 10
                    self.pellets_eaten += 1
                elif self.power_pellets[grid_y][grid_x]:
                    self.power_pellets[grid_y][grid_x] = False
                    self.pacman.score += 50
                    self.pacman.power_mode = True
                    self.pacman.power_timer = 0  # Reset timer
                    self.pellets_eaten += 1
            
            # Check ghost-Pacman collision
            for ghost in self.ghosts:
                if not ghost.eaten:  # Only check collision with non-eaten ghosts
                    distance = math.sqrt((self.pacman.x - ghost.x)**2 + (self.pacman.y - ghost.y)**2)
                    if distance < (self.pacman.radius + ghost.radius):
                        # Collision detected
                        if self.pacman.power_mode and ghost.vulnerable:
                            # Pacman eats the ghost
                            ghost.eaten = True
                            self.pacman.score += 200
                            self.pacman.ghosts_eaten += 1
                            self.life_lost_message = f"GHOST EATEN! +200 points (Total: {self.pacman.ghosts_eaten})"
                            self.life_lost_timer = 0
                        else:
                            # Pacman loses a life
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
            
            # Check level completion
            remaining_pellets = sum(sum(row) for row in self.pellets) + sum(sum(row) for row in self.power_pellets)
            if remaining_pellets == 0:
                if self.level < 2:  # Only 2 levels for now
                    self.level_complete_message = f"LEVEL {self.level} COMPLETE! Next: Level {self.level + 1}"
                    self.level_complete_timer = 0
                else:
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
                elif self.power_pellets[y][x]:
                    center_x = x * TILE_SIZE + TILE_SIZE // 2
                    center_y = y * TILE_SIZE + TILE_SIZE // 2
                    pygame.draw.circle(screen, WHITE, (center_x, center_y), 8)  # Thicker power pellet
        
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
        
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        
        # Power mode indicator
        if self.pacman.power_mode:
            power_text = font.render("POWER MODE!", True, YELLOW)
            screen.blit(power_text, (10, 50))
            
            # Power timer bar
            power_remaining = (self.pacman.power_duration - self.pacman.power_timer) / self.pacman.power_duration
            bar_width = 200
            bar_height = 10
            bar_x = 10
            bar_y = 80
            
            # Background bar
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
            # Power bar
            pygame.draw.rect(screen, YELLOW, (bar_x, bar_y, bar_width * power_remaining, bar_height))
        
        # Skip level indicator
        if self.can_skip_level():
            skip_text = font.render("Press F to skip level!", True, GREEN)
            screen.blit(skip_text, (10, 50 if not self.pacman.power_mode else 100))
        
        # Progress indicators
        progress_text = font.render(f"Pellets: {self.pellets_eaten}/{self.total_pellets}", True, WHITE)
        screen.blit(progress_text, (10, 130 if not self.pacman.power_mode else 180))
        
        ghosts_text = font.render(f"Ghosts eaten: {self.pacman.ghosts_eaten}", True, WHITE)
        screen.blit(ghosts_text, (10, 170 if not self.pacman.power_mode else 220))
        
        # Draw life lost message
        if self.life_lost_message:
            life_lost_text = font.render(self.life_lost_message, True, RED)
            text_rect = life_lost_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(life_lost_text, text_rect)
        
        # Draw level complete message
        if self.level_complete_message:
            level_complete_text = font.render(self.level_complete_message, True, GREEN)
            text_rect = level_complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(level_complete_text, text_rect)
        
        # Draw game over/win messages
        if self.game_over:
            game_over_text = font.render("GAME OVER - Press R to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            screen.blit(game_over_text, text_rect)
        elif self.win:
            win_text = font.render("YOU WIN! - Press R to restart", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(win_text, text_rect)
