import pygame
import random


class Render:
    def __init__(self, screen, camera, map, player, clock, tree, images):
        self.screen = screen
        self.camera = camera
        self.map = map
        self.player = player
        self.clock = clock
        self.tree = tree
        self.images = images

        path = 'res/images/snow_ground.png'
        self.ground_image = self.images.preloading('ground', path)

        # listid
        self.ground_images = []
        self.tree_images = []
        self.combined_images = []


    def get_terrain_in_view(self):  # FIXME: EI TÖÖTA VIST?
        terrain_in_view = {}
        # Determine the player's position on the grid
        player_grid_x = self.player.grid_x_center
        player_grid_y = self.player.grid_y_center

        # Define the render range (10x10 visible tiles)
        row_range_0 = max(0, player_grid_y - 5)
        row_range_1 = min(self.map.height, player_grid_y + 6)
        col_range_0 = max(0, player_grid_x - 10)
        col_range_1 = min(self.map.width, player_grid_x + 10)

        # Collect terrain data within the render range
        for row in range(row_range_0, row_range_1):
            for col in range(col_range_0, col_range_1):
                terrain_value = self.map.data[row][col]
                terrain_in_view[(col, row)] = terrain_value  # Store terrain by grid coordinates

        return terrain_in_view

    def render_terrain_in_view(self):
        self.reset_image_lists()

        for row_idx, row in enumerate(self.map.data):
            for col_idx, terrain_value in enumerate(row):
                position = (row_idx * self.map.tile_size - self.camera.offset.x, col_idx * self.map.tile_size - self.camera.offset.y)
                # water
                if terrain_value == 0:
                    pass

                # terrain
                elif terrain_value == 1:
                    self.ground_images.append((self.ground_image, position))
                
                # tree
                elif terrain_value == 10:
                    self.tree_images.append((self.tree.image, position))
                
        self.combined_images = self.ground_images + self.tree_images
        self.screen.blits(self.combined_images, doreturn=False)


    def reset_image_lists(self):
        self.ground_images = []
        self.tree_images = []
        self.combined_images = []


    def render_player(self):
        # Adjust player position relative to the camera's offset
        player_position_adjusted = (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y)
        pygame.draw.rect(self.screen, color='red', rect=pygame.Rect(player_position_adjusted[0], player_position_adjusted[1], self.player.width, self.player.height))


    def update(self):
        # self.render_terrain_in_view(self.get_terrain_in_view())
        self.render_terrain_in_view()
        self.render_player()
        print(f"FPS: {int(self.clock.get_fps())}")  # Display FPS