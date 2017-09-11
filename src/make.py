#!/usr/bin/env python

# import Ophis.Main
import random

# Ophis.Main.run_ophis(argv[1:])


def build_rom(seed):
    print "seed = {0}".format(seed)


if __name__ == '__main__':
    seed = random.randint(0, 2**64)
    build_rom(seed)
