class RenderSequence:
    def __init__(self, tree, player, map):
        self.tree = tree
        self.player = player
        self.map = map

        self.render_after = False

        self.render_after_player = []

    def player_collided_with(self):
        """ Find collided obj that player collides with and return pygame.Rect """
        self.render_after_player = []

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

            tree_rect = (tree_rect[0], tree_rect[1], tree_rect[2], tree_rect[3] - tree_rect[3] // 2)

            if self.player.rect.colliderect(tree_rect):
                self.render_after = True
                self.render_after_player.append(tree_grid)
                break

    def add_to_render_sequence(self):
        """ Append position of collided rect to a list so 
            the list items can be rendered after the player """
        for tree_grid, tree_rect in self.tree.rects_map_coord.items():
            tree_rect = (tree_rect[0], tree_rect[1], tree_rect[2], tree_rect[3] - tree_rect[3] // 2)
            if (tree_rect[1] + (tree_rect[3] - tree_rect[3] // 2)) > self.player.rect.y:
                    
                self.render_after = True
                self.render_after_player.append(tree_grid)
        


    def update(self):
        self.render_after = False
        self.player_collided_with()
        self.add_to_render_sequence()