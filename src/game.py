import pygame
import jurigged

from weather import Weather
from map import Map
from tree import Tree
from camera import Camera
from player import Player

jurigged.watch()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Set up the game window
        pygame.display.set_caption("Ice Age")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game components
        self.player = Player(self.screen)
        self.camera = Camera(self.player)
        self.map = Map(self.screen, self.camera)


    def logic(self):
        self.camera.update()


    def render(self):
        self.screen.fill((0, 0, 0))  # Clear the screen with a black color
        self.map.update()
        self.player.update()
        pygame.display.flip()  # Update the display


    def run(self):
        """Main game loop."""
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.logic()
            self.render()
            self.clock.tick(60)  # Limit the game to 60 FPS
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()