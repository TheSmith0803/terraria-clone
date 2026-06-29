import pygame

ITEM_TYPES = {
    'block': {'subtype': ['grass', 'dirt', 'wood', 'stone']},
    'ore': {'subtype': ['copper', 'iron', 'gold', 'platinum', 'uranium', 'chromium']},
    'tool': ['pickaxe'],
    'weapon': ['sword'],
}

#this dict will define different behaviors for the different block types
BLOCK_TYPES = {
    'grass': {
        'drop': 'dirt',
        'autotile': True,
        'stackable': True,
        'hardness': 1,
    },
    'stone': {
        'drop': 'stone',
        'autotile': True,
        'stackable': True,
        'hardness': 2,
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

        if subtype not in ITEM_TYPES['block']['subtype']:
            raise RuntimeError('block type not in listed in subtypes')
        
        super().__init__(ITEM_TYPES['block'], img, True)

        self.type = 'block'
        self.subtype = subtype

        