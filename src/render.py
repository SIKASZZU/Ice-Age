import pygame
import random

class Render:
    def __init__(self, game, camera, map, player, tree, images, tile_set, heat_zone, items, r_sequence):
        self.game = game
        self.camera = camera
        self.map = map
        self.player = player
        self.tree = tree
        self.images = images
        self.tile_set = tile_set
        self.heat_zone = heat_zone
        self.items = items
        self.r_sequence = r_sequence

        # Calculate number of tiles covering the full screen
        self.tiles_x = self.game.screen_x // self.map.tile_size + 1
        self.tiles_y = self.game.screen_y // self.map.tile_size + 2

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

        defencive_wooden_wall = 'res/images/defencive_wooden_wall.png'
        self.defencive_wooden_wall_image = self.images.preloading('defencive_wooden_wall', defencive_wooden_wall)
        self.defencive_wooden_wall_image = pygame.transform.scale(self.defencive_wooden_wall_image, (self.map.tile_size, self.map.tile_size * 1.5))

        # listid
        self.water_images = []
        self.ground_images = []
        self.tree_images = []
        self.tree_images_before = []  # before on aeg, ehk before playerit tuleb need pildid renderida
        self.tree_images_after = []
        self.defencive_images = []

        self.combined_images = []  # koik pildid koos, mis peavad renderitud olema
        self.images_witho_afters = []  # siin listis ei ole tree'sid, mis peavad after player renderitud olema.
        self.tree_images = []  # koik tree pildid koos

        self.heat_source_images = []
        self.snowy_heated_ground_image = []

        self.ground_surrounding_values = [0, ]
        self.snowy_heated_ground_surrounding_values = [1, 10]
        self.melted_water_values = [0, ]

        self.defencive_wooden_wall_values = [9, ]

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
                        surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.ground_surrounding_values)
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

    def get_terrain_in_view(self):
        terrain_in_view = []

        # Determine player's position on the grid
        player_grid_x = int(self.player.x // self.map.tile_size)
        player_grid_y = int(self.player.y // self.map.tile_size)

        # Ensure proper left and top coverage
        row_range_0 = max(0, player_grid_y - (self.tiles_y // 2) - 1)
        row_range_1 = min(self.map.height, player_grid_y + (self.tiles_y // 2) + 2)
        col_range_0 = max(0, player_grid_x - (self.tiles_x // 2) - 2)
        col_range_1 = min(self.map.width, player_grid_x + (self.tiles_x // 2) + 2)

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
            position = (row_idx * self.map.tile_size - self.camera.offset.x, col_idx * self.map.tile_size - self.camera.offset.y)

            # water
            if terrain_value in [0]:
                self.water_images.append((self.water_image, position))
                continue

            # terrain
            elif terrain_value in self.items.areas_combined:
                ground_image = None

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

                # def wall
                if terrain_value == 9:
                    position = (row_idx * self.map.tile_size - self.camera.offset.x,
                                col_idx * self.map.tile_size - self.camera.offset.y - self.map.tile_size // 1.1)

                    surroundings = self.tile_set.check_surroundings(row_idx, col_idx, self.defencive_wooden_wall_values)
                    defencive_wooden_wall_image = self.tile_set.determine_defencive_wooden_wall_image(surroundings)

                    self.defencive_images.append((defencive_wooden_wall_image, position))


        images = (self.water_images, self.ground_images, self.heat_source_images, self.tree_images)
        return images


    def render_after_ground(self, terrain_value, position_by_grid, row_idx, col_idx):
        # tree
        if terrain_value in self.items.trees:
            
            tree_image = self.tree.image if terrain_value == 110 else self.tree.image_snowy

            if terrain_value == 10_5:  
                tree_image = self.tree.image_lean_left_1_snowy
            
            elif terrain_value == 10_6:  
                tree_image = self.tree.image_lean_left_2_snowy
            
            elif terrain_value == 110_5:  
                tree_image = self.tree.image_lean_left_1
            
            elif terrain_value == 110_6:  
                tree_image = self.tree.image_lean_left_2
            
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
            tree_position = (position[0] - self.camera.offset.x - (self.tree.width // 4),
                             position[1] - self.camera.offset.y - (self.tree.height // 2))

            self.tree_images.append((tree_image, tree_position))

            if position_by_grid in self.r_sequence.render_after_player:
                self.tree_images_after.append((tree_image, tree_position))                

            else:
                self.tree_images_before.append((tree_image, tree_position))

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

        self.tree_images_before = []
        self.tree_images_after = []

        self.images_witho_afters = []
        self.combined_images = []

        self.heat_source_images = []
        self.snowy_heated_ground_image = []

        self.defencive_images = []

    def render_player(self):
        # Adjust player position relative to the camera's offset
        player_position_adjusted = (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y)
        pygame.draw.rect(self.game.screen, color='red', rect=pygame.Rect(player_position_adjusted[0], player_position_adjusted[1], self.player.width, self.player.height))


    def update(self, render_after, animations):
        animation_x, animation_y = animations
        terrain_in_view = self.get_terrain_in_view()
        
        self.combined_images = self.render_terrain_in_view(terrain_in_view)
        self.images_witho_afters = self.combined_images[:3]
        self.tree_images = self.combined_images[3]  # render after if render_after == True

        self.combined_images = self.combined_images[0] + self.combined_images[1] + self.combined_images[2] + self.combined_images[3]
        self.images_witho_afters = self.images_witho_afters[0] + self.images_witho_afters[1] + self.images_witho_afters[2] + self.tree_images_before
        self.game.screen.blits(self.defencive_images)

        if render_after:
            self.game.screen.blits(self.images_witho_afters, doreturn=False)
            self.render_player()
            self.player.animations[self.player.current_animation].draw(self.game.screen, animation_x, animation_y)
            self.game.screen.blits(self.tree_images_after, doreturn=False)
            self.game.screen.blits(self.defencive_images)
            return

        self.game.screen.blits(self.combined_images, doreturn=False)
        self.render_player()
        self.player.animations[self.player.current_animation].draw(self.game.screen, animation_x, animation_y)

            

        # print(f"FPS: {int(self.game.clock.get_fps())}")  # Display FPS

    # for tree around player in range of 2:
    #     dont render in render_terrain_in_view


