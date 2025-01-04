import pygame


class Player:
    def __init__(self, screen, camera, map):
        self.screen = screen
        self.camera = camera
        self.map = map

        player_pos_grid = self.map.get_terrain_value_positions(20)  # 20 -> Torch ID

        self.x = player_pos_grid[0][0] * self.map.tile_size
        self.y = player_pos_grid[0][1] * self.map.tile_size
        self.height = 50
        self.width = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement_speed = 5
        
        self.inv = {}


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


    def add_items(self, item_name, amount=1):
        """ Add items by name to player's inventory """
        if item_name in self.inv:
            self.inv[item_name] += amount    
        else: 
            self.inv[item_name] = amount

        print(f'Collected {amount, item_name}. INV:{self.inv}')

    def remove_items(self, item_name, amount=-1):
        """ Remove items by name to player's inventory """
        if item_name in self.inv:    
            self.inv[item_name] += amount
        else: 
            self.inv[item_name] = amount

        print(f'Removed {amount, item_name}. INV:{self.inv}')


    def inventory(self):
        pass
            

    def update(self):
        self.movement()
        self.inventory()
