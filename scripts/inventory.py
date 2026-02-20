import pygame
from .items import Item

TILE_TYPES = {'grass'}

class Inventory:
    def __init__(self, game, ui):
        self.game = game
        self.ui = ui
        self.size = 10
        self.contents = []

        self.stack_size = 999

        for i in range(10):
            self.contents.append([Item(None, None), 0])

    def update(self, new_item):
        #add new item to inventory
        for index, item in enumerate(self.contents):
            if item[0].type == None:
                self.contents[index] = [new_item, 1]
                break
            elif item[0].stackable and item[0].type == self.contents[index][0].type and item[1] < self.stack_size:
                self.contents[index][1] += 1
                break
    
    def render_contents(self, surf):
        for index, item in enumerate(self.contents):
            if item[0].type != None: #item[0] contains item obj, item[1] is just the quanity of that item
                if item[1] == 0:
                    self.contents[index][0] = Item(None, None)  
                if item[0].type in TILE_TYPES:
                    surf.blit(pygame.transform.scale_by(self.game.tiles[item[0].type][0], 0.75), (self.ui.pos[0] + self.ui.hotbar_positions[index] + (self.game.inventory_assets['slot'].get_width() / 2 + 1), self.ui.pos[1] + (self.game.inventory_assets['slot'].get_height() / 2 + 1)))
                    font = pygame.font.SysFont('Consolas', 8)
                    text_surf = font.render(str(item[1]), True, (255, 255, 255))
                    text_rect = text_surf.get_rect()
                    hotbar_offset = (self.ui.hotbar_positions[index] + self.ui.x_offset, self.ui.y_offset)
                    text_rect.bottomright = (self.ui.pos[0] + hotbar_offset[0] + self.game.inventory_assets['slot'].get_width() + 5, self.ui.pos[1] + hotbar_offset[1] + self.game.inventory_assets['slot'].get_height() + 5)
                    surf.blit(text_surf, text_rect)
                      
