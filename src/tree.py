import random

class Tree:
    def __init__(self, map):
        self.map = map
        self.sprite = 0
        self.width = 100
        self.heigth = 100
        self.spots = self.get_potential_spots()

    def get_potential_spots(self):
        spots = set()
        for row_idx, row in enumerate(self.map.data):
            for col_idx, value in enumerate(row):
                if value == 1:
                    if random.random() < 0.4:
                        spots.add((row_idx, col_idx))
        return spots


    def spawn(self):
        for index in self.spots: 
            self.map.data[index[0]][index[1]] = 10

    def update(self):
        pass
        #self.spawn()
