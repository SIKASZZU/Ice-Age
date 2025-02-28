import pygame

class Building:
    def __init__(self, map, player):
        self.map = map
        self.player = player

    def open_menu(self):
        ...
        # Clickable icon -> avab menu

    def allow_building(self):
        ...
        # Et ehitada peab olema heat-zone'is.
        # Kui menu lahti siis saab ainult ehitada ja liikuda.

    def select_item(self):
        ...
        # Click'id valitud item'i peale.
        # Fire source
        # Defencive wall
        # Auto fire source tanker
        # Ect...

    def hover_effect(self):
        ...
        # Kui valid ja hover'id player'i range'is siis näitab pre-built image't roheliselt või väiksema transparenciga.
        # Sinna kuhu ei saa ehitada ei tehi seda pre-buildt imaget või on punane

    def build_item(self):
        ...
        # Kui valitud item + sobiv koht + piisavalt looti playeril -> vasaku clickiga placeib itemi

    def update(self):
        ...
        # open_menu()
        # if not open_menu:
        #   return
        #
        # select_item()
        # allow_building() + hover_effect()
        # if not allow_building:
        #   return
        #
        #   build_item()

