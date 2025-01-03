import pygame

class Player:
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera

        self.x = 10
        self.y = 10
        self.height = 50
        self.width = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement_speed = 5


    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.movement_speed
        if keys[pygame.K_d]:
            self.x += self.movement_speed
        if keys[pygame.K_w]:
            self.y -= self.movement_speed
        if keys[pygame.K_s]:
            self.y += self.movement_speed

        self.rect.x = self.x
        self.rect.y = self.y


    def update(self):
        self.movement()
