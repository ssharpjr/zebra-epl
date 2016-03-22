#!/usr/bin/python3
# -*- coding: utf-8 -*-

# grupolabel.py - Print a label when a button is pushed
# Author: Stacey Sharp (github.com/ssharpjr)
# Version: 2016-03-22

from time import time, strftime
# import RPi.GPIO as GPIO

# TODO: Setup RTC
# TODO: Setup LCD

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


def setSerialNumberTime(part_number):
    _part_number = part_number
    curtime = time()
    localtime = strftime('%m/%d/%Y %H:%M:%S')
    dectime = int(curtime)
    hexstr = str(hex(dectime)).upper()[-8:]

    part_number = '403319PA'  # Will be dynamic later
    serial_number = hexstr + 'P' + _part_number
    print(serial_number)
    print(localtime)


def printLabel(part_number, part_description, serial_number, localtime):
    print(part_description)
    print(serial_number)
    print(localtime)

if __name__ == '__main__':
    print(part_number)
    print(part_description)
    setSerialNumberTime(part_number)
