import pygame


class RenderSequence:
    def __init__(self, tree, player, map):
        self.tree = tree
        self.player = player
        self.map = map

        self.render_after = False

        self.in_view_objects = []
        self.render_after_player = []

    def player_collided_with(self):
        """ Find collided obj that player collides with and return pygame.Rect """

        # check only grids around player
        x = self.player.rect[0] // self.map.tile_size
        y = self.player.rect[1] // self.map.tile_size

        self.render_after = False
        for tree in self.tree.rects_map_coord.items():
            tree_grid, tree_rect = tree
            if abs(tree_grid[0] - x) > 2:
                continue
            if abs(tree_grid[1] - y) > 2:
                continue

            if self.player.rect.colliderect(tree_rect):
                self.render_after = True
                break

    def add_to_render_sequence(self, collided_tree_rect):
        """ Append position of collided rect to a list so 
            the list items can be rendered after the player """
        
        pass

    def update(self):
        collided_tree_rect = self.player_collided_with()
        self.add_to_render_sequence(collided_tree_rect)