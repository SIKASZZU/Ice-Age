import pygame


class Player:
    def __init__(self, screen, camera, map, font, images):
        self.screen = screen
        self.camera = camera
        self.map = map
        self.font = font
        self.images = images

        player_pos_grid = self.map.get_terrain_value_positions(20)  # 20 -> Torch ID

        self.x = player_pos_grid[0][0] * self.map.tile_size
        self.y = player_pos_grid[0][1] * self.map.tile_size
        self.height = 50
        self.width = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement_speed = 5
        
        self.inv = {}
        tree_logs_path = 'res/images/wood_icon.png'
        tree_log_img = self.images.preloading('log', tree_logs_path)
        self.tree_log_image = pygame.transform.scale(tree_log_img, (self.width, self.height)) 


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


    def inventory_display(self):
        """ Above player """
            
        # FIXME: autistic
        item = 'Wood'

        # for item in self.inv:
        #     print(item)
        if item not in self.inv:
            return
        
        text_amount = str(self.inv[item])

        text_surface = self.font.render(text_amount, True, 'gray')
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 35, self.screen.get_height() // 2 - 70))
        # log_rect  = text_surface.get_rect(center=(self.screen.get_width() // 2 - 35, self.screen.get_height() // 2 - 65))

        self.screen.blit(self.tree_log_image, (self.screen.get_width() // 2 - 70, self.screen.get_height() // 2 - 100))
        self.screen.blit(text_surface, text_rect)



    def update(self):
        self.movement()
        self.inventory_display()
