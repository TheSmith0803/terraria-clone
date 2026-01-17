import pygame
import json



class Tilemap:
    def __init__(self, game, map_size=1, tile_size=16):
        self.game = game
        self.map_size = map_size
        self.tile_size = tile_size


        self.tile_map = {}
        self.offgrid_tiles = []

    #temp
    def generate_map(self):
        pass
    
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
        countx = 0
        for i in range(10):
            pos =(countx, 300)
            self.xpos = pos[0] // self.tile_size
            self.ypos = pos[1] // self.tile_size
            self.tile_map[str(self.xpos) + ";" + str(self.ypos)] = {'type': 'grass/top', 'pos': pos,}
            surf.blit(self.game.tiles['grass/top'], pos)
            countx += self.tile_size
