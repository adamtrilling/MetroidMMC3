from os import mkdir

import Ophis.Main
import os
import random
import re
import shutil


def generate(seed):
    # assemble non-randomized files if necessary
    if (os.path.isfile("work/Defines.asm") is not True):
        shutil.copy("src/asm/code/Defines.asm", "work")
    if (os.path.isfile("work/0.bin") is not True):
        Ophis.Main.run_ophis(["-o", "work/0.bin", "src/asm/PRG/0.asm"])
    if (os.path.isfile("work/3.bin") is not True):
        Ophis.Main.run_ophis(["-o", "work/3.bin", "src/asm/PRG/3.asm"])
    if (os.path.isfile("work/6.bin") is not True):
        Ophis.Main.run_ophis(["-o", "work/6.bin", "src/asm/PRG/6.asm"])
    if (os.path.isfile("work/7.bin") is not True):
        Ophis.Main.run_ophis(["-o", "work/7.bin", "src/asm/PRG/7.asm"])

    randomize(seed)

    # assemble PRGs
    prg = open("work/1-{0}.asm".format(seed), 'w')
    prg.write(".require \"Brinstar-{0}.asm\"  ; Brinstar, pg 1\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/1-{0}.bin".format(seed), "work/1-{0}.asm".format(seed)])

    prg = open("work/2-{0}.asm".format(seed), 'w')
    prg.write(".require \"Norfair-{0}.asm\" ; pg 2\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/2-{0}.bin".format(seed), "work/2-{0}.asm".format(seed)])

    prg = open("work/4-{0}.asm".format(seed), 'w')
    prg.write(".require \"Kraid-{0}.asm\" ; pg 4\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/4-{0}.bin".format(seed), "work/4-{0}.asm".format(seed)])

    prg = open("work/5-{0}.asm".format(seed), 'w')
    prg.write(".require \"Ridley-{0}.asm\" ; pg 5\n".format(seed))
    prg.close()
    Ophis.Main.run_ophis(["-o", "work/5-{0}.bin".format(seed), "work/5-{0}.asm".format(seed)])

    # generate and execute makefile
    output_file = "work/metroid-{0}.nes".format(seed)
    makefile = open("work/make-{0}.asm".format(seed), 'w')
    makefile.write(".outfile \"{0}\"\n".format(output_file))
    makefile.write(".include \"../src/asm/code/header.asm\"\n")
    makefile.write(".incbin \"0.bin\"\n")
    makefile.write(".incbin \"1-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"2-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"3.bin\"\n")
    makefile.write(".incbin \"4-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"5-{0}.bin\"\n".format(seed))
    makefile.write(".incbin \"6.bin\"\n")
    makefile.write(".incbin \"7.bin\"\n")
    makefile.close()

    Ophis.Main.run_ophis(["work/make-{0}.asm".format(seed)])

    return output_file


# randomizer constants
ITEM_LOCATIONS = {
    "Brinstar": ["LA3DE", "LA3E7", "LA3ED", "LA3F6", "LA3FC", "LA409", "LA412",
                 "LA41F", "LA433"],
    "Kraid": ["LA27F", "LA286", "LA28F", "LA298", "LA2A1", "LA2B1"],
    "Norfair": ["LA2E2", "LA2F0", "LA2F6", "LA2FC", "LA305", "LA316", "LA326",
                "LA32C", "LA33E", "LA35D", "LA370", "LA383", "LA38C", "LA39A",
                "LA3A0"],
    "Ridley": ["LA21E", "LA227", "LA230", "LA239"]
}

ITEM_TYPES = {
    "$00": "bombs", "$01": "high jump", "$02": "long beam",
    "$04": "morph ball", "$05": "varia", "$06": "wave beam",
    "$07": "ice beam", "$08": "energy tank", "$09": "missiles"
}


def randomize(seed):
    SINGLE_ITEMS = ["$00", "$01", "$02", "$05", "$06"]
    ITEMS = SINGLE_ITEMS + ["$07"] * 2 + ["$08"] * 8 + ["$09"] * 21

    random.seed(int(seed, 16))
    random.shuffle(ITEMS)

    for filename, lines in ITEM_LOCATIONS.iteritems():
        input_path = "src/asm/code/{0}.asm".format(filename)
        output_path = "work/{0}-{1}.asm".format(filename, seed)
        with open(input_path, 'r') as file:
            filedata = file.read()

        for line in lines:
            item = ITEMS.pop()
            print "putting {0} in {1}:{2}".format(ITEM_TYPES[item], filename, line)

            exp = r"({0}:\s+\.byte\ \$\w\w,\ \$\w\w,\ \$\w\w, )\$\w\w".format(line)
            regex = re.compile(exp, re.MULTILINE)
            filedata = regex.sub(r"\1{0}".format(item), filedata)

        with open(output_path, 'w') as file:
            file.write(filedata)
