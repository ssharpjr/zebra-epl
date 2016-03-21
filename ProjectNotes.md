## Project:  Grupo Part Label Project

## Purpose:
Print a 1" X 2" barcode label with the press of a button.

## Solution:
A mini-computer connected to a label printer that is capable to producing a label when a button is pressed.

## Steps:
- Select the part with a 3-position switch.
- Press a button to print a label for the select part.

## Thought Process:
There are 2 workstations each making 3 parts (colors) for a total of 6 parts (3 left, 3 right).
The switch position determines the part number that will be printed.
A display will show what part is currently selected and the current date and time.
When the button is pushed, the part number, date and time, and a serial number are printed on a 1" X 2" label.
The serial number is made of 3 variables:
- The Epoch time (integer) in hexadecimal, truncated to the last 8 digits.
- The Letter "P" as a separator.
- The Part Number.

## Label Contents:
- Part-# 403319PA (3 numbers hardcoded to the switch)
- Part Description (3 descriptions hardcoded to the switch)
- Serial Number C128 Barcode
- Printed Serial Number
- Date and Time (MM/DD/YYYY HH:MM:SS)

## Computer Functionality:
- Send Print Commands
- Display Feedback to User
    + Currently Selected Part
    + Current Date and Time
    + Color Background to Determine Device/Process Status
        * Green - Okay to proceed
        * Red - Display Error
        * Yellow - System Issue?
- Log Data
    + Number of Labels Printed per Part
    + Date/Time of Printed Part


## Hardware Parts Lists and Notes:
(*2 of everything.  2 workstations*)
- Zebra ZT230 203dpi Label Printer (ribbon, 1x2 yellow labels)
- Raspberry Pi B+ or 2
- 8GB Micro SD Card
- USB Wireless Adapter (for remote access)
- Real Time Clock (RTC) Circuit
- LCD Display (16x2 or 20x4 plus the MCP I2C controller)?
- 3-Position Cam Switch
- 60mm White Backlit Button
- Enclosure (prefab or custom)?
- USB A-B Cable for Printer
- Power Cable for RPI (USB vs Barrel)?
- Button Cable (Stereo Plug)?
- Cam Switch Cable (Stereo Plug)?

## Software Logic and Notes:
*Language: Python 3*

**System is Idle:**
- Static variables are assigned to the switch position inputs.  The selected input's variable is assigned to the current part/desc variables.
- Program waits for the button to be pressed.

**Button is Pressed:**
- The date/time is captured from the RTC circuit and assigned to the current time variable.
- The current time variable is converted to hexadecimal, parsed to 8-digits and assigned to a hexstr variable.
- The hexstr and part_number variables are combined into the serial_number variable.
- The Zebra EPL code is generated and the variables are added.  This is saved to an EPL file.
- The EPL file is sent to the printer directly using 'lpr' commands (lpr -P <PRINTER> -o raw <EPL_FILENAME>).
- The EPL file and the current variables are deleted.
- The program pauses 1 second.
- Program returns to Idle status.

## EPL Programming Notes
##### EPL commands (*case sensitive*)
**N** - New label (Delete buffer)
**q406** - Sets label width in dots (203 dpi X 2 inch label = 406 dots)
**D7** - Density (print darkness 1-15)
**A20,25,0,1,1,N,"Part-# 403319PA"** - A = Text, HPos, VPos, Rot, Font, HX, VX, Rev?, DATA
**B20,75,0,1,2,5,40,N,"12345678P403319PA"** - B = Barcode, HPos, VPos, Rot, BC Type, NBar Width, WBar Width, PHRC?, DATA
P1 = P = Print, Number of labels

# RPI Packages and Python Modules
sudo apt-get install build-essential python-dev python-smbus python-pip git
sudo pip install RPi.GPIO
git clone https://github.com/adafruit/Adafruit_Python_charLCD.git
sudo python setup.py install

## RPI GPIO Pins Used
- LCD = 6 pins
- Button = 1 pin
- Cam Switch = 3 pins

## Unanswered Questions:
- Where will the device be mounted?
- Where will the printer be placed?
- Where will the button be mounted?
- Where will the switch be mounted?
