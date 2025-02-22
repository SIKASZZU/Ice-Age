import pygame
import random

class Render:
    def __init__(self, screen, camera, map, player, clock, tree, images, tile_set, heat_zone, items):
        self.screen = screen
        self.camera = camera
        self.map = map
        self.player = player
        self.clock = clock
        self.tree = tree
        self.images = images
        self.tile_set = tile_set
        self.heat_zone = heat_zone
        self.items = items

        ground_path = 'res/images/snowy_ground.png'
        self.ground_image = self.images.preloading('ground', ground_path)
        self.ground_image = pygame.transform.scale(self.ground_image, (self.map.tile_size, self.map.tile_size))

        water_path = 'res/images/snowy_water.png'
        self.water_image = self.images.preloading('water', water_path)
        self.water_image = pygame.transform.scale(self.water_image, (self.map.tile_size, self.map.tile_size))

        snowy_heated_path = 'res/images/snowy_heated_ground.png'
        self.snowy_heated_image = self.images.preloading('snowy_heated_ground', snowy_heated_path)
        self.snowy_heated_image = pygame.transform.scale(self.snowy_heated_image, (self.map.tile_size, self.map.tile_size))


        torch_path = 'res/images/torch.png'
        self.torch_image = self.images.preloading('torch', torch_path)
        self.torch_image = pygame.transform.scale(self.torch_image, (self.map.tile_size, self.map.tile_size))

        firepit_path = 'res/images/firepit.png'
        self.firepit_image = self.images.preloading('firepit', firepit_path)
        self.firepit_image = pygame.transform.scale(self.firepit_image, (self.map.tile_size, self.map.tile_size))

        campfire_path = 'res/images/campfire.png'
        self.campfire_image = self.images.preloading('campfire', campfire_path)
        self.campfire_image = pygame.transform.scale(self.campfire_image, (self.map.tile_size, self.map.tile_size))

        bonfire_path = 'res/images/bonfire.png'
        self.bonfire_image = self.images.preloading('bonfire', bonfire_path)
        self.bonfire_image = pygame.transform.scale(self.bonfire_image, (self.map.tile_size, self.map.tile_size))

        furnace_path = 'res/images/furnace.png'
        self.furnace_image = self.images.preloading('furnace', furnace_path)
        self.furnace_image = pygame.transform.scale(self.furnace_image, (self.map.tile_size, self.map.tile_size))

        blast_furnace_path = 'res/images/blast_furnace.png'
        self.blast_furnace_image = self.images.preloading('blast_furnace', blast_furnace_path)
        self.blast_furnace_image = pygame.transform.scale(self.blast_furnace_image, (self.map.tile_size, self.map.tile_size))


        # listid
        self.water_images = []
        self.ground_images = []
        self.tree_images = []
        self.combined_images = []

        self.heat_source_images = []
        self.snowy_heated_ground_image = []

        self.ground_surrounding_values = [0, ]
        self.snowy_heated_ground_surrounding_values = [1, 10]
        self.melted_water_values = [0, ]

        self.static_map_surface = None  # Will hold the entire static map surface

    def create_static_map_surface(self):
        # Create a new surface to hold the entire map's static tiles
        width, height = self.map.width * self.map.tile_size, self.map.height * self.map.tile_size
        self.static_map_surface = pygame.Surface((width, height))

        for row_idx, row in enumerate(self.map.data):
            for col_idx, terrain_value in enumerate(row):
                position = (col_idx * self.map.tile_size, row_idx * self.map.tile_size)

                if terrain_value in [0]:
                    self.static_map_surface.blit(self.water_image, position)

                elif terrain_value in [1, 10, 100, 110, 20]:
                    ground_image = None

                    if terrain_value in [1, 10]:
                        surroundings = self.tile_set.check_surroundings(row_idx, col_idx,
                                                                        self.ground_surrounding_values)
                        ground_image = self.tile_set.determine_snowy_ground_image(surroundings)
                        if not ground_image:
                            ground_image = self.ground_image

                    if terrain_value in [100, 110, 20]:
                        surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.snowy_heated_ground_surrounding_values)
                        ground_image = self.tile_set.determine_snowy_heated_ground_image(surroundings)

                        if not ground_image:
                            surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.melted_water_values)
                            ground_image = self.tile_set.determine_melted_water_image(surroundings)

                        if not ground_image:
                            ground_image = self.snowy_heated_image

                    if ground_image:
                        self.static_map_surface.blit(ground_image, position)

    def get_terrain_in_view(self):  # FIXME: EI TÖÖTA VIST?
        terrain_in_view = []
        # Determine the player's position on the grid
        player_grid_x = self.player.x // self.map.tile_size
        player_grid_y = self.player.y // self.map.tile_size

        # Define the render range (11x6 visible tiles)
        row_range_0 = max(0, player_grid_y - 3)  # 6 tiles: 3 above and 3 below
        row_range_1 = min(self.map.height, player_grid_y + 5)  # 5
        col_range_0 = max(0, player_grid_x - 5)  # 11 tiles: 5 to the left and 5 to the right
        col_range_1 = min(self.map.width, player_grid_x + 6)  # 6

        # Collect terrain data within the render range
        for row in range(row_range_0, row_range_1):
            for col in range(col_range_0, col_range_1):
                terrain_in_view.append((col, row))

        return terrain_in_view

    def render_terrain_in_view(self, terrain_in_view):
        self.reset_image_lists()

        for position_by_grid in terrain_in_view:
            row_idx, col_idx = position_by_grid
            terrain_value = self.map.data[row_idx][col_idx]

            # water
            if terrain_value in [0]:
                position = (row_idx * self.map.tile_size - self.camera.offset.x, col_idx * self.map.tile_size - self.camera.offset.y)
                self.water_images.append((self.water_image, position))

            # terrain
            elif terrain_value in self.items.areas_combined:
                ground_image = None
                position = (row_idx * self.map.tile_size - self.camera.offset.x, col_idx * self.map.tile_size - self.camera.offset.y)

                if terrain_value in self.items.cold_area:
                    surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.ground_surrounding_values)
                    ground_image = self.tile_set.determine_snowy_ground_image(surroundings)
                    if not ground_image:
                        ground_image = self.ground_image

                # TODO: Ground + Melted + Water -> Tilesetti vaja
                if terrain_value in self.items.heated_area:
                    surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.snowy_heated_ground_surrounding_values)
                    ground_image = self.tile_set.determine_snowy_heated_ground_image(surroundings)
                    if not ground_image:
                        surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.melted_water_values)
                        ground_image = self.tile_set.determine_melted_water_image(surroundings)

                    if not ground_image:
                        ground_image = self.snowy_heated_image

                self.render_after_ground(terrain_value, position_by_grid, row_idx, col_idx)

                if ground_image:
                    self.ground_images.append((ground_image, position))

        self.combined_images = self.water_images + self.ground_images + self.heat_source_images + self.tree_images
        self.screen.blits(self.combined_images, doreturn=False)


    def render_after_ground(self, terrain_value, position_by_grid, row_idx, col_idx):
        # tree
        if terrain_value in [10, 110]:
            if position_by_grid in self.tree.tree_position_coord:
                position = self.tree.tree_position_coord[position_by_grid]
                # print('position', position)
                self.tree.tree_position_coord[position_by_grid] = position

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
                        position[0] - random.uniform(self.map.tile_size * 0.05, self.map.tile_size * 0.2),
                        position[1] + random.uniform(self.map.tile_size * 0.05, self.map.tile_size * 0.2)
                    )

                # Store tree position in the map (to avoid duplicating)
                self.tree.tree_position_coord[position_by_grid] = (round(position[0], 2), round(position[1], 2))

            # self.tree.width, self.tree.height

            # Append tree image and position
            tree_position = (
            position[0] - self.camera.offset.x - (self.tree.width // 4), position[1] - self.camera.offset.y - (self.tree.height // 2))  #

            self.tree_images.append((self.tree.image, tree_position))

        # heat source
        if terrain_value in [20, 25, 30, 35, 40, 45, 120, 125, 130, 135, 140, 145]:
            image = None
            if terrain_value == 20 or terrain_value == 120:
                image = self.torch_image
            if terrain_value == 25 or terrain_value == 125:
                image = self.firepit_image
            if terrain_value == 30 or terrain_value == 130:
                image = self.campfire_image
            if terrain_value == 35 or terrain_value == 135:
                image = self.bonfire_image
            if terrain_value == 40 or terrain_value == 140:
                image = self.furnace_image
            if terrain_value == 45 or terrain_value == 145:
                image = self.blast_furnace_image

            position = (row_idx * self.map.tile_size - self.camera.offset.x, col_idx * self.map.tile_size - self.camera.offset.y)
            self.heat_source_images.append((image, position))


    def reset_image_lists(self):
        self.water_images = []
        self.ground_images = []
        self.tree_images = []
        self.combined_images = []

        self.heat_source_images = []
        self.snowy_heated_ground_image = []


    def render_player(self):
        # Adjust player position relative to the camera's offset
        player_position_adjusted = (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y)
        pygame.draw.rect(self.screen, color='red', rect=pygame.Rect(player_position_adjusted[0], player_position_adjusted[1], self.player.width, self.player.height))


    def update(self):
        terrain_in_view = self.get_terrain_in_view()
        self.render_terrain_in_view(terrain_in_view)
        self.render_player()

        # print(f"FPS: {int(self.clock.get_fps())}")  # Display FPS

    # for tree around player in range of 2:
    #     dont render in render_terrain_in_view


