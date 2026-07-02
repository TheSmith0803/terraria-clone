import pygame, random, math

"""
This class will be responsible for world generation,
and possibly how the player will interact with the world
random spawning and spawning rules will take place here.
"""

class World:
    def __init__(self, game, map_size):
        self.game = game
        self.start_pos = (0, 0)
        self.tiles = self.game.tiles
        
        #tile size of world
        if map_size == 'small':
            map_size = (1248, 800) 
        if map_size == 'medium':
            map_size = (2500, 1000)
        if map_size == 'large':
            map_size = (5000, 2000)
        self.map_size = map_size

    def _generate_tiles(self):
        for x in range(-(self.map_size[0] / 2), (self.map_size[0] / 2)):
            for y in range(-(self.map_size[1] / 2), (self.map_size[1] / 2)):
                print(f"{x};{y}")

    def generate_world(self):
        self._generate_tiles()

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
