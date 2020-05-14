#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-05-11"
__doc__ =     "Class to operate at least 64 servos, 16 relays, and 32 motors at once with latency less then 100 ms"

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
from time import sleep

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

# Create an array of specific length to restrict resizing and appending (like Pythom list) to improve performance
import numpy as np
from numpy import ndarray, empty #Pick the one that is faster

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
    #TODO DO LOW LEVEL PIN CONTROL THAT WORKS EVER WHERE? http://wiringpi.com/the-gpio-utility/
    ImportDebugObject = Debug(True)
    Debug.Dprint(ImportDebugObject, "WARNING: You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")

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

    # Global class variables
    currentNumOfActuators = 0
	
    # wires are on the actuator side of hardwrae schematic. While pins are on the CPU side, but often have similar names
    wires = [NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE, NO_WIRE]

    def __init__(self, aType, pins, partNumber, direction):
	    """
	    Constructor to initialize an Actutator object, which can be a Servo(), Motor(), or Relay()
	
	    Key arguments:
	    self - Newly created object
	    wires[] - Array to document wires / pins being used by Raspberry Pi to control an actuator
	    aType - Single String character to select type of actuator to create (S=Servo, M=Motor, R=Relay)
	    TODO REMOVE THIS PARAMETER-currentNumOfActuators - Global Class variable holding the number of actuators in a system
	    actuatorID - Auto-incremented interger bassed off the number of actuator currently in system
	    partNumber - Vendor part number string variable (e.g. Seamuing MG996R)
	    forwardDirection - Set counter-clockwise (CCW) / Linear IN or clockwise (CW) / Linear OUT as the forward direction
	 
	    Return value:
	    Newly created Actuator object
	    """
	    
	    self.DebugObject = Debug(True)
	    wires = np.empty(len(pins), dtype=object)   # TODO wires = ndarray((len(pins),),int) OR wires = [None] * len(pins) 				# Create an array on same length as pins[?, ?, ?]
	    for i in pins:
		self.wires[i] = pins[i]
	    
	    self.actuatorType = aType
	    self.actuatorID = currentNumOfActuators	# Auto-incremented interger class variable
	    currentNumOfActuators = currentNumOfActuators + 1
	    self.partNumber = partNumber
	    self.forwardDirection = direction
		
	    # https://gist.github.com/johnwargo/ea5edc8516b24e0658784ae116628277
	    # https://gpiozero.readthedocs.io/en/stable/api_output.html
	    # https://stackoverflow.com/questions/14301967/bare-asterisk-in-function-arguments/14302007#14302007
	    if(type == "S"):
		    # The last wire in array is the PWM control pin
		    self.actuatorObject = Servo.AngularServo(wires[len(wires)-1])
		    #TODO If above DOES NOT WORK: self.actuatorType = Servo(wires[0], initial_value=0, min_pulse_width=1/1000, max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None)
	    elif(type == "M"):
		    # The last two wires in array are the INPUT control pins
		    self.actuatorObject = Motor(wires[len(wires)-2], wires[len(wires)-1])
		    #TODO If above DOES NOT WORK: self.actuatorType = Motor(wires[0], wires[1], pwm=true, pin_factory=None)
	    elif(type == "R"):
		    # The last wire in array is the relay control pin
		    self.actuatorObject = OutputDevice(wires[len(wires)-1])
		    #TODO If above DOES NOT WORK: self.actuatorObject = gpiozero.OutputDevice(wired[0], active_high=False, initial_value=False)
	    else:
		    Debug.Dprint(DebugObject, "INVALID Actutator Type in __init__ method, please use S, M, R as first parameter to Actuator() Object")
		
    def Run(self, duration, newPosition, speed, direction):
	    #TODO https://www.google.com/search?q=pass+object+to+python+function&rlz=1C1GCEA_enUS892US892&oq=pass+object+to+python+function&aqs=chrome..69i57.5686j0j7&sourceid=chrome&ie=UTF-8
		#TODO https://stackoverflow.com/questions/20725699/how-do-i-pass-instance-of-an-object-as-an-argument-in-a-function-in-python
		"""
		Run an actuator for a given number of milliseconds to a given position at percentage of max speed in FORWARD or BACKWARDS direction
		    
		self - Instance of object being called
		duration - Time actuator is in motion, for Servo() objects this can be used to control speed of movement
		newPosition - New position between -1 and 1 that  actuator should move to
		speed - Speed at which actuator moves at, for Servo() objects this parameter is NOT used
		direction - Set counter-clockwise (CCW or LINEAR_IN) or clockwise (CW or LINEAR_OUT) as the forward direction
		
		return NOTHING
		"""
		
		Debug.Dprint(DebugObject, "Actuator.py Run() function started!")

		if(type == "S"):
			currentPosition = Servo.value()
			if(currentPosition < (newPosition - Actuator.SERVO_SLACK)):
			    actuatorObject.max() #TODO THIS MAY NOT STOP AND GO ALL THE WAY TO MAX POS
			elif(currentPosition > (newPosition - Actuator.SERVO_SLACK)):
			    actuatorObject.min() #TODO THIS MAY NOT STOP AND GO ALL THE WAY TO MIN POS
			else:
			    # NEAR to new position DO NOTHING
			    Servo.dettach()
		elif(type == "M"):
			Debug.Dprint(DebugObject, "Write motor control code")
			Motor.enable()
			currentPosition = actuatorObject.value
			while(currentPosition != newPosition):
				if(actuatorObject.forwardDirection == Actuator.CW):
					Motor.forward(speed)
				else:
					Motor.reverse(speed)
				currentPosition = actuatorObject.value

			sleep(duration)    #TODO signal.pause(duration)
			Motor.disable()

		elif(type == "R"):
			relay.on()
			sleep(duration) 	#TODO signal.pause(duration)
			relay.off()
		else:
			Debug.Dprint(DebugObject, "INVALID Actutator Type sent to Run method, please use S, M, R as first parameter to Actuator() Object")

		Debug.Dprint(DebugObject, "Run function completed!")

    def setAngularPosition(self, newAngle):
        """
        Set the rotational position of a AngularServo() or Motor() object
        
        self - Instance of object being called
        newAngle - Rotational angle to set actuator to, more exact for Servo() objects then Motor() object
        
        return NOTHING
        """
        
    	if(self.actuatorType == "S"):
    	    self.angle = newAngle
    	elif(self.actuatorType == "M"):
    	    Debug.Dprint(self.DebugObject, "THIS CODE IS GOING TO BE HARD") 
		    #TODO Possible global variable with dead recoking needed
    	elif(self.actuatorType == "R"):
    	    Debug.Dprint(self.DebugObject, "Relays do not have rotational positions. Are you sure you called the correct object?")
    	else:
    	    Debug.Dprint(DebugObject, "INVALID Actutator Type sent to SetAngularPosition method, please use S, M, R as first parameter to Actuator() Object")
	
	###
	# Read the linear or rotational positon on an actuator
	#
	# @self - Instance of object being called
	#
	# return The position of actuator, with value between -1.0 and 1.0 inclusively
	###
	def getPosition(self):
		if(self.actuatorType == "S"):
			print("TODO")
			#TODO return self.value

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
	    UnitTest()
	    relay = gpiozero.OutputDevice(8) #BCM-8
	    relay.on()
	    time.sleep(20) # seconds or milliseconds?
	    relay.off()
	except NameError:
	    Debug.Dprint(DebugObject, "WARNING: IDIOT! You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")
	    print("END ACTUATOR.PY MAIN")

def UnitTest():
    pins = [HIGH_PWR_12V, GND, I2C_SDA, I2C_SCL]
    coconutLiftingLinearMotor1 = Actuator("L", pins, "PA-07-12-5V", Actuator.LINEAR_OUT)
    coconutLiftingLinearMotor2 = Actuator("L", pins, "PA-07-12-5V", Actuator.LINEAR_OUT)
    coconutLiftingLinearMotor1.Run(Actuator.N_A, 1, Actuator.N_A, Actuator.FORWARD)
    coconutLiftingLinearMotor2.Run(Actuator.N_A, 1, Actuator.N_A, Actuator.FORWARD)
    
