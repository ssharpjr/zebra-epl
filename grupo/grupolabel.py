#!/usr/bin/python3
# -*- coding: utf-8 -*-

# grupolabel.py - Print a label when a button is pushed
# Author: Stacey Sharp (github.com/ssharpjr)
# Version: 2016-03-22

import os
import sys
from subprocess import check_output, STDOUT

from time import time, strftime, sleep
# import RPi.GPIO as io

# TODO: Setup RTC
# TODO: Setup LCD

# Sanity Checks
# TODO: Verify the LCD is present (query the dev)
# DONE: Verify the printer is present (lpstat -p)
# TODO: Verify the switch is present (at least one input is on)
# TODO: Verify the button is present (check the light?)

# Assign RTC pins
# rtc_clock_pin = ''
# rtc_data_pin = ''

# Assign LCD pins
# 4-6 pins here

# Assign switch pins
sw_pos1_pin = 23
sw_pos2_pin = 24
sw_pos3_pin = 25

# Setup GPIO, pull-down resistors (False)
# io.setmode(io.BCM)
# io.setup(sw_pos1_pin, io.IN, pull_up_down=io.PUD_DOWN)
# io.setup(sw_pos2_pin, io.IN, pull_up_down=io.PUD_DOWN)
# io.setup(sw_pos3_pin, io.IN, pull_up_down=io.PUD_DOWN)


def checkSwitch():
    pass


# Assign Part Number based on switch position
# def setPartNumber():
#     if (io.input(sw_pos1_pin)):
#         part_number = '403319PA'
#         part_description = 'F15 ACS LID LH BSE WRN TRI BLK'
#     elif (io.input(sw_pos2_pin)):
#         part_number = 'partno2'
#         part_description = 'partdesc2'
#     elif (io.input(sw_pos3_pin)):
#         part_number = 'partno3'
#         part_description = 'partdesc3'
#     return part_number, part_description


# Defaults for testing
part_number = '403319PA'
part_description = 'F15 ACS LID LH BSE WRN TRI BLK'


def setPrinter():
    p = check_output("lpstat -p | grep ZT230; exit 0",
                     stderr=STDOUT, shell=True)
    if not len(p) > 0:
        print("ZT230 Label Printer not found!")
        # lcdError("Error: No Printer")
        exitProgram()
    else:
        printer = 'ZT230'
    return printer


def setSerialNumberTime(part_number):
    curtime = time()
    hexstr = str(hex(int(curtime))).upper()[-8:]
    localtime = strftime('%m/%d/%Y %H:%M:%S')
    serial_number = hexstr + 'P' + part_number
    return serial_number, localtime


def printLabel():
    printer = setPrinter()  # Testing
    # printer = 'ZT230'
    serial_number, localtime = setSerialNumberTime(part_number)
    label = """N
q406
D7
S2
A20,20,0,4,1,1,N,"Part-# {pn}"
A20,50,0,2,1,1,N,"{pd}"
B90,75,0,1,1,3,50,N,"{sn}"
A90,135,0,1,1,1,N,"S/N {sn}"
A50,155,0,4,1,1,N,"{lt}"
P1
""".format(pn=part_number, pd=part_description, sn=serial_number,
             lt=localtime)

    epl_file = '/tmp/label.epl'
    with open(epl_file, 'w') as f:
        f.write(label)

    cmd = "lpr -P " + printer + " -o raw " + epl_file
    os.system('cat /tmp/label.epl')
    sleep(0.5)
    os.system(cmd)

    try:
        sleep(1.5)
        os.remove(epl_file)
    except OSError:
        pass


def main():
    # setPrinter()
    printLabel()


def exitProgram():
    print("Exiting")
    # io.cleanup()  # Clean up GPIO
    sys.exit()


if __name__ == '__main__':
    main()
