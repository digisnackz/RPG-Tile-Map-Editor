import pygame

class MapEditor:
    def __init__(self, grid_size, width, height):
        """
        Initialize the map editor
        
        Parameters:
        - grid_size: size of each tile in pixels
        - width: number of tiles horizontally
        - height: number of tiles vertically
        """
        self.grid_size = grid_size
        self.width = width
        self.height = height
        
        # Initialize an empty map grid
        # Each cell contains the tile object or None if empty
        self.grid = [[None for _ in range(width)] for _ in range(height)]
    
    def place_tile(self, x, y, tile):
        """Place a tile at the specified grid position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile
            return True
        return False
    
    def remove_tile(self, x, y):
        """Remove a tile at the specified grid position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = None
            return True
        return False
    
    def get_tile(self, x, y):
        """Get the tile at the specified grid position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def clear(self):
        """Clear the entire map"""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def resize(self, new_width, new_height):
        """Resize the map grid"""
        # Create a new grid with the desired size
        new_grid = [[None for _ in range(new_width)] for _ in range(new_height)]
        
        # Copy existing tiles to the new grid
        for y in range(min(self.height, new_height)):
            for x in range(min(self.width, new_width)):
                new_grid[y][x] = self.grid[y][x]
        
        # Update grid and dimensions
        self.grid = new_grid
        self.width = new_width
        self.height = new_height
    
    def draw(self, surface):
        """Draw the map to the provided surface"""
        # Clear the surface first (optional, depends on your needs)
        # surface.fill((230, 230, 230))
        
        # Draw each tile in the grid
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile and tile.image:
                    # Calculate the position to draw the tile
                    pos_x = x * self.grid_size
                    pos_y = y * self.grid_size
                    
                    # Make sure the image size matches the grid size
                    if tile.image.get_width() != self.grid_size or tile.image.get_height() != self.grid_size:
                        scaled_image = pygame.transform.scale(tile.image, (self.grid_size, self.grid_size))
                        surface.blit(scaled_image, (pos_x, pos_y))
                    else:
                        surface.blit(tile.image, (pos_x, pos_y))
    
    def to_data(self):
        """Convert the map to a serializable format for saving"""
        data = {
            'width': self.width,
            'height': self.height,
            'grid_size': self.grid_size,
            'tiles': []
        }
        
        # Store each tile by its name rather than the object itself
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = self.grid[y][x]
                if tile:
                    row.append(tile.name)
                else:
                    row.append(None)
            data['tiles'].append(row)
        
        return data
    
    def from_data(self, data, tile_manager):
        """Load a map from data"""
        self.width = data.get('width', self.width)
        self.height = data.get('height', self.height)
        self.grid_size = data.get('grid_size', self.grid_size)
        
        # Initialize an empty grid
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        
        # Load tiles from data
        tiles_data = data.get('tiles', [])
        for y, row in enumerate(tiles_data):
            if y >= self.height:
                break
                
            for x, tile_name in enumerate(row):
                if x >= self.width:
                    break
                    
                if tile_name:
                    # Look up the tile by name in the tile manager
                    tile = tile_manager.get_tile_by_name(tile_name)
                    if tile:
                        self.grid[y][x] = tile
