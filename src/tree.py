import pygame
import random


class Tree:
    def __init__(self, screen, images, map, camera, player, heat_zone):
        self.images = images
        self.map = map
        self.screen = screen
        self.camera = camera
        self.player = player
        self.heat_zone = heat_zone

        self.width = self.map.tile_size * 1
        self.height = self.map.tile_size * 1.5

        self.total_trees_harvested = 0
        self.resource_stages = {
            'Torch': {
                'Wood': (1, 2)},

            'Firepit': {
                'Wood': (2, 3)},

            'Campfire': {
                'Wood': (3, 4),
                'Sap': (4, 6)},

            'Bonfire': {
                'Wood': (4, 6),
                'Sap': (2, 4)},

            'Furnace': {
                'Wood': (5, 7),
                'Sap': (3, 6)},

            'Blast Furnace': {
                'Wood': (6, 9),
                'Sap': (4, 8)}
        }

        self.resource_value = self.heat_zone.fire_source_dict[self.heat_zone.fire_source_grid]['stage']


        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.random_tree_positions = {}  # grid: pos
        self.tree_rect_dict = {}  # grid: rect
        self.rects = {}  # grid: pos

        path = 'res/images/snowy_tree.png'
        self.img = self.images.preloading('tree', path)
        self.image = pygame.transform.scale(self.img, (self.width, self.height))

    def change_stage(self):
        current_heat_source_stage = self.heat_zone.fire_source_dict[self.heat_zone.fire_source_grid]['stage']
        if current_heat_source_stage in self.resource_stages:
            self.resource_value = self.resource_stages[current_heat_source_stage]
        else:
            self.resource_value = {}

    def gather(self, position=None, required_wood=None):
        if position:
            self.player.remove_items(item_name='Wood', amount=required_wood)

            # removib listidest
            self.random_tree_positions.pop(position)
            self.rects.pop(position)
            self.map.data[position[0]][position[1]] = 20  # muudab terrain value puu asemel fireplace
            self.heat_zone.all_fire_source_list = self.map.get_terrain_value_positions((20, 25, 30, 35, 40, 45))

            return True

        # pick uppimine kaib real coordide jargi, mitte windowi
        for tree in self.rects.items():
            position, tree_rect = tree
            if not self.player.rect.colliderect(tree_rect):
                continue

            # TODO: lisada puude lohkumisele cooldown, animatsioon puudele
            keys = pygame.key.get_pressed()
            if not keys[pygame.K_SPACE]:
                continue
            
            try:
                # Lisab saadud itemid invi
                resources_collected = {
                    resource: random.randint(value_range[0], value_range[1])
                    for resource, value_range in self.resource_value.items()
                }

                # Add each resource to the player's inventory
                for resource, amount in resources_collected.items():
                    self.player.add_items(item_name=resource, amount=amount)

                self.total_trees_harvested += 1

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
        self.tree_rect_dict = {}   # Reset

        # draw rect kaib windowi jargi.
        for position, coord in self.random_tree_positions.items():
            # FIXME: siin teha niimodi et ta ei arvutaks alati recti uuesti.
            # ehk if position in self.rects: ss youkknowww
            half_width, half_height = self.width // 5, self.height // 2
            
            # need vaartused tunduvad vb lambised, aga need on mul tapselt vaadatud maitse jargi.
            # kui tree rect tundub perses ss x,y width ja height on su parimad sobrad
            x = round(coord[0] + half_width, 2)
            y = round(coord[1] - half_height // 1.8, 2)

            width = round(self.width - half_width * 2, 2)
            height = round(self.height - half_height // 1.5, 2)

            # Visuaalsete (window coordinaatide pohine) rectide listi tegemine
            x_for_rect = round(coord[0] - self.camera.offset.x + half_width, 2)
            y_for_rect = round(coord[1] - self.camera.offset.y - half_height // 1.8, 2)
            self.tree_rect_dict[position] = pygame.Rect(x_for_rect, y_for_rect, width, height)

            # Coordinaatide pohine rectide list
            tree_rect = (x, y, width, height)
            if position not in self.rects:
                self.rects[position] = tree_rect

        # Drawing tree rects
        for pos in self.tree_rect_dict:
            pygame.draw.rect(self.screen, 'red', self.tree_rect_dict[pos], 2)

        for pos in self.rects:
            pygame.draw.rect(self.screen, 'yellow', self.rects[pos], 4)
        return


    def update(self):
        self.change_stage()
        self.calculate_rects()
        self.gather()

        return self.tree_rect_dict, self.random_tree_positions
