#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3 Position ON-ON-ON DPDT Switch.
# Switch poles 1, 3, and 5 are on in position 1.

import RPi.GPIO as io


# Switch Pins
sw1 = 23
sw2 = 24
sw3 = 25

io.setmode(io.BCM)
io.setup(sw1, io.IN, pull_up_down=io.PUD_UP)
io.setup(sw2, io.IN, pull_up_down=io.PUD_UP)
io.setup(sw3, io.IN, pull_up_down=io.PUD_UP)


while True:

    # Get switch state
    if sw1 and sw3:
        pos = 1
    elif sw2:
        pos = 2
    elif sw3:
        pos = 3

    print("The switch is in position: " + str(pos))
