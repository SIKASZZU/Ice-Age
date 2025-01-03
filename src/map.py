import numpy as np
from noise import pnoise2

class Map:
    def __init__(self, screen, camera):
        self.width = 100  # Player saab korraga näha max 20 - (1920 / 100 = 19.2 -> 20)
        self.height = 100  # Player saab korraga näha max 11 - (1080 / 100 = 10.8 -> 11)
        self.tile_size = 100
        self.screen = screen
        self.camera = camera

        # Initialize data with procedural noise
        self.data = self.generate_data(width=self.width, height=self.height)

    @staticmethod
    def generate_data(width, height, scale=50.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=42):
        data = np.zeros((height, width), dtype=int)
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
                    data[y, x] = 10  # Trees
                elif 0.04 < noise_value <= 0.07 or (0 > noise_value > -0.01):
                    data[y, x] = 1  # Ground
                elif -0.01 >= noise_value >= -0.03 or (0 < noise_value <= 0.04):
                    data[y, x] = 0  # Ice Water

        return data

    def update(self):
        return self.data