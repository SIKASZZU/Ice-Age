import math

class HeatZone:
    def __init__(self, screen, map, camera):
        self.map = map
        self.camera = camera


        self.screen = screen

        self.heat_zones_dict: dict = {
            'Torch': 1,           # ID 20
            'Firepit': 2,         # ID 25
            'Campfire': 3,        # ID 30
            'Bonfire': 5,         # ID 35
            'Furnace': 7,         # ID 40
            'Blast Furnace': 9,   # ID 45
        }

        self.fire_source_grid = self.map.get_terrain_value_positions(20)
        self.fire_source = (self.fire_source_grid[0][0] * self.map.tile_size, self.fire_source_grid[0][1] * self.map.tile_size)
        self.current_heat_source = "Torch"
        self.radius = 0

        self.get_radius(self.current_heat_source)


    def get_radius(self, current_heat_source):
        self.current_heat_source = current_heat_source
        self.radius = self.heat_zones_dict[self.current_heat_source]  # 2

    import math

    def update_heat_zone(self):
        """Update the terrain values around the fire source."""
        if not self.fire_source:
            return

        minus = self.radius
        plus = self.radius + 1

        fire_x, fire_y = self.fire_source  # Get the fire source position
        fire_x = fire_x // self.map.tile_size
        fire_y = fire_y // self.map.tile_size
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

    def normalize_distance(self, pos):
        """
        Normalize the distance from the fire source.

        :param pos: Tuple representing the (x, y) position of the point
        :return: Normalized distance (0 to 1)
        """
        distance = math.dist(self.fire_source, pos)
        return min(distance / self.radius, 1)

    def get_color(self, pos):
        """
        Get the color based on the normalized distance.

        :param pos: Tuple representing the (x, y) position of the point
        :return: Color (white for close, brown for far)
        """
        normalized = self.normalize_distance(pos)
        return (255, 255, 255) if normalized < 0.8 else (139, 69, 19)

    def draw_heat_map(self):
        """
        Draw the heat map on the screen.
        """
        for x in range(self.screen.get_width()):
            for y in range(self.screen.get_height()):
                color = self.get_color((x, y))
                self.screen.set_at((x, y), color)

    def update(self, new_fire_source=None):
        """
        Update the heat zone with a new fire source if provided.

        :param new_fire_source: Tuple representing the new (x, y) position of the fire source
        """
        if new_fire_source:
            self.fire_source = new_fire_source
        self.draw_heat_map()

