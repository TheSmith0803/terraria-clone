import pygame

ITEM_TYPES = {
    'block': {'subtype': ['grass', 'dirt', 'wood', 'stone']},
    'ore': {'subtype': ['copper', 'iron', 'gold', 'platinum', 'uranium', 'chromium']},
    'tool': ['pickaxe', 'axe', 'hammer'],
    'weapon': ['sword'],
}

#this dict will define different behaviors for the different block types
BLOCK_TYPES = {
    'grass': {
        'drop': 'dirt',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 1,
        'tools': {'hand', 'pickaxe'}
    },
    'dirt': {
        'drop': 'dirt',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 1,
        'tools': {'hand', 'pickaxe'}
    },
    'stone': {
        'drop': 'stone',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'pickaxe'}
    },
    'wood' : {
        'drop': 'wood',
        'autotile': True,
        'stackable': True,
        'stack limit': 999,
        'hardness': 2,
        'tools': {'axe'}
    }
}

ORE_TYPES = {
    'copper': {
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

        if subtype not in BLOCK_TYPES.keys():
            raise RuntimeError('block type not in listed in subtypes')
        
        super().__init__(ITEM_TYPES['block'], img, True)

        self.type = 'block'
        self.subtype = subtype
        self.block_info = BLOCK_TYPES[subtype]

        