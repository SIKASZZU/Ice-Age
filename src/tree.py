import pygame
import random

class Tree:
    def __init__(self, screen, images, map, camera, player):
        self.images = images
        self.map = map
        self.screen = screen
        self.camera = camera
        self.player = player

        self.width = self.map.tile_size * 1
        self.height = self.map.tile_size * 1.5
        
        self.resource_value = (50, 120)

        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.random_tree_positions = {}
        self.rects = {}

        path = 'res/images/snowy_tree.png'
        self.img = self.images.preloading('tree', path)
        self.image = pygame.transform.scale(self.img, (self.width, self.height))
        


    def gather(self):
        # pick uppimine kaib real coordide jargi, mitte windowi
        for tree in self.rects.items():
            position, tree_rect = tree
            #print(self.player.rect, tree_rect)
            if not self.player.rect.colliderect(tree_rect):
                continue

            # TODO: lisada puude lohkumisele cooldown, animatsioon puudele
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                try:
                    # inventory taiendamine woodiga
                    wood_amount = random.randint(self.resource_value[0], self.resource_value[1])
                    self.player.add_items(item_name='Wood', amount=wood_amount)

                    # removib listidest
                    self.random_tree_positions.pop(position)
                    self.rects.pop(position)
                    self.map.data[position[0]][position[1]] = 1  # muudab terrain value puu asemel groundiks
                except Exception as e: 
                    print('Tree removing error @ Tree.gather()', e)
                break  # kui ei breaki, siis error, et self.rects dict changed sizes during iteration.

    def spawn(self):
        pass


    def calculate_rects(self):
        """Draws the trees at their positions."""
        
        # draw rect kaib windowi jargi.
        for position, coord in self.random_tree_positions.items():
            # FIXME: siin teha niimodi et ta ei arvutaks alati recti uuesti.
                # ehk if position in self.rects: ss youkknowww
            half_width, half_height =  self.width // 5, self.height // 2
            
            # need vaartused tunduvad vb lambised, aga need on mul tapselt vaadatud maitse jargi.
            # kui tree rect tundub perses ss x,y width ja height on su parimad sobrad
            x = round(coord[0] + half_width, 2)
            y = round(coord[1], 2)

            width = round(self.width - half_width * 2, 2)
            height = round(self.height - half_height // 1.1, 2)

            # JOONISTAMISEKS AINULT
            x_for_rect = round(coord[0] - self.camera.offset.x + half_width, 2)
            y_for_rect = round(coord[1] - self.camera.offset.y, 2)
            pygame.draw.rect(self.screen, 'red', (x_for_rect, y_for_rect, width, height), 2)
            ###

            tree_rect = (x, y, width, height)
            if position not in self.rects:  self.rects[position] = tree_rect
            

    def update(self):
        self.calculate_rects()
        self.gather()
