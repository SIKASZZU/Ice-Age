import pygame


class Goods:
    def __init__(self, images, map):
        self.wood = 0
        self.images = images
        self.map = map

        wood_path = 'res/images/snowy_ground.png'
        self.wood_image = self.images.preloading('ground', wood_path)
        self.wood_image = pygame.transform.scale(self.wood_image, (self.map.tile_size, self.map.tile_size))


    def


    def update(self):
