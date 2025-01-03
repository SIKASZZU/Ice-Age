import pygame

class Camera:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        self.offset = pygame.math.Vector2()
        
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.borders['left']
        t = self.borders['top']
        w = self.display_surface.get_size()[0]  - (self.borders['left'] + self.borders['right'])
        h = self.display_surface.get_size()[1]  - (self.borders['top'] + self.borders['bottom'])
        self.rect = pygame.Rect(l,t,w,h)


    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def update(self):
        self.center_target_camera(self.player)