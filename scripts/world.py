import pygame, random, math, struct
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
        self.map_size_str = map_size
        self.objects = []

        #tile size of world
        if map_size == 'debug':
            self.map_size = (200, 100)
            self.surface_height = 50
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

        
        for cy in range(self.map_size[1]//16):
            for cx in range(self.map_size[0]//16):
                chk_key = (cx, cy)
                self.tilemap[chk_key] = []
                for y in range(cy*16,cy*16+16):
                    for x in range(cx*16,cx*16+16):
                        if y < self.surface_height:
                            self.tilemap[chk_key].append([BlockType.AIR, 0]) 
                        else:
                            self.tilemap[chk_key].append([BlockType.GRASS, 0])

        world_limits = [0, 0, self.map_size[0]*16, self.map_size[1]*16]

        self.lh_world_lim = world_limits[0]
        self.rh_world_lim = world_limits[2]
        self.upr_world_lim = world_limits[1]
        self.lwr_world_lim = world_limits[3]

    def _surface_noise_pass(self):
        """Creates dynamic terrain on the surface. Will eventually change based upon biome"""
        
        pass

    def generate_world(self):
        """Generates the world. Includes all noise passes."""
        self._generate_tiles()
        self._surface_noise_pass()

    def save_world(self, filename):
        """saves entire world"""
        with open(filename, "wb") as f:
            WLD_SV_HDR = b"WORLDSTART"
            MAP_HDR = b"TILEMAP"
            MAP_SIZE = b"S" if self.map_size_str == "small" else \
                       b"M" if self.map_size_str == "medium" else \
                       b"L" if self.map_size_str == "large" else b"D"
            wld_hdr_bytes = struct.pack("<10s", WLD_SV_HDR)
            map_hdr_bytes = struct.pack("<7s", MAP_HDR)
            map_size_bytes = struct.pack("<s", MAP_SIZE)

            f.write(wld_hdr_bytes)  #indicates a world file
            f.write(map_hdr_bytes)  #indicates start of map
            f.write(map_size_bytes) #indicated size of map

            #saving of world chunks
            for k in self.tilemap.keys():
                for block in self.tilemap[k]:
                    f.write(struct.pack("<2I", *block))

    def load_world(self):
        pass
    
    def get_tile_pos_world(x, y) -> list [int, int]:
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
