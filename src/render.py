import pygame
import random


class Render:
    def __init__(self, screen, camera, map, player, clock, tree, images, tile_set):
        self.screen = screen
        self.camera = camera
        self.map = map
        self.player = player
        self.clock = clock
        self.tree = tree
        self.images = images
        self.tile_set = tile_set

        path = 'C:/Users/Olari/Documents/GitHub/Ice-Age/res/images/snowy_ground.png'
        self.ground_image = self.images.preloading('ground', path)
        self.ground_image = pygame.transform.scale(self.ground_image, (self.map.tile_size, self.map.tile_size))

        path = 'C:/Users/Olari/Documents/GitHub/Ice-Age/res/images/snowy_water.png'
        self.water_image = self.images.preloading('water', path)

        self.water_image = pygame.transform.scale(self.water_image, (self.map.tile_size, self.map.tile_size))

        # listid
        self.water_images = []
        self.ground_images = []
        self.tree_images = []
        self.combined_images = []
        self.random_tree_positions = {}

        self.ground_surrounding_values = [0,]

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
                position_by_grid = (row_idx, col_idx)

                # water
                if terrain_value in [0]:
                    position = (row_idx * self.map.tile_size - self.camera.offset.x, col_idx * self.map.tile_size - self.camera.offset.y)
                    self.water_images.append((self.water_image, position))

                # terrain
                elif terrain_value in [1, 10]:
                    position = (row_idx * self.map.tile_size - self.camera.offset.x, col_idx * self.map.tile_size - self.camera.offset.y)

                    surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.ground_surrounding_values)
                    ground_image = self.tile_set.determine_snowy_ground_image(surroundings)
                    if not ground_image:
                        ground_image = self.ground_image

                    self.ground_images.append((ground_image, position))

                    # tree
                    if terrain_value in [10]:
                        if position_by_grid in self.random_tree_positions:
                            position = self.random_tree_positions[position_by_grid]
                            self.random_tree_positions[position_by_grid] = position

                        else:
                            # Base position without random offset
                            position = (row_idx * self.map.tile_size, col_idx * self.map.tile_size)
                            # Random offset


                            if random.random() > 0.5:
                                position = (
                                    position[0] + random.uniform(self.map.tile_size * 0.01, self.map.tile_size * 0.2),
                                    position[1] + random.uniform(self.map.tile_size * 0.01, self.map.tile_size * 0.2)
                                )

                            else:
                                position = (
                                    position[0] - random.uniform(self.map.tile_size * 0.01, self.map.tile_size * 0.2),
                                    position[1] + random.uniform(self.map.tile_size * 0.01, self.map.tile_size * 0.2)
                                )

                            # Store tree position in the map (to avoid duplicating)
                            self.random_tree_positions[position_by_grid] = position

                        # Append tree image and position
                        tree_position = (position[0] - self.camera.offset.x, position[1] - self.camera.offset.y - self.tree.height // 2)
                        self.tree_images.append((self.tree.image, tree_position))

        self.combined_images = self.water_images + self.ground_images + self.tree_images
        self.screen.blits(self.combined_images, doreturn=False)


    def reset_image_lists(self):
        self.water_images = []
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
        # print(f"FPS: {int(self.clock.get_fps())}")  # Display FPS