import pygame

class ManageBuilding:
  def __init__(self, map_instance, player_instance):
    self.map = map_instance
    self.player = player_instance
    
    self.menu_state = False

  def toggle_menu(self):
      self.menu_state = not self.menu_state

  def display_menu(self):
     self.menu_state = not self.menu_state

  def decide_action(self):
    ...
    # Vaatab mida clickiti ja selle järgi 
  
  def update(self):
    ...

class ManageHeatSources:
  def __init__(self):
    ...
  
  def display(self):
    ...
    # Teeb UI ära... aka buttonid tekst mida iganes seletab ära mis seal teha saab

  def options(self):
    ...
    # Lõhub ära vms
  
  def upgrade(self):
    ...

  def fuel(self):
    ...

  def update(self):
    ...

class ManageDefenciveWalls:
  def __init__(self):
    ...

  def display(self):
    ...
    # Teeb UI ära... aka buttonid tekst mida iganes seletab ära mis seal teha saab

  def options(self):
    ...
    # Muudab ukseks
    # Lõhub ära
    
