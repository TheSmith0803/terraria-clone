import pygame, random, math
from .items import *
from .objects import *

"""
This class will be responsible for world generation,
and possibly how the player will interact with the world
random spawning and spawning rules will take place here.
"""

class World:
    def __init__(self, game, map_size, tilemap):
        self.game = game
        self.tilemap = tilemap
        self.start_pos = (0, 0)

        self.objects = []

        #tile size of world
        if map_size == 'debug':
            self.map_size = (800, 600)
            self.surface_height = 400
        if map_size == 'small':
            self.map_size = (2800, 1200) 
            self.surface_height = 1000
        if map_size == 'medium':
            self.map_size = (5000, 1488)
            self.surface_height = 1288
        if map_size == 'large':
            self.map_size = (8000, 2000)
            self.surface_height = 1800

    def _generate_tiles(self):
        """
        Base tile generation.
        Generates a base block of grass and dirt tiles.
        """
        x_vals = []
        y_vals = []
        for x in range(1, self.map_size[0]):
            x_vals.append(x*self.tilemap.tile_size)
            for y in range(1, self.map_size[1]):
                y_vals.append(y*self.tilemap.tile_size)
                self.tilemap[f"{x};{y}"] = {'type': 'block', 'subtype': BlockType.GRASS, 'variant': 0,'pos': (x*self.tilemap.tile_size, y*self.tilemap.tile_size),}
                self.tilemap._autotile((x, y), place=True)
            
        
        #stupid random terrain i guess
        """y_min = min(y_vals_tiles)
        for x in x_vals_tiles:
            rand_height = random.randint(0, 10)
            pos = self.tilemap._tile_map[f'{x};{y_min}']['pos']
            while rand_height != 0:
                for num in range(rand_height):
                    y = round(math.sin(y_min - rand_height))
                    self.tilemap._tile_map[f'{x};{y}'] = {'type': 'block', 'subtype': 'grass', 'variant': 0,'pos': (x*self.tilemap.tile_size, y*self.tilemap.tile_size),}
                    self.tilemap._autotile((x, y), place=True)
                    rand_height -= 1"""

        
        self.lh_world_lim = min(x_vals)
        self.rh_world_lim = max(x_vals) + self.tilemap.tile_size - self.game.display.get_width()
        self.upr_world_lim = min(y_vals) - 1200 #1200 == 75 tiles
        self.lwr_world_lim = max(y_vals) + self.tilemap.tile_size - self.game.display.get_height()

        self.tilemap._tile_map["world limits"]["left world limit"] = self.lh_world_lim
        self.tilemap._tile_map["world limits"]["right world limit"] = self.rh_world_lim
        self.tilemap._tile_map["world limits"]["upper world limit"] = self.upr_world_lim
        self.tilemap._tile_map["world limits"]["lower world limit"] = self.lwr_world_lim

    def _surface_noise_pass(self):
        """Creates dynamic terrain on the surface. Will eventually change based upon biome"""
        
        pass

    def generate_world(self):
        """Generates the world. Includes all noise passes."""
        self._generate_tiles()
        self._surface_noise_pass()

    def save_world(self):
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
