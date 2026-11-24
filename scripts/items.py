import pygame
from enum import IntEnum

ITEM_TYPES = {
    'block': {'subtype': ['grass', 'dirt', 'wood', 'stone']},
    'ore': {'subtype': ['copper', 'iron', 'gold', 'platinum', 'uranium', 'chromium']},
    'tool': ['pickaxe', 'axe', 'hammer'],
    'weapon': ['sword'],
}

class BlockType(IntEnum):
    NONE = 0
    AIR = 1
    GRASS = 2
    DIRT = 3
    STONE =4
    WOOD = 5

class ToolType(IntEnum):
    HAND = 0
    WOOD_PICKAXE = 1
    WOOD_AXE = 2

class WeaponType(IntEnum):
    WOOD_SWORD = 0

#this dict will define different behaviors for the different block types
BLOCK_DATA = {
    BlockType.GRASS: {
        'name': 'grass block',
        'drop': BlockType.DIRT,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'hand', 'pickaxe'}
    },
    BlockType.DIRT: {
        'name': 'dirt block',
        'drop': BlockType.DIRT,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'hand', 'pickaxe'}
    },
    BlockType.STONE: {
        'name': 'stone block',
        'drop': BlockType.STONE,
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 5,
        'tools': {'pickaxe'}
    },
    BlockType.WOOD: {
        'name': 'wood',
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

TOOL_DATA = {

}

WEAPON_DATA = {
    WeaponType.WOOD_SWORD: {
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
