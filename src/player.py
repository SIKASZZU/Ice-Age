import pygame

class Player:
    def __init__(self, screen):
        self.screen = screen

        self.x = 10
        self.y = 10
        self.height = 50
        self.width = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprite = 0
        self.health = 100  # freeze meter
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

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def update(self):

        self.movement()
        pygame.draw.rect(self.screen, color='red', rect=self.rect)

