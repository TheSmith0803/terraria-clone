from scripts.items import *
import struct, json

"""
FILE STUCTURE:

header -> WLDSTART

tiles -> MAP
    sub chunks -> CHK1, CHK2
        u_int(tile_pos_x), u_int(tile_pos_y), u_int(blocktype), u_int(blockvariant) 
"""

with open('map.json', 'r') as f:
    data = json.load(f)


map_size = (800, 600) 
surface_height = 240
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

    return chunks

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
    
chunks = {}
chunks = generate_base_world(mapsize=map_size)
find_chunk(chunks, 2100, 456)

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

def load_world(filename):
    """loads world data"""
    with open(filename, "rb") as f:
        #world and map headers are 17 bytes
        cursor_pos = 17
        f.seek(cursor_pos)

        #read map size and convert to string ('S'=small, 'M'=medium, 'L'=large, 'D'=debug)
        map_size = f.read(1)
        map_size = struct.unpack("<s", map_size)[0].decode('utf-8')
        print(map_size)
        if map_size == 'D':
            map_size = (800, 600) 
        
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
    for cy in range(map_size[1]//16):
        for cx in range(map_size[0]//16):
            data[(cx, cy)] = []
            for y in range(cy*16, cy*16+16):
                for x in range(cx*16, cx*16+16):
                    data[(cx, cy)].append(raw_data[x+y])


    return data

def save_chunk():
    """this function saves a particular chunk at a particular position."""
    pass

save_world('test.world')
chunks = load_world('test.world')
