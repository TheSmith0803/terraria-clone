import pygame
import json, random
import os

from .items import Item

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
    tuple(sorted([(-1, 0), (1, 0), (0, 1), (0, -1)])): 8,   #none
    tuple(sorted([(-1, 0)])): 9,                            #top, right, bottom
    tuple(sorted([(0, 1)])): 10,                            #left, top, right
    tuple(sorted([(1, 0)])): 11,                            #left, top, bottom
    tuple(sorted([(0, -1)])): 12,                           #left, bottom, top
    tuple(sorted([(-1, 0), (1, 0)])): 13,                   #top, bottom 
    tuple(sorted([(0, -1), (0, 1)])): 14,                   #left, right
}

TILE_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
AUTOTILE_TPYE = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, map_size='small', tile_size=16):
        self.game = game
        self.tile_size = tile_size

        if map_size == 'small':
            map_size = (1000, 1000)
        if map_size == 'medium':
            map_size = (2000, 1000)
        if map_size == 'large':
            map_size = (3000, 1000)
        self.map_size = map_size

        self.tile_map = {}
        self.offgrid_tiles = []

    #temp
    def generate_map(self):
        county = 350
        for k in range(50): 
            countx = -100
            for i in range(0, 100):
                pos = (countx, county)
                self.xpos = pos[0] // self.tile_size
                self.ypos = pos[1] // self.tile_size
                if str(self.xpos) + ';' + str(self.ypos - 1) in self.tile_map.keys():
                    self.tile_map[str(self.xpos) + ";" + str(self.ypos)] = {'basetype': 'block', 'type': 'grass', 'variant': 8,'pos': pos,}
                else:
                    self.tile_map[str(self.xpos) + ";" + str(self.ypos)] = {'basetype': 'block', 'type': 'grass', 'variant': 0,'pos': pos,}
                countx += self.tile_size
            county += self.tile_size
    
    def physics_rects_around(self, pos):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1), (0, 0)]

        tiles_around = []
        for adjacent_tile in offsets:
            if str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1]) in self.tile_map:
                tiles_around.append(pygame.FRect(self.tile_map[str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1])]['pos'], (self.tile_size, self.tile_size)))
        return tiles_around

    #will take in a tile coord string and remove that particular tile from the tilemap will handle tile sprite changes, same with the place tile
    def remove_tile(self, world_tile_pos) -> Item:
        
        remove_tile = None
        if f'{str(world_tile_pos[0])};{str(world_tile_pos[1])}' in self.tile_map.keys():
                remove_tile = f'{str(world_tile_pos[0])};{str(world_tile_pos[1])}'

        #maybe make the tile actually pop out into the world later, right now it is just removed
        #currently gets 
        if remove_tile != None:
            removed_item = Item(self.tile_map[remove_tile]['type'], self.game.tiles[self.tile_map[remove_tile]['type']][self.tile_map[remove_tile]['variant']], stackable=True)
            self.tile_map.pop(remove_tile)

            adjacent_tiles = []

            for tileoffset in TILE_OFFSETS:
                curr_tile = (world_tile_pos[0] + tileoffset[0], world_tile_pos[1] + tileoffset[1])
                if f'{curr_tile[0]};{curr_tile[1]}' in self.tile_map:
                    adjacent_tiles.append(curr_tile)

            
            if not adjacent_tiles:
                return removed_item

            for tile in adjacent_tiles:
                check_tiles = []
                for tile_offset in TILE_OFFSETS:
                    curr_tile = (tile[0] + tile_offset[0], tile[1] + tile_offset[1])
                    if f'{curr_tile[0]};{curr_tile[1]}' in self.tile_map:
                        check_tiles.append(tile_offset)
                
                check_tiles = tuple(sorted(check_tiles))

                for autotile in AUTOTILE_MAP.keys():
                    if check_tiles == autotile:
                        self.tile_map[f'{tile[0]};{tile[1]}']['variant'] = AUTOTILE_MAP[autotile]
            
            return removed_item
        else:
            return None

    #read comment above remove tile
    def insert_tile(self):
        pass

    def render_map(self, surf , offset=(0, 0)):
        """
        for x in range(int(offset[0] // self.tile_size), int((offset[0] + surf.get_width()) // self.tile_size + 1)):
            for y in range(int(offset[1] // self.tile_size), int((offset[1] + surf.get_height()) // self.tile_size + 1)):
                loc = str(x) + ';' + str(y)
                for tile in self.tile_map:
                    if loc == tile:
                        surf.blit(self.game.tiles['grass'][0], (self.tile_map[tile]['pos'][0] - offset[0], self.tile_map[tile]['pos'][0] - offset[1]))
        """
        
        for tile in self.tile_map:
            surf.blit(self.game.tiles[self.tile_map[tile]['type']][self.tile_map[tile]['variant']], (self.tile_map[tile]['pos'][0] - offset[0], self.tile_map[tile]['pos'][1] - offset[1]))

    def save(self, filepath=r'map.json'):
        with open(filepath, "w") as f:
            json.dump(self.tile_map, f)
        
