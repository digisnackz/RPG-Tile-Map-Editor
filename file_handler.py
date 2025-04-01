import os
import json
import pygame
from tkinter import Tk, filedialog
from PIL import Image

class FileHandler:
    def __init__(self, map_editor):
        """
        Initialize the file handler
        
        Parameters:
        - map_editor: Reference to the map editor
        """
        self.map_editor = map_editor
        self.default_save_dir = os.path.join(os.getcwd(), "saved_maps")
        
        # Create the save directory if it doesn't exist
        if not os.path.exists(self.default_save_dir):
            os.makedirs(self.default_save_dir)
    
    def save_map(self):
        """Save the current map to a JSON file"""
        # Convert map to serializable format
        map_data = self.map_editor.to_data()
        
        # Create root Tkinter window but hide it
        root = Tk()
        root.withdraw()
        
        # Open file dialog to select save location
        file_path = filedialog.asksaveasfilename(
            initialdir=self.default_save_dir,
            title="Save Map",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        
        # Destroy the Tkinter window
        root.destroy()
        
        # If a file path was selected
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(map_data, f, indent=2)
                print(f"Map saved to {file_path}")
                return True
            except Exception as e:
                print(f"Error saving map: {e}")
                return False
        
        return False
    
    def load_map(self):
        """Load a map from a JSON file"""
        # Create root Tkinter window but hide it
        root = Tk()
        root.withdraw()
        
        # Open file dialog to select file to load
        file_path = filedialog.askopenfilename(
            initialdir=self.default_save_dir,
            title="Load Map",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        # Destroy the Tkinter window
        root.destroy()
        
        # If a file path was selected
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    map_data = json.load(f)
                
                # Import the tile manager here to avoid circular imports
                from tile_manager import TileManager
                tile_manager = TileManager()
                
                # Load the map data
                self.map_editor.from_data(map_data, tile_manager)
                print(f"Map loaded from {file_path}")
                return True
            except Exception as e:
                print(f"Error loading map: {e}")
                return False
        
        return False
    
    def export_map_as_image(self):
        """Export the current map as a PNG image"""
        # Create a surface to render the map
        width = self.map_editor.width * self.map_editor.grid_size
        height = self.map_editor.height * self.map_editor.grid_size
        surface = pygame.Surface((width, height))
        
        # Fill with a background color
        surface.fill((230, 230, 230))
        
        # Draw the map without grid lines
        self.map_editor.draw(surface)
        
        # Create root Tkinter window but hide it
        root = Tk()
        root.withdraw()
        
        # Open file dialog to select save location
        file_path = filedialog.asksaveasfilename(
            initialdir=self.default_save_dir,
            title="Export Map as Image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            defaultextension=".png"
        )
        
        # Destroy the Tkinter window
        root.destroy()
        
        # If a file path was selected
        if file_path:
            try:
                # Save the surface as an image
                pygame.image.save(surface, file_path)
                print(f"Map exported as image to {file_path}")
                return True
            except Exception as e:
                print(f"Error exporting map: {e}")
                return False
        
        return False
