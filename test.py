from scripts.items import *
from scripts.world import World
from scripts.tilemap import Tilemap
import struct, json

"""
FILE STUCTURE:

header -> WLDSTART

tiles -> MAP
    sub chunks -> CHK1, CHK2
        u_int(tile_pos_x), u_int(tile_pos_y), u_int(blocktype), u_int(blockvariant) 
"""




map_size = (32, 32) 
surface_height = 16
CHK_SIZE = 256
num_chunks = map_size[0]*map_size[1] // CHK_SIZE

offset = 0

# initial world generation
def generate_base_world(mapsize):
    chunks = {}
    for cy in range(mapsize[1]//16):
        for cx in range(mapsize[0]//16):
            chk_key = (cx, cy)
            chunks[chk_key] = []
            for y in range(cy*16,cy*16+16):
                for x in range(cx*16,cx*16+16):
                    if y < surface_height:
                        chunks[chk_key].append([BlockType.AIR, 0]) 
                    else:
                        chunks[chk_key].append([BlockType.GRASS, 0])

    world_limits = [0, 0, mapsize[0]*16, mapsize[1]*16]

    return chunks, world_limits

#x and y are pixel positions
def find_chunk(chks, x, y):
    """Find a given chunk, given a pixle position x and y"""
    tile_x = x // 16
    tile_y = y // 16
    chk_x = tile_x // 16
    chk_y = tile_y // 16
    try:
        thing = chks[(chk_x, chk_y)]
    except KeyError:
        raise KeyError(f"chunk ({chk_x}, {chk_y}) does not exist. Out of range.")
    



def save_world(filename, size=None):
    """saves entire world"""
    with open(filename, "wb") as f:
        WLD_SV_HDR = b"WORLDSTART"
        MAP_HDR = b"TILEMAP"
        MAP_SIZE = b"S" if size == "small" else b"M" if size == "medium" else b"L" if size == "large" else b"D"
        wld_hdr_bytes = struct.pack("<10s", WLD_SV_HDR)
        map_hdr_bytes = struct.pack("<7s", MAP_HDR)
        map_size_bytes = struct.pack("<s", MAP_SIZE)

        f.write(wld_hdr_bytes)  #indicates a world file
        f.write(map_hdr_bytes)  #indicates start of map
        f.write(map_size_bytes) #indicated size of map

        #saving of world chunks
        for k in chunks:
            for block in chunks[k]:
                f.write(struct.pack("<2I", *block))

def load_world(filename) -> dict:
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
        if map_size == 'D':
            map_size = (32, 32) 
        
        cursor_pos += 1
        f.seek(cursor_pos)
        chunk_bytes = f.read()
        ints = struct.unpack(f"<{len(chunk_bytes)//4}I", chunk_bytes)
        raw_data = []
        for i in range(0, len(ints), 2):
            info = list(ints[i:i+2])
            info[0] = BlockType(info[0])
            raw_data.append(info)

    data = {}
    chk_num = 0
    for cy in range(map_size[1]//16):
        for cx in range(map_size[0]//16):
            data[(cx, cy)] = []
            for indx in range(chk_num*256, chk_num*256+256):
                data[(cx, cy)].append(raw_data[indx])
            chk_num += 1



    return data

def get_chunk():
    """this function saves a particular chunk at a particular position."""
    pass



#chunks = {}
#chunks, wld_limits = generate_base_world(mapsize=map_size)
#save_world('test.world')
#chunks = load_world('test.world')
#for k, v in chunks.items():
#    print(k, v, end='\n\n\n')
game = "hi"
t = Tilemap(game)
w = World(game, "debug", t)

w.generate_world()

x_offset = 0
y_offset = 0
indx = 0
for chk in t.keys():
    y = chk[1]*16
    for tile in t[chk]:
        x = (chk[0]*16)+x_offset
        indx += 1
        if x >= chk[0]*16+15:
            x_offset = 0
            y += 1
            continue
        x_offset += 1

class CoordinateSpace(IntEnum):
    PIXEL = 0
    TILE = 1
    CHUNK = 2
    SCREEN = 3
    WORLD = 4

def get_tile(tilemap, x, y, ret=CoordinateSpace.TILE):
    """
    Returns a particular tiles location, in either tile coords, or pixel coords

    Args:

    """
    x_offset = 0

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

    if (cx_origin, cy_origin) in tilemap.keys():
        tile = tilemap[(cx_origin, cy_origin)][indx]
    else:
        raise KeyError(f"({cx_origin},{cy_origin}) is not a chunk! trying to access tile ({x}, {y})")
    
    return tile

def set_tile(tilemap, x, y, tile):
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

    if (cx_origin, cy_origin) in tilemap.keys():
        tile = tilemap[(cx_origin, cy_origin)][indx]
    else:
        raise KeyError(f"({cx_origin},{cy_origin}) is not a chunk! trying to access tile ({x}, {y})")

def get_tiles(tilemap, x1, y1, x2, y2):
    pass

print(get_tile(t, x=16, y=16))
