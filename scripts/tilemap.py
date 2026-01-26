import pygame
import json, random

#rules for spawinging tiles, variants equate to file names --> '0.png'
AUTOTILE_MAP = {
    tuple(sorted([(-1, 0), (1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1)])): 1,
    tuple(sorted([(-1, 0), (1, 0)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 4,
    tuple(sorted([(-1, 0), (1, 0), (0, 1)])): 5,
    tuple(sorted([(-1, 0), (1, 0), (0, -1), (0, 1)])): 5,
}

AUTOTILE_TPYE = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, map_size=1, tile_size=16):
        self.game = game
        self.map_size = map_size
        self.tile_size = tile_size


        self.tile_map = {}
        self.offgrid_tiles = []

    #temp
    def generate_map(self):
        county = 350
        for k in range(10): 
            countx = 150
            for i in range(-125, -115):
                pos = (countx, county)
                self.xpos = pos[0] // self.tile_size
                self.ypos = pos[1] // self.tile_size
                if str(self.xpos) + ';' + str(self.ypos - 1) in self.tile_map.keys():
                    self.tile_map[str(self.xpos) + ";" + str(self.ypos)] = {'type': 'grass', 'variant': 5,'pos': pos,}
                else:
                    self.tile_map[str(self.xpos) + ";" + str(self.ypos)] = {'type': 'grass', 'variant': 0,'pos': pos,}
                countx += self.tile_size
            county += self.tile_size
    
    def physics_rects_around(self, pos):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1), (0, 0)]

        tiles_around = []
        for adjacent_tile in offsets:
            if str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1]) in self.tile_map:
                tiles_around.append(pygame.FRect(self.tile_map[str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1])]['pos'], (self.tile_size, self.tile_size)))
        return tiles_around

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

        
