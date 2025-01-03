import pygame


class Render:
    def __init__(self, screen, camera, map, player, font, clock):
        self.screen = screen
        self.camera = camera
        self.map = map
        self.player = player
        self.font = font
        self.clock = clock

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
        ...


    def update(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        # self.render_terrain_in_view(self.get_terrain_in_view())
        self.player.update()  # Update player position and render

        # Display FPS
        fps_text = self.font.render(f"FPS: {self.clock.get_fps():.2f}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        pygame.display.flip()  # Update the screen with the new rendering