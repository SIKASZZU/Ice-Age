import pygame


class Building:
    def __init__(self, game, images, map, player, render):
        # ------- # Load Instances # ------- #
        self.game = game
        self.images = images
        self.map = map
        self.player = player
        self.render = render

        # ------- # Do other stuff xD LOL *_* # ------- #
        self.buildings_dict = {
            'Torch': self.render.torch_image,
            'Firepit': self.render.firepit_image,
            'Campfire': self.render.campfire_image,
            'Bonfire': self.render.bonfire_image,
            'Furnace': self.render.furnace_image,
            'Blast Furnace': self.render.blast_furnace_image,
        }

        self.items_to_display = []
        self.items_to_display_rects = []
        self.menu_state = False

        self.building_icon_x = self.building_icon_y = 20
        self.building_menu_pos = self.building_icon_x, self.building_icon_y
        self.width = self.height = 50

        # ------- # Load Building icon # ------- #
        building_icon_path = 'res/images/building_icon.png'
        self.building_icon = self.images.preloading('building_icon', building_icon_path)
        self.building_icon = pygame.transform.scale(self.building_icon, (self.width, self.height))
        self.building_icon_rect = pygame.rect.Rect(self.building_menu_pos[0], self.building_menu_pos[1], self.width, self.height)

        # ------- # Run some funcs # ------- #
        self.scaled_images = self.precompute_scaled_images()


    def precompute_scaled_images(self):
        scaled_images = {}
        for key, image in self.buildings_dict.items():
            size_key = f"{key}_{self.width}x{self.height}"
            scaled_images[size_key] = pygame.transform.scale(image, (self.width, self.height))
        return scaled_images

    def toggle_menu(self):
        self.menu_state = not self.menu_state

        if not self.menu_state:
            self.items_to_display = []

    def display_menu(self):
        self.items_to_display = []
        self.items_to_display_rects = []

        for i, key in enumerate(self.buildings_dict):
            x = self.building_icon_x + 10 + self.width + i * 60
            y = self.building_icon_y
            size_key = f"{key}_{self.width}x{self.height}"

            scaled_image = self.scaled_images[size_key]  # No scaling needed here
            building_rect = pygame.rect.Rect(x, y, self.width, self.height)

            self.items_to_display.append((scaled_image, (x, y)))
            self.items_to_display_rects.append(((x, y), building_rect))

        if self.items_to_display:
            self.game.screen.blits(self.items_to_display)

        # Näitab itemeid mida saab ehitada ja mida ei saa.
        # Nende juures on ka kirjas mida vaja, et neid ehitada.

    def allow_building(self):
        ...
        # Et ehitada peab olema heat-zone'is.
        # Kui menu lahti siis saab ainult ehitada ja liikuda.

    def select_item(self):
        ...
        # Click'id valitud item'i peale.
        # Fire source
        # Defencive wall
        # Auto fire source tanker
        # Ect...

    def hover_effect(self):
        ...
        # Kui valid ja hover'id player'i range'is siis näitab pre-built image't roheliselt või väiksema transparenciga.
        # Sinna kuhu ei saa ehitada ei tehi seda pre-buildt imaget või on punane

    def build_item(self):
        ...
        # Kui valitud item + sobiv koht + piisavalt looti playeril -> vasaku clickiga placeib itemi

    def update(self):
        self.game.screen.blit(self.building_icon, self.building_menu_pos)

        if self.menu_state:
            self.display_menu()
