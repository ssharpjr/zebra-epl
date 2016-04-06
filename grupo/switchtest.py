#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 3 Position ON-ON-ON DPDT Switch.
# Position 1: Poles 5/6 AND 1/3 are closed.
# Position 2: Poles 1/3 AND 4/6 are closed.
# Position 3: Poles 2/3 AND 4/6 are closed.
# Pole 4 is not used.


import RPi.GPIO as io


# Switch Pins
sw1 = 23
sw2 = 24
sw3 = 25

io.setmode(io.BCM)
io.setup(sw1, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(sw2, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(sw3, io.IN, pull_up_down=io.PUD_DOWN)


def setPos():
    # Get switch position
    pos = ''
    if (io.input(sw1) and io.input(sw2)):
        pos = 1
    elif (io.input(sw3)):
        pos = 3
    elif (io.input(sw2)):
        pos = 2
    print("Pos: %s" % pos)
    return pos


def my_callback(channel):
    setPos()


pos = setPos()
print("Pos: %s" % pos)


io.add_event_detect(sw1, io.BOTH, callback=my_callback, bouncetime=50)
io.add_event_detect(sw2, io.BOTH, callback=my_callback, bouncetime=50)
io.add_event_detect(sw3, io.BOTH, callback=my_callback, bouncetime=50)


while True:
    pass
