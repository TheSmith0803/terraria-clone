import pygame

ITEM_TYPES = {
    'block': {'subtype': ['grass', 'dirt', 'wood', 'stone']},
    'ore': {'subtype': ['copper', 'iron', 'gold', 'platinum', 'uranium', 'chromium']},
    'tool': ['pickaxe'],
    'weapon': ['sword'],
}

class Item:
    def __init__(self, type, img, stackable=False):
        self.type = type 
        self.img = img
        self.stackable = stackable

class Block(Item):
    def __init__(self, subtype, img):

        if subtype not in ITEM_TYPES['block']['subtype']:
            raise RuntimeError('block type in listed in subtypes')
        
        super().__init__(ITEM_TYPES['block'], img, True)

        self.subtype = subtype

        