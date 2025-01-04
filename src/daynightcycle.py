import pygame

class Cycle:
    def __init__(self, screen):
        self.screen = screen
        self.color = [0, 0, 50]  # Start with a night-like dark blue color
        self.transition_speed = 1  # Speed of transition
        self.direction = 1  # 1 for day to night, -1 for night to day

    def day_night_cycle(self):
        """Simulate day-night transition by changing the background color."""
        for i in range(3):
            self.color[i] += self.transition_speed * self.direction

        # Reverse the direction if limits are reached
        if self.color[0] >= 135 and self.direction == 1:  # Transition to day (light blue)
            self.direction = -1
        elif self.color[0] <= 0 and self.direction == -1:  # Transition to night (dark blue)
            self.direction = 1

        # Ensure RGB values are within bounds
        self.color = [max(0, min(255, c)) for c in self.color]

        # Update screen with the new color
        self.screen.fill(self.color)

# Integrate with the game
if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Day-Night Cycle")
    clock = pygame.time.Clock()

    # Create Cycle instance
    cycle = Cycle(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update day-night cycle
        cycle.day_night_cycle()

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()