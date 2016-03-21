#!/usr/bin/python3
# -*- coding: utf-8 -*-

# grupolabel.py - Print a label when a button is pushed
# Author: Stacey Sharp (github.com/ssharpjr)
# Version: 2016-03-21


import RPi.GPIO as GPIO

# TODO: Setup RTC
# TODO: Setup LCD

# Assign switch pins
sw_pos1_pin = 23
sw_pos2_pin = 24
sw_pos3_pin = 25

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(sw_pos1_pin, GPIO.IN)
GPIO.setup(sw_pos2_pin, GPIO.IN)
GPIO.setup(sw_pos3_pin, GPIO.IN)


# Assign Part Number based on switch position
if (GPIO.input(sw_pos1_pin)):
    part_number = '403319PA'
elif (GPIO.input(sw_pos2_pin)):
    part_number = 'partno2'
elif (GPIO.input(sw_pos3_pin)):
    part_number = 'partno3'
