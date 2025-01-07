import pygame
import jurigged

from weather import Weather
from map import Map
from tree import Tree
from camera import Camera
from player import Player
from render import Render
from images import Images
from tileset import TileSet
from heat_zone import HeatZone
from framerate import Framerate

jurigged.watch()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))  # Set up the game window
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 50)

        # Initialize game components
        self.camera = Camera()
        self.map = Map(self.screen, self.camera)
        self.images = Images()
        self.player = Player(self.screen, self.camera, self.map, self.font, self.images)
        self.heat_zone = HeatZone(self.screen, self.map, self.camera, self.player, self.images)
        self.tree = Tree(self.screen, self.images, self.map, self.camera, self.player, self.heat_zone)
        self.tile_set = TileSet(self.images, self.map)

        self.renderer = Render(self.screen, self.camera, self.map, self.player, self.clock, self.tree, self.images, self.tile_set, self.heat_zone)
        self.weather = Weather(self.screen, self.player)
        self.framerate = Framerate()


        self.terrain_in_view = self.renderer.get_terrain_in_view()

        self.tree_rect_dict = self.tree.calculate_rects()


        self.required_wood = self.heat_zone.new_heat_source_cost


    def logic(self):
        self.camera.update(self.player.rect)  # Keep camera updated with player position


    def render(self, mouse_pos):
        terrain_in_view = self.renderer.get_terrain_in_view()

        self.screen.fill((0, 0, 255))  # FIRST // Clear the screen with a black color
        self.renderer.update()

        self.tree_rect_dict, self.random_tree_positions = self.tree.update()

        # During hover, show the cost
        if self.tree_rect_dict:
            self.heat_zone.display_new_heat_source_cost(mouse_pos, self.tree_rect_dict, self.random_tree_positions, self.required_wood)

        self.player.update()  # Alati enne renderer'i

        self.heat_zone.update()
        self.heat_zone.draw_all_progress_bars(terrain_in_view)

        self.weather.update()

        pygame.display.flip()  # LAST // Update display

    def run(self):
        """Main game loop."""

        while self.running:
            self.required_wood = self.heat_zone.new_heat_source_cost + len(self.heat_zone.all_fire_source_list) * 2
            mouse_pos = pygame.mouse.get_pos()  # Get the mouse position

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.heat_zone.feed_heat_source(mouse_pos)
                        if 'Wood' in self.player.inv:
                            if self.player.inv['Wood'] >= self.required_wood:
                                tree_pos = self.heat_zone.create_new_heat_source(mouse_pos, self.tree_rect_dict)
                                self.tree.gather(tree_pos, self.required_wood)

            self.render(mouse_pos)
            self.logic()

            # Update FPS list
            current_fps = self.clock.get_fps()
            self.framerate.update(current_fps)

            # Display FPS statistics

            fps_text = self.framerate.display_fps_statistics()

            self.clock.tick(5000)  # Limit the game to 60 FPS
            pygame.display.set_caption(f"Ice Age - {fps_text}")

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()