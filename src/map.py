import numpy as np
from noise import pnoise2
import pygame


class Map:
    def __init__(self, screen, camera):
        self.width = 100  # Player saab korraga näha max 20 - (1920 / 100 = 19.2 -> 20)
        self.height = 100  # Player saab korraga näha max 11 - (1080 / 100 = 10.8 -> 11)
        self.tile_size = 100
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
                data[y, x] = 1 if noise_value > 0 else 0

        return data

    def update(self):
        for y in range(self.width):
            for x in range(self.height):
                color = (0, 128, 0) if self.data[y, x] == 1 else (0, 0, 128)  # Green for land, Blue for water
                rect = pygame.Rect(x * self.tile_size - self.camera.offset.x, y * self.tile_size -  self.camera.offset.y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, color, rect)
        print(self.data)