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

class WeaponType(IntEnum):
    SHORT_SWORD = 0
    LONG_SWORD = 1

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
    
#### EVERY SINGLE ITEM MUST HAVE THESE DATA FIELDS ####
    # category
    # name
    # stackable


#THESE DICTS ARE SEPERATED IN SUCH A WAY
#THAT IT MAKES IT EASIER TO NAVIGATE THIS FILE
#FOR ALL DIFFERENT REPRESENTATION TYPES, CHECK ITEM_DATA, 
#WHICH CONTAINS ALL THE DIFFERENT SUB CATEGORIES 

BLOCK_DATA = {
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
}

    #########################
    ##### ALL TOOL DATA #####
    #########################
TOOL_DATA = {
    ItemID.WOOD_PICKAXE: {
        'category': ItemCategory.TOOL,
        'tool type': ToolType.PICKAXE,
        'stackable': False,
        'name': 'wooden pickaxe',
        'power': 1,
        'speed': 1
    },
}
    ###########################
    ##### ALL WEAPON DATA #####
    ###########################
WEAPON_DATA = {
    ItemID.WOOD_SWORD: {
        'category': ItemCategory.WEAPON,
        'weapon type': WeaponType.SHORT_SWORD,
        'stackable': False,
        'name': 'wooden sword',
        'power': 1,
        'speed': 1
    },
}

ITEM_DATA = {
    **BLOCK_DATA,
    **TOOL_DATA,
    **WEAPON_DATA,
}

#generic item class
class Item:
    """Takes in an item ID, and the pygame image to represent an in game item. Mainly to be used in inventories."""
    def __init__(self, typ:ItemID, img:pygame.Surface):

        self.item_empty = False
        if typ == None:
            self.item_empty = True
        
        if not self.item_empty and not isinstance(typ, ItemID):
            raise RuntimeError(f'Item type {typ} not in listed in ITEM_DATA')

        self.type = typ
        self.img = img

    @property
    def data(self):
        if self.item_empty: return None
        return ITEM_DATA[self.type]

    @property
    def name(self):
        if self.item_empty: return None
        return ITEM_DATA[self.type]

    @property
    def stackable(self):
        if self.item_empty: return None
        return ITEM_DATA[self.type]['stackable']

    @property
    def category(self):
        if self.item_empty: return None
        return ITEM_DATA[self.type]['category']
