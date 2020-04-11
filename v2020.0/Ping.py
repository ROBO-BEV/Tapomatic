#!/usr/bin/env python

__author__ =  “Blaze Sanders”
__email__ =   “blaze.d.a.sanders@gmail.com”
__company__ = “Robotic Beverage Technologies Inc”
__status__ =  “Development”
__date__ =    “Late Updated: 2020-04-10”
__doc__ =     “Class to operate up to 8 PING LASER Or Ultrasonic rangefinders from Parallax Inc”

# Useful documentation:
# https://gpiozero.readthedocs.io/en/stable/installing.html
# https://gpiozero.readthedocs.io/en/stable/api_output.html
# https://gpiozero.readthedocs.io/en/stable/api_input.html

import Serial 

# Allow program to pause operation and create local timestamps
from time import sleep

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

try:
	# The following imports do NOT work in a Mac oor PC dev enviroment (but are needed for Pi product) 

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
	DebugObject = Debug(True)
	Debug.Dprint(DebugObject, “WARNING: You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.”)


def GetMillimeters(pin):
    """
    Measure distance to closest object in direct line of sight for PING LASER rangefinder
    
    @pin - GPIO pin PING sensor is connected to
    
    Return range - Distance in mm to closest object 
    """
    
    return range

 
def GetInches(pin):
    """
    Calculate distance to closet object using Get Millimeters() function above. Metric FTW!
    
    Return range - Distance is gross imperial units to closest object
    """
    
    range = 25.4 * millimeters(pin) 
    
    return range