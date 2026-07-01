import pygame, random, math

"""
This class will be responsible for world generation,
and possibly how the player will interact with the world
random spawning and spawning rules will take place here.
"""

class World:
    def __init__(self, game, tilemap):
        self.game =game
        self.tilemap = tilemap
        self.start_pos = (0, 0)
        self.tiles = self.game.tiles

    def generate_world(self):
        pass

    def load_world(self):
        pass

class WorldObject:
    def __init__(self):
        pass

class Tree(WorldObject):
    def __init__(self):
        pass

class Bush(WorldObject):
    def __init__(self):
        pass

class Grass(WorldObject):
    def __init__(self):
        pass
