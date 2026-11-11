import pickle, os, struct
savepth = r'C:\Repos\terraria-clone\saves'
if not os.path.exists(savepth):
    os.makedirs(savepth)

wld = {}

for i in range(200):
    chunk = [(1, 12) for i in range(256)]
    wld[f'chunk_{i}'] = chunk

def sv_chk(data):
    raw = bytes(data)
    with open(os.path.join(savepth, "wld.bin"), "w+b") as f:
        f.write(raw)

def read_chk(offset):
    with open(os.path.join(savepth, "wld.bin"), "r+b") as f:
        f.seek(offset)
        data = f.read(2)
    return data


