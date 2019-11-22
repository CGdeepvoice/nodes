"""
实现十进制转为26个字母， 如 1： A, 26: Z, 27 : AA
这里采用26进制的计算方式，但是又不完全相同，即 27： AA 而不是BA
"""

import string
map = {}
for num, letter in enumerate(string.ascii_uppercase):
    map[num + 1] = letter
print(map)

def to_letter(num, letter = ""):
    if num > 26:
        rel, mod = divmod(num, 26)
        if mod == 0:
            mod = 26
            rel -= 1
        return to_letter(rel, map.get(mod) + letter)
    else:
        return map.get(num) +  letter

for x in range(1, 1000):
    res = to_letter(x)
    print("{} : {}".format(x, res))


"""
0: A 
1: B 
25: Z
26: AA
"""
import string
map = {}
for num, letter in enumerate(string.ascii_uppercase):
    map[num] = letter
print(map)

def to_letter2(num, letter = ""):
    if num > 25:
        rel, mod = divmod(num, 26)
        rel -= 1
        return to_letter2(rel, map.get(mod) + letter)
    else:
        return map.get(num) +  letter

for x in range(1000):
    res = to_letter2(x)
    print("{} : {}".format(x, res))
