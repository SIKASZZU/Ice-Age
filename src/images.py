import os
import sys
import pygame


class Images:
    def __init__(self):
        self.loaded_item_images = {}

    def preloading(self, image_name, image_path=None):
        # Return already loaded image
        if image_name in self.loaded_item_images:
            return self.loaded_item_images[image_name]

        # Adjust path if provided
        if image_path:
            image_path = self.resource_path(image_path)
        else:
            raise ValueError("Image path must be provided.")

        # Load and convert the image
        return self._load_and_convert_image(image_path, image_name)


    def _load_and_convert_image(self, image_path: str, image_name: str):
        """Utility method to load and convert images."""
        try:
            loaded_image = pygame.image.load(image_path)
            converted_image = loaded_image.convert_alpha()
            self.loaded_item_images[image_name] = converted_image
            return converted_image
        except (pygame.error, FileNotFoundError):
            print(f"Failed to load image: {image_path}")
            return None

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        # Get the directory of the current script (e.g., src)
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Move up to project root
        return os.path.normpath(os.path.join(base_path, relative_path))

