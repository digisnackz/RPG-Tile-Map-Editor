import os
import sys
import pygame
from tile_manager import TileManager
from map_editor import MapEditor
from file_handler import FileHandler

class TileMapGenerator:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1024, 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("RPG Tile Map Generator")
        
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        
        # Load assets
        self.tile_manager = TileManager()
        
        # Map settings
        self.grid_size = 32  # Size of each tile in pixels
        self.map_width = 20  # Number of tiles horizontally
        self.map_height = 20  # Number of tiles vertically
        
        # Initialize the map editor
        self.map_editor = MapEditor(self.grid_size, self.map_width, self.map_height)
        
        # Initialize file handler
        self.file_handler = FileHandler(self.map_editor)
        
        # UI elements
        self.editor_x = 250  # Editor starts at this x position
        self.sidebar_width = 200
        self.toolbar_height = 50
        
        # Compute editor surface size and position
        self.editor_width = self.grid_size * self.map_width
        self.editor_height = self.grid_size * self.map_height
        self.editor_surface = pygame.Surface((self.editor_width, self.editor_height))
        
        # Current selected tile
        self.selected_tile = None
        
        # UI state
        self.scroll_offset = 0
        self.max_scroll = max(0, len(self.tile_manager.tiles) * 40 - (self.height - self.toolbar_height))
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Check if click is in sidebar (tile selection)
                    if mouse_x < self.sidebar_width:
                        # Calculate which tile was clicked based on scroll position
                        tile_index = (mouse_y - self.toolbar_height + self.scroll_offset) // 40
                        if 0 <= tile_index < len(self.tile_manager.tiles):
                            self.selected_tile = self.tile_manager.tiles[tile_index]
                    
                    # Check if click is in editor area
                    elif self.editor_x <= mouse_x < self.editor_x + self.editor_width and \
                         self.toolbar_height <= mouse_y < self.toolbar_height + self.editor_height:
                        # Convert screen coordinates to grid coordinates
                        grid_x = (mouse_x - self.editor_x) // self.grid_size
                        grid_y = (mouse_y - self.toolbar_height) // self.grid_size
                        
                        # Place or remove tile based on mouse button
                        if event.button == 1:  # Left click
                            if self.selected_tile:
                                self.map_editor.place_tile(grid_x, grid_y, self.selected_tile)
                        elif event.button == 3:  # Right click
                            self.map_editor.remove_tile(grid_x, grid_y)
                    
                    # Check if click is in toolbar
                    elif mouse_y < self.toolbar_height:
                        button_width = 100
                        # Save button
                        if 10 <= mouse_x < 10 + button_width:
                            self.file_handler.save_map()
                        # Load button
                        elif 120 <= mouse_x < 120 + button_width:
                            self.file_handler.load_map()
                        # Export button
                        elif 230 <= mouse_x < 230 + button_width:
                            self.file_handler.export_map_as_image()
                            
                if event.type == pygame.MOUSEWHEEL:
                    # Scroll the sidebar
                    if pygame.mouse.get_pos()[0] < self.sidebar_width:
                        self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset - event.y * 20))
            
            # Draw everything
            self.draw()
            
            # Update the display
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()
    
    def draw(self):
        # Fill the background
        self.screen.fill(self.WHITE)
        
        # Draw toolbar
        pygame.draw.rect(self.screen, self.GRAY, (0, 0, self.width, self.toolbar_height))
        
        # Draw toolbar buttons
        self.draw_button("Save", 10, 10, 100, 30)
        self.draw_button("Load", 120, 10, 100, 30)
        self.draw_button("Export", 230, 10, 100, 30)
        
        # Draw sidebar
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, (0, self.toolbar_height, self.sidebar_width, self.height - self.toolbar_height))
        
        # Draw tiles in sidebar
        for i, tile in enumerate(self.tile_manager.tiles):
            tile_y = self.toolbar_height + i * 40 - self.scroll_offset
            # Only draw visible tiles
            if self.toolbar_height <= tile_y < self.height:
                if tile == self.selected_tile:
                    pygame.draw.rect(self.screen, self.GRAY, (5, tile_y, self.sidebar_width - 10, 35))
                
                # Draw tile preview
                if tile.image:
                    tile_rect = tile.image.get_rect()
                    tile_rect.topleft = (10, tile_y + 2)
                    self.screen.blit(tile.image, tile_rect)
                
                # Draw tile name
                font = pygame.font.SysFont(None, 20)
                name_text = font.render(tile.name, True, self.BLACK)
                self.screen.blit(name_text, (45, tile_y + 10))
        
        # Draw the grid on a separate surface
        self.editor_surface.fill(self.LIGHT_GRAY)
        
        # Draw the map on the editor surface
        self.map_editor.draw(self.editor_surface)
        
        # Draw grid lines
        for x in range(0, self.editor_width + 1, self.grid_size):
            pygame.draw.line(self.editor_surface, self.GRAY, (x, 0), (x, self.editor_height))
        for y in range(0, self.editor_height + 1, self.grid_size):
            pygame.draw.line(self.editor_surface, self.GRAY, (0, y), (self.editor_width, y))
        
        # Blit the editor surface to the screen
        self.screen.blit(self.editor_surface, (self.editor_x, self.toolbar_height))
        
        # Draw border around editor
        pygame.draw.rect(self.screen, self.BLACK, 
                         (self.editor_x, self.toolbar_height, self.editor_width, self.editor_height), 1)
    
    def draw_button(self, text, x, y, width, height):
        # Draw button background
        pygame.draw.rect(self.screen, self.DARK_GRAY, (x, y, width, height))
        
        # Draw button text
        font = pygame.font.SysFont(None, 24)
        text_surf = font.render(text, True, self.WHITE)
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surf, text_rect)


if __name__ == "__main__":
    # Fix missing LIGHT_GRAY color
    TileMapGenerator.LIGHT_GRAY = (230, 230, 230)
    
    # Start the application
    app = TileMapGenerator()
    app.run()
