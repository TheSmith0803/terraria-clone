import pygame, random, math, struct
from .items import *
from .objects import *

class CoordinateSpace(IntEnum):
    PIXEL = 0
    TILE = 1
    CHUNK = 2
    SCREEN = 3
    WORLD = 4



class World:
    """
    This class will be responsible for world generation,
    and possibly how the player will interact with the world
    random spawning and spawning rules will take place here.
    """
    def __init__(self, game, map_size, tilemap):
        self.game = game
        self.tilemap = tilemap
        self.start_pos = (0, 0)
        self.map_size_str = map_size
        self.objects = []

        #tile size of world
        if map_size == 'debug':
            self.map_size = (32, 32)
            self.surface_height = 16
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
                y_pos = 0
                x_pos = 0
                for y in range(cy*16,cy*16+16):
                    for x in range(cx*16,cx*16+16):
                        if y < self.surface_height:
                            self.tilemap[chk_key].append([BlockType.AIR, 0]) 
                        else:
                            self.tilemap[chk_key].append([BlockType.GRASS, 15])

        for chk in self.tilemap:
            x_offset = chk[0] * 16
            y_offset = chk[1] * 16
            for x in range(x_offset, x_offset+16):
                for y in range(y_offset, y_offset+16):
                    self.tilemap._autotile((x, y))

        
        self.lh_world_lim = 0
        self.upr_world_lim = 0
        self.rh_world_lim = (self.map_size[0] * 16) - self.game.display.get_width()
        self.lwr_world_lim = (self.map_size[1] * 16) - self.game.display.get_height()

    def _surface_noise_pass(self):
        """Creates dynamic terrain on the surface. Will eventually change based upon biome"""
        
        pass

    def get_tile(self, x, y):
        """
        Returns a particular tiles location, in either tile coords, or pixel coords

        Args:
            x: tiles world positin in x axis
            y: tiles world positin in y axis
        """

        if x < 0 or y < 0:
            return None

        cx_origin = ((x // 16) * 16) // 16
        cy_origin = ((y // 16) * 16) // 16

        cx_origin_tile = (x // 16) * 16
        cy_origin_tile = (y // 16) * 16

        x_indx = x - cx_origin_tile
        y_indx = y - cy_origin_tile

        indx = 0
        if y_indx != 0:
            indx += y_indx*16

        if x_indx != 0:
            indx += x_indx

        if (cx_origin, cy_origin) in self.tilemap.keys():

            tile = self.tilemap[(cx_origin, cy_origin)][indx]
        else:
            return None
        
        return tile

    def set_tile(self, x, y, type=BlockType.AIR, variant=0):
        cx_origin = ((x // 16) * 16) // 16
        cy_origin = ((y // 16) * 16) // 16

        cx_origin_tile = (x // 16) * 16
        cy_origin_tile = (y // 16) * 16

        x_indx = x - cx_origin_tile
        y_indx = y - cy_origin_tile

        indx = 0
        if y_indx != 0:
            indx += y_indx*16

        if x_indx != 0:
            indx += x_indx

        if (cx_origin, cy_origin) in self.tilemap.keys():
            self.tilemap[(cx_origin, cy_origin)][indx] = [type, variant]
        else:
            return None
    
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
    
    def get_tile_pos_world(pos) -> list [int, int]:
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
