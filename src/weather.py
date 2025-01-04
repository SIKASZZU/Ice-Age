import pygame
import random

class Weather:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.snowflakes = self.create_snowflakes()


    def create_snowflakes(self, count=100):
        """Create an initial set of snowflakes."""
        return [
            {
                "x": random.randint(0, self.screen_width),
                "y": random.randint(-self.screen_height, 0),
                "size": random.randint(2, 5),
                "speed": random.uniform(1, 3),
            }
            for _ in range(count)
        ]


    def draw(self):
        """Draw the snowflakes on the screen."""
        for snowflake in self.snowflakes:
            pygame.draw.circle(self.screen, (240, 240, 240), (snowflake["x"], snowflake["y"]), snowflake["size"])


    def update(self):
        """Update snowflake positions."""
        for snowflake in self.snowflakes:
            #snowflake["x"] += self.player.x
            snowflake["y"] += snowflake["speed"]

            # Wrap snowflakes horizontally if they move off-screen
            if snowflake["x"] < 0:
                snowflake["x"] += self.screen_width
            elif snowflake["x"] > self.screen_width:
                snowflake["x"] -= self.screen_width

            # Reset snowflake when it falls off the screen
            if snowflake["y"] > self.screen_height:
                snowflake["y"] = random.randint(-self.screen_height, 0)
                snowflake["x"] = random.randint(0, self.screen_width)
        self.draw()
