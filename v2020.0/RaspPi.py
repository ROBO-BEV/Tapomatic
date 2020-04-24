#!/usr/bin/env python
"""
__author__  = "Blaze Sanders"
__email__   = "blaze@cocotaps.com"
__company__ = "CocoTaps"
__status__  = "Development"
__date__    = "Late Updated: 2020-04-23"
__doc__     = "Class to document the configurations of the multiple Raspberry Pi 4 inside the Tampomatic"
"""
# Internal local network IP addresses and ports
GUI_PI_IP = "127.168.1.69"
VEND_PI_IP = "127.168.1.42"
UDP_PORT = 5005

# External network IP addresses
LINODE_MYSQL_IP = "45.79.104.34"
RAVEN_DB_IP = "TODO"

# Raspberry Pi 4B refernce pin constants as defined in ???rc.local script???
NUM_PI_GPIO_PINS = 8              		# Outputs: GPO0 to GPO3 Inputs: GPI0 to GPI3
MAX_NUM_PI_A_OR_B_PLUS_GPIO_PINS = 40 	# Pins 1 to 40 on Raspberry Pi A+ or B+ or ZERO W
MAX_NUM_PI_A_OR_B_GPIO_PINS = 26      	# Pins 1 to 26 on Raspberry Pi A or B
NUM_PI_OUTPUT_PINS = 4                	# This software instance of Raspberry Pi can have up to four output pins
NUM_PI_INPUT_PINS = 4                 	# This software instance of Raspberry Pi can have up to four input pins
#UART pins in BCM mode are: 14, 15 /dev/ttyAMA0

# Wire value CONTSTANTS 
# Raspberry Pi 4 Pin Layout 
# https://pinout.xyz/pinout 
# https://www.element14.com/community/docs/DOC-92640/l/raspberry-pi-4-model-b-default-gpio-pinout-with-poe-header
NO_PIN = -1  						#TODO This constant may not be needed :)
NO_WIRE = 0
VCC_3_3V = 1
VCC_3_3V_NAME = "BOARD1"     		# 3.3 Volts @ upto 0.050 Amps = 0.165 Watts https://pinout.xyz/pinout/pin1_3v3_power
VCC_5V = 2
VCC_5V_NAME = "BOARD2"        		# 5 Volts @ upto ~1.5 Amps (Power Adapter - Pi usgae) = 7.5 Watts https://pinout.xyz/pinout/pin2_5v_power
I2C_SDA0 = 3					
PI0_I2C_SDA1_NAME  = "BOARD3"		# Fixed, 1.8 kohms pull-up to 3.3v https://pinout.xyz/pinout/pin3_gpio2
I2C_SCL0 = 5
PI0I2C_SCL1_NAME = "BOARD5"			# Fixed, 1.8 kohms pull-up to 3.3v https://pinout.xyz/pinout/pin5_gpio3
TXD = 8
TXD_NAME = "BOARD8" 				# UART transmit pin / Serial Port https://pinout.xyz/pinout/pin8_gpio14 
RXD = 10	
RXD_NAME = "BOARD10" 				# UART recieve pin / Serial Port https://pinout.xyz/pinout/pin10_gpio15					
GND = "BOARD6&9&14&20&25&30&34&39"	# Digital Ground (0 Volts) https://pinout.xyz/pinout/ground
PWM0 = 12
PWM0_NAME = "BOARD12"				#Pulse Width Modulation https://pinout.xyz/pinout/pin12_gpio18 
