#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-02-19"
__doc__ =     "Class to operate at least 8 servos, 4 relays, and 4 motors at once with latency less then 100 ms"

# Useful documentation:
# https://gpiozero.readthedocs.io/en/stable/installing.html
# https://gpiozero.readthedocs.io/en/stable/
# https://gpiozero.readthedocs.io/en/stable/api_output.html
# https://gpiozero.readthedocs.io/en/stable/api_input.html

# Replacement code if GPIOzero doesn't work...
# https://www.adafruit.com/product/2348
# https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software
# https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/circuitpython-raspi
# https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi

#TODO REMOVE? import datetime
#TODO REMOVE? import time

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

try:
	# The following imports do NOT work in a Mac oor PC dev enviroment (but are needed for Pi product) 
	
	# CircuitPython library for the DC & Stepper Motor Pi Hat kits using I2C interface
	from adafruit_motorkit import MotorKit

	# Allow asynchrous event to occur in parallel and pause threads as needed
	# Might work on Windows in the future https://github.com/vibora-io/vibora/issues/126
	from signal import pause 

	# Allow control of input devices such as Buttons
	from gpiozero import Button

	# Allow control of output devices such as Motors, Servos, LEDs, and Relays
	from gpiozero import Motor, Servo, LED, Energenie, OutputDevice

	# Check status of network / new device IP addresses and Pi hardware
	from gpiozero import PingServer, pi_info

	# Useful pin status tools and math tools
	from gpiozero.tools import all_values, negated, sin_values

	# Useful for controlling devices based on date and time
	from gpiozero import TimeOfDay

except ImportError:
	DebugObject = Debug(True)
	Debug.Dprint(DebugObject, "WARNING: You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")


class Actuator:

	# Class attributes that can be accessed using ActuatorControl.X (not actuatorcontrol.X)
	MAX_NUM_OF_SERVOS = 8		# Circular servos
	MAX_NUM_OF_MOTORS = 2		# Circular motors
	MAX_NUM_OF_LINEAR_ACT = 4  	# Linear actuators
	N_A = 0				# Not Applicable

	# Actuator "forward" direction constants
	CCW = -1  		# Counter-Clockwise
	CW = 1    		# Clockwise
	SERVO_SLACK = 0.2	# Positional accuaracy slack for servo so that control system does not go crazy
	FORWARD = 1
	BACKWARD = -1

	# Pin value constants
	LOW =  0
	HIGH = 1

	# Wire value constants (interger values don't really matter, but are easy to loop thru)
	NO_PIN = 0  #TODO This constant may not be needed :)
	NO_WIRE = -1
	VCC_5V = "BOARD2"        # 5 Volts @ upto ??? Amps = ??? Watts
	VCC_3_3V = "BOARD1"      # 3.3 Volts @ upto ??? Amps =  ??? Watts
	GND = "BOARD6&9&14&20&25&30&34&39"
	PWR_12V = -4

	# Raspberry Pi B+ refernce pin constants as defined in ???rc.local script???
	NUM_GPIO_PINS = 8                       # Outputs: GPO0 to GPO3 Inputs: GPI0 to GPI3
	MAX_NUM_A_OR_B_PLUS_GPIO_PINS = 40      # Pins 1 to 40 on Raspberry Pi A+ or B+ or ZERO W
	MAX_NUM_A_OR_B_GPIO_PINS = 26           # Pins 1 to 26 on Raspberry Pi A or B
	NUM_OUTPUT_PINS = 4                     # This software instance of Raspberry Pi can have up to four output pins
	NUM_INPUT_PINS = 4                      # This software instance of Raspberry Pi can have up to four input pins

	# Class variables
	currentNumOfActuators = 0

	wires = [NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE]

	###
	# Constructor to initialize an Actutator object, which can be a Servo(), Motor(), or Relay()
	#
	# @self - Newly created object
	# @type - Single String character to select type of actuator to create (S=Servo, M=Motor, R=Relay)
	# @wires[] - Array to document wires / pins being used by Pi 3 to control an actuator
	# @partNumber - Vendor part number string variable (e.g. Seamuing MG996R)
	# @forwardDirection - Set counter-clockwise (CCW) or clockwise (CW) as the forward direction
	#
	# return NOTHING
	###
	def __init__(self, type, pins, partNumber, direction):
		for i in pins:
			self.wires[i] = pins[i]
		self.type = type
		self.actuatorID = currentNumOfActuators	# Auto-incremented interger Class variable
		self.partNumber = partNumber
		self.forwardDirection = direction
		self.currentNumOfActuators += 1

		#https://gist.github.com/johnwargo/ea5edc8516b24e0658784ae116628277
		# https://gpiozero.readthedocs.io/en/stable/api_output.html
		# https://stackoverflow.com/questions/14301967/bare-asterisk-in-function-arguments/14302007#14302007
		if(type == "S"):
			#self.actuatorType = Servo(wires[0], initial_value=0, min_pulse_width=1/1000, max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None)
			#NOTE: The last wire in array is the PWM control pin
			self.actuatorObject = AngularServo(wires[len(wires)-1])
		elif(type == "M"):
			#self.actuatorType = Motor(wires[0], wires[1], pwm=true, pin_factory=None)
			#NOTE: The last two wires in array are the INPUT control pins
			self.actuatorObject = gpiozero.Motor(wires[len(wires)-2], wires[len(wires)-1])
		elif(type == "R"):
			#self.actuatorObject = gpiozero.OutputDevice(wired[0], active_high=False, initial_value=False)
			#NOTE: The last wire in array is the relay control pin
			self.actuatorObject = gpiozero.OutputDevice(wires[len(wires)-1])
		else:
			Debug.DPrint("INVALID Actutator Type in __init__ method, please use S, M, R as first parameter to Actuator() Object")

	###
	# Run an actuator for a given number of milliseconds to a given position at percentage of max speed in FORWARD or BACKWARDS direction
	#
	# @self - Instance of object being called
	# @duration - Time actuator is in motion, for Servo() objects this can be used to control speed of movement
	# @newPosition - New position between -1 and 1 that  actuator should move to
	# @speed - Speed at which actuator moves at, for Servo() objects this parameter is NOT used
	# @direction - Set counter-clockwise (CCW) or clockwise (CW) as the forward direction
	#
	# return NOTHING
	###
	def run(self, duration, newPosition, speed, direction):
		Debug.DPrint("Run function started!")

		if(type == "S"):
			currentPosition = self.value
			if(currentPosition < (newPosition - SERVO_SLACK)):
				self.max() #TODO THIS MAY NOT STOP AND GO ALL THE WAY TO MAX POS
			elif(currentPosition > (newPosition - SERVO_SLACK)):
				self.min() #TODO THIS MAY NOT STOP AND GO ALL THE WAY TO MIN POS
			else:
				# NEAR to new position DO NOTHING
				self.dettach()
		elif(type == "M"):
			Debug.DPrint("Write motor control code")
			self.enable()
			currentPosition = self.value
			while(currentPosition != newPosition):
				if(self.forwardDirection == CW):
					self.forward(speed)
				else:
					self.reverse(speed)
				currentPosition = self.value

			time.sleep(duration)
			self.disable()

		elif(type == "R"):
			self.on()
			time.sleep(duration)
			self.off()
		else:
			Debug.DPrint("INVALID Actutator Type sent to Run method, please use S, M, R as first parameter to Actuator() Object")

		Debug.DPrint("Run function completed!")

	###
	# Set the rotational position of a AngularServo() or Motor() object
	#
	# @self - Instance of object being called
	# @newAngle - Rotational angle to set actuator to, more exact for Servo() objects then Motor() objects
	#
	# return NOTHING
	###
	def setAngularPosition(self, newAngle):
		if(actuatorType == "S"):
			self.angle = newAngle
		elif(actuatorType == "M"):
			DebbugPrint("THIS CODE IS GOING TO BE HARD") #TODO global variable with dead recoking
		elif(actuatorType == "R"):
			print("Relays do not have rotational positions. Are you sure you called the correct object?")
		else:
			Debug.DPrint("INVALID Actutator Type sent to SetAngularPosition method, please use S, M, R as first parameter to Actuator() Object")
	###
	# Read the linear or rotational positon on an actuator
	#
	# @self - Instance of object being called
	#
	# return The position of actuator, with value between -1.0 and 1.0 inclusively
	###
	def getPosition(self):
		if(actuatorType == "S"):
			return self.value

	###
	# Determine if actuator is moving
	#
	# @self - Instance of object being called
	#
	# return TRUE if actuator is powered on and moving, FALSE otherwise
	###
	def isActive(self):
		return self.isActive


	def setAngle(self, angle):
		print("TODO")


if __name__ == "__main__":
	try:
		#DELETE currentNumOfActuators = 0
		#pins = [PWR, GND, 1, GND, SIG_1, SIG_2]
		#cupSepServo1 = Actuator("S", pins, "MG996R", CW)
		relay = gpiozero.OutputDevice(8) #BCM-8
		relay.on()
		time.sleep(20) #seconds of milliseconds?
		relay.off()

	except NameError:
		Debug.Dprint(DebugObject, "WARNING: IDIOT! You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")
		print("END ACTUATOR.PY MAIN")