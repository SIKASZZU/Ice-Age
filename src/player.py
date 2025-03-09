import pygame
from sprite import Sprite


class Player:
    def __init__(self, screen, camera, map, font, images, items, inv):
        self.screen = screen
        self.camera = camera
        self.map = map
        self.font = font
        self.images = images
        self.items = items
        self.inventory = inv

        player_pos_grid = self.map.get_terrain_value_positions(20)  # 20 -> Torch ID

        self.x = player_pos_grid[0][0] * self.map.tile_size
        self.y = player_pos_grid[0][1] * self.map.tile_size
        self.height = 50
        self.width = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.movement_speed = 20
        self.travelled_path = {}

        # Animation
        self.last_input = "s"
        self.scale_factor = 100/130  # kui suur on player. 130px on max (sprite ise on 520x130 ehk 4 pilti 130x130)

        self.current_animation = "idle_down"
        self.animation_speed = 5
        self.frame_size = 130

        self.animations = {
            "idle_left": Sprite("res/images/player/Idle_Left.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),
            "idle_right": Sprite("res/images/player/Idle_Right.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),
            "idle_up": Sprite("res/images/player/Idle_Up.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),
            "idle_down": Sprite("res/images/player/Idle_Down.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),

            "move_left": Sprite("res/images/player/Left.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),
            "move_right": Sprite("res/images/player/Right.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),
            "move_up": Sprite("res/images/player/Up.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),
            "move_down": Sprite("res/images/player/Down.png", self.frame_size, self.frame_size, 4, self.animation_speed, self.scale_factor),
        }

        # Cold
        self.player_is_cold = False
        self.player_is_warm = False        
        self.cold_tolerance = 10
        self.damage_by_cold = 1
        self.regen_by_heat = 1
        self.cold_status = 'Ok'  # NEAR_FROZEN, Extreme, Mild, Ok
        self.last_time_damaged = None
        self.last_time_healed = None


    def movement(self):
        """ Move player x,y, current_animation, last_input and update self.x,y + rect.x,y values. """
        
        # FIXME: Kui pelama hakkab ss muuta õigeks
        if self.cold_status == 'MILD':
            self.movement_speed = 20

        if self.cold_status == 'EXTREME':
            self.movement_speed = 20

        if self.cold_status == 'NEAR_FROZEN':
            self.movement_speed = 20

        moving = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.movement_speed
            self.current_animation = "move_left"
            self.last_input = "a"
            moving = True

        if keys[pygame.K_d]:
            self.x += self.movement_speed
            self.current_animation = "move_right"
            self.last_input = "d"
            moving = True

        if keys[pygame.K_w]:
            self.y -= self.movement_speed
            self.current_animation = "move_up"
            self.last_input = "w"
            moving = True

        if keys[pygame.K_s]:
            self.y += self.movement_speed
            self.current_animation = "move_down"
            self.last_input = "s"
            moving = True

        if keys[pygame.K_a] and keys[pygame.K_d] and keys[pygame.K_w] and keys[pygame.K_s]:
            self.current_animation = "idle_down"
            moving = True

        if not moving:
            if self.last_input == "a":
                self.current_animation = "idle_left"

            if self.last_input == "d":
                self.current_animation = "idle_right"

            if self.last_input == "w":
                self.current_animation = "idle_up"

            if self.last_input == "s":
                self.current_animation = "idle_down"

        # TODO: x,y -- grid -- window x,y -- window grid ja ss igalpool nende kasutamine või teha funcid siit
        self.rect.x = self.x
        self.rect.y = self.y


    def cold_regulator(self, current_time):
        """ In cold player is slower """
        """ Player cold damage -> if 0, movement speed slow, health damage until death. """
        terrain_value = self.map.get_terrain_value_at(self.rect.x // self.map.tile_size, self.rect.y // self.map.tile_size)
        
        self.player_is_cold = False
        self.player_is_warm = False

        # DAMAGE in cold zones (map.py) every 2 sec 1/10 of max health
        if terrain_value in self.items.cold_area:
            self.player_is_cold = True
            if self.last_time_damaged == None: self.last_time_damaged = current_time

            if current_time > self.last_time_damaged + 2000:  # every 2 sec damage by cold
                self.last_time_damaged = current_time  # update for next loop
                if self.cold_tolerance > 0:  self.cold_tolerance -= self.damage_by_cold

        # HEALING in heat_zone every 4 sec heal 1/10 of max health
        if terrain_value in self.items.heated_area:
            self.player_is_warm = True
            if self.last_time_healed == None: self.last_time_healed = current_time

            if current_time > self.last_time_healed + 4000:  # every 4 sec heal by heat_zone
                self.last_time_healed = current_time
                if self.cold_tolerance < 10:self.cold_tolerance += self.regen_by_heat

        # Cold status -> Selle jargi saab settida ntks movementspeedi
        if self.cold_tolerance >= 8:    self.cold_status = 'OK'
        elif 4 < self.cold_tolerance <= 7:  self.cold_status = 'MILD'
        elif 0 < self.cold_tolerance <= 4:  self.cold_status = 'EXTREME'
        elif self.cold_tolerance == 0:  self.cold_status = 'NEAR_FROZEN'

        # print()
        # print('self.cold_tolerance', self.cold_tolerance)
        # print('self.cold_status   ', self.cold_status)
        # print('cold', self.player_is_cold, 'warm', self.player_is_warm)


    def save_travelling_path(self, current_time):
        player_grid = (int(self.x // self.map.tile_size), int(self.y // self.map.tile_size))
        pos_to_pop = set()

        if player_grid in self.travelled_path.keys():
            self.travelled_path[player_grid] = current_time  # update grid's last time visited
            
        else:
            
            # update travlled path dict with new value
            self.travelled_path[player_grid] = current_time

        # after some time remove the player_grid from self.travelled_path

        for grid_info in self.travelled_path.items():
            pos, visited_time = grid_info
            if current_time - visited_time > 6000:
                pos_to_pop.add(pos)

        for pos in pos_to_pop:
            self.travelled_path.pop(pos)


    def update(self):
        current_time = pygame.time.get_ticks()  # time for tracking the last damage,heal

        animation_x = animation_y = None
        self.cold_regulator(current_time)
        self.movement()
        self.save_travelling_path(current_time)
        self.animations[self.current_animation].update()

        ### Animatsion, player Spritei keskele viimine ###
        sprite_size = self.frame_size * self.scale_factor

        # sprite_size on sprite keskkoha viimine ruudu vasakusse nurka. 
        # (self.rect[2 ja 3] // 2) on spritei viimine ruudu keskkohta.
        animation_x = self.x - self.camera.offset.x - sprite_size // 2 + self.rect[2] // 2
        animation_y = self.y - self.camera.offset.y - sprite_size // 2 + self.rect[3] // 2

        return animation_x, animation_y
