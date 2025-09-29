"""
Main entry point for the Pacman game
"""

import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game import Game


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
                    game.level = 1
                    game.generate_map()
                elif event.key == pygame.K_f and not game.game_over and not game.win:
                    # Skip level if conditions are met
                    if game.can_skip_level():
                        game.skip_to_next_level()
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
