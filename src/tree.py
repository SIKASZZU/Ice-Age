import pygame

class Tree:
    def __init__(self, images, map):
        self.images = images
        self.map = map

        self.width = self.map.tile_size * 1
        self.height = self.map.tile_size * 1.5
        
        self.resource_value = (50, 120)

        path = 'res/images/snowy_tree.png'
        self.img = self.images.preloading('tree', path)
        self.image = pygame.transform.scale(self.img, (self.width, self.height))
        


    def gather(self):
        pass


    def spawn(self):
        pass


    def update(self):
        pass
        #self.spawn()
