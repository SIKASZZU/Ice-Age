import pygame


class Collision:
    def __init__(self, player, tree, map, screen, camera):
        self.player = player
        self.tree = tree
        self.map = map
        self.screen = screen
        self.camera = camera
        self.rect_list = []


    def detection(self):
        # check only grids around player
        x = self.player.rect[0] // self.map.tile_size
        y = self.player.rect[1] // self.map.tile_size
        self.rect_list = []

        for tree in self.tree.rects_map_coord.items():
            tree_grid, tree_rect = tree

            tree_rect = (tree_rect[0] +2, tree_rect[1] +2, tree_rect[2] -4, tree_rect[3]-4)


            # check options close to player
            if abs(tree_grid[0] - x) > 1:
                if tree_rect in self.rect_list:
                    self.rect_list.remove(tree_rect)
                continue
                
            if abs(tree_grid[1] - y) > 2:
                if tree_rect in self.rect_list:
                    self.rect_list.remove(tree_rect)
                continue

            self.rect_list.append(tree_rect)
            self.adjust_player(tree_rect)


    def adjust_player(self, tree_rect):
        """ If player collides with a tree, adjust position to prevent overlap. """
        player_rect = self.player.rect

        if (player_rect[0] < tree_rect[0] + tree_rect[2] and
            player_rect[0] + player_rect[2] > tree_rect[0] and
            player_rect[1] < tree_rect[1] + tree_rect[3] and
            player_rect[1] + player_rect[3] > tree_rect[1]):

            # Determine the direction of collision
            dx_left = abs(player_rect[0] + player_rect[2] - tree_rect[0])  # Distance from player's right to tree's left
            dx_right = abs(tree_rect[0] + tree_rect[2] - player_rect[0])  # Distance from player's left to tree's right
            dy_top = abs(player_rect[1] + player_rect[3] - tree_rect[1])  # Distance from player's bottom to tree's top
            dy_bottom = abs(tree_rect[1] + tree_rect[3] - player_rect[1])  # Distance from player's top to tree's bottom

            # Move the player out of the collision area in the smallest direction
            min_dx = min(dx_left, dx_right)
            min_dy = min(dy_top, dy_bottom)

            if min_dx < min_dy:
                if dx_left < dx_right:
                    self.player.x = tree_rect[0] - player_rect[2]  # Push left
                else:
                    self.player.x = tree_rect[0] + tree_rect[2]  # Push right
            else:
                if dy_top < dy_bottom:
                    self.player.y = tree_rect[1] - player_rect[3]  # Push up
                else:
                    self.player.y = tree_rect[1] + tree_rect[3]  # Push down


    def draw_rects(self):
        for rect in self.rect_list:
            rect = (rect[0] - self.camera.offset.x, rect[1] - self.camera.offset.y, rect[2], rect[3])
            pygame.draw.rect(self.screen, 'limegreen', rect, 6, 8)


    def update(self):
        self.detection()