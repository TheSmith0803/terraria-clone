import pygame

class UI:
    def __init__(self, game, inventory, images, init_pos):
        self.images = images
        self.pos = init_pos
        self.spacing = 20 #space between each inventory slot
        self.positions = [x * self.spacing for x in range(10)]

    def update(self):
        #updates to player inventory

        self.game.player.inventory
        #updates to world container inventories

    def render_inventory(self, surf):
        
        for pos in self.positions:
            surf.blit(self.images[0], (self.pos[0] + pos, self.pos[1]))
        