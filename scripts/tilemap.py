import pygame
import json

AUTOTILE_MAP = {
    tuple(sorted([]))
}

class Tilemap:
    def __init__(self, game, map_size=1, tile_size=16):
        self.game = game
        self.map_size = map_size
        self.tile_size = tile_size


        self.tile_map = {}
        self.offgrid_tiles = []

    #temp
    def generate_map(self):
        county = 0
        for k in range(10): 
            countx = 0
            for i in range(25):
                pos =(countx, 300 + county)
                self.xpos = pos[0] // self.tile_size
                self.ypos = pos[1] // self.tile_size
                self.tile_map[str(self.xpos) + ";" + str(self.ypos)] = {'type': 'grass/top', 'pos': pos,}
                countx += self.tile_size
            county += self.tile_size
    
    def physics_rects_around(self, pos):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1), (0, 0)]

        tiles_around = []
        for adjacent_tile in offsets:
            if str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1]) in self.tile_map:
                tiles_around.append(pygame.FRect(self.tile_map[str(int(pos[0] // self.tile_size) + adjacent_tile[0]) + ";" + str(int(pos[1] // self.tile_size) + adjacent_tile[1])]['pos'], (self.tile_size, self.tile_size)))
        return tiles_around

    #how the player and other objects can remove tiles in the world
    def remove_tile(self):
        pass    

    def render_map(self, surf , offset=(0, 0)):
        
        
        for tile in self.tile_map:
            surf.blit(self.game.tiles['grass'][1], self.tile_map[tile]['pos'])
            

        
