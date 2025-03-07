import random
import pygame


class TileSet:
    def __init__(self, image_instance, map_instance):
        self.images = image_instance
        self.map = map_instance

        self.snowy_ground_tileset_image = self.get_tileset_image('Water_Ground_Tileset', 'res/images/snowy_ground_snowy_water.png')
        self.snowy_ground_tileset_image = pygame.transform.scale(self.snowy_ground_tileset_image, (6 * self.map.tile_size, 3 * self.map.tile_size))

        self.snowy_ground_snowy_heated_ground_tileset_image = self.get_tileset_image('Snowy_Melted_Ground_Tileset', 'res/images/snowy_ground_snowy_heated_ground.png')
        self.snowy_ground_snowy_heated_ground_tileset_image = pygame.transform.scale(self.snowy_ground_snowy_heated_ground_tileset_image, (6 * self.map.tile_size, 3 * self.map.tile_size))

        melted_water_path = 'res/images/melted_water.png'
        self.melted_water_image = self.get_tileset_image('Melted_Water_Tileset', melted_water_path)
        self.melted_water_image = pygame.transform.scale(self.melted_water_image, (6 * self.map.tile_size, 3 * self.map.tile_size))

        self.load_def_wall_images()

    def load_def_wall_images(self):
        for i in range(16):
            setattr(self, f"def_wall_{i}", pygame.transform.scale(
                self.get_tileset_image(f"def_wall_{i}", f"res/images/def_walls/def_wall_{i}.png"),
                (self.map.tile_size, self.map.tile_size * 2)))

    def get_tileset_image(self, image_name, image_path):
        return self.images.preloading(image_name, image_path=image_path)

    def get_tile(self, tileset, tile_size, col, row, width=None, height=None):
        if width and height:
            rect = pygame.Rect(col * width,
                               row * height,
                               tile_size,
                               tile_size)
            return pygame.transform.scale(tileset.subsurface(rect), (self.map.tile_size, self.map.tile_size * 1.5))

        else:
            rect = pygame.Rect(col * tile_size,
                               row * tile_size,
                               tile_size,
                               tile_size)
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

        if not top_empty and not bottom_empty and not left_empty and not right_empty:
            return None

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

    def determine_snowy_heated_ground_image(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty = surroundings

        if not top_empty and not bottom_empty and not left_empty and not right_empty:
            return None

        tileset_image = self.snowy_ground_snowy_heated_ground_tileset_image  # Preloaded tileset image

        if top_empty and bottom_empty and left_empty and right_empty:
            return self.get_tile(tileset_image, self.map.tile_size, 5, 1)  # Center tile

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


    def determine_melted_water_image(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty = surroundings

        if not top_empty and not bottom_empty and not left_empty and not right_empty:
            return None

        tileset_image = self.melted_water_image  # Preloaded tileset image

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


    def determine_defencive_wooden_wall_image(self, surroundings):
        top_empty, bottom_empty, left_empty, right_empty = surroundings

        # All full
        if not top_empty and not bottom_empty and not left_empty and not right_empty:
            return self.def_wall_0

        # All empty
        if top_empty and bottom_empty and left_empty and right_empty:
            return self.def_wall_7

        # Three sides empty
        if top_empty and bottom_empty and left_empty:
            return self.def_wall_9
        if top_empty and bottom_empty and right_empty:
            return self.def_wall_8
        if top_empty and left_empty and right_empty:
            return self.def_wall_6
        if bottom_empty and left_empty and right_empty:
            return self.def_wall_5

        # Two sides empty
        if top_empty and left_empty:
            return self.def_wall_15
        if top_empty and right_empty:
            return self.def_wall_12
        if bottom_empty and left_empty:
            return self.def_wall_14
        if bottom_empty and right_empty:
            return self.def_wall_13
        if left_empty and right_empty:
            return self.def_wall_4
        if bottom_empty and top_empty:
            return self.def_wall_3

        # Single side empty
        if top_empty:
            return self.def_wall_2
        if bottom_empty:
            return self.def_wall_1
        if left_empty:
            return self.def_wall_11
        if right_empty:
            return self.def_wall_10
