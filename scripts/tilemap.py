import pygame
import json



class Tilemap:
    def __init__(self, game, map_size=1, tile_size=14):
        self.game = game
        self.map_size = map_size
        self.tile_size = tile_size

        self.tile_map = {}
        self.offgrid_tiles = []

    #temp
    def generate_map(self):
        pass
    
    def get_rects(self):
        pass

    def render_map(self):
        countx = 0
        for j in range(50):
            self.game.display.blit(self.game.tiles['grass/top'], (countx + (j * 2) + 20, 100))
            countx += self.tile_size