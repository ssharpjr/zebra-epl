#!/usr/bin/python3
# -*- coding: utf-8 -*-

# grupolabel.py - Print a label when a button is pushed
# Author: Stacey Sharp (github.com/ssharpjr)
# Version: 2016-03-22

import sys
from subprocess import check_output, STDOUT

from time import time, strftime
# import RPi.GPIO as GPIO

# TODO: Setup RTC
# TODO: Setup LCD

# Sanity Checks
# TODO: Verify the LCD is present (query the dev)
# DONE: Verify the printer is present (lpstat -p)
# TODO: Verify the switch is present (at least one input is on)
# TODO: Verify the button is present (check the light?)

# Assign switch pins
# sw_pos1_pin = 23
# sw_pos2_pin = 24
# sw_pos3_pin = 25

# Setup GPIO
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(sw_pos1_pin, GPIO.IN)
# GPIO.setup(sw_pos2_pin, GPIO.IN)
# GPIO.setup(sw_pos3_pin, GPIO.IN)


# Assign Part Number based on switch position
# if (GPIO.input(sw_pos1_pin)):
#     part_number = '403319PA'
#     part_description = 'F15 ACS LID LH BSE WRN TRI BLK'
# elif (GPIO.input(sw_pos2_pin)):
#     part_number = 'partno2'
#     part_description = 'partdesc2'
# elif (GPIO.input(sw_pos3_pin)):
#     part_number = 'partno3'
#     part_description = 'partdesc3'

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
    printer = setPrinter()
    serial_number, localtime = setSerialNumberTime(part_number)
    label = """N
q406
D7
A20,25,0,1,1,1,N,"Part-# {pn}"
A20,50,0,1,1,1,N,"{pd}"
B20,75,0,1,2,5,40,N,"{sn}"
A20,120,0,1,1,1,N,"S/N {sn}"
A20,145,0,1,1,1,N,"{lt}"
P1""".format(pn=part_number, pd=part_description, sn=serial_number,
             lt=localtime)
    print("lpr -P " + printer + " -o raw < " + label)


def main():
    setPrinter()
    printLabel()


def exitProgram():
    print("Exiting")
    sys.exit()


if __name__ == '__main__':
    main()
