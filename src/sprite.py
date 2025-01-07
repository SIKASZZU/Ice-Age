import pygame
import os


class Sprite:
    def __init__(self, image_path, frame_width, frame_height, num_frames, animation_speed):
        """
        Initialize the sprite.

        :param image_path: Path to the sprite sheet image.
        :param frame_width: Width of each frame in the sprite sheet.
        :param frame_height: Height of each frame in the sprite sheet.
        :param num_frames: Total number of frames in the sprite sheet.
        :param animation_speed: Animation speed (frames per second).
        """

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Move up to project root
        os_path = os.path.normpath(os.path.join(base_path, image_path))

        self.image = pygame.image.load(os_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.animation_speed = animation_speed

        self.frames = [
            self.image.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            for i in range(num_frames)
        ]

        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

    def update(self):  # Updateb animationi
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 / self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, surface, x, y):
        """
        Draw the current frame of the sprite on the given surface.

        :param surface: The surface to draw the sprite on.
        :param x: The x-coordinate to draw the sprite.
        :param y: The y-coordinate to draw the sprite.
        """
        surface.blit(self.frames[self.current_frame], (x, y))
