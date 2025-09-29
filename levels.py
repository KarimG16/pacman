"""
Level generation and map logic
"""

import random
from constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, RED, PINK, CYAN, ORANGE, GREEN
from ghosts import Ghost


class LevelGenerator:
    def __init__(self):
        self.walls = []
        self.pellets = []
        self.power_pellets = []
    
    def generate_map(self, level):
        """Generate a map layout based on current level"""
        # Create a simple maze pattern
        self.walls = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.pellets = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        self.power_pellets = [[False for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        
        if level == 1:
            self.generate_level1_map()
        elif level == 2:
            self.generate_level2_map()
        else:
            # Default to level 1 for now
            self.generate_level1_map()
        
        # Place pellets in empty spaces
        for y in range(1, MAP_HEIGHT-1):
            for x in range(1, MAP_WIDTH-1):
                if not self.walls[y][x]:
                    self.pellets[y][x] = True
        
        # Place power pellets in corners (ensure they're accessible)
        power_pellet_positions = [
            (1, 1), (MAP_WIDTH-2, 1), (1, MAP_HEIGHT-2), (MAP_WIDTH-2, MAP_HEIGHT-2)  # Corners only
        ]
        
        for x, y in power_pellet_positions:
            if not self.walls[y][x]:
                self.power_pellets[y][x] = True
                self.pellets[y][x] = False  # Remove regular pellet if power pellet is placed
        
        # Ensure all areas are accessible by clearing some walls if needed
        self.ensure_accessibility()
        
        return self.walls, self.pellets, self.power_pellets
    
    def generate_level1_map(self):
        """Generate Level 1 map (simple accessible maze)"""
        # Create border walls
        for x in range(MAP_WIDTH):
            self.walls[0][x] = True
            self.walls[MAP_HEIGHT-1][x] = True
        for y in range(MAP_HEIGHT):
            self.walls[y][0] = True
            self.walls[y][MAP_WIDTH-1] = True
        
        # Create a simple maze with guaranteed paths
        # Add some strategic walls but ensure connectivity
        
        # Add a few horizontal walls (with gaps)
        for y in range(3, MAP_HEIGHT-3, 4):
            for x in range(2, MAP_WIDTH-2, 3):
                if random.random() < 0.4:  # 40% chance of wall
                    self.walls[y][x] = True
        
        # Add a few vertical walls (with gaps)
        for x in range(3, MAP_WIDTH-3, 4):
            for y in range(2, MAP_HEIGHT-2, 3):
                if random.random() < 0.4:  # 40% chance of wall
                    self.walls[y][x] = True
        
        # Ensure center area is accessible
        center_x, center_y = MAP_WIDTH // 2, MAP_HEIGHT // 2
        # Clear a path around center
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= center_x + dx < MAP_WIDTH and 0 <= center_y + dy < MAP_HEIGHT:
                    self.walls[center_y + dy][center_x + dx] = False
    
    def generate_level2_map(self):
        """Generate Level 2 map (cross pattern with accessible paths)"""
        # Create border walls
        for x in range(MAP_WIDTH):
            self.walls[0][x] = True
            self.walls[MAP_HEIGHT-1][x] = True
        for y in range(MAP_HEIGHT):
            self.walls[y][0] = True
            self.walls[y][MAP_WIDTH-1] = True
        
        # Create a cross pattern in the center but ensure accessibility
        center_x, center_y = MAP_WIDTH // 2, MAP_HEIGHT // 2
        
        # Horizontal cross (with gaps for access)
        for x in range(center_x - 1, center_x + 2):
            if 0 <= x < MAP_WIDTH and x != center_x:  # Leave center open
                self.walls[center_y][x] = True
        
        # Vertical cross (with gaps for access)
        for y in range(center_y - 1, center_y + 2):
            if 0 <= y < MAP_HEIGHT and y != center_y:  # Leave center open
                self.walls[y][center_x] = True
        
        # Add corner blocks (2x2 blocks) but ensure paths around them
        corner_blocks = [(2, 2), (MAP_WIDTH-3, 2), (2, MAP_HEIGHT-3), (MAP_WIDTH-3, MAP_HEIGHT-3)]
        for x, y in corner_blocks:
            self.walls[y][x] = True
            if x+1 < MAP_WIDTH:
                self.walls[y][x+1] = True
            if y+1 < MAP_HEIGHT:
                self.walls[y+1][x] = True
            if x+1 < MAP_WIDTH and y+1 < MAP_HEIGHT:
                self.walls[y+1][x+1] = True
        
        # Add some strategic walls but ensure connectivity
        for y in range(2, MAP_HEIGHT-2, 3):
            for x in range(2, MAP_WIDTH-2, 3):
                if random.random() < 0.2:  # 20% chance of wall (reduced)
                    self.walls[y][x] = True
        
        # Ensure all corners are accessible by clearing paths
        corner_paths = [(1, 2), (2, 1), (MAP_WIDTH-3, 1), (MAP_WIDTH-2, 2), 
                       (1, MAP_HEIGHT-3), (2, MAP_HEIGHT-2), (MAP_WIDTH-3, MAP_HEIGHT-2), (MAP_WIDTH-2, MAP_HEIGHT-3)]
        for x, y in corner_paths:
            if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                self.walls[y][x] = False
    
    def ensure_accessibility(self):
        """Ensure all areas of the map are accessible by clearing some walls if needed"""
        # Create a simple accessibility check by ensuring there are paths from center to corners
        center_x, center_y = MAP_WIDTH // 2, MAP_HEIGHT // 2
        
        # Clear paths from center to each corner
        corners = [(1, 1), (MAP_WIDTH-2, 1), (1, MAP_HEIGHT-2), (MAP_WIDTH-2, MAP_HEIGHT-2)]
        
        for corner_x, corner_y in corners:
            # Clear a path from center to corner (simple L-shaped path)
            # Horizontal path first
            start_x, end_x = min(center_x, corner_x), max(center_x, corner_x)
            for x in range(start_x, end_x + 1):
                if 0 <= x < MAP_WIDTH and 0 <= center_y < MAP_HEIGHT:
                    self.walls[center_y][x] = False
            
            # Then vertical path
            start_y, end_y = min(center_y, corner_y), max(center_y, corner_y)
            for y in range(start_y, end_y + 1):
                if 0 <= corner_x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    self.walls[y][corner_x] = False
    
    def create_ghosts(self, level, center_x, center_y):
        """Create ghosts based on current level"""
        ghosts = []
        
        if level == 1:
            # Level 1: 4 ghosts
            ghost_colors = [RED, PINK, CYAN, ORANGE]
            ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
            num_ghosts = 4
        elif level == 2:
            # Level 2: 6 ghosts
            ghost_colors = [RED, PINK, CYAN, ORANGE, GREEN, (255, 100, 255)]  # Purple
            ghost_names = ["Blinky", "Pinky", "Inky", "Clyde", "Speedy", "Shadow"]
            num_ghosts = 6
        else:
            # Default to level 1
            ghost_colors = [RED, PINK, CYAN, ORANGE]
            ghost_names = ["Blinky", "Pinky", "Inky", "Clyde"]
            num_ghosts = 4
        
        # Find empty positions for ghosts (avoid center area where Pacman is)
        ghost_positions = []
        for y in range(1, MAP_HEIGHT-1):
            for x in range(1, MAP_WIDTH-1):
                if (not self.walls[y][x] and 
                    abs(x - center_x) > 1 and abs(y - center_y) > 1):  # Keep ghosts away from Pacman (reduced distance for smaller map)
                    ghost_positions.append((x, y))
        
        # Create ghosts at random positions
        for i in range(min(num_ghosts, len(ghost_positions))):
            x, y = random.choice(ghost_positions)
            ghost_positions.remove((x, y))  # Remove to avoid duplicates
            ghost = Ghost(x * TILE_SIZE + TILE_SIZE // 2, 
                         y * TILE_SIZE + TILE_SIZE // 2,
                         ghost_colors[i], ghost_names[i])
            ghosts.append(ghost)
        
        return ghosts
