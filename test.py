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


map_size = (1248, 208) 

num_chunks = map_size[0]*map_size[1] // 256

chunks = []

offset = 0


for x in range(map_size[0]):
    for y in range(map_size[1]):
        try:
            chunks.append([x, y, data["tiles"][f"{x};{y}"]["subtype"], data["tiles"][f"{x};{y}"]["variant"]])
        except KeyError:
            chunks.append([x, y, BlockType.AIR, 0])

WLD_SV_HDR = b"WORLDSTART"
MAP_HDR = b"MAPHDR"

wld_hdr_bytes = struct.pack("<10s", WLD_SV_HDR)
map_hdr_bytes = struct.pack("<6s", MAP_HDR)


def write_file():
    with open('file.bin', "wb") as f:
        f.write(wld_hdr_bytes)
        f.write(map_hdr_bytes)
        f.write(struct.pack("<4s", b"CHK1"))
        for i in chunks:
            f.write(struct.pack("<4I", *i))

def read_file():
    with open('file.bin', "rb") as f:
        cursor_pos = 20
        f.seek(cursor_pos)
        chunk_bytes = f.read()
        ints = struct.unpack(f"<{len(chunk_bytes)//4}I", chunk_bytes)
        data = []
        for i in range(0, len(ints), 4):
            data.append(list(ints[i:i+4]))
    return data

def get_chunk(x=0, y=0):
    cursor_pos = 20
    cursor_pos += x*256
    cursor_pos += y*256
    with open('file.bin', "rb") as f:
        f.seek(cursor_pos)
        data = f.read(4096) # size of a chunk
    chunk = []
    for i in range(0, len(data), 16):
        chunk.append(list(struct.unpack("<4I", data[i:i+16])))
    return chunk
write_file()
info = get_chunk(x=0, y=0)
for tile in info:
    print(tile)


