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

        self.width = self.map.tile_size * 1.75
        self.height = self.map.tile_size * 2.5
        self.rect_width = 0
        self.rect_height = 0

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
        self.tree_position_coord = {}  # grid: pos // pos on coordinaatides
        self.rects_window_coord = {}  # grid: rect // visuaalselt joonistamiseks sobilikud koordinaatidega rectid
        self.rects_map_coord = {}  # grid: rect // map koordinaatide jargi rectid

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
            self.tree_position_coord.pop(position)
            self.rects_map_coord.pop(position)
            self.map.data[position[0]][position[1]] = 20  # muudab terrain value puu asemel fireplace
            self.heat_zone.all_fire_source_list = self.map.get_terrain_value_positions((20, 25, 30, 35, 40, 45))

            return True

        # pick uppimine kaib real coordide jargi, mitte windowi
        for tree in self.rects_map_coord.items():
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
                    self.player.add_items(item_name=resource, amount=amount+100)

                self.total_trees_harvested += 1

                # removib listidest
                self.tree_position_coord.pop(position)
                self.rects_map_coord.pop(position)
                self.map.data[position[0]][position[1]] = 1  # muudab terrain value puu asemel groundiks

            except Exception as e: 
                print('Tree removing error @ Tree.gather()', e)
            break  # kui ei breaki, siis error, et self.rects_map_coord dict changed sizes during iteration.


    def spawn(self):
        pass


    def calculate_rects(self):
        """Draws the trees at their positions."""
        self.rects_window_coord = {}   # Reset

        # draw rect kaib windowi jargi.
        for position, coord in self.tree_position_coord.items():
            # need vaartused tunduvad vb lambised, aga need on mul tapselt vaadatud maitse jargi.
            # kui tree rect tundub perses ss x,y width ja height on su parimad sobrad
            width = round(self.width - (self.width // 1.4) // 1.5, 2)
            height = round(self.height - (self.height // 2) // 1.5, 2)

            #### Visuaalsete (window coordinaatide pohine) rectide listi tegemine ####
            x_for_rect = round(coord[0] - self.camera.offset.x, 2)
            y_for_rect = round((coord[1] - self.camera.offset.y) - self.height + self.map.tile_size * 2, 2)
            self.rects_window_coord[position] = pygame.Rect(
                x_for_rect, y_for_rect, width, height)

            #### Coordinaatide pohine rectide list // SELLE JARGI TOIMUB KA PICK UPPIMINE ####
            if position in self.rects_map_coord:
                continue

            x = round(coord[0], 2)
            y = round(coord[1] - self.height + self.map.tile_size * 2, 2)
            tree_rect = (x, y, width, height)
            self.rects_map_coord[position] = tree_rect

    def draw_rects(self):
        # Drawing tree rects
        for pos in self.rects_window_coord:
            pygame.draw.rect(self.screen, 'red', self.rects_window_coord[pos], 2)


    def update(self):
        self.change_stage()
        self.calculate_rects()
        self.gather()
        # self.draw_rects()

        return self.rects_window_coord, self.tree_position_coord
