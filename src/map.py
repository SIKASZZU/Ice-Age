import numpy as np
from noise import pnoise2
import pygame


class Map:
    def __init__(self, screen, camera):
        self.size = 100  # Reduced size for demonstration; adjust as needed
        self.tile_size = 10
        self.screen = screen
        self.camera = camera

        # Initialize data with procedural noise
        self.data = self.generate_data()

    def generate_data(self):
        scale = 50.0  # Adjust for noise scaling
        octaves = 6  # Detail level of the noise
        persistence = 0.5  # Amplitude of each octave
        lacunarity = 2.0  # Frequency of each octave

        data = np.zeros((self.size, self.size), dtype=int)
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
                # Convert noise value to binary data (1 for land, 0 for water)
                data[y, x] = 1 if noise_value > 0 else 0

        return data

    def update(self):
        for y in range(self.size):
            for x in range(self.size):
                color = (0, 128, 0) if self.data[y, x] == 1 else (0, 0, 128)  # Green for land, Blue for water
                rect = pygame.Rect(x * self.tile_size - self.camera.offset.x, y * self.tile_size -  self.camera.offset.y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, color, rect)
        print(self.data)