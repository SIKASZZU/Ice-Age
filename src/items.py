# water   id 0
# terrain id 1
# tree    id 10 - 19

# fire    id 20 - 59
    # pitfire  id 20 - 29
    # campfire id 30 - 39
    # bonfire  id 40 - 49
    # furnice  id 50 - 59

    # 'Torch'         - ID 20
    # 'Firepit'       - ID 25
    # 'Campfire       - ID 30
    # 'Bonfire'       - ID 35
    # 'Furnace'       - ID 40
    # 'Blast Furnace' - ID 45

class Items:
    def __init__(self):
        # 110_5 = harvest tree image

        self.trees = [10, 110, 10_5, 110_5, 10_6, 110_6]
            
        self.heated_area = [100, 110, 20, 25, 30, 35, 40, 45, 110_5, 110_6, 9, 8, 7]
        self.cold_area = [0, 1, 10, 120, 125, 130, 135, 140, 145, 10_5, 10_6, 109, 108, 107]
        self.areas_combined = self.heated_area + self.cold_area
