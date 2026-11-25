import pygame, random, math, struct
from .items import *
from .objects import *

class CoordinateSpace(IntEnum):
    PIXEL = 0
    TILE = 1
    CHUNK = 2
    SCREEN = 3
    WORLD = 4

DEBUG_W, DEBUG_SH = (256, 128), 64
SMALL_W, SMALL_SH = (2800, 1200), 200
MEDIUM_W, MEDIUM_SH = (5000, 1488), 200
LARGE_W, LARGE_SH = (8000, 2000), 200

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
        self.time = 1200

        #tile size of world
        if map_size == 'debug':
            self.map_size = DEBUG_W
            self.surface_height = 64
        if map_size == 'small':
            self.map_size = SMALL_W
            self.surface_height = 200
        if map_size == 'medium':
            self.map_size = MEDIUM_W
            self.surface_height = 200
        if map_size == 'large':
            self.map_size = LARGE_W
            self.surface_height = 200

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
                        #these init variants are set just so that initial world data gen doesnt take forever
                        #top
                        blk_type = ItemID.GRASS_BLK
                        variant = 0
                        if y == self.surface_height and x != 0 and x != self.map_size[0] - 1:
                            variant = 0
                        elif y == self.surface_height and x == 0:
                            variant = 1
                        elif y == self.surface_height and x == self.map_size[0] - 1:
                            variant = 2
                        #bottom
                        elif y == self.map_size[1] - 1 and x != 0 and x != self.map_size[0] - 1:
                            variant = 7
                        elif y == self.map_size[1] - 1 and x == 0:
                            variant = 3
                        elif y == self.map_size[1] - 1 and x == self.map_size[0] - 1:
                            variant = 4
                        #sides
                        elif x == 0:
                            variant = 6
                        elif x == self.map_size[0] - 1:
                            variant = 5
                        else:
                            variant = 8
                            blk_type = ItemID.DIRT_BLK

                        if y < self.surface_height:
                            self.tilemap[chk_key].append([ItemID.AIR_BLK, 0]) 
                        else:
                            self.tilemap[chk_key].append([blk_type, variant])
        
        self.lh_world_lim = 18
        self.upr_world_lim = 18
        self.rh_world_lim = (self.map_size[0] * 16) - self.game.display.get_width() - 18
        self.lwr_world_lim = (self.map_size[1] * 16) - self.game.display.get_height() - 18

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

        indx = int(indx)

        if (cx_origin, cy_origin) in self.tilemap.keys():
            tile = self.tilemap[(cx_origin, cy_origin)][indx]
        else:
            return None
        
        return tile

    def set_tile(self, x, y, type=ItemID.AIR_BLK, variant=0):
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

        indx = int(indx)

        if (cx_origin, cy_origin) in self.tilemap.keys():
            self.tilemap[(cx_origin, cy_origin)][indx] = [type, variant]
        else:
            return None
    
    def generate_world(self):
        """Generates the world. Includes all noise passes."""
        self._generate_tiles()
        self._surface_noise_pass()

    def save_world(self, filename="map.dig"):
        """saves entire world"""
        with open(filename, "wb") as f:
            WLD_SV_HDR = b"WORLDSTART"
            MAP_HDR = b"TILEMAP"
            MAP_SIZE = b"S" if self.map_size == SMALL_W else \
                       b"M" if self.map_size == MEDIUM_W else \
                       b"L" if self.map_size == LARGE_W else b"D"
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

    def load_world(self, filename="map.dig"):
        """ Loads world data.
        Returns a dictionary of chunks
        Key:
            tuple(x, y) chunk coords. Ex. -> (0,0) top left chunk, (0,1) chunk under top left chunk.
        Value:
            list(256 tiles) -> each tile represented as [BlockType[IntEnum], variant[int]]"""
        with open(filename, "rb") as f:
            #world and map headers are 17 bytes
            cursor_pos = 17
            f.seek(cursor_pos)

            #read map size and convert to string ('S'=small, 'M'=medium, 'L'=large, 'D'=debug)
            map_size = f.read(1)
            map_size = struct.unpack("<s", map_size)[0].decode('utf-8')
            print(map_size)
            if map_size == 'D':
                self.map_size = DEBUG_W
                self.surface_height = DEBUG_SH
            if map_size == 'S':
                self.map_size = SMALL_W
                self.surface_height = SMALL_SH
            if map_size == 'M':
                self.map_size = MEDIUM_W
                self.surface_height = MEDIUM_SH
            if map_size == 'L':
                self.map_size = LARGE_W
                self.surface_height = LARGE_SH
            
            cursor_pos += 1
            f.seek(cursor_pos)
            chunk_bytes = f.read()
            ints = struct.unpack(f"<{len(chunk_bytes)//4}I", chunk_bytes)
            raw_data = []
            for i in range(0, len(ints), 2):
                info = list(ints[i:i+2])
                info[0] = ItemID(info[0])
                raw_data.append(info)

        data = {}
        chk_num = 0
        for cy in range(self.map_size[1]//16):
            for cx in range(self.map_size[0]//16):
                data[(cx, cy)] = []
                for indx in range(chk_num*256, chk_num*256+256):
                    data[(cx, cy)].append(raw_data[indx])
                chk_num += 1

        self.tilemap._tile_map = data
        self.lh_world_lim = 0
        self.upr_world_lim = 0
        self.rh_world_lim = (self.map_size[0] * 16) - self.game.display.get_width()
        self.lwr_world_lim = (self.map_size[1] * 16) - self.game.display.get_height()

        
    
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
