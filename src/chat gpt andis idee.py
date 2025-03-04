class Building:
    def __init__(self, game, images, map, player, render):
        # Existing initialization code...
        self.player_moved = True
        self.mouse_moved = True
        self.last_mouse_pos = pygame.mouse.get_pos()
        # Other initialization code...

    def update(self):
        current_mouse_pos = pygame.mouse.get_pos()
        if current_mouse_pos != self.last_mouse_pos:
            self.mouse_moved = True
            self.last_mouse_pos = current_mouse_pos

        if self.player_moved or self.mouse_moved:
            self.hover_effect()
            self.player_moved = False
            self.mouse_moved = False

        self.game.screen.blit(self.building_icon, self.building_menu_pos)

        if self.menu_state:
            self.display_menu()
Step 2: Update Hover Effect Method
def hover_effect(self):
    mouse_pos = pygame.mouse.get_pos()

    if self.selected_item:
        size_key = f"{self.selected_item}_{self.width}x{self.height}"
        hover_image = self.scaled_images[size_key]
        hover_rect = hover_image.get_rect(center=mouse_pos)

        if self.is_within_player_range(mouse_pos):
            hover_image.set_alpha(128)  # Semi-transparent
        else:
            hover_image = hover_image.copy()
            hover_image.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)

        self.game.screen.blit(hover_image, hover_rect.topleft)

def is_within_player_range(self, pos):
    player_pos = self.player.rect.center
    distance_sq = (player_pos[0] - pos[0]) ** 2 + (player_pos[1] - pos[1]) ** 2
    return distance_sq <= self.player.build_range ** 2
Step 3: Track Player Movement
Ensure you set self.player_moved = True whenever the player moves. This can be done in the player movement logic:

class Player:
    def move(self, direction):
        # Existing movement code...
        self.rect.move_ip(direction)
        self.building.player_moved = True  # Notify the Building class of player movement
