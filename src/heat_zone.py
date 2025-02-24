import pygame


class HeatZone:
    def __init__(self, screen, map, camera, player, images):
        self.map = map
        self.camera = camera
        self.screen = screen
        self.player = player
        self.images = images

        self.fire_source_dict = {}
        self.position_upgradable = []
        self.position_upgradable = []

        # self.fire_source_dict = {
        # position: {
        # 'stage': "Torch",
        # 'count': 0,
        # 'position': self.fire_source_grid,
        # 'rect': None
        # 'fuel count': 0  <- lisab kui lisatakse puitu, muidu pole listis
        # 'fuel counter': 0,
        # 'heat range': self.new_heat_source
        # }}

        self.fire_source_rect_list = []

        self.heat_zones_dict: dict = {
            'Torch': 0,           # ID 20
            'Firepit': 1,         # ID 25
            'Campfire': 2,        # ID 30
            'Bonfire': 3,         # ID 35
            'Furnace': 4,         # ID 40
            'Blast Furnace': 6,   # ID 45
        }

        self.max_fuel_counter = 10
        self.max_fuel_dict: dict = {
            'Torch': 3,           # ID 20
            'Firepit': 4,         # ID 25
            'Campfire': 5,        # ID 30
            'Bonfire': 8,         # ID 35
            'Furnace': 10,         # ID 40
            'Blast Furnace': 15,   # ID 45
        }

        self.heat_zones_id_dict: dict = {
            'Torch': 20,
            'Firepit': 25,
            'Campfire': 30,
            'Bonfire': 35,
            'Furnace': 40,
            'Blast Furnace': 45,
        }

        self.heat_zone_stages = {
            'Torch': 15,
            'Firepit': 30,
            'Campfire': 60,
            'Bonfire': 120,
            'Furnace': 240,
            'Blast Furnace': 480
        }

        self.allow_new_heat_source_list = 'Blast Furnace', 'Furnace', 'Bonfire', 'Campfire', 'Firepit', 'Torch'
        self.radius = 0
        self.new_heat_source = "Torch"
        self.new_heat_source = "Torch"
        self.new_heat_source_cost = 8  # Wood

        self.all_fire_source_list = self.map.get_terrain_value_positions(20)

        self.fire_source_grid = self.all_fire_source_list[0][0], self.all_fire_source_list[0][1]
        self.fire_source = (self.fire_source_grid[0] * self.map.tile_size, self.fire_source_grid[1] * self.map.tile_size)

        self.first_stage_dict = {
            'stage': "Torch",
            'count': 0,
            'position': self.fire_source_grid,
            'rect': None,
            'fuel count': 0,
            'fuel counter': 0,
            'heat range': "Torch"
        }

        self.fire_source_dict[self.fire_source_grid] = self.first_stage_dict

        # ---- Progressbar ---- #
        self.height = 50
        self.width = 50

        tree_logs_path = 'res/images/wood_icon.png'
        tree_log_img = self.images.preloading('log', tree_logs_path)
        self.tree_log_image = pygame.transform.scale(tree_log_img, (self.width, self.height))
        self.progress_bar_image = self.tree_log_image

        # Load progress bar images
        self.progress_bar_background = self.tree_log_image
        self.progress_bar_foreground = self.tree_log_image

        self.progress_bar_height = 10
        self.progress_bar_width = 100


    def update_heat_zone(self):
        self.snow = []
        self.heat = []

        for pos in self.fire_source_dict:
            real_stage = self.fire_source_dict[pos]['stage']
            stage = self.fire_source_dict[pos]['heat range']
            radius = self.heat_zones_dict[stage]

            # Set radius values
            minus = radius
            plus = radius + 1


            fire_x, fire_y = pos

            if real_stage != stage:
                # If the fire's real stage has changed, update the heat range and radius
                radius = self.heat_zones_dict[real_stage]
                minus = radius
                plus = radius + 1
                # Update the terrain around the fire source based on the new radius
                for x in range(fire_y - minus, fire_y + plus):
                    for y in range(fire_x - minus, fire_x + plus):
                        if 0 <= x < self.map.width and 0 <= y < self.map.height:
                            self.snow.append((y, x))

                continue


            # Iterate over the tiles for general heat zone update
            for x in range(fire_y - minus, fire_y + plus):
                for y in range(fire_x - minus, fire_x + plus):
                    if 0 <= x < self.map.width and 0 <= y < self.map.height:
                        terrain_value = self.map.data[y, x]
                        self.heat.append((y, x))



        for pos in self.snow:
            if pos in self.heat:
                self.snow.remove(pos)
        for y, x in self.snow:
            terrain_value = self.map.data[y, x]
            if terrain_value == 100:  # Ground
                self.map.data[y, x] = 1  # Mark as Ground near fire
            elif terrain_value == 110:  # Trees
                self.map.data[y, x] = 10  # Mark as Trees near fire

        for y, x in self.heat:
            terrain_value = self.map.data[y, x]
            if terrain_value == 1:  # Ground
                self.map.data[y, x] = 100  # Mark as Ground near fire
            elif terrain_value == 10:  # Trees
                self.map.data[y, x] = 110  # Mark as Trees near fire


    def feed_heat_source(self, mouse_pos):
        for pos, rect in self.fire_source_rect_list:
            if rect.collidepoint(mouse_pos):
                self.upgrade_fire_source_stage(pos)
                break

    def fuel_heat_source(self, mouse_pos):
        for pos, rect in self.fire_source_rect_list:
            if not rect.collidepoint(mouse_pos):
                continue

            if 'Wood' in self.player.inv:
                max_fuel = self.max_fuel_dict[self.fire_source_dict[pos]['stage']]
                current_fuel = self.fire_source_dict[pos]['fuel count']
                stage = self.fire_source_dict[pos]['stage']

                available_space = max_fuel - current_fuel
                amount = min(self.player.inv['Wood'], available_space)

                self.player.inv['Wood'] -= amount
                self.fire_source_dict[pos]['fuel count'] += amount
                self.fire_source_dict[pos]['heat range'] = stage
                return

    def heat_zone_status(self):
        # First, update all the 'fuel count' values
        for pos in self.fire_source_dict:
            if 'fuel count' not in self.fire_source_dict[pos]:
                continue

            fuel_count = self.fire_source_dict[pos]['fuel count']
            fuel_counter = self.fire_source_dict[pos]['fuel counter']

            if fuel_count <= 0:
                self.fire_source_dict[pos]['heat range'] = 'Torch'
                continue

            if fuel_counter < self.max_fuel_counter:
                self.fire_source_dict[pos]['fuel counter'] += 1

            # Decrease the fuel count by 1
            if fuel_counter >= self.max_fuel_counter:
                self.fire_source_dict[pos]['fuel count'] = fuel_count - 1
                self.fire_source_dict[pos]['fuel counter'] = 0

        # # Then, print all the fire source data after the loop has finished
        # for pos in self.fire_source_dict:
        #     print(self.fire_source_dict[pos])

    def draw_heat_source_cost(self, tree_pos, required_wood):
        # Set up the text
        font = pygame.font.Font(None, 45)  # Font and size
        text = f"{required_wood}"  # Cost as string

        if 'Wood' in self.player.inv and self.player.inv['Wood'] >= required_wood:
            text_color = (0, 255, 0)  # Green text
        else:
            text_color = (255, 0, 0)  # Red text


        text_surface = font.render(text, True, text_color)

        # Set up the icon (assuming you have a wood icon loaded)
        tree_log_img = self.images.loaded_item_images['log']
        wood_icon = pygame.transform.scale(tree_log_img, (self.width, self.height))
        icon_rect = wood_icon.get_rect()

        # Position the text and icon
        x, y = tree_pos
        text_rect = text_surface.get_rect(center=(x + 70, y - 100))  # Above the tree
        icon_rect.midleft = text_rect.midright  # Icon next to the text

        # Blit both text and icon
        self.screen.blit(text_surface, text_rect)
        self.screen.blit(wood_icon, icon_rect)

    def display_new_heat_source_cost(self, mouse_pos, tree_rect_dict, random_tree_positions, required_wood):
        for pos, rect in tree_rect_dict.items():
            if rect.collidepoint(mouse_pos):  # Check if mouse is over the tree
                terrain_pos = random_tree_positions.get(pos)  # Safely get the terrain position
                if terrain_pos:
                    new_pos = terrain_pos[0] - self.camera.offset.x, terrain_pos[1] - self.camera.offset.y
                    self.draw_heat_source_cost(new_pos, required_wood)
                return  # Exit after the first match

    def upgrade_fire_source_stage(self, pos):
        current_stage = self.fire_source_dict[pos]['stage']
        current_count = self.fire_source_dict[pos]['count']

        if current_stage is list(self.heat_zones_dict.keys())[-1]:  # Vaatab viimast fire source stage'i
            return

        item = 'Wood'

        if item not in self.player.inv or self.player.inv[item] <= 0:
            return  # No wood in inventory to feed

        # Get the required amount to upgrade
        required_to_upgrade = self.heat_zone_stages[current_stage] - current_count

        # Determine how much wood to use
        wood_to_use = min(self.player.inv[item], required_to_upgrade)

        # Update the fire source count and reduce player inventory
        self.fire_source_dict[pos]['count'] += wood_to_use
        self.player.inv[item] -= wood_to_use
        # Check if the fire source is ready to upgrade
        if self.fire_source_dict[pos]['count'] >= self.heat_zone_stages[current_stage]:
            # Get all the stages in order
            stages = list(self.heat_zone_stages.keys())

            # Find the index of the current stage
            current_index = stages.index(current_stage)

            if current_index < len(stages) - 1:  # Ensure we are not at the last stage
                # Upgrade to the next stage
                next_stage = stages[current_index + 1]

                max_fuel = self.max_fuel_dict[next_stage]
                self.fire_source_dict[pos]['fuel count'] = max_fuel
                self.fire_source_dict[pos]['heat range'] = next_stage

                self.fire_source_dict[pos]['stage'] = self.fire_source_dict[pos]['heat range'] = next_stage

                # Remove the amount needed for this upgrade from the count
                self.fire_source_dict[pos]['count'] -= self.heat_zone_stages[current_stage]


                self.map.data[pos] = self.heat_zones_id_dict[next_stage]

        if pos in self.position_upgradable: 
            self.position_upgradable.remove(pos)

    def create_new_heat_source(self, mouse_pos, tree_rect_dict):
        # Check if all fire sources are fully upgraded
        for pos in self.fire_source_dict:
            stage = self.fire_source_dict[pos]['stage']
            if stage not in self.allow_new_heat_source_list:
                return  # Exit if any source is not fully upgraded

        # Check for interaction with a tree to create a new fire source
        for tree_pos, tree_rect in tree_rect_dict.items():
            if tree_rect.collidepoint(mouse_pos):  # Check if mouse is over a tree

                # Add a new fire source at the tree's position
                new_fire_source = {
                    'stage': 'Torch',
                    'count': 0,
                    'position': tree_pos,
                    'rect': pygame.Rect(tree_rect.x, tree_rect.y, self.map.tile_size, self.map.tile_size),
                    'fuel count': 0,
                    'fuel counter': 0,
                    'heat range': 'Torch'

                }
                self.fire_source_dict[tree_pos] = new_fire_source

                # Remove the tree from the tree rect dictionary
                del tree_rect_dict[tree_pos]
                return tree_pos
        return None

    def create_heat_zone_rect_list(self):
        self.fire_source_rect_list.clear()  # Reset

        for pos in self.fire_source_dict:
            x, y = pos
            rect = pygame.Rect(x * self.map.tile_size - self.camera.offset.x, y * self.map.tile_size - self.camera.offset.y, self.map.tile_size, self.map.tile_size)

            self.fire_source_rect_list.append(((x, y), rect))
            self.fire_source_dict[pos]['rect'] = rect

    # ------- DRAWING ------- #
    def draw_heat_zones(self):
        """Draw all the heat zone rectangles."""

        for rect_pos, rect in self.fire_source_rect_list:
            if rect_pos in self.position_upgradable:
                pygame.draw.rect(self.screen, 'limegreen', rect, 10, 4)
            
            else:
                pygame.draw.rect(self.screen, 'black', rect, 10, 4)

    def draw_progress_bar(self, rect, position, progress, max_progress):
        progress_percent = min(max(progress / max_progress, 0), 1)
        # Position to draw progress bar
        bar_width, bar_height = self.progress_bar_background.get_size()
        bar_x = rect.centerx - bar_width // 2
        bar_y = rect.top - bar_height - 5  # 5px padding above the rect

        # Blit the low-transparency background image
        low_transparency_bar = self.progress_bar_background.copy()
        low_transparency_bar.set_alpha(100)  # Low transparency (100/255)
        self.screen.blit(low_transparency_bar, (bar_x, bar_y))

        # Calculate the visible height of the foreground image
        visible_height = int(bar_height * progress_percent)
        if visible_height > 0:
            # Create a subsurface for the visible part of the foreground
            visible_part = self.progress_bar_foreground.subsurface(
                pygame.Rect(0, bar_height - visible_height, bar_width, visible_height)
            )
            # Position the visible part to appear growing from the bottom
            visible_y = bar_y + bar_height - visible_height
            self.screen.blit(visible_part, (bar_x, visible_y))

        if progress_percent * 100 == 100 and position not in self.position_upgradable:
            self.position_upgradable.append(position)

        if position in self.position_upgradable and progress_percent * 100 != 100:
            self.position_upgradable.remove(position)

        # if progress_percent * 100 == 100:
        #     if position not in self.position_upgradable:
        #         self.position_upgradable.append(position)

        # if position in self.position_upgradable and progress_percent * 100 != 100:
        #     self.position_upgradable.remove(position)

    def draw_all_progress_bars(self, get_terrain_in_view):
        """Draw progress bars for all fire sources."""

        for fire_source in self.fire_source_dict.values():
            position = fire_source['position']

            if position in get_terrain_in_view:
                rect = fire_source['rect']
                count = fire_source['count']
                stage = fire_source['stage']
                max_count = self.heat_zone_stages[stage]
                
                if count != 0:
                    count = fire_source['count']
                
                try: # try error catch sest 'Wood' ei pruugi inventoris olemas olla
                    count += self.player.inv['Wood']  # player count, liidab countile, mis positionil on
                    if count == 0: count = fire_source['count']
                except Exception: pass

                if stage is "Blast Furnace":
                    continue

                self.draw_progress_bar(rect, position, count, max_count)

    def update(self, terrain_in_view):
        self.update_heat_zone()
        self.update_heat_zone()
        self.create_heat_zone_rect_list()
        self.draw_all_progress_bars(terrain_in_view)
        self.draw_heat_zones()

        self.heat_zone_status()