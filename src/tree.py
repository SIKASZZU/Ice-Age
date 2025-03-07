import pygame
import random

class Tree:
    def __init__(self, screen, images, map, camera, player, heat_zone, items):
        self.images = images
        self.map = map
        self.screen = screen
        self.camera = camera
        self.player = player
        self.heat_zone = heat_zone
        self.items = items

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

        # snowy tree image
        path_snowy = 'res/images/snowy_tree.png'
        self.img_snowy = self.images.preloading('tree_snowy', path_snowy)
        self.image_snowy = pygame.transform.scale(self.img_snowy, (self.width, self.height))

        # normal tree image
        path = 'res/images/tree.png'
        self.img = self.images.preloading('tree', path)
        self.image = pygame.transform.scale(self.img, (self.width, self.height))

        # harvestimisel leaning left, et luua animatsioon puule
        path = 'res/images/tree_lean_left_1.png' 
        self.img = self.images.preloading('tree_lean_left_1', path)
        self.image_lean_left_1 = pygame.transform.scale(self.img, (self.width, self.height))

        path = 'res/images/tree_lean_left_2.png' 
        self.img = self.images.preloading('tree_lean_left_2', path)
        self.image_lean_left_2 = pygame.transform.scale(self.img, (self.width, self.height))

        path = 'res/images/tree_lean_left_1_snowy.png' 
        self.img = self.images.preloading('tree_lean_left_1_snowy', path)
        self.image_lean_left_1_snowy = pygame.transform.scale(self.img, (self.width, self.height))

        path = 'res/images/tree_lean_left_2_snowy.png' 
        self.img = self.images.preloading('tree_lean_left_2_snowy', path)
        self.image_lean_left_2_snowy = pygame.transform.scale(self.img, (self.width, self.height))

        self.cut_anim_sorted_snowy = [10, 10_5, 10_6]
        self.cut_anim_sorted       = [110, 110_5, 110_6]

        self.harvest_times = {}  # Igal tree'l on oma harvest time
        self.latest_harvest = pygame.time.get_ticks()
        self.anim_change_timings = (300, 1500)
        self.pick_up_time = 3000


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

        ### pick uppimine kaib real coordide jargi, mitte windowi
        current_time = pygame.time.get_ticks()

        if self.harvest_times:
            positions_to_pop = []
            for pos, timings in self.harvest_times.items():
                # if puu muutus fire sourciks randomly => ei anna playerile harvest woodi ning ei updatei tree animationi.
                if pos in self.heat_zone.fire_source_dict:
                    continue
                positions_to_pop = self.change_animation_stage(current_time, timings, pos, positions_to_pop)
                
            for pos_to_pop in positions_to_pop:
                self.gather_tree_at_pos(pos_to_pop)
                self.harvest_times.pop(pos_to_pop)

        for tree in self.rects_map_coord.items():
            position, tree_rect = tree
            if not self.player.rect.colliderect(tree_rect):
                continue

            keys = pygame.key.get_pressed()
            if not keys[pygame.K_SPACE]:
                continue

            if position not in self.harvest_times:
                self.harvest_times[position] = (current_time, current_time, 0)


    def change_animation_stage(self, current_time, timings, pos, positions_to_pop):
        change_interval = random.randint(self.anim_change_timings[0], self.anim_change_timings[1])
        x_grid, y_grid = pos
        time_of_harvest, last_anim_update, cut_anim_index = timings

        if current_time - time_of_harvest < self.pick_up_time and current_time - last_anim_update > change_interval:
            cut_anim_index +=1  # select next animation in cut animation
            cut_anim_index %=3  # arvuta ymber et index pysis range 0-2 ehk reminder of max list value
            self.harvest_times[pos] = (time_of_harvest, current_time, cut_anim_index)
            terrain_value = self.map.data[x_grid, y_grid]
            
            if terrain_value in self.items.cold_area:
                self.map.data[x_grid, y_grid] = self.cut_anim_sorted_snowy[cut_anim_index]

            elif terrain_value in self.items.heated_area:
                self.map.data[x_grid, y_grid] = self.cut_anim_sorted[cut_anim_index]

        # add to list if harvest animation cooldown is reached. Time to remove the tree
        if current_time - time_of_harvest > self.pick_up_time:
            positions_to_pop.append(pos)

        return positions_to_pop


    def gather_tree_at_pos(self, position):
        """ Extension function of tree.gather()"""
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


    def spawn(self):
        pass


    def calculate_rects(self):
        """Draws the trees at their positions."""
        self.rects_window_coord = {}   # Reset

        # draw rect kaib windowi jargi.
        for position, coord in self.tree_position_coord.items():
            
            if position not in self.rects_window_coord:
                # need vaartused tunduvad vb lambised, aga need on mul tapselt vaadatud maitse jargi.
                # kui tree rect tundub perses ss x,y width ja height on su parimad sobrad
                width = round(self.width - (self.width // 1.4), 2)
                height = round(self.height - (self.height // 2), 2)

                #### Visuaalsete (window coordinaatide pohine) rectide listi tegemine ####
                x_for_rect = round(coord[0] - self.camera.offset.x + self.width // 8, 2)
                y_for_rect = round((coord[1] - self.camera.offset.y) - self.height + self.map.tile_size * 2, 2)
                self.rects_window_coord[position] = pygame.Rect(
                    x_for_rect, y_for_rect, width, height)

            #### Coordinaatide pohine rectide list // SELLE JARGI TOIMUB KA PICK UPPIMINE ####
            if position not in self.rects_map_coord:

                x = round(x_for_rect + self.camera.offset.x, 2)
                y = round(y_for_rect + self.camera.offset.y, 2)
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
        #self.draw_rects()

        return self.rects_window_coord, self.tree_position_coord
