import pygame


class ManageBuilding:
    def __init__(self, game_instance, map_instance, player_instance, manage_heat_source_instance):
        self.game = game_instance
        self.map = map_instance
        self.player = player_instance
        self.manage_heat_source = manage_heat_source_instance

        self.buildings_list = [20, 25, 30, 35, 40, 45, 9]
        self.menu_state = False

        self.building_pos = None

    def toggle_menu(self, pos):
        self.menu_state = not self.menu_state
        if self.menu_state and not self.building_pos:
            self.building_pos = pos
            return

        self.building_pos = None
        return

    def display_menu(self):
        ...

    def decide_action(self):
        ...
        # Vaatab mida clickiti ja selle järgi

    def update(self):
        if self.menu_state:
            self.manage_heat_source.update(self.game.screen)


class ManageHeatSources:
    def __init__(self, game_instance, heat_zone_instance, map_instance, render_instance):
        self.game = game_instance
        self.heat_zone = heat_zone_instance
        self.map = map_instance
        self.render = render_instance

        self.gui_background_color = (50, 50, 50, 200)  # Dark gray with transparency
        self.title_font = pygame.font.Font(None, 35)
        self.base_font = pygame.font.Font(None, 24)

        # FIXME: values funcid
        # Example values
        self.upgrade_text = self.base_font.render('Upgrade:', True, (255, 255, 255))
        self.fuel_text = self.base_font.render('Fuel:', True, (255, 255, 255))

        self.upgrade_cost = '1 Wood'
        self.fuel_count = '0/5'

        self.upgrade_cost_label = self.base_font.render(f'Cost: {self.upgrade_cost}', True, (255, 255, 255))

        # FIXME: entryt vaja
        self.fuel_entry_text = self.base_font.render('Enter amount', True, (255, 255, 255))
        self.fuel_count_label = self.base_font.render(f'Count: {self.fuel_count}', True, (255, 255, 255))


        # - # - # - # - # - # Gui background # - # - # - #  - # - #
        self.menu_width = 375  # self.game.screen_x // 1.5
        self.menu_height = 160  # self.game.screen_y // 5
        self.menu_x = (self.game.screen_x - self.menu_width) // 2
        self.menu_y = self.game.screen_y - self.menu_height - self.map.tile_size
        self.gui_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)

        self.padding = 15

        # - # - # - # - # - # Buttons # - # - # - #  - # - #
        self.button_padding = self.padding

        self.button_width = 105
        self.button_height = 30

        self.button_x = self.menu_x + self.button_padding
        self.button_y = self.menu_y + self.menu_height - self.button_padding - self.button_height

        self.upgrade_button = pygame.Rect(self.button_x, self.button_y, self.button_width, self.button_height)
        self.fuel_button = pygame.Rect(self.button_x + self.button_width + self.button_padding, self.button_y, self.button_width, self.button_height)
        self.destroy_button = pygame.Rect(self.button_x + 2 * (self.button_width + self.button_padding), self.button_y, self.button_width, self.button_height)

        # - # - # - # - # - # Button texts # - # - # - #  - # - #
        self.upgrade_label = self.base_font.render('Upgrade', True, (255, 255, 255))
        self.fuel_label = self.base_font.render('Fuel', True, (255, 255, 255))
        self.destroy_label = self.base_font.render('Destroy', True, (255, 255, 255))

        # - # - # - # - # - # Button labels # - # - # - #  - # - #
        self.upgrade_label_x = self.upgrade_button.x + (self.button_width - self.upgrade_label.get_width()) // 2
        self.upgrade_label_y = self.upgrade_button.y + self.button_height // 4

        self.fuel_label_x = self.fuel_button.x + (self.button_width - self.fuel_label.get_width()) // 2
        self.fuel_label_y = self.fuel_button.y + self.button_height // 4

        self.destroy_label_x = self.destroy_button.x + (self.button_width - self.destroy_label.get_width()) // 2
        self.destroy_label_y = self.destroy_button.y + self.button_height // 4

        self.building_image = pygame.transform.scale(self.render.campfire_image, (85, 85))



    def destroy(self, pos):
        self.map.data[pos[0]][pos[1]] = 1

    def handle_event(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.upgrade_button.collidepoint(mouse_pos):
                print("Upgrade button clicked")
            elif self.fuel_button.collidepoint(mouse_pos):
                print("Fuel entry clicked")
            elif self.destroy_button.collidepoint(mouse_pos):
                self.destroy(pos)
                return True

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Default button colors
        upgrade_color = '#8AAD62'
        fuel_color = '#8AAD62'
        destroy_color = '#AF0D05'

        # Darker hover effect
        if self.upgrade_button.collidepoint(mouse_pos):
            upgrade_color = '#728E51'
        if self.fuel_button.collidepoint(mouse_pos):
            fuel_color = '#728E51'
        if self.destroy_button.collidepoint(mouse_pos):
            destroy_color = '#8E0B04'

        # Draw semi-transparent background
        gui_background = pygame.Surface((self.gui_rect.width, self.gui_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(gui_background, self.gui_background_color, gui_background.get_rect())
        screen.blit(gui_background, self.gui_rect.topleft)

        # Blit building
        screen.blit(self.building_image, (self.menu_x + self.padding + self.padding // 2, self.menu_y + self.padding))


        # Draw buttons with hover effect
        pygame.draw.rect(screen, upgrade_color, self.upgrade_button)
        pygame.draw.rect(screen, fuel_color, self.fuel_button)
        pygame.draw.rect(screen, destroy_color, self.destroy_button)

        # Blit text

        screen.blit(self.upgrade_label, (self.upgrade_label_x, self.upgrade_label_y))
        screen.blit(self.fuel_label, (self.fuel_label_x, self.fuel_label_y))
        screen.blit(self.destroy_label, (self.destroy_label_x, self.destroy_label_y))


        screen.blit(self.upgrade_cost_label, (220, 210))
        screen.blit(self.fuel_entry_text, (225, 315))
        screen.blit(self.fuel_count_label, (220, 350))
        screen.blit(self.upgrade_text, (self.upgrade_label_x + self.button_width, self.menu_y + self.padding))
        screen.blit(self.fuel_text, (self.upgrade_label_x + self.button_width * 2, self.menu_y + self.padding))


class ManageDefenciveWalls:
    def __init__(self):
        ...

    def display(self):
        ...
        # Teeb UI ära... aka buttonid tekst mida iganes seletab ära mis seal teha saab

    def options(self):
        ...
        # Muudab ukseks
        # Lõhub ära
