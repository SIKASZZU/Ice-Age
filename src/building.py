import pygame


class Building:
    def __init__(self, game_instance, images_instance, map_instance, player_instance, render_instance, camera_instance, heat_zone_instance, inv):
        # ------- # Load Instances # ------- #
        self.map = map_instance
        self.game = game_instance
        self.images = images_instance
        self.player = player_instance
        self.render = render_instance
        self.camera = camera_instance
        self.heat_zone = heat_zone_instance
        self.inventory = inv

        # ------- # Do other stuff xD LOL *_* # ------- #
        self.buildings_dict = {
            'Torch': {
                'image': self.render.torch_image,
                'id': 20
            },

            'Firepit': {
                'image': self.render.firepit_image,
                'id': 25
            },

            'Campfire': {
                'image': self.render.campfire_image,
                'id': 30
            },

            'Bonfire': {
                'image': self.render.bonfire_image,
                'id': 35
            },

            'Furnace': {
                'image': self.render.furnace_image,
                'id': 40
            },

            'Blast Furnace': {
                'image': self.render.blast_furnace_image,
                'id': 45
            },

            'Defencive Wooden Wall': {  # 75x113
                'image': self.render.defencive_wooden_wall_image,
                'id': 9,
                'offset': (0, -self.map.tile_size // 1.5)  # x, y
            },

        }

        self.items_to_display = []
        self.menu_state = False

        self.selected_item = None
        self.selected_item_pos = None
        self.can_place_selected_item = False

        self.building_icon_x = self.building_icon_y = 20
        self.building_menu_pos = self.building_icon_x, self.building_icon_y
        self.width = self.height = 50

        # ------- # Load Building icon # ------- #
        building_icon_path = 'res/images/building_icon.png'
        self.building_icon = self.images.preloading('building_icon', building_icon_path)
        self.building_icon = pygame.transform.scale(self.building_icon, (self.width, self.height))
        self.building_icon_rect = pygame.rect.Rect(self.building_menu_pos[0], self.building_menu_pos[1], self.width,
                                                   self.height)

        # ------- # Run some funcs # ------- #
        self.scaled_images = self.precompute_scaled_images()

    def precompute_scaled_images(self):
        scaled_images = {}
        for name, info in self.buildings_dict.items():
            size_key = f"{name}_{self.width}x{self.height}"
            image = info['image']
            scaled_images[size_key] = pygame.transform.scale(image, (self.width, self.height))
        return scaled_images

    def toggle_menu(self):
        self.menu_state = not self.menu_state

        if not self.menu_state:
            self.selected_item = None
            self.selected_item_pos = None

    @staticmethod
    def apply_red_filter(image):
        """Apply a red filter to the image by modifying its pixels."""
        image_copy = image.copy()  # Copy the image to avoid modifying the original
        image_copy = image_copy.convert_alpha()  # Ensure the image has an alpha channel

        # Access the pixels of the image
        pixels = pygame.surfarray.pixels3d(image_copy)
        alpha = pygame.surfarray.pixels_alpha(image_copy)

        # Iterate over all pixels
        for y in range(image_copy.get_height()):
            for x in range(image_copy.get_width()):
                if alpha[x, y] > 0:  # If the pixel is not transparent

                    # FIXME: muuda mind tagasi vb?
                    # r, g, b = pixels[x, y]
                    # r = min(r + 150, 255)  # Make sure the red component doesn't exceed 255
                    # pixels[x, y] = (r, g, b)

                    pixels[x, y] = (255, 0, 0)

        return image_copy

    def create_building_rects(self):
        self.items_to_display = []

        for i, (key, data) in enumerate(self.buildings_dict.items()):
            x = self.building_icon_x + 10 + self.width + i * 60
            y = self.building_icon_y
            size_key = f"{key}_{self.width}x{self.height}"

            # Get the original image from the dictionary
            image = self.buildings_dict[key]['image']

            # Get the scaled image
            scaled_image = self.scaled_images[size_key]  # No scaling needed here

            # Apply half transparency to the original image (can_place)
            can_place_image = image.copy()  # Create a copy of the original image
            can_place_image.set_alpha(128)  # Apply 50% transparency (128 out of 255)

            # Apply half transparency to the red-filtered image (can_not_place)
            can_not_place_image = self.apply_red_filter(image)  # Red filter applied
            can_not_place_image.set_alpha(128)  # Apply 50% transparency (128 out of 255)

            # Store the images with transparency in the dictionary
            self.buildings_dict[key]['can_place'] = can_place_image
            self.buildings_dict[key]['can_not_place'] = can_not_place_image

            # Create a rect for the building
            building_rect = pygame.Rect(x, y, self.width, self.height)

            # Assign the rect to the dictionary entry
            self.buildings_dict[key]['rect'] = building_rect

            # Store the scaled image and position (to be used for display)
            self.items_to_display.append((scaled_image, (x, y)))

    def display_menu(self):
        if not self.items_to_display:
            self.create_building_rects()

        if self.items_to_display:
            self.game.screen.blits(self.items_to_display)

        # Näitab itemeid mida saab ehitada ja mida ei saa.
        # Nende juures on ka kirjas mida vaja, et neid ehitada.

    def allow_building(self):
        if 'Wood' not in self.inventory.inv_items:
            return False

        if self.inventory.inv_items['Wood'] < self.heat_zone.new_heat_source_cost:
            return False

        return True
        # Et ehitada peab olema heat-zone'is. vb? ainult mingfi autofeeder ja def wallide jaoks vms
        # Kui menu lahti siis saab ainult ehitada ja liikuda.

    def select_item(self, mouse_pos) -> bool:
        for building_name, data in self.buildings_dict.items():
            if data['rect'].collidepoint(mouse_pos):
                self.selected_item = building_name
                return True

        return False

    def hover_effect(self):
        mouse_pos = pygame.mouse.get_pos()  # Get the mouse position

        world_grid_x, world_grid_y = self.camera.click_to_world_grid(self.player.rect.center, mouse_pos, self.map.tile_size)  # Click coords to world grid
        world_x, world_y = world_grid_x * self.map.tile_size - self.camera.offset.x, world_grid_y * self.map.tile_size - self.camera.offset.y

        self.selected_item_pos = world_grid_x, world_grid_y

        terrain_value = self.map.get_terrain_value_at(world_grid_y, world_grid_x)

        if terrain_value in [1, 100] and self.allow_building():
            image = self.buildings_dict[self.selected_item]['can_place']
            self.can_place_selected_item = True

        else:
            image = self.buildings_dict[self.selected_item]['can_not_place']
            self.can_place_selected_item = False

        if 'offset' in self.buildings_dict[self.selected_item]:
            offset_x, offset_y = self.buildings_dict[self.selected_item]['offset']
            self.game.screen.blit(image, (world_x + offset_x, world_y + offset_y))
            return

        self.game.screen.blit(image, (world_x, world_y))
        return

        # Kui saab ehitada siis image on half trasnparent
        # Kui ei saa ehitada siis image on half transparent ja punane

    def build_item(self):
        grid_x, grid_y = self.selected_item_pos
        self.map.data[grid_x][grid_y] = self.buildings_dict[self.selected_item]['id']

        if self.selected_item is self.heat_zone.new_heat_source:
            self.heat_zone.create_new_heat_source((grid_x, grid_y))

        # Kui valitud item + sobiv koht + piisavalt looti playeril -> vasaku clickiga placeib itemi

    def update(self):
        self.game.screen.blit(self.building_icon, self.building_menu_pos)

        if self.menu_state:
            self.display_menu()
