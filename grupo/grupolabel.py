#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import check_output, STDOUT

from time import time, strftime, sleep
import RPi.GPIO as io

# [X]: Setup RTC
# [ ]: Setup LCD

# Sanity Checks
# [ ]: Verify the RTC is present (query the dev)
# [ ]: Verify the LCD is present (query the dev)
# [X]: Verify the printer is present (lpstat -p)
# [X]: Verify the switch is present (at least one input is on)
# [ ]: Verify the button is present (check the light?)

# Assign LCD pins
# 4-6 pins here

# Assign button and switch pins
btn_pin = 16
sw_pos1_pin = 23
sw_pos2_pin = 24
sw_pos3_pin = 25

# Setup GPIO, pull-down resistors from 3V3 (False by default)
io.setmode(io.BCM)
io.setup(btn_pin, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(sw_pos1_pin, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(sw_pos2_pin, io.IN, pull_up_down=io.PUD_DOWN)
io.setup(sw_pos3_pin, io.IN, pull_up_down=io.PUD_DOWN)


def checkSwitch():
    # Check if switch is connected.
    # At least one position should True.
    sw = False
    if not (io.input(sw_pos1_pin)):
        sw = True
    elif not (io.input(sw_pos2_pin)):
        sw = True
    elif not (io.input(sw_pos3_pin)):
        sw = True

    if sw:
        print("Switch detected")
    else:
        print("Switch not detected!")
        exit_program()


def setPos():
    # Get switch position
    pos = ''
    if (io.input(sw_pos1_pin) and io.input(sw_pos2_pin)):
        pos = 1
    elif (io.input(sw_pos3_pin)):
        pos = 3
    elif (io.input(sw_pos2_pin)):
        pos = 2
    print("Pos: %s" % pos)
    return pos


def sw_callback():
    setPartNumber()


def setPartNumber():
    # Get current switch position
    pos = setPos()

    # Assign Part Number based on switch position
    lh_pn = ''
    lh_pd = ''
    rh_pn = ''
    rh_pd = ''

    #############################
    # Defaults for testing
    lh_pn = '24680LH'
    lh_pd = 'LH PART NUMBER'
    rh_pn = '24680RH'
    rh_pd = 'RH PART NUMBER'
    #############################

    if pos == 1:
        lh_pn = '12345LH'
        lh_pd = 'LH PART NUMBER 1'
        rh_pn = '12345RH'
        rh_pd = 'RH PART NUMBER 1'
    elif pos == 2:
        lh_pn = '23456LH'
        lh_pd = 'LH PART NUMBER 2'
        rh_pn = '23456RH'
        rh_pd = 'RH PART NUMBER 2'
    elif pos == 3:
        lh_pn = '34567LH'
        lh_pd = 'LH PART NUMBER 3'
        rh_pn = '34567RH'
        rh_pd = 'RH PART NUMBER 3'

    print("Selected Parts:")
    print(lh_pn, lh_pd)
    print(rh_pn, rh_pd)
    return lh_pn, lh_pd, rh_pn, rh_pd


def setPrinter():
    lh_printer = check_output("lpstat -p | grep ZT230-LH; exit 0",
                              stderr=STDOUT, shell=True)
    if not len(lh_printer) > 0:
        print("ZT230-LH Label Printer not found!")
        # lcdError("Err: Left Hand\n Printer Missing")
        exit_program()
    else:
        lh_printer = 'ZT230-LH'

    rh_printer = check_output("lpstat -p | grep ZT230-RH; exit 0",
                              stderr=STDOUT, shell=True)
    if not len(rh_printer) > 0:
        print("ZT230-RH Label Printer not found!")
        # lcdError("Err: Right Hand\n Printer Missing")
        exit_program()
    else:
        rh_printer = 'ZT230-RH'

    print("Printers:")
    print(lh_printer, rh_printer)
    return lh_printer, rh_printer


def setSerialNumberTime(pn):
    curtime = time()
    hexstr = str(hex(int(curtime))).upper()[-8:]
    localtime = strftime('%m/%d/%Y %H:%M:%S')
    sn = hexstr + 'P' + pn
    return sn, localtime


def printLabel():
    lh_printer, rh_printer = setPrinter()
    lh_pn, lh_pd, rh_pn, rh_pd = setPartNumber()
    lh_sn, localtime = setSerialNumberTime(lh_pn)
    rh_sn, localtime = setSerialNumberTime(rh_pn)

    # Create LH label
    # TODO: Refactor: DRY?
    lh_label = """N
q406
D7
S2
A20,20,0,4,1,1,N,"Part-# {pn}"
A20,50,0,2,1,1,N,"{pd}"
B90,75,0,1,1,3,60,N,"{sn}"
A90,140,0,1,1,1,N,"S/N {sn}"
A50,155,0,4,1,1,N,"{lt}"
P1
""".format(pn=lh_pn, pd=lh_pd, sn=lh_sn,
           lt=localtime)

    lh_epl_file = '/tmp/lh_label.epl'
    with open(lh_epl_file, 'w') as f:
        f.write(lh_label)

    # Create RH label
    rh_label = """N
q406
D5
S2
A20,20,0,4,1,1,N,"Part-# {pn}"
A20,50,0,2,1,1,N,"{pd}"
B90,75,0,1,1,3,60,N,"{sn}"
A90,140,0,1,1,1,N,"S/N {sn}"
A50,155,0,4,1,1,N,"{lt}"
P1
""".format(pn=rh_pn, pd=rh_pd, sn=rh_sn,
           lt=localtime)

    rh_epl_file = '/tmp/rh_label.epl'
    with open(rh_epl_file, 'w') as f:
        f.write(rh_label)

    # Print labels
    lh_cmd = "lpr -P " + lh_printer + " -o raw " + lh_epl_file
    rh_cmd = "lpr -P " + rh_printer + " -o raw " + rh_epl_file
    os.system(lh_cmd)
    os.system(rh_cmd)

    try:
        sleep(1)
        os.remove(lh_epl_file)
        os.remove(rh_epl_file)
    except OSError:
        pass


def exit_program():
    print("Exiting")
    io.cleanup()
    sys.exit()


def main():
    # Perform checks on startup
    checkSwitch()
    setPrinter()
    setPartNumber()

    # Create switch events
    io.add_event_detect(sw_pos1_pin, io.BOTH,
                        callback=sw_callback,
                        bouncetime=50)
    io.add_event_detect(sw_pos2_pin, io.BOTH,
                        callback=sw_callback,
                        bouncetime=50)
    io.add_event_detect(sw_pos3_pin, io.BOTH,
                        callback=sw_callback,
                        bouncetime=50)

    print("Started")
    while True:
        try:
            print("Waiting for button")
            io.wait_for_edge(btn_pin, io.FALLING, bouncetime=300)
            print("Printing")
            printLabel()
        except KeyboardInterrupt:
            exit_program()


if __name__ == '__main__':
    main()
