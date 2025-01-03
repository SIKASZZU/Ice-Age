import numpy as np
from noise import pnoise2

class Map:
    def __init__(self, screen, camera):
        self.width = 100  # Player saab korraga näha max 20 - (1920 / 100 = 19.2 -> 20)
        self.height = 100  # Player saab korraga näha max 11 - (1080 / 100 = 10.8 -> 11)
        self.tile_size = 10
        self.screen = screen
        self.camera = camera

        # Initialize data with procedural noise
        self.data = self.generate_data()

    def generate_data(self):
        scale = 50.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0

        data = np.zeros((self.height, self.width), dtype=int)
        for y in range(self.height):
            for x in range(self.width):
                noise_value = pnoise2(
                    x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=self.width,
                    repeaty=self.height,
                    base=42,
                )
                
                if 0.07 < noise_value:
                    data[y, x] = 10

                elif 0.07 > noise_value > 0.05 or 0.01 > noise_value > -0.04 > noise_value:
                    data[y, x] = 1

                else:
                    data[y, x] = 0

        return data

    def update(self):
        return self.data