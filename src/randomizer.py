#!/usr/bin/env python

import random
import re
import sys

ITEM_LOCATIONS = {
    "Brinstar": ["LA3DE", "LA3E7", "LA3ED", "LA3F6", "LA3FC", "LA409", "LA412",
                 "LA41F", "LA433"],
    "Kraid": ["LA27F", "LA286", "LA28F", "LA298", "LA2A1", "LA2B1"],
    "Norfair": ["LA2E2", "LA2F0", "LA2F6", "LA2FC", "LA305", "LA316", "LA326",
                "LA32C", "LA33E", "LA35D", "LA370", "LA383", "LA38C", "LA39A",
                "LA3A0"],
    "Ridley": ["LA21E", "LA227", "LA230", "LA239"]
}

# 00 bombs
# 01 high jump
# 02 long beam
# 04 morph ball
# 05 varia
# 06 wave beam
# 07 ice beam
# 08 energy tank
# 09 missiles

def randomize(rand_seed, location):
    SINGLE_ITEMS = ["$00", "$01", "$02", "$05", "$06"]
    ITEMS = SINGLE_ITEMS + ["$07"] * 2 + ["$08"] * 8 + ["$09"] * 21

    random.seed(rand_seed)
    random.shuffle(ITEMS)
    
    for filename, lines in ITEM_LOCATIONS.iteritems():
        full_path = location + "/" + filename + ".asm"
        with open(full_path, 'r') as file:
            filedata = file.read()

        for line in lines:
            item = ITEMS.pop()
            print "putting item {0} in {1}:{2}".format(item, filename, line)

            exp = r"({0}:\s+\.byte\ \$\w\w,\ \$\w\w,\ \$\w\w, )\$\w\w".format(line)
            regex = re.compile(exp, re.MULTILINE)
            filedata = regex.sub(r"\1{0}".format(item), filedata)

        with open(full_path, 'w') as file:
            file.write(filedata)
