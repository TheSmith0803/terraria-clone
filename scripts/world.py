import pygame, random, math

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
        self.tiles = self.game.tiles

        #tile size of world
        if map_size == 'small':
            #map_size = (1248, 208) 
            map_size = (128, 64)
        if map_size == 'medium':
            map_size = (2496, 800)
        if map_size == 'large':
            map_size = (5000, 1200)
        self.map_size = map_size

    #generates the tiles for the map and sets the world limits
    def _generate_tiles(self):
        x_vals_tiles = []
        y_vals_tiles = []
        x_vals = []
        y_vals = []
        for x in range(-self.map_size[0] // 2, self.map_size[0] // 2):
            x_vals_tiles.append(x)
            x_vals.append(x*self.tilemap.tile_size)
            for y in range(1, self.map_size[1]):
                y_vals_tiles.append(y)
                y_vals.append(y*self.tilemap.tile_size)
                self.tilemap.tile_map[f"{x};{y}"] = {'type': 'block', 'subtype': 'grass', 'variant': 0,'pos': (x*self.tilemap.tile_size, y*self.tilemap.tile_size),}

        for tile in self.tilemap:
            self.tilemap._autotile(tile, place=True)
        
        #stupid random terrain i guess
        """y_min = min(y_vals_tiles)
        for x in x_vals_tiles:
            rand_height = random.randint(0, 5)
            pos = self.tilemap.tile_map[f'{x};{y_min}']['pos']
            while rand_height != 0:
                for num in range(rand_height):
                    y = y_min - rand_height
                    self.tilemap.tile_map[f'{x};{y}'] = {'type': 'block', 'subtype': 'grass', 'variant': 0,'pos': (x*self.tilemap.tile_size, y*self.tilemap.tile_size),}
                    self.tilemap._autotile((x, y), place=True)
                    rand_height -= 1"""


        self.lh_world_lim = min(x_vals)
        self.rh_world_lim = max(x_vals) + self.tilemap.tile_size - self.game.display.get_width()
        self.upr_world_lim = min(y_vals) - 1200
        self.lwr_world_lim = max(y_vals) + self.tilemap.tile_size - self.game.display.get_height()

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
