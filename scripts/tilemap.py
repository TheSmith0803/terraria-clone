import pygame
import json, random

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
}

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
    def remove_tile(self):
        pass

    #read comment above remove tile
    def place_tile(self):
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

        
