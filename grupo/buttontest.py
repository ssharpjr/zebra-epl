#!/usr/bin/env python3

import RPi.GPIO as io

io.setmode(io.BCM)

# Button wired from 3V3 to Pin.
io.setup(16, io.IN, pull_up_down=io.PUD_DOWN)

# Button wired from Pin to GND.
io.setup(17, io.IN, pull_up_down=io.PUD_UP)


def callback(channel):
    channel = str(channel)
    print("Falling edge detected on " + channel)


io.add_event_detect(16, io.FALLING, callback=callback, bouncetime=300)

while True:
    try:
        print("Waiting on button")
        io.wait_for_edge(17, io.RISING, bouncetime=300)
        print("Button press detected")
    except KeyboardInterrupt:
        io.cleanup()
