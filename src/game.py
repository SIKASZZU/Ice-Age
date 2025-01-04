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

jurigged.watch()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920 // 1.5, 1080 // 1.5))  # Set up the game window
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game components
        self.camera = Camera()
        self.player = Player(self.screen, self.camera)
        self.map = Map(self.screen, self.camera)
        self.images = Images()
        self.tree = Tree(self.images, self.map)
        self.tile_set = TileSet(self.images, self.map)
        self.renderer = Render(self.screen, self.camera, self.map, self.player, self.clock, self.tree, self.images, self.tile_set)
        self.weather = Weather(self.screen, self.player)

    def logic(self):
        self.camera.update(self.player.rect)  # Keep camera updated with player position


    def render(self):
        self.screen.fill((0, 0, 255))  # FIRST // Clear the screen with a black color
        
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
            self.clock.tick(6000)  # Limit the game to 60 FPS
            pygame.display.set_caption(f"Ice Age - {int(self.clock.get_fps())}")
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()