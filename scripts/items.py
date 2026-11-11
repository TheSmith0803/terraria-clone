import pygame
from enum import IntEnum

ITEM_TYPES = {
    'block': {'subtype': ['grass', 'dirt', 'wood', 'stone']},
    'ore': {'subtype': ['copper', 'iron', 'gold', 'platinum', 'uranium', 'chromium']},
    'tool': ['pickaxe', 'axe', 'hammer'],
    'weapon': ['sword'],
}

class BlockType(IntEnum):
    AIR = 0
    GRASS = 1
    DIRT = 2
    STONE = 3
    WOOD = 4

#this dict will define different behaviors for the different block types
BLOCK_DATA = {
    BlockType.GRASS: {
        'drop': BlockType.DIRT,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'hand', 'pickaxe'}
    },
    BlockType.DIRT: {
        'drop': BlockType.DIRT,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'hand', 'pickaxe'}
    },
    BlockType.STONE: {
        'drop': BlockType.STONE,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 5,
        'tools': {'pickaxe'}
    },
    BlockType.WOOD: {
        'drop': BlockType.WOOD,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 3,
        'tools': {'axe'}
    }
}

ORE_TYPES = {
    5: {
        'type': 'copper',
        'drop': 'copper ore',
        'autotile': True,
        'stackable': True,
        'stack limit': 99,
        'hardness': 2,
        'tools': {'pickaxe'}
    }
}

#generic item class
class Item:
    def __init__(self, type, img, stackable=False):
        self.type = type
        self.subtype = None 
        self.img = img
        self.stackable = stackable


class Block(Item):
    def __init__(self, subtype, img):

        if subtype not in BLOCK_DATA.keys():
            raise RuntimeError('block type not in listed in subtypes')
        
        super().__init__(ITEM_TYPES['block'], img, True)

        self.type = 'block'
        self.subtype = subtype
        self.block_info = BLOCK_DATA[subtype]

        