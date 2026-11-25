
from enum import IntEnum

class test_enum(IntEnum):
    t1=0
    t2=1
    t3=3

test_dict = {
    test_enum.t1: 'hi',
    test_enum.t2: 'mom',
}

td2 = {
    **test_dict,
    test_enum.t3: 'hello mom'
}

print(td2)