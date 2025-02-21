import pygame
import jurigged

from weather import Weather
from map import Map
from tree import Tree
from camera import Camera
from items import Items
from player import Player
from render import Render
from images import Images
from tileset import TileSet
from heat_zone import HeatZone
from framerate import Framerate

jurigged.watch()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920 // 2, 1080 // 2))  # Set up the game window
        self.clock = pygame.time.Clock()
        self.running = True 
        self.font = pygame.font.Font(None, 50)

        # Initialize game components
        self.items = Items()
        self.camera = Camera()
        self.map = Map(self.screen, self.camera)
        self.images = Images()
        self.player = Player(self.screen, self.camera, self.map, self.font, self.images, self.items)
        self.heat_zone = HeatZone(self.screen, self.map, self.camera, self.player, self.images)
        self.tree = Tree(self.screen, self.images, self.map, self.camera, self.player, self.heat_zone)
        self.tile_set = TileSet(self.images, self.map)

        self.renderer = Render(self.screen, self.camera, self.map, self.player, self.clock, self.tree, self.images, self.tile_set, self.heat_zone, self.items)
        self.weather = Weather(self.screen, self.player)
        self.framerate = Framerate()

        # Tickrate
        self.TICK_RATE = 48  # Set your desired tick rate (logic updates per second)
        self.tick_interval = 1000 // self.TICK_RATE  # Time per tick in milliseconds
        self.last_tick = pygame.time.get_ticks()


        self.terrain_in_view = self.renderer.get_terrain_in_view()

        self.rects_window_coord = self.tree.calculate_rects()


        self.required_wood = self.heat_zone.new_heat_source_cost


    def logic(self):
        self.camera.update(self.player.rect)  # Keep camera updated with player position


    def render(self, mouse_pos):
        terrain_in_view = self.renderer.get_terrain_in_view()

        self.screen.fill((0, 0, 255))  # FIRST // Clear the screen with a black color
        self.renderer.update()

        self.rects_window_coord, self.tree_position_coord = self.tree.update()

        # During hover, show the cost
        if self.rects_window_coord:
            self.heat_zone.display_new_heat_source_cost(mouse_pos, self.rects_window_coord, self.tree_position_coord, self.required_wood)

        self.player.update()  # Alati enne renderer'i

        self.heat_zone.update(terrain_in_view)

        self.weather.update()

        pygame.display.flip()  # LAST // Update display

    def run(self):
        """Main game loop."""

        while self.running:
            self.required_wood = self.heat_zone.new_heat_source_cost + len(self.heat_zone.all_fire_source_list) * 2  # mdv xD
            mouse_pos = pygame.mouse.get_pos()  # Get the mouse position
            current_fps = self.clock.get_fps()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    # Feedi heat_zonei
                    self.heat_zone.fuel_heat_source(mouse_pos, 'left_click')

                    # Asenda puu heat_zoneiga
                    if self.player.inv.get('Wood', 0) >= self.required_wood:  
                        tree_pos = self.heat_zone.create_new_heat_source(mouse_pos, self.rects_window_coord)
                        if hasattr(self, 'tree'):  # Ensure self.tree exists before calling gather
                            self.tree.gather(tree_pos, self.required_wood)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right mouse button
                    self.heat_zone.fuel_heat_source(mouse_pos, 'right_click')

            # tickratei lisamine
            current_time = pygame.time.get_ticks()
            if current_time - self.last_tick >= self.tick_interval:
                
                # RUNS AT TICKRATE SPEED
                self.logic()
                self.render(mouse_pos)
                self.last_tick = current_time

                # print(f"FPS: {current_fps:.2f} | Tick Rate: {self.TICK_RATE}")


            self.framerate.update(current_fps)
            fps_text = self.framerate.display_fps_statistics()

            self.clock.tick(1000)  # Cap FPS at 60
            pygame.display.set_caption(f"Ice Age - {fps_text} | Tick Rate: {self.TICK_RATE}")

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()