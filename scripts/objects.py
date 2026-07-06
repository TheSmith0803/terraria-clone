from .inventory import Inventory

class InteractableObjects:
    def __init__(self, game, ui, assets, pos):
        self.game = game
        self.ui = ui
        self.states = 2
        self.assets = assets
        self.img = None
        self.pos = pos

        self.objects = []

    def update(self):
        pass

    def render(self):
        pass

class Chest(InteractableObjects):
    def __init__(self):
        self.img = self.assets['chest']
        self.inventory = Inventory(self.game, self.ui)

        self.inventory.size = 20
        