import random

import numpy as np
from noise import pnoise2
import random


class Map:
    def __init__(self, screen, camera):
        self.width = 10  # Player saab korraga näha max 20 - (1920 / 200 = 19.2 -> 20 + 1 // 2 -> 11)
        self.height = 10  # Player saab korraga näha max 11 - (1080 / 200 = 10.8 -> 11 + 1 // 2 -> 6)
        self.tile_size = 75
        self.screen = screen
        self.camera = camera

        # Võtab alati seedi kui on vähemalt 1 puu, mille saaks muuta fire sourceiks
        self.seed = None
        self.data = None
        while self.data is None or self.data.size == 0:  # Check if data is None or empty
            self.seed = random.randint(1, 500)
            self.data = self.generate_data(width=self.width, height=self.height, seed=self.seed)

    @staticmethod
    def generate_data(width, height, scale=50.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=42):
        data = np.zeros((height, width), dtype=int)
        tree_positions = []

        # Generate terrain
        for y in range(height):
            for x in range(width):
                noise_value = pnoise2(
                    x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=width,
                    repeaty=height,
                    base=seed,
                )

                if noise_value > 0.07:
                    if 4 > random.randint(0, 10):
                        data[y, x] = 1  # Ground
                        continue

                    data[y, x] = 10  # Trees
                    tree_positions.append((x, y))
                elif 0.04 < noise_value <= 0.07 or (0 > noise_value > -0.01):
                    data[y, x] = 1  # Ground

                elif -0.01 >= noise_value >= -0.03 or (0 < noise_value <= 0.04):
                    data[y, x] = 0  # Ice Water

        # Place heat source near the center of trees
        if tree_positions:
            # Calculate approximate center
            avg_x = sum(pos[0] for pos in tree_positions) // len(tree_positions)
            avg_y = sum(pos[1] for pos in tree_positions) // len(tree_positions)

            # Find the closest tree to the calculated center
            closest_tree = min(tree_positions, key=lambda pos: (pos[0] - avg_x) ** 2 + (pos[1] - avg_y) ** 2)
            heat_x, heat_y = closest_tree

            # Place the heat source at the closest tree
            data[heat_y, heat_x] = 20  # Heat Source
            return data

        return None

    def get_terrain_value_positions(self, target_value) -> list:
        if isinstance(target_value, int):  # Single value case
            return np.argwhere(self.data == target_value).tolist()  # Convert to list for consistency

        if isinstance(target_value, (tuple, list)):  # Multiple values case
            target_value_pos_list = []
            for terrain_value in target_value:
                target_value_pos_list.extend(np.argwhere(self.data == terrain_value).tolist())
            return target_value_pos_list

        raise ValueError("target_value must be an int, tuple, or list")

    def get_terrain_value_at(self, x, y) -> int:
        if 0 <= x < self.width and 0 <= y < self.height:

            return self.data[y, x]
        else:
            print(f'Out of bounds or smth - ({x};{y})')
            return None

    def update(self):
        return self.data