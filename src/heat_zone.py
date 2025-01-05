import pygame


class HeatZone:
    def __init__(self, screen, map, camera, player):
        self.map = map
        self.camera = camera
        self.screen = screen
        self.player = player

        self.fire_source_dict = {}

        # self.fire_source_dict = {
        # position {
        # 'stage': "Torch",
        # 'count': 0,
        # 'position': self.fire_source_grid,
        # 'rect': None
        # }}

        self.fire_source_rect_list = []

        self.heat_zones_dict: dict = {
            'Torch': 1,           # ID 20
            'Firepit': 2,         # ID 25
            'Campfire': 3,        # ID 30
            'Bonfire': 5,         # ID 35
            'Furnace': 7,         # ID 40
            'Blast Furnace': 9,   # ID 45
        }

        self.heat_zone_stages = {
            'Torch': 25,
            'Firepit': 60,
            'Campfire': 150,
            'Bonfire': 500,
            'Furnace': 1600,
            'Blast Furnace': 4000,
        }

        self.all_fire_source_list = self.map.get_terrain_value_positions(20)

        self.fire_source_grid = self.all_fire_source_list[0][0], self.all_fire_source_list[0][1]
        self.fire_source = (self.fire_source_grid[0] * self.map.tile_size, self.fire_source_grid[1] * self.map.tile_size)


        first_stage_dict = {
            'stage': "Torch",
            'count': 0,
            'position': self.fire_source_grid,
            'rect': None
        }

        self.fire_source_dict[self.fire_source_grid] = first_stage_dict

        self.radius = 0
        self.current_heat_source = "Torch"
        self.get_radius(self.current_heat_source)

        # Progress bar settings
        self.progress_bar_height = 10
        self.progress_bar_width = 100


    def get_radius(self, current_heat_source):
        self.current_heat_source = current_heat_source
        self.radius = self.heat_zones_dict[self.current_heat_source]  # 2


    def update_heat_zone(self):
        for pos in self.fire_source_dict:
            stage = self.fire_source_dict[pos]['stage']
            radius = self.heat_zones_dict[stage]

            minus = radius
            plus = radius + 1

            fire_x, fire_y = pos

            # Iterate over the terrain grid around the fire source to update the tiles
            for x in range(fire_y - minus, fire_y + plus):
                for y in range(fire_x - minus, fire_x + plus):
                    # Ensure we're within the bounds of the map
                    if 0 <= x < self.map.width and 0 <= y < self.map.height:
                        # Get the terrain value at the current tile position
                        terrain_value = self.map.data[y, x]

                        # Check if the terrain is Ground (1) or Trees (10) and update accordingly
                        if terrain_value == 1:  # Ground
                            self.map.data[y, x] = 100  # Ground near fire
                        elif terrain_value == 10:  # Trees
                            self.map.data[y, x] = 110  # Trees near fire


    def feed_heat_source(self, mouse_pos):
        for pos, rect in self.fire_source_rect_list:
            if rect.collidepoint(mouse_pos):
                self.perform_action_on_fire_source(pos)
                break

    def perform_action_on_fire_source(self, pos):
        item = 'Wood'

        if item not in self.player.inv:
            return

        self.fire_source_dict[pos]['count'] += self.player.inv[item]
        self.player.inv[item] = 0

        self.upgrade_fire_source_stage(pos)


    def upgrade_fire_source_stage(self, pos):
        current_stage = self.fire_source_dict[pos]['stage']
        current_count = self.fire_source_dict[pos]['count']

        # Get all the stages in order
        stages = list(self.heat_zone_stages.keys())

        # Find the index of the current stage
        current_index = stages.index(current_stage)

        # Check if we can upgrade to the next stage
        if current_index < len(stages) - 1:  # Ensure we are not at the last stage
            next_stage = stages[current_index + 1]

            # Check if the count exceeds the current stage's limit
            if current_count > self.heat_zone_stages[current_stage]:
                # Upgrade to the next stage
                self.fire_source_dict[pos]['stage'] = next_stage
                self.fire_source_dict[pos]['count'] = 0  # Reset count for the new stage
                print(f"Fire source at {pos} upgraded to {next_stage}!")

    def create_new_heat_source(self):
        ...


    def create_heat_zone_rect_list(self):
        self.fire_source_rect_list.clear()  # Reset

        for pos in self.fire_source_dict:
            x, y = pos
            rect = pygame.Rect(x * self.map.tile_size - self.camera.offset.x, y * self.map.tile_size - self.camera.offset.y, self.map.tile_size, self.map.tile_size)

            self.fire_source_rect_list.append(((x, y), rect))
            self.fire_source_dict[pos]['rect'] = rect

    def draw_heat_zones(self):
        """Draw all the heat zone rectangles."""
        for _, rect in self.fire_source_rect_list:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 10)  # Example: Draw in red color


    def draw(self):
        # for rect in self.fire_source_rect_list:
        ...

        # # Draw the heat zone rect
        # heat_zone_rect = self.get_heat_zone_rect()
        # pygame.draw.rect(self.screen, (255, 0, 0), heat_zone_rect, 2)  # Red outline for the heat zone
        #
        # # Draw the progress bar above the heat zone
        # progress_bar_rect = pygame.Rect(
        #     self.fire_source[0] - self.progress_bar_width // 2,
        #     self.fire_source[1] - self.radius * self.map.tile_size - self.progress_bar_height - 10,
        #     self.progress_bar_width,
        #     self.progress_bar_height
        # )
        #
        # # Draw the background of the progress bar (gray)
        # pygame.draw.rect(self.screen, (150, 150, 150), progress_bar_rect)
        #
        # # Draw the progress (based on radius)
        # progress = self.radius / 9  # Max radius from the heat zone dict is 9 (from 'Blast Furnace')
        # progress_width = int(self.progress_bar_width * progress)
        # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(progress_bar_rect.x, progress_bar_rect.y, progress_width, self.progress_bar_height))
        #
        # # Draw the text for progress bar (optional)
        # font = pygame.font.Font(None, 24)
        # progress_text = f"Heat Zone: {self.radius}"
        # text_surface = font.render(progress_text, True, (255, 255, 255))
        # self.screen.blit(text_surface, (progress_bar_rect.x + 5, progress_bar_rect.y - 25))  # Text above the progress bar


    def update(self):
        self.update_heat_zone()
        self.create_heat_zone_rect_list()
        self.draw_heat_zones()
