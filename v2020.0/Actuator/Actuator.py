#!/usr/bin/env python3
"""
__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-07-21"
__doc__ =     "Class to operate at least 64 servos, 16 relays, and 32 motors at once with latency less then 100 ms"
"""

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

# Allow program to pause operation and create local timestamps
from builtins import ImportError, len, NameError
from time import sleep

# Allow program to extract filename of the current file
import sys, os.path
v2020 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(v2020)
# Custom CocoTaps and Robotic Beverage Technologies code
import RaspPi
import Debug
# # Create an array of specific length to restrict resizing and appending (like Pythom list) to improve performance
# import numpy as np
#TODO REMOVE? from numpy import ndarray, empty #Pick the one that is faster

try:
	# The following imports do NOT work in a Mac oor PC dev enviroment (but are needed for Pi product) 

	# CircuitPython library for the DC & Stepper Motor Pi Hat kits using I2C interface
	#from adafruit_motorkit import MotorKit

	# Allow asynchrous event to occur in parallel and pause threads as needed
	# MAY  work on Windows sometime in the future https://github.com/vibora-io/vibora/issues/126
	#from signal import pause

	# Allow control of input devices such as Buttons
	from gpiozero import Button

	# Check status of network / new device IP addresses and Pi hardware
	from gpiozero import PingServer, pi_info

	# Useful pin status tools and math tools
	from gpiozero.tools import all_values, negated, sin_values

	# Useful for controlling devices based on date and time
	from gpiozero import TimeOfDay

	# Allow control of output devices such as Motors, Servos, LEDs, and Relays
	from gpiozero import Motor, Servo, LED, Energenie, OutputDevice, AngularServo
	#import gpiozero
	#from gpiozero.pins.mock import MockFactory
	#gpiozero.Device.pin_factory = MockFactory()

except ImportError:
	#TODO DO LOW LEVEL PIN CONTROL THAT WORKS EVER WHERE? http://wiringpi.com/the-gpio-utility/
	currentProgramFilename = os.path.basename(__file__)
	TempDebugObject = Debug(True, "Try/Catch ImportError in " + currentProgramFilename)
	RaspPi.DevPinConfigError(TempDebugObject)

class Actuator:

	# Class attributes that can be accessed using ActuatorControl.X (not actuatorcontrol.X)
	MAX_NUM_OF_SERVOS = 0		# Circular servos
	MAX_NUM_OF_MOTORS = 12		# Circular stepper or brushless DC motors
	MAX_NUM_OF_LINEAR_ACT = 5 	# Linear actuators
	N_A = 0						# Not Applicable

	# Circular & linear actuator direction CONSTANTS
	CCW = -1  			# Counter-Clockwise
	CW = 1    			# Clockwise
	LINEAR_IN = CCW		# Towardsbase of linear actuator
	LINEAR_OUT = CW		# Away from base of linear
	SERVO_SLACK = 0.2	# Positional accuaracy slack for servo so that control system does not go crazy
	FORWARD = 1
	BACKWARD = -1
	I2C_SCL = 5
	I2C_SDA = 3
	# Pin value CONSTANTS
	LOW =  0
	HIGH = 1

	# Wire value CONTSTANTS
	# Raspberry Pi 4 Pin Layout https://pinout.xyz/pinout/pin1_3v3_power
	NO_PIN = -1  						#TODO This constant may not be needed :)
	NO_WIRE = 0
	VCC_3_3V = 1
	VCC_3_3V_NAME = "BOARD1"     		# 3.3 Volts @ upto 0.050 Amps = 0.165 Watts https://pinout.xyz/pinout/pin1_3v3_power
	VCC_5V = 2
	VCC_5V_NAME = "BOARD2"        		# 5 Volts @ upto ~1.5 Amps (Power Adapter - Pi usgae) = 7.5 Watts https://pinout.xyz/pinout/pin2_5v_power
	GND = "BOARD6&9&14&20&25&30&34&39"	# Digital Ground (0 Volts) https://pinout.xyz/pinout/ground

	# Negative to NOT confuse it with Pi BOARD 12 https://pinout.xyz/pinout/pin12_gpio18
	HIGH_PWR_5V = 5					# 5.00 Volts @ upto 5.0 Amps = 25.0 Watts to power Pi, force / load cell sensor and servos
	HIGH_PWR_12V = 12					# 12.0 Volts @ upto 5.0 Amps = 70.0 Watts to power linear actuators
	HIGH_PWR_36V = 36					# TODO (30 or 36) Volts @ upto 5 Amps = 150 Watts to power Stepper Motors

	# wires are on the actuator side of hardwrae schematic. While pins are on the CPU side, but often have similar names
	wires = [NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE]

    # Class variable
	actuatorID = 0
	usedActuatorPins = [False] * 40


	def __init__(self, pins, partNumber, direction):
		"""
		Constructor to initialize an Actutator object, which can be an AngularServo(), Motor(), or Relay()

		Key arguments:
		self -- Newly created object
		actuatorID -- Interger CONSTANT defined in Driver.py to enable quick array searches
		pins -- Array to document wires / pins being used by Raspberry Pi to control an actuator
		partNumber -- Vendor part number string variable (e.g. Seamuing MG996R)
		direction -- Set counter-clockwise (CCW) / Linear IN or clockwise (CW) / Linear OUT as the forward direction

		Return value:
		Newly created Actuator1() object
	    """
		currentProgramFilename = os.path.basename(__file__)
		self.DebugObject = Debug(True, currentProgramFilename)
		self.actuatorID = Actuator.actuatorID
		Actuator.actuatorID = Actuator.actuatorID + 1

		numOfWires = len(pins)
		wires = np.empty(numOfWires, dtype=object)   # TODO wires = ndarray((len(pins),),int) OR wires = [None] * len(pins) 				# Create an array on same length as pins[?, ?, ?]
		for i in range(numOfWires):
			#TODO REMOVE print("PIN: "  + repr(i))
			#TODO REMOVE print(pins[i])
			usedActuatorPins = RaspPi.reservePin(i)
			wires[i] = pins[i]

		self.partNumber = partNumber
		self.forwardDirection = direction

		# The last wire in array is the PWM control pin
		#tempServoObject = Servo(pins[0]) #TODO REMOVE BECAUSE TO SIMPLE AN OBJECT
		#tempServoObject = gpiozero.Servo(pins[0]) #TODO REMOVE BECAUSE TO SIMPLE AN OBJECT
		#tempAngularServoObject = AngularSevo(wires[len(wires)-1])



	def Run(self, duration, newPosition, speed, direction):
		#TODO https://www.google.com/search?q=pass+object+to+python+function&rlz=1C1GCEA_enUS892US892&oq=pass+object+to+python+function&aqs=chrome..69i57.5686j0j7&sourceid=chrome&ie=UTF-8
		#TODO https://stackoverflow.com/questions/20725699/how-do-i-pass-instance-of-an-object-as-an-argument-in-a-function-in-python
		"""
		Run an actuator for a given number of milliseconds to a given position at percentage of max speed in FORWARD or BACKWARDS direction

		Key arguments:
		duration - Time actuator is in motion, for Servo() objects this can be used to control speed of movement
		newPosition - New position between -1 and 1 that  actuator should move to
		speed - Speed at which actuator moves at, for Servo() objects this parameter is NOT used
		direction - Set counter-clockwise (CCW or LINEAR_IN) or clockwise (CW or LINEAR_OUT) as the forward direction

		Return Value:
		NOTHING
		"""
		print("Actuator1.py Run() function started!")




	def setAngularPosition(self, newAngle):
		"""
		Set the rotational position of a AngularServo() or Motor() object

		Key arguments:
        newAngle - Rotational angle to set actuator to, more exact for Servo() objects then Motor() object

        Return value:
        NOTHING
        """
		self.Debug.Dprint("Relays do not have rotational positions.")


	def getPosition(self):
		"""
		Read the linear or rotational positon on an actuator

		Return value:
		The position of actuator, with value between -1.0 and 1.0 inclusively
		"""

	def isActive(self):
		"""
		Determine if actuator is moving

		Return value:
		TRUE if actuator is powered on and moving, FALSE otherwise
		"""

		return self.actuatorOjbect.isActive


	def setAngle(self, angle):
			print("TODO")


	def UnitTest():
		pins = [HIGH_PWR_12V, GND, I2C_SDA, I2C_SCL]
		coconutLiftingLinearMotor1 = Actuator('M', Actuator.actuatorID, pins, "PA-07-12-5V", Actuator.LINEAR_OUT)
		coconutLiftingLinearMotor2 = Actuator('M', Actuator.actuatorID, pins, "PA-07-12-5V", Actuator.LINEAR_OUT)

		pins = [Actuator.HIGH_PWR_5V, RaspPi.PWM0, Actuator.GND]
		tapHolderServo.Run('S', Actuator.actuatorID, pins, Actuator.FORWARD)

		TODO.Run(Actuator.N_A, 1, Actuator.N_A, Actuator.FORWARD)


if __name__ == "__main__":

	try:
		#Actuator1.UnitTest()
		#relay = OutputDevice(8) #BCM-8
		#relay.on()
		#time.sleep(20) # seconds or milliseconds?
		#relay.off()
		print("THIS CANT FAIL?")
		v2020 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
		print('******** ' + v2020)

	except NameError:
		currentProgramFilename = os.path.basename(__file__)
		NameDebugObject = Debug(True, currentProgramFilename)
		NameDebugObject.Dprint("Try fail in __main__ of " + str(currentProgramFilename))

	print("END ACTUATOR.PY MAIN")
