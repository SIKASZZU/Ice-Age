import numpy as np
from noise import pnoise2


class Map:
    def __init__(self):
        self.size = 100  # Reduced size for demonstration; adjust as needed
        self.tile_size = 10

        # Initialize terrain with procedural noise
        self.terrain = self.generate_terrain()

    def generate_terrain(self):
        scale = 50.0  # Adjust for noise scaling
        octaves = 6  # Detail level of the noise
        persistence = 0.5  # Amplitude of each octave
        lacunarity = 2.0  # Frequency of each octave

        terrain = np.zeros((self.size, self.size), dtype=int)
        for y in range(self.size):
            for x in range(self.size):
                noise_value = pnoise2(
                    x / scale,
                    y / scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=self.size,
                    repeaty=self.size,
                    base=42,
                )
                # Convert noise value to binary terrain (1 for land, 0 for water)
                terrain[y, x] = 1 if noise_value > 0 else 0

        return terrain

    def update():
        pass

# Create the map
map_instance = Map()
