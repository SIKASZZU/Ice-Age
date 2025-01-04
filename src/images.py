import pygame
import os
import sys

class Images:
    def __init__(self):
        self.loaded_item_images = {}


    def preloading(self, image_name, image_path):

        # already loaded
        if image_name in self.loaded_item_images:
            return self.loaded_item_images[image_name]

        if image_path:
            return self._load_and_convert_image(image_path, image_name)
        
        else:
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            self.loaded_item_images[image_name] = converted_image
            return converted_image


    def _load_and_convert_image(self, image_path: str, image_name: str):
        """Utility method to load and convert images."""
        try:
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            self.loaded_item_images[image_name] = converted_image
            return converted_image
        except pygame.error:
            return None


    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        return os.path.join(base_path, relative_path)
