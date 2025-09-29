# Pacman Game - Modular Structure

This is a modular Pacman game implementation with separated components for better organization and maintainability.

## File Structure

- **`main.py`** - Main entry point and game loop
- **`game.py`** - Main Game class that manages game state and logic
- **`pacman.py`** - Pacman character class with movement and drawing logic
- **`ghosts.py`** - Ghost character class with AI behavior
- **`levels.py`** - Level generation and map logic
- **`constants.py`** - Game constants, colors, and configuration

## How to Run

```bash
python main.py
```

## Controls

- **Arrow Keys** or **WASD** - Move Pacman
- **F** - Skip level (when conditions are met)
- **R** - Restart game (when game over or won)
- **ESC** - Quit game

## Features

- Multiple levels with different map layouts
- Ghost AI with different behaviors
- Power pellets that make ghosts vulnerable
- Score system and lives
- Level progression system

## Original Files

The original monolithic files are still available:
- `simple_pacman_game.py` - Original complete game in one file
- `pygame-karim.py` - Simple pygame implementation
- `pacman_terminal.py` - Terminal-based version
