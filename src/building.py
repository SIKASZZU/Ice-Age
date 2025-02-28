import pygame

class Building:
    def __init__(self, game, images, map, player):
        self.game = game
        self.images = images
        self.map = map
        self.player = player

        self.items_to_display = []
        self.menu_state = False

        self.building_icon_x = self.building_icon_y = 20
        self.building_menu_pos = self.building_icon_x, self.building_icon_y
        self.width = self.height = 50
        building_icon_path = 'res/images/building_icon.png'
        self.buidling_icon = self.images.preloading('building_icon', building_icon_path)
        self.buidling_icon = pygame.transform.scale(self.buidling_icon, (self.width, self.height))
        self.building_icon_rect = pygame.rect.Rect(self.building_menu_pos[0], self.building_menu_pos[1], self.width, self.height)


    def toggle_menu(self):
        self.menu_state = not self.menu_state

        if not self.menu_state:
            self.items_to_display = []
        print(f"Building menu: {'ON' if self.menu_state else 'OFF'}")

    def display_menu(self):
        self.items_to_display = []
        for i in range(3):
            x = self.building_icon_x + 10 + self.width + i * 60
            y = self.building_icon_y
            self.items_to_display.append((self.buidling_icon, (x, y)))

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
        self.game.screen.blit(self.buidling_icon, self.building_menu_pos)

        if self.menu_state:
            self.display_menu()
