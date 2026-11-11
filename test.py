import struct
HEADER = b"HEADER"

HEADER_FMT = "<6s"

header_bytes = struct.pack(HEADER_FMT, HEADER)

nums = []
for i in range(200):
    nums.append(struct.pack("<i", i))

def save_bin_data(data):
    with open('file.bin', "wb") as f:
        f.write(data)
        for num in nums:
            f.write(num)

def load_bin_data(path):
    with open(path, "rb") as f:
        data = f.read()

    header = data[:6]

    list_of_nums = []
    for i in range(6, len(data), 4):
        num = struct.unpack("<I", data[i:i+4])[0]
        list_of_nums.append(num)
    return header, list_of_nums


save_bin_data(header_bytes)

h, l = load_bin_data('file.bin')
print(h, l)


