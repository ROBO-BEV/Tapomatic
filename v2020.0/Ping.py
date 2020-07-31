#!/usr/bin/env python
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-07-29"
__doc__     = "Class to operate up to 8 PING LASER Or Ultrasonic rangefinders from Parallax Inc"
"""

# Useful documentation:
# https://gpiozero.readthedocs.io/en/stable/installing.html
# https://gpiozero.readthedocs.io/en/stable/api_output.html
# https://gpiozero.readthedocs.io/en/stable/api_input.html

# Allow program to pause operation and create local timestamps
import time

# Allow program to extract filename of the current file
import os

# Custom CocoTaps and Robotic Beverage Technologies Inc code
from Debug import *             # Configure datalogging parameters and debug printing control
from RaspPi import *            # Contains usefull GPIO pin CONSTANTS and setup configurations

# PING type Global CONSTANTS
LASER = 0
ULTRASONIC = 1

# PING type Global Variable
pingType = -1

try:
	# The following imports do NOT work in a Mac oor PC dev enviroment (but are needed for Pi product) 

	# Allow control of low level General Purpose Input/Output pins on Rapsberry Pi
	import RPi.GPIO as GPIO

	# Allow asynchrous event to occur in parallel and pause threads as needed
	# Might work on Windows in the future https://github.com/vibora-io/vibora/issues/126
	from signal import pause

	# Allow control of input and out pins
	from gpiozero import OutputDevice, InputDevice

	# Check status of network / new device IP addresses and Pi hardware
	from gpiozero import PingServer, pi_info

	# Useful pin status tools and math tools
	from gpiozero.tools import all_values, negated, sin_values

	# Useful for controlling devices based on date and time
	from gpiozero import TimeOfDay

except ImportError:
	currentProgramFilename = os.path.basename(__file__)
	TempDebugObject = Debug(True, "Try/Catch ImportError in " + currentProgramFilename)
	TempDebugObject.Dprint(DebugObject, "WARNING: You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")


def GetMillimeters(pin):
    """
    Get distance to closest object in direct line of sight for PING LASER rangefinder

    Key arguments:
    pin -- GPIO pin PING sensor is connected to

    Return value: range -- Distance in mm to closest object
    """

    range = 10 * distance(pin)

    return range


def GetInches(pin):
    """
    Calculate distance to closet object using Get Millimeters() function above. Metric FTW!

    Key arguments:
    pin -- GPIO pin PING sensor is connected to

    Return value:
    range - Distance in gross imperial units to closest object
    """

    range = 25.4 * GetMillimeters(pin)

    return range


def distance(pin):
    """
    Measure distance to the closest object using the time of flight of a LASER or ULTRASONIC pulse 

    Key arguments:
    pin -- GPIO pin PING sensor is connected to
    pingType -- Either LASER or ULTRASONIC

    Return value:
    distance --
    """

    # Set GPIO Pin for PING sensors (Only one of three axis is powered at a time to reduce LASER and ultrasonic cross talk)
    GPIO_TRIGGER = pin
    GPIO_ECHO = pin

    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)

    # set Trigger to HIGH
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s) or TODO light speed (30000000000 cm/s)
    # and divide by 2, because there and back
    if(pingType == LASER):
        distance = (TimeElapsed * 30000000000) / 2
    else:
        distance = (TimeElapsed * 34300) / 2

    return distance


    def SetPingType(type):
        pingType = type


    def GetPingType():
        return pingType


if __name__ == '__main__':
    try:
        while True:
            dist = distance(4) #BOARD7 = GPIO4
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
