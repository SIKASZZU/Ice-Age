from game import Game
from weather import Weather
from map import Map
from tree import Tree
from camera import Camera
from player import Player

class Main():
    def __init__(self):
            
        self.player = Player()
        self.camera = Camera(self.player)
    
    def run()

if __name__ == '__main__':
    main = Main()
    main.run()