import os
import pygame

class Tile:
    def __init__(self, name, image_path=None, image=None):
        self.name = name
        self.image_path = image_path
        self.image = image
        
        # Load image if path is provided but image is not
        if image_path and not image:
            self.load_image()
    
    def load_image(self):
        if os.path.exists(self.image_path):
            try:
                self.image = pygame.image.load(self.image_path).convert_alpha()
                # Resize image to fit the grid if needed
                # self.image = pygame.transform.scale(self.image, (32, 32))
            except pygame.error:
                print(f"Error loading image: {self.image_path}")
                self.image = None
        else:
            print(f"Image file not found: {self.image_path}")
            self.image = None

class TileManager:
    def __init__(self):
        self.tiles = []
        self.load_default_tiles()
    
    def load_default_tiles(self):
        """Load default tiles or create placeholder tiles if no assets exist"""
        tiles_dir = os.path.join("assets", "tiles")
        
        # Check if the tiles directory exists and has files
        if os.path.exists(tiles_dir) and any(os.path.isfile(os.path.join(tiles_dir, f)) for f in os.listdir(tiles_dir)):
            # Load tiles from the tiles directory
            for file_name in os.listdir(tiles_dir):
                if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    image_path = os.path.join(tiles_dir, file_name)
                    tile_name = os.path.splitext(file_name)[0].replace('_', ' ').title()
                    self.tiles.append(Tile(tile_name, image_path))
        else:
            # Create placeholder colored tiles if no assets exist
            colors = [
                ("Grass", (0, 150, 0)),
                ("Water", (0, 100, 255)),
                ("Sand", (255, 220, 100)),
                ("Stone", (150, 150, 150)),
                ("Dirt", (150, 75, 0)),
                ("Snow", (255, 255, 255)),
                ("Lava", (255, 100, 0)),
                ("Wood", (150, 100, 50)),
                ("Bush", (0, 200, 0)),
                ("Flowers", (200, 150, 200))
            ]
            
            for name, color in colors:
                # Create a colored square surface
                image = pygame.Surface((32, 32))
                image.fill(color)
                self.tiles.append(Tile(name, image=image))
    
    def add_tile(self, name, image_path):
        """Add a new tile to the collection"""
        tile = Tile(name, image_path)
        self.tiles.append(tile)
        return tile
    
    def remove_tile(self, tile):
        """Remove a tile from the collection"""
        if tile in self.tiles:
            self.tiles.remove(tile)
            return True
        return False
    
    def get_tile_by_name(self, name):
        """Get a tile by its name"""
        for tile in self.tiles:
            if tile.name == name:
                return tile
        return None
