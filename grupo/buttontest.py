#!/usr/bin/env python3

import RPi.GPIO as io

io.setmode(io.BCM)

io.setup(16, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(17, io.IN, pull_up_down=io.PUD_DOWN)


def callback(channel):
    channel = str(channel)
    print("Falling edge detected on " + channel)


io.add_event_detect(16, io.FALLING, callback=callback, bouncetime=300)

while True:

    try:
        print("Waiting on button")
        io.wait_for_edge(17, io.FALLING, bouncetime=300)
        print("Button press detected")
    except KeyboardInterrupt:
        io.cleanup()

