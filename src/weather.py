import pygame
import random


class Weather:
    def __init__(self, game, screen, player):
        self.game = game
        self.screen = screen
        self.player = player

        self.screen_width = self.game.screen_x
        self.screen_height = self.game.screen_y
        self.snowflakes = self.create_snowflakes()


    def create_snowflakes(self, count=100):
        """Create an initial set of snowflakes."""
        return [
            {
                "x": random.randint(0, self.screen_width),
                "y": random.randint(-self.screen_height, 0),
                "size": random.randint(2, 5),
                "speed": random.uniform(1, 3),
                "drift": random.uniform(-1, 1),  # Horizontal drift for diagonal movement
            }
            for _ in range(count)
        ]

    def update(self):
        """Update snowflake positions."""
        for snowflake in self.snowflakes:
            # Update positions for diagonal fall
            snowflake["x"] += snowflake["drift"]
            snowflake["y"] += snowflake["speed"]

            # Wrap horizontally if snowflake moves off the screen
            if snowflake["x"] < 0:
                snowflake["x"] += self.screen_width
            elif snowflake["x"] > self.screen_width:
                snowflake["x"] -= self.screen_width

            # Reset snowflake if it falls below the screen
            if snowflake["y"] > self.screen_height:
                snowflake["y"] = random.randint(-self.screen_height, 0)
                snowflake["x"] = random.randint(0, self.screen_width)
                snowflake["drift"] = random.uniform(-1, 1)  # Reset drift for randomness

        self.draw()

    def draw(self):
        """Draw the snowflakes on the screen."""
        for snowflake in self.snowflakes:
            pygame.draw.circle(self.screen, (240, 240, 240), (snowflake["x"], snowflake["y"]), snowflake["size"])
