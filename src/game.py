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

        # Initialize game components
        self.camera = Camera()
        self.map = Map(self.screen, self.camera)
        self.player = Player(self.screen, self.camera, self.map)
        self.images = Images()
        self.tree = Tree(self.images, self.map)
        self.tile_set = TileSet(self.images, self.map)

        self.heat_zone = HeatZone(self.screen, self.map, self.camera)
        self.renderer = Render(self.screen, self.camera, self.map, self.player, self.clock, self.tree, self.images, self.tile_set, self.heat_zone)
        self.weather = Weather(self.screen, self.player)
        self.framerate = Framerate()




    def logic(self):
        self.camera.update(self.player.rect)  # Keep camera updated with player position

    def render(self):
        self.screen.fill((0, 0, 255))  # FIRST // Clear the screen with a black color
        self.heat_zone.update_heat_zone()
        self.renderer.update()
        self.player.update()  # Update player and keep them at the center of the screen
        self.tree.update()
        self.weather.update()
        
        pygame.display.flip()  # LAST // Update display

    def run(self):
        """Main game loop."""

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.render()
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