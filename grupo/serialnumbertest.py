#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import time, strftime, sleep

for i in range(10):
    curtime = time()
    localtime = strftime('%m/%d/%Y %H:%M:%S')
    dectime = int(curtime)
    hexstr = str(hex(dectime)).upper()[-8:]

    part_number = '403319PA'  # Will be dynamic later
    serial_number = hexstr + 'P' + part_number

    print(i, serial_number, localtime)
    sleep(1)
