#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3 Position ON-ON-ON DPDT Switch.
# Switch poles 1, 3, and 5 are on in position 1.

import sys
import RPi.GPIO as io


# Switch Pins
sw1 = 23
sw2 = 24
sw3 = 25

io.setmode(io.BCM)
io.setup(sw1, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(sw2, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(sw3, io.IN, pull_up_down=io.PUD_DOWN)


while True:

    # Get switch state
    pos = ''
    if (io.input(sw1) and io.input(sw2)):
        pos = 1
    elif (io.input(sw3)):
        pos = 3
    elif (io.input(sw2)):
        pos = 2

    if not pos:
        print("Switch not detected")
        io.cleanup()
        sys.exit()
    else:
        print("pos: " + str(pos))

