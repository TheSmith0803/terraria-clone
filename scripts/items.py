import pygame
from enum import IntEnum

class ItemCategory(IntEnum):
    TOOL = 0
    WEAPON = 1
    BLOCK = 2
    ORE = 3

class ToolType(IntEnum):
    HAND = 0
    PICKAXE = 1
    AXE = 2
    HAMMER = 3

class ItemID(IntEnum):
    AIR_BLK = 0
    GRASS_BLK = 1
    DIRT_BLK = 2
    STONE_BLK = 3
    WOOD_BLK = 4

    HAND = 500
    WOOD_PICKAXE = 501
    WOOD_AXE = 502

    WOOD_SWORD = 800
    

#this dict will define different behaviors for the different block types

#### EVERY SINGLE ITEM MUST HAVE THESE DATA FIELDS ####
    # category
    # name
    # stackable

ITEM_DATA = {

    ##########################
    ##### ALL BLOCK DATA #####
    ##########################

    ItemID.GRASS_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.DIRT_BLK,
        'name': 'grass',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {ToolType.HAND, ToolType.PICKAXE}
    },
    ItemID.DIRT_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.DIRT_BLK,
        'name': 'dirt',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {ToolType.HAND, ToolType.PICKAXE}
    },
    ItemID.STONE_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.STONE_BLK,
        'name': 'stone',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 5,
        'tools': {ToolType.PICKAXE}
    },
    ItemID.WOOD_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.WOOD_BLK,
        'name': 'wood',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 3,
        'tools': {ToolType.AXE}
    },

    #########################
    ##### ALL TOOL DATA #####
    #########################

    ItemID.WOOD_PICKAXE: {
        'category': ItemCategory.TOOL,
        'stackable': False,
        'name': 'wooden pickaxe',
        'power': 1,
        'speed': 1
    },

    ###########################
    ##### ALL WEAPON DATA #####
    ###########################

    ItemID.WOOD_SWORD: {
        'category': ItemCategory.WEAPON,
        'stackable': False,
        'name': 'wooden sword',
        'power': 1,
        'speed': 1
    },
}



#generic item class
class Item:
    def __init__(self, typ, img):

        if typ not in ITEM_DATA.keys():
            raise RuntimeError(f'Item type {typ} not in listed in ITEM_DATA')

        self.type = typ
        self.img = img

    @property
    def data(self):
        return ITEM_DATA[self.type]

    @property
    def name(self):
        return ITEM_DATA[self.type]

    @property
    def stackable(self):
        return ITEM_DATA[self.type]['stackable']

    @property
    def category(self):
        return ITEM_DATA[self.type]['category']
    