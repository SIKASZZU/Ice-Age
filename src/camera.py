import pygame


class Camera:
    def __init__(self, game_instance):
        self.game = game_instance
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.borders['left']
        t = self.borders['top']
        w = self.display_surface.get_size()[0] - (self.borders['left'] + self.borders['right'])
        h = self.display_surface.get_size()[1] - (self.borders['top'] + self.borders['bottom'])
        self.rect = pygame.Rect(l, t, w, h)


    def center_target_camera(self, target):
        self.offset.x = target.centerx - self.half_w
        self.offset.y = target.centery - self.half_h

    def click_to_world_coordinate(self, player_rect_center, mouse_pos):
        """
        Converts mouse position to world coordinates.

        player_rect_center -> self.player.rect.center,
        mouse_pos -> pygame.mouse.get_pos(),

        Returns world_x, world_y -> Coordinate position
        """

        world_x = player_rect_center[0] + (mouse_pos[0] - self.game.screen_x // 2)
        world_y = player_rect_center[1] + (mouse_pos[1] - self.game.screen_y // 2)
        return world_x, world_y

    def click_to_world_grid(self, player_rect_center, mouse_pos, tile_size):
        """
        Converts mouse position to world grid coordinates.

        player_rect_center -> self.player.rect.center,
        mouse_pos -> pygame.mouse.get_pos(),
        tile_size -> self.map.tile_size,

        Returns world_grid_x, world_grid_y -> Grid position
        """

        world_grid_x = (player_rect_center[0] + (mouse_pos[0] - self.game.screen_x // 2)) // tile_size
        world_grid_y = (player_rect_center[1] + (mouse_pos[1] - self.game.screen_y // 2)) // tile_size

        return world_grid_x, world_grid_y

    def update(self, player):
        self.center_target_camera(player)
