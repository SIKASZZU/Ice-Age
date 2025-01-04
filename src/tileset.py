import random
import pygame


class TileSet:
    def __init__(self, image, map):
        self.images = image
        self.map = map

        self.snowy_ground_tileset_image = self.get_tileset_image('Water_Ground_Tileset', 'res/images/snowy_ground_snowy_water.png')
        self.snowy_ground_tileset_image = pygame.transform.scale(self.snowy_ground_tileset_image, (6 * self.map.tile_size, 3 * self.map.tile_size))
    def get_tileset_image(self, image_name, image_path):
        return self.images.preloading(image_name, image_path=image_path)
    @staticmethod
    def get_tile(tileset, tile_size, col, row):
        rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
        if rect.right > tileset.get_width() or rect.bottom > tileset.get_height():
            raise ValueError(
                f"Subsurface rectangle {rect} is outside surface bounds ({tileset.get_width()}x{tileset.get_height()}).")
        return tileset.subsurface(rect)

    def check_surroundings(self, row: int, col: int, terrain_values: tuple):
        if self.map.data.size == 0 or not terrain_values:
            return False, False, False, False

        # Boundary and terrain checks
        top_match = row > 0 and self.map.data[row - 1, col] in terrain_values
        bottom_match = row < self.map.data.shape[0] - 1 and self.map.data[row + 1, col] in terrain_values
        left_match = col > 0 and self.map.data[row, col - 1] in terrain_values
        right_match = col < self.map.data.shape[1] - 1 and self.map.data[row, col + 1] in terrain_values

        return top_match, bottom_match, left_match, right_match

    def determine_snowy_ground_image(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty = surroundings
        tileset_image = self.snowy_ground_tileset_image  # Preloaded tileset image

        if top_empty and bottom_empty and left_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 1, 1)  # Center tile

        # Three sides empty
        if top_empty and bottom_empty and left_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 3, 0)  # Top-edge tile
        if top_empty and bottom_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 3, 2)  # Bottom-edge tile
        if top_empty and left_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 4, 0)  # Left-edge tile
        if bottom_empty and left_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 5, 0)  # Right-edge tile

        # Two sides empty
        if top_empty and left_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 0, 0)  # Top-left corner
        if top_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 0, 2)  # Top-right corner
        if bottom_empty and left_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 2, 0)  # Bottom-left corner
        if bottom_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 2, 2)  # Bottom-right corner
        if left_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 4, 1)  # Bottom-right corner
        if bottom_empty and top_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 3, 1)  # Bottom-right corner

        # Single side empty
        if top_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 0, 1)  # Top edge
        if bottom_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 2, 1)  # Bottom edge
        if left_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 1, 0)  # Left edge
        if right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 1, 2)  # Right edge

        # Default case: No surrounding match
        return None
