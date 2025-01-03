import random

class Tree:
    def __init__(self, map):
        self.data = map.data

    def get_potential_spots(self):
        potential_spots = set()

        for row_idx, row in enumerate(self.data):
            for col_idx, value in enumerate(row):
                if value == 1:
                    if random.random() < 0.9:
                        self.data[row_idx][col_idx] = 10

        
    def update(self):
        print(self.get_potential_spots())