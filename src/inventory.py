import pygame

class Inventory:
    def __init__(self, screen, images, font):
        self.screen = screen
        self.images = images
        self.font = font
        self.inv_items = {'Wood': 5000}

        width = 50
        height = 50
        
        # tree log image
        tree_logs_path = 'res/images/wood_icon.png'
        tree_log_img = self.images.preloading('log', tree_logs_path)
        self.tree_log_image = pygame.transform.scale(tree_log_img, (width, height))


    def add_items(self, item_name, amount=1):
        """ Add items by name to player's inventory """
        if item_name in self.inv_items:
            self.inv_items[item_name] += amount    
        else: 
            self.inv_items[item_name] = amount

        # print(f'Collected {amount, item_name}. INV:{self.inv_items}')


    def remove_items(self, item_name, amount=-1):
        """ Remove items by name to player's inventory """
        if item_name in self.inv_items:
            self.inv_items[item_name] -= amount
            print(f'Removed {amount, item_name}. INV:{self.inv_items}')
            return True
        else:
            print(f'{item_name} not in INV:{self.inv_items}')
            return False


    def display(self):
        """ Above player HUD for inv """
            
        # FIXME: autistic
        item = 'Wood'

        # for item in self.inv_items:
        #     print(item)
        if item not in self.inv_items:
            text_amount = '0'

        else:
            text_amount = str(self.inv_items[item])

        text_surface = self.font.render(text_amount, True, 'gray')
        screen_center_pos = self.screen.get_width() // 2 + 35, self.screen.get_height() // 2 - 70
        text_rect = text_surface.get_rect(center=screen_center_pos)

        # log_rect  = text_surface.get_rect(center=(self.screen.get_width() // 2 - 35, self.screen.get_height() // 2 - 65))
        self.screen.blit(self.tree_log_image, (self.screen.get_width() // 2 - 70, self.screen.get_height() // 2 - 100))
        self.screen.blit(text_surface, text_rect)


    def update(self):
        self.display()