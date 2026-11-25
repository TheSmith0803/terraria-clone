import pygame
import math
from .items import *

TILE_TYPES = {'grass'}

class Inventory:
    def __init__(self, game, ui):
        self.game = game
        self.ui = ui
        self.size = 10
        self.contents = []

        for i in range(10):
            self.contents.append([Item(None, None), 0])

    def update(self, new_item=None):
        #add new item to inventory
        
        if new_item == None:
            if self.contents[self.ui.selected].type == None:
                return
        
        #iterate over all items in hotbar/inventory to see if there are matching stacks
        elif isinstance(new_item, ItemID) and ITEM_DATA[new_item]['category'] == ItemCategory.BLOCK:
            
            for index, item in enumerate(self.contents):
                if item[0].type == None:
                    blk_drop = ITEM_DATA[new_item]['drop']
                    self.contents[index] = [Item(blk_drop, self.game.tiles[blk_drop]), 1]
                    break
                elif item[0].stackable and ITEM_DATA[new_item]['drop'] == self.contents[index][0].type and item[1] < ITEM_DATA[new_item]['stack limit']:
                    self.contents[index][1] += 1
                    break
                else:
                    continue
        else:
            for index, item in enumerate(self.contents):
                if item[0].type == None:
                    self.contents[index] = [new_item, 1]
                    break
                #for other items
                elif item[0].stackable and item[0].type == self.contents[index][0].type and item[1] < self.stack_size:
                    self.contents[index][1] += 1
                    break

    #specific to the player                
    def render_contents(self, surf):
        for index, item in enumerate(self.contents):
            if item[0] != ItemID.AIR_BLK: #item[0] contains item obj, item[1] is just the quanity of that item
                if item[1] == 0:
                    self.contents[index][0] = Item(None, None)  
                if item[0].type is None:
                    return
                is_block = False    
                if item[0].type in ITEM_DATA.keys() and item[0].category == ItemCategory.BLOCK:
                    assets = self.game.tiles
                    is_block = True
                elif item[0].type in ITEM_DATA.keys() and item[0].category == ItemCategory.WEAPON:
                    assets = self.game.weapons

                if is_block:
                    surf.blit(pygame.transform.scale_by(assets[item[0].type][15], 0.75), (self.ui.hotbar_origin[0] + self.ui.hotbar_positions[index] + (self.game.ui_assets['slot'].get_width() / 2 + 1), self.ui.hotbar_origin[1] + (self.game.ui_assets['slot'].get_height() / 2 + 1)))
                else:
                    asset_ctr = (assets[item[0].type].get_width() / 2, math.floor(assets[item[0].type].get_height() / 2))
                    surf.blit(assets[item[0].type], (self.ui.hotbar_origin[0] + self.ui.hotbar_positions[index] + self.game.ui_assets['slot'].get_width() - asset_ctr[0], self.ui.hotbar_origin[1] + self.game.ui_assets['slot'].get_height() - asset_ctr[1]))

                if item[0].stackable:
                    font = pygame.font.SysFont('Consolas', 8)
                    text_surf = font.render(str(item[1]), True, (255, 255, 255))
                    text_rect = text_surf.get_rect()
                    hotbar_offset = (self.ui.hotbar_positions[index] + self.ui.x_offset, self.ui.y_offset)
                    text_rect.bottomright = (self.ui.hotbar_origin[0] + hotbar_offset[0] + self.game.ui_assets['slot'].get_width() + 5, self.ui.hotbar_origin[1] + hotbar_offset[1] + self.game.ui_assets['slot'].get_height() + 5)
                    surf.blit(text_surf, text_rect)
                
                      
