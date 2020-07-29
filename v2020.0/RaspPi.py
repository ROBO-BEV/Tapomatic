#!/usr/bin/env python3
"""
__author__  = "Blaze Sanders"
__email__   = "blaze@cocotaps.com"
__company__ = "CocoTaps"
__status__  = "Development"
__date__    = "Late Updated: 2020-07-28"
__doc__     = "Class to document the internal configurations of the Raspberry Pi's"
"""

# Allow program to extract filename of the current file
import os

# Allow BASH command to be run inside Python3 code like this file
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_call

# Custom CocoTaps and Robotic Beverage Technologies Inc code
from Debug import *             # Configure datalogging parameters and debug printing control
from Actuator import *          # Modular plug and play control of motors, servos, and relays

# Import the whole gpiozero library for low level control or pins and high level Pi data
import gpiozero


class RaspPi:

    # Internal local network IP addresses and ports
    # TODO Configure with /etc/rc.local startup script ipconfig command
    # ifconfig eth0 192.168.0.69 netmask 255.255.255.0 up
    GUI_PI_IP = "192.168.0.69"
    VEND_PI_IP = "69.69.1.42"
    UDP_PORT = 5005

    # External network IP addresses
    LINODE_MYSQL_IP = "45.79.104.34"
    RAVEN_DB_IP = "TODO"

    # GPIO & POWER configuration CONSTANTS
    GPIO_MODE_0 = 0			# Default GPIO configutation that doesn't initialize any pins
    GPIO_MODE_1 = 1         # Enable all 16 GPIO pins to allow max relay control
    GPIO_MODE_2 = 2         # Enable all 4 PWM pins (2 channels) to allow max servo control
    HIGH_POWER = 1          # Use all CPU cores, high screen brightness, and all motors
    LOW_POWER = 0           # Use only one CPU core, low screen brightness, and disable main motor relay to reduce phathom drain while on battery power

    # TODO Raspberry Pi 4B refernce pin constants as defined in rc.local script at ~/usr/??? 
    NUM_PI_GPIO_PINS = 8              	    # Outputs: GPO0 to GPO3 Inputs: GPI0 to GPI3
    MAX_NUM_PI_A_OR_B_PLUS_GPIO_PINS = 40 	# Pins 1 to 40 on Raspberry Pi A+ or B+ or ZERO W
    MAX_NUM_PI_A_OR_B_GPIO_PINS = 26      	# Pins 1 to 26 on Raspberry Pi A or B
    NUM_PI_OUTPUT_PINS = 4                	# This software instance of Raspberry Pi can have up to four output pins
    NUM_PI_INPUT_PINS = 4                 	# This software instance of Raspberry Pi can have up to four input pins

    # Wire value CONTSTANTS
    # Raspberry Pi 4 Pin Layout https://pinout.xyz/pinout
    # https://www.element14.com/community/docs/DOC-92640/l/raspberry-pi-4-model-b-default-gpio-pinout-with-poe-header
    # BOARDX pin names are preferred in this code but in BCM mode GPIOX can SOMETIMES be used
    NO_PIN = -1  				#TODO This constant may not be needed :)
    NO_WIRE = 0

    # 3.3 Volts @ upto 0.050 Amps = 0.165 Watts
    # 5 Volts @ upto ~1.5 Amps (Power Adapter - Pi usgae) = 7.5 Watts https://pinout.xyz/pinout/pin2_5v_power
	# https://pinout.xyz/pinout/pin1_3v3_power
	# https://pinout.xyz/pinout/pin2_5v_power
    VCC_3_3V = 1
    VCC_3_3V_NAME = 'BOARD1'
    VCC_5V = 2
    VCC_5V_NAME = 'BOARD2'
    GND = 'BOARD6&9&14&20&25&30&34&39'	# Digital Ground (0 Volts) https://pinout.xyz/pinout/ground

    # Both I2C lines have fixed, 1.8 kohms pull-ups to 3.3v
    # https://pinout.xyz/pinout/pin3_gpio2
    # https://pinout.xyz/pinout/pin5_gpio3
    I2C_SDA0 = 3
    I2C_SDA1_NAME  = 'BOARD3'
    I2C_SCL0 = 5
    I2C_SCL1_NAME = 'BOARD5'

    # Pulse Width Modulation
    # https://pinout.xyz/pinout/pin12_gpio18
    # https://pinout.xyz/pinout/pin32_gpio12
    # https://pinout.xyz/pinout/pin33_gpio13
    # https://pinout.xyz/pinout/pin35_gpio19
    PWM0_0 = 18
    PWM0_0_BCM_NAME = 'GPIO18'
    PWM0_0_NAME = 'BOARD12'
    PWM0_1 = 24
    PWM0_1_BCM_NAME = 'GPIO24'
    PWM0_1_NAME = 'BOARD18'

    PWM1_0 = 13
    PWM1_0_BCM_NAME = 'GPIO13'
    PWM1_0_NAME = 'BOARD33'
    PWM1_1 = 19
    PWM1_1_BCM_NAME = 'GPIO19'
    PWM1_1_NAME = 'BOARD35'

    # UART recieve pin / Serial Port
    # https://pinout.xyz/pinout/pin10_gpio15
    TXD = 8
    TXD_NAME = 'BOARD8'
    TXD_BCM_NAME = 'GPIO14'
    RXD = 10
    RXD_NAME = 'BOARD10'
    RXD_BCM_NAME = 'GPIO15'

    # General Purpose Input / Output (GPIO) pins that work in default mode
    # Format for following pin "BCM mode pin name= BOARD mode pin name":
    BOARD7  = 'GPIO4'
    BOARD11 = 'GPIO17'
    BOARD13 = 'GPIO27'
    BOARD15 = 'GPIO22'
    BOARD16 = 'GPIO23'
    BOARD18 = 'GPIO24'
    BOARD22 = 'GPIO25'
    BOARD29 = 'GPIO5'
    BOARD31 = 'GPIO6'
    BOARD32 = 'GPIO1'
    BOARD33 = 'GPIO13'
    BOARD35 = 'GPIO19'
    BOARD36 = 'GPIO16'
    BOARD37 = 'GPIO26'
    BOARD38 = 'GPIO20'
    BOARD40 = 'GPIO21'

    # Global class variable
    pinUsageList = [False] * 40	# Make List filled with 40 False variables


    def __init__(self, gpioMode, cpuPowerMode):
        """
        Create Raspberry Pi 4 GPIO and power configuration

        Key arguments:
        self --
        gpioModes --Interger CONSTANT, that
        cpuPowerMode -- Interger CONSTANT, that defines CPU computation power

        Return value:
        New RaspPi() object
        """

        currentProgramFilename = os.path.basename(__file__)
        self.DebugObject = Debug(True, currentProgramFilename)

        self.gpioMode = gpioMode
        self.cpuPowerMode = cpuPowerMode
        self.PiInfo = gpiozero.pi_info()

        if(gpioMode == RaspPi.GPIO_MODE_0):
        	# DO NOTHING BY SLEEPING 10 ms
        	sleep(0.010)
        elif(gpioMode == RaspPi.GPIO_MODE_1):
        	# Define each of the pins to a specific type
         	gpiozero.OutputDevice(RaspPi.BOARD7)
         	gpiozero.OutputDevice(RaspPi.BOARD11)
         	gpiozero.OutputDevice(RaspPi.BOARD13)
         	gpiozero.OutputDevice(RaspPi.BOARD15)
         	gpiozero.OutputDevice(RaspPi.BOARD16)
         	gpiozero.OutputDevice(RaspPi.BOARD18)
         	gpiozero.OutputDevice(RaspPi.BOARD22)
         	gpiozero.OutputDevice(RaspPi.BOARD29)
         	gpiozero.OutputDevice(RaspPi.BOARD31)
         	gpiozero.OutputDevice(RaspPi.BOARD32)
         	gpiozero.OutputDevice(RaspPi.BOARD33)
         	gpiozero.OutputDevice(RaspPi.BOARD35)
         	gpiozero.OutputDevice(RaspPi.BOARD36)
         	gpiozero.OutputDevice(RaspPi.BOARD37)
         	gpiozero.OutputDevice(RaspPi.BOARD38)
         	gpiozero.OutputDevice(RaspPi.BOARD40)

        elif(gpioMode == RaspPi.GPIO_MODE_2):
         	gpiozero.PWMOutputDevice(RaspPi.PWM0_0)
         	gpiozero.PWMOutputDevice(RaspPi.PWM0_1)
         	gpiozero.PWMOutputDevice(RaspPi.PWM1_0)
         	gpiozero.PWMOutputDevice(RaspPi.PWM1_1)

        else:
            self.DebugObject.Dprint("ERROR: Invalid GPIO mode, see RaspPi.py CONSTANTS")

        if(cpuPowerMode == RaspPi.HIGH_POWER):
        	check_call("xrandr --output LVDS --brightness 0.90", shell=True)
        	print("TODO RaspPi.py cpuPowerMode == RaspPi.HIGH_POWER")
        elif(cpuPowerMode == RaspPi.LOW_POWER):
        	check_call("xrandr --output LVDS --brightness 0.20", shell=True)
        	pin = [RaspPi.BOARD7]
        	mainPowerRelay = Actuator('R', 0, pin, "Main 120VAC Tapomatic Relay: P/N SRD-05VDC-SL-C?", Actuator.CW) #mainPowerRelay = gpiozero.OutputDevice(RaspPi.BOARD7)
        else:
        	self.DebugObject.Dprint("ERROR: Invalid CPU power mode, see RaspPi.py CONSTANTS")


    def DevPinConfigError(TempDebugObject):
        """
        Inform programmer that control of Raspberry Pi pins from a Mac or PC is not possible without advance settings

        Key arguments:
        TempDebugObject -- Debug() Object from python Class where error occured

        Return value:
        NONE
        """

        TempDebugObject.Dprint("WARNING - You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")
        TempDebugObject.Dprint("Try using Mock pin fatory setting https://gpiozero.readthedocs.io/en/stable/api_pins.html#mock-pins")
        TempDebugObject.Dprint("Or Remote GPIO setup https://gpiozero.readthedocs.io/en/stable/remote_gpio.html")


    def isPinFree(self, pinNum):
        """
        Determine if pin has been used in another part of the program. Helps developers from accidentally using pin for two different functions 

        Key arguments:
        pinNum -- GPIO pin to change usage state of

        Return value:
        state -- Boolean, describing is pin is in use by the program for a Sensor() or Actuator() or TODO object
        """

        if(self.DebugObject.DEBUG_MODE == True):
        	state = pinUsageList[pinNum]

        return state


    def reservePin(pinNum):
        """
        Reserve the use of a pin by part of the program

        Key arguments:
        pinNum -- GPIO pin to change usage state of

        Return value:
        pinUsageList -- ByValue List with updates
        """

		#TODO Reverse lookup of GPIO4 should return 7 from BOARD7
		#Device.pin_factory = ??
        #gpiozero.Factory.reserve_pins(pinNum)

        return RaspPi.pinUsageList[pinNum]


    def releasePin(pinNum):
        """
        Release use of a pin for use by other parts of program

        Key arguments:
        pinNum -- GPIO pin to change usage state of

        Return value:
        NONE
        """

		#TODO Reverse lookup of GPIO4 should return 7 from BOARD7
        pinUsageList[pinNum] = False


    def UnitTest():
        """

        """
        print("START RaspPi.py UnitTest()")

        testObject0 = RaspPi(RaspPi.GPIO_MODE_1, RaspPi.HIGH_POWER)
        testObject1 = RaspPi(RaspPi.GPIO_MODE_1, RaspPi.LOW_POWER)
        testObject2 = RaspPi(RaspPi.GPIO_MODE_2, RaspPi.HIGH_POWER)
        testObject3 = RaspPi(RaspPi.GPIO_MODE_2, RaspPi.LOW_POWER)

        print("END RaspPi.py UnitTest()")

        return 0


if __name__ == "__main__":

#    try:
	RaspPi.UnitTest()

#   except NameError:

	currentProgramFilename = os.path.basename(__file__)
	NameDebugObject = Debug(True, currentProgramFilename)
#   	NameDebugObject.Dprint("Try fail in __main__ of " + str(currentProgramFilename))

	print("END RaspPi.py __main__")
