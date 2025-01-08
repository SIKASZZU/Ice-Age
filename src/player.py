import pygame
from sprite import Sprite


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

        # Animation
        self.last_input = "s"

        self.current_animation = "idle_down"
        self.animation_speed = 5
        
        self.animations = {
            "idle_left": Sprite("res/images/Idle_Left.png", 130, 130, 4, self.animation_speed),
            "idle_right": Sprite("res/images/Idle_Right.png", 130, 130, 4, self.animation_speed),
            "idle_up": Sprite("res/images/Idle_Up.png", 130, 130, 4, self.animation_speed,
            "idle_down": Sprite("res/images/Idle_Down.png", 130, 130, 4, self.animation_speed),

            "move_left": Sprite("res/images/Left.png", 130, 130, 4, self.animation_speed),
            "move_right": Sprite("res/images/Right.png", 130, 130, 4, self.animation_speed),
            "move_up": Sprite("res/images/Up.png", 130, 130, 4, self.animation_speed),
            "move_down": Sprite("res/images/Down.png", 130, 130, 4, self.animation_speed),
        }


    def movement(self):
        moving = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.movement_speed
            self.current_animation = "move_left"
            self.last_input = "a"
            moving = True

        if keys[pygame.K_d]:
            self.x += self.movement_speed
            self.current_animation = "move_right"
            self.last_input = "d"
            moving = True

        if keys[pygame.K_w]:
            self.y -= self.movement_speed
            self.current_animation = "move_up"
            self.last_input = "w"
            moving = True

        if keys[pygame.K_s]:
            self.y += self.movement_speed
            self.current_animation = "move_down"
            self.last_input = "s"
            moving = True

        if keys[pygame.K_a] and keys[pygame.K_d] and keys[pygame.K_w] and keys[pygame.K_s]:
            self.current_animation = "idle_down"
            moving = True

        if not moving:
            if self.last_input == "a":
                self.current_animation = "idle_left"

            if self.last_input == "d":
                self.current_animation = "idle_right"

            if self.last_input == "w":
                self.current_animation = "idle_up"

            if self.last_input == "s":
                self.current_animation = "idle_down"


        self.rect.x = self.x
        self.rect.y = self.y


    def add_items(self, item_name, amount=1):
        """ Add items by name to player's inventory """
        if item_name in self.inv:
            self.inv[item_name] += amount    
        else: 
            self.inv[item_name] = amount

        # print(f'Collected {amount, item_name}. INV:{self.inv}')

    def remove_items(self, item_name, amount=-1):
        """ Remove items by name to player's inventory """
        if item_name in self.inv:
            self.inv[item_name] -= amount
            print(f'Removed {amount, item_name}. INV:{self.inv}')
            return True
        else:
            print(f'{item_name} not in INV:{self.inv}')
            return False



    def inventory_display(self):
        """ Above player """
            
        # FIXME: autistic
        item = 'Wood'

        # for item in self.inv:
        #     print(item)
        if item not in self.inv:
            text_amount = '0'

        else:
            text_amount = str(self.inv[item])

        text_surface = self.font.render(text_amount, True, 'gray')
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2 + 35, self.screen.get_height() // 2 - 70))


        # log_rect  = text_surface.get_rect(center=(self.screen.get_width() // 2 - 35, self.screen.get_height() // 2 - 65))
        self.screen.blit(self.tree_log_image, (self.screen.get_width() // 2 - 70, self.screen.get_height() // 2 - 100))
        self.screen.blit(text_surface, text_rect)



    def update(self):
        self.movement()
        self.animations[self.current_animation].update()

        animation_x = self.x - self.camera.offset.x
        animation_y = self.y - self.camera.offset.y
        self.animations[self.current_animation].draw(self.screen, animation_x, animation_y)


        self.inventory_display()
