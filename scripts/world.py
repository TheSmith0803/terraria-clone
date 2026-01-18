import pygame, random, math

"""
This class will be responsible for world generation,
and possibly how the player will interact with the world
random spawning and spawning rules will take place here.
"""

class World:
    def __init__(self, game, tilemap):
        
        self.start_pos = (0, 0)
        self.tiles = self.game.tiles
        self.tilemap = tilemap



    def generate_world(self):
        pass

    def load_world(self):
        pass