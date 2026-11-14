import pygame
import json, random, orjson, pickle
import os
from .items import *

from .items import Item, Block, BLOCK_DATA, ORE_TYPES

#rules for spawinging tiles, variants equate to file names --> '0.png'
AUTOTILE_MAP = {                                            #exposed sides
    tuple(sorted([(-1, 0), (1, 0), (0, 1)])): 0,            #top
    tuple(sorted([(1, 0), (0, 1)])): 1,                     #left, top
    tuple(sorted([(-1, 0), (0, 1)])): 2,                    #right, top
    tuple(sorted([(1, 0), (0, -1)])): 3,                    #left, bottom
    tuple(sorted([(-1, 0), (0, -1)])): 4,                   #right, bottom
    tuple(sorted([(-1, 0), (0, 1), (0, -1)])): 5,           #right
    tuple(sorted([(1, 0), (0, 1), (0, -1)])): 6,            #left
    tuple(sorted([(-1, 0), (1, 0), (0, -1)])): 7,           #bottom
    tuple(sorted([(-1, 0), (1, 0), (0, 1), (0, -1)])): 8,   #all
    tuple(sorted([(-1, 0)])): 9,                            #top, right, bottom
    tuple(sorted([(0, 1)])): 10,                            #left, top, right
    tuple(sorted([(1, 0)])): 11,                            #left, top, bottom
    tuple(sorted([(0, -1)])): 12,                           #left, bottom, top
    tuple(sorted([(-1, 0), (1, 0)])): 13,                   #top, bottom 
    tuple(sorted([(0, -1), (0, 1)])): 14,                   #left, right
    tuple(sorted([])): 15,                                  #none
}

TILE_OFFSETS = tuple(sorted([(-1, 0), (1, 0), (0, -1), (0, 1)]))
AUTOTILE_TPYE = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
    
        self._tile_map = {}
        self._tile_map["tiles"] = {} #where actual tile data is stored
        self._tile_map["world limits"] = {} #world limit information

        self.offgrid_tiles = []

        self.tile_coords = {}        

    def __iter__(self):
        for tile in self._tile_map["tiles"]:
            parts = tile.split(';')
            coord = tuple(int(c) for c in parts)
            coord = tuple(coord)
            yield coord

    def __getitem__(self, key):
        return self._tile_map["tiles"][key]
    
    def __setitem__(self, key, value):
            self._tile_map["tiles"][key] = value

    def keys(self):
        return self._tile_map["tiles"].keys()

    def values(self):
        return self._tile_map["tiles"].values()

    def items(self):
        return self._tile_map["tiles"].items()
    
    #takes in a tuple of tile coords and returns the associated tile data
    def _get_tile_data(self, tile_coords):
        return self._tile_map["tiles"][f'{str(tile_coords[0])};{str(tile_coords[1])}']

    def physics_rects_around(self, pos):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1), (0, 0)]

        tiles_around = []
        for adjacent_tile in offsets:
            if str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1]) in self._tile_map["tiles"]:
                rect = pygame.Rect(self._tile_map["tiles"][str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1])]['pos'], (self.tile_size, self.tile_size))
                tiles_around.append(rect)
        return tiles_around
    

    #this is just to check the surrounding tiles on a tilemap change, for both placement and removal
    def _block_type_check(self, tile):
        pass
    
    #just putting the autotile code in one place for both removing and placing tiles
    def _autotile(self, world_tile_pos, place=False):
        adjacent_tiles = []

        if place:
            adjacent_tiles.append(world_tile_pos)

        for tileoffset in TILE_OFFSETS:
            curr_tile = (world_tile_pos[0] + tileoffset[0], world_tile_pos[1] + tileoffset[1])
            if f'{curr_tile[0]};{curr_tile[1]}' in self._tile_map["tiles"]:
                adjacent_tiles.append(curr_tile)
        if not adjacent_tiles:
            return

        for tile in adjacent_tiles:
            check_tiles = []
            for tile_offset in TILE_OFFSETS:
                curr_tile = (tile[0] + tile_offset[0], tile[1] + tile_offset[1])
                if f'{curr_tile[0]};{curr_tile[1]}' in self._tile_map["tiles"]:
                    check_tiles.append(tile_offset)
            
            check_tiles = tuple(sorted(check_tiles))
            for autotile in AUTOTILE_MAP:
                if check_tiles == autotile:
                    self._tile_map["tiles"][f'{tile[0]};{tile[1]}']['variant'] = AUTOTILE_MAP[autotile]

                
                    if AUTOTILE_MAP[autotile] == 8 and self._tile_map["tiles"][f'{tile[0]};{tile[1]}']['subtype'] == BlockType.GRASS:
                        self._tile_map["tiles"][f'{tile[0]};{tile[1]}']['subtype'] = BlockType.DIRT


    #will take in a tile coord string and remove that particular tile from the tilemap will handle tile sprite changes, same with the place tile
    #this is specifically for removing block type objects, the logic for that is natrually simpler
    def rmv_tile(self, world_tile_pos) -> Block:
        remove_tile = None
        if f'{str(world_tile_pos[0])};{str(world_tile_pos[1])}' in self._tile_map["tiles"].keys():
                remove_tile = f'{str(world_tile_pos[0])};{str(world_tile_pos[1])}'
        #print(remove_tile)
        #maybe make the tile actually pop out into the world later, right now it is just removed
        #currently gets
        
        if remove_tile != None:
            removed_item = Block(BLOCK_DATA[self._tile_map["tiles"][remove_tile]['subtype']]['drop'], self.game.tiles[BLOCK_DATA[self._tile_map["tiles"][remove_tile]['subtype']]['drop']][self._tile_map["tiles"][remove_tile]['variant']])
            self._tile_map["tiles"].pop(remove_tile)
            self._autotile(world_tile_pos)
            return removed_item
        else:
            return None

    #read comment above remove tile
    def insert_tile(self, world_tile_pos, block: Block) -> None:
        place_tile = None
        if f'{str(world_tile_pos[0])};{str(world_tile_pos[1])}' not in self._tile_map["tiles"].keys():
                place_tile = f'{str(world_tile_pos[0])};{str(world_tile_pos[1])}'
        #print(f"world tile pos: {world_tile_pos[0]}, {world_tile_pos[1]}")
        if place_tile != None:
            pos = (world_tile_pos[0] * self.tile_size, world_tile_pos[1] * self.tile_size)
            self._tile_map["tiles"][place_tile] = {'type': block.type, 'subtype': block.subtype, 'variant': 0,'pos': pos,}
            self._autotile(world_tile_pos, place=True)
            return True
        else:
            return False


    def render_map(self, surf , offset=(0, 0)):
        
        #this is da way
        for x in range(int(offset[0] // self.tile_size), int((offset[0] + surf.get_width()) // self.tile_size + 1)):
            for y in range(int(offset[1] // self.tile_size), int((offset[1] + surf.get_height()) // self.tile_size + 1)):
                loc = (f'{x};{y}')
                
                if loc in self._tile_map["tiles"]:
                    tile = self._tile_map["tiles"][loc]
                    surf.blit(self.game.tiles[tile['subtype']][tile['variant']], 
                                (
                                    tile['pos'][0] - offset[0], 
                                    tile['pos'][1] - offset[1]
                                )
                             )

    #maybe implement chunking? also make world saving async
    def save(self, filename=r'map.json'):
            
        with open(filename, "w") as f:
            json.dump(self._tile_map, f)

    def load(self, filepath=r'map.json'):
        try:
            with open(filepath, 'r') as f:
                print("loading world")
                self._tile_map = json.load(f)
                
            self.game.world.lh_world_lim = self._tile_map["world limits"]["left world limit"]
            self.game.world.rh_world_lim = self._tile_map["world limits"]["right world limit"]
            self.game.world.upr_world_lim = self._tile_map["world limits"]["upper world limit"]
            self.game.world.lwr_world_lim = self._tile_map["world limits"]["lower world limit"]
            return True 
        except FileNotFoundError:
            print(f"{filepath} does not exist.")
            return False
        
        
