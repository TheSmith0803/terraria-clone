import pygame
from enum import IntEnum

class ItemCategory(IntEnum):
    TOOL = 0
    WEAPON = 1
    BLOCK = 2
    ORE = 3


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
BLOCK_DATA = {

    ##########################
    ##### ALL BLOCK DATA #####
    ##########################
    
    ItemID.GRASS_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.DIRT_BLK,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'hand', 'pickaxe'}
    },
    ItemID.DIRT_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.DIRT_BLK,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'hand', 'pickaxe'}
    },
    ItemID.STONE_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.STONE_BLK,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 5,
        'tools': {'pickaxe'}
    },
    ItemID.WOOD_BLK: {
        'category': ItemCategory.BLOCK,
        'drop': ItemID.WOOD_BLK,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 3,
        'tools': {'axe'}
    }
}

WEAPON_DATA = {
    ItemID.WOOD_SWORD: {
        'category': ItemCategory.WEAPON,
        'name': 'Wooden Sword',
        'power': 1,
        'speed': 1
    }
}

#generic item class
class Item:
    def __init__(self, type, img, stackable=False):
        self.type = type
        self.img = img
        self.stackable = stackable


class Block(Item):
    def __init__(self, type, img):

        if type not in BLOCK_DATA.keys():
            raise RuntimeError(f'Block type {type} not in listed in BLOCK_DATA')
        
        super().__init__(type, img, True)

        self.type = type
        self.block_info = BLOCK_DATA[type]

class Tool(Item):
    def __init__(self, type, img):
        super().__init__(type, img, stackable=False)

class Weapon(Item):
    def __init__(self, type, img):

        if type not in WEAPON_DATA.keys():
            raise RuntimeError(f'Weapon type {type} not in listed in WEAPON_DATA')

        super().__init__(type, img, stackable=False)

        self.type = type
        self.weapon_info = WEAPON_DATA[type]
