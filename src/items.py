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
            
        self.heated_area = [100, 110, 20, 25, 30, 35, 40, 45]
        self.cold_area = [0, 1, 10, 120, 125, 130, 135, 140, 145]
        self.areas_combined = self.heated_area + self.cold_area