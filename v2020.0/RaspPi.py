#!/usr/bin/env python

"""
__author__  = "Blaze Sanders"
__email__   = "blaze@cocotaps.mvp"
__company__ = "CocoTaps"
__status__  = "Development"
__date__    = "Late Updated: 2020-05-08"
__doc__     = "Class to document the configurations of the multiple Raspberry Pi 4 inside the Tampomatic"
"""

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

class RaspPi:
    # Internal local network IP addresses and ports
    GUI_PI_IP = "69.69.1.69"
    VEND_PI_IP = "69.69.1.42"
    UDP_PORT = 5005

    # External network IP addresses
    LINODE_MYSQL_IP = "45.79.104.34"
    RAVEN_DB_IP = "TODO"

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

    # 3.3 Volts @ upto 0.050 Amps = 0.165 Watts https://pinout.xyz/pinout/pin1_3v3_power
    # 5 Volts @ upto ~1.5 Amps (Power Adapter - Pi usgae) = 7.5 Watts https://pinout.xyz/pinout/pin2_5v_power
    VCC_3_3V = 1
    VCC_3_3V_NAME = "BOARD1"     		
    VCC_5V = 2
    VCC_5V_NAME = "BOARD2"        		
    GND = "BOARD6&9&14&20&25&30&34&39"	# Digital Ground (0 Volts) https://pinout.xyz/pinout/ground

    # Both I2C lines have fixed, 1.8 kohms pull-ups to 3.3v 
    # https://pinout.xyz/pinout/pin3_gpio2
    # https://pinout.xyz/pinout/pin5_gpio3
    I2C_SDA0 = 3					
    I2C_SDA1_NAME  = "BOARD3"		
    I2C_SCL0 = 5
    I2C_SCL1_NAME = "BOARD5"	

    # Pulse Width Modulation https://pinout.xyz/pinout/pin12_gpio18 
    PWM0 = 12
    PWM0_NAME = "BOARD12"				
    PWM0_BCM_NAME = "GPIO18"

    # UART recieve pin / Serial Port https://pinout.xyz/pinout/pin10_gpio15					
    TXD = 8
    TXD_NAME = "BOARD8" 				
    TXD_BCM_NAME = "GPIO14"
    RXD = 10	
    RXD_NAME = "BOARD10"
    RXD_BCM_NAME = "GPIO15"

    # General Purpose Input / Output (GPIO) pins that work in default mode 
    # Format for following pin "BCM mode pin name= BOARD mode pin name":
    BOARD7 = "GPIO4"
    BOARD11 = "GPIO17"
    BOARD13 = "GPIO27"
    BOARD15 = "GPIO22"  
    BOARD16 = "GPIO23"
    BOARD18 = "GPIO24"
    BOARD22 = "GPIO25"
    BOARD29 = "GPIO5"    
    BOARD31 = "GPIO6"
    BOARD32 = "GPIO12"
    BOARD33 = "GPIO13"
    BOARD35 = "GPIO19"
    BOARD36 = "GPIO16"
    BOARD37 = "GPIO26"
    BOARD38 = "GPIO20"
    BOARD40 = "GPIO21"

class Raspi:
    
    def __init__(self):
        self.DebugObject = Debug(True)


#    ROTATAIIONAL_MOTOR_
#    Z_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[1]
#    X_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[2]
#    Y_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[3]

#    Z1_LINEAR_LIFT_MOTOR = actuatorObjects[4]
#    Z2_LINEAR_LIFT_MOTOR = actuatorObjects[5]

#    Y1_LINEAR_CUT_MOTOR = actuatorObjects[6]
#    Y2_LINEAR_CUT_MOTOR = actuatorObjects[7]
#    X1_LINEAR_KNIFE_POSITION_MOTOR = actuatorObjects[8]

#    Y1_LINEAR_COVER_MOTOR = actuatorObjects[9]
#    Y2_LINEAR_COVER_MOTOR = actuatorObjects[10]

#    ROTATIONAL_DISK_STEPPER_MOTOR = actuatorObjects[19]
