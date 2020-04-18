#!/usr/bin/env python

"""
__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-04-17"
__doc__ =     "Class to communicate with all sensors inside the Tapomatic kiosk" 
"""

# Allow program to pause operation and create local timestamps
from time import sleep

# Allow communication (Read and write) to senors via the serial port 
#TODO import serial if gpiozero or RPi.GPIO as GPIO doesn't support 

# Allow communication between one or more kiosks with central server
#TODO from MissionControl import *

try:
	# The following imports do NOT work in a Mac or PC dev enviroment 
	# But are needed for a Raspberry Pi controlled kiosk

	# Allow control of input and output devices such as Sensors
	from gpiozero import InputDevice, OutputDevice, Energenie
	
	# Allow control of  HC-SR04 ultrasonic distance sensor (See CamJam #3 EduKit)
	# http://camjam.me/?page_id=1035
	from gpiozero import DistanceSensor
	
	# Library to scan and create custom QR codes 
	from MyQR.terminal import main


except ImportError:
	
	"""
	# TODO MOVE THIS TO install.py file 
	# Allow BASH command to be run inside Python3 code like this file
	import subprocess
	from subprocess import Popen, PIPE
	from subprocess import check_call

	# This import SHOULD work on both Mac & PC to allow software dev work (no hardware in the loop testing)
	check_call("pip3 install gpiozero pigpio", shell=True)
	"""
	
	DebugObject = Debug(True)
	Debug.Dprint(DebugObject, "WARNING: You are running code on Mac or PC (NOT a Raspberry Pi)")

class Sensor():	
	# TODO Compare how many taps have been used vs the number of coconuts drill to
	# make sure vendor is buying from us

	BOTTLE_WEIGHT = 1.5 #Units Newtons TODO WEIGHT EMPTY BOTTLE

	# TODO Define all pins in schematic and measure density of each liquid
	RED_BULL_FORCE_SENSOR = 0
	RED_BULL_DENSITY = 1.1      	# Units grams/mL
	IMMUNITY_FORCE_SENSOR = 1
	IMMUNITY__DENSITY = 1.001      	# Units grams/mL
	VITAMINS_FORCE_SENSOR = 2
	VITAMINS_DENSITY = 1.3      	# Units grams/mL
	PINA_COLADA_FORCE_SENSOR = 3
	PINA_COLADA_DENSITY = 1.5      	# Units grams/mL
	ORANGE_FORCE_SENSOR = 4	
	ORANGE_DENSITY = 1.01      		# Units grams/mL
	PINEAPPLE_FORCE_SENSOR = 5
	PINEAPPLE_DENSITY = 1.12      	# Units grams/mL
	LIFTING_PLATFORM_FORCE_SENSOR = 6
	
	LOW_LEVEL = 10.0 				# 10.0% 
	
	# TODO Define all pins in schematic
	NUM_X_AXIS_PING_SENSORS = 6
	NUM_Y_AXIS_PING_SENSORS = 4
	NUM_Z_AXIS_PING_SENSORS = 14
	PING_Xaxis_Pin = 12
	PING_Xaxis_Pin_Name = "Board12"
	PING_Yaxis_Pin = 13
	PING_Yaxis_Pin_Name = "Board13"
	PING_Zaxis_Pin = 14
	PING_Zaxis_Pin_Name = "Board14"
	PING_GPIO_TRIGGER = -1
	PING_GPIO_ECHO = -1
	
	def __init__(self, currentNumOfSensors, sType, pins, partNumber, currentCount):
		wires = numpy.empty(len(pins), dtype=object)   # TODO wires = ndarray((len(pins),),int) OR wires = [None] * len(pins) 				# Create an array on same length as pins[?, ?, ?]
		for i in pins:
			self.wires[i] = pins[i]
		self.sensorType = sType
		currentNumOfActuators += 1
		self.sensorID = currentNumOfSensors# Auto-incremented interger class variable
		self.partNumber = partNumber
		self.currentCount = 0
		
	def StartFullDuplexSerial():
		print("TODO")
		#Serial.
		
	def SendSerialCommand():
		print("TODO")
	
	def ReceiveSerialCommand():
		print("TODO")
		
	def StartI2C():
		print("TODO")
		#gpio. 
		
	def SendI2C():
		print("TODO")
		
	def GetLiftPlatformCount(self):
		"""
		
		Key arguments:
		self --
		
		Return value:
		currentCount -- Number of times coconuts have been lifted into the Tapomatic 
		"""
		return self.currentCount = self.currentCount + 1

	def ScanQRcode():
		print("TODO")
		"""
		Use camera with white LED to scan a QR
		
		Return value:
		id -- Interger CONSTANT of liquid type as defined in CocoDrinks.py (e.g. TODO ORANGE_FLAVOR, IMMUNITY_) 
		"""
		
		
		id = 
		
		return id
		
	def CreateQRcode(bottleID):
		"""
		Create PNG QR code file for print
		
		Key arguments:
		bottleID --
		
		Return vale:
		filemane -- fileName.png of custom QR code
		"""
		#MyQR.
		print("TODO")
		
	def PrintQRcode(png):
		"""
		https://smallbusiness.chron.com/sending-things-printer-python-58655.html
		"""
		print("TODO")
	
	def GetLevel(self, lType):
		"""
		Determine level / percentage of liquid left in a 750 ml glass bottle to notify service employee refill needed at 10%

		Keyword arguments:
		self - Instance of object being called
		lType - Type of liquid being measured as defined in CocoDrink.py (Density of liquid and weight of bottle is define in Sensor.py)

		Return value:
		percentage - The amount of liquid left as percentage based on know density for that liquid type
		"""

		if(lType == CocoDrink.CBD):
  			liquidWeightAt100percent = 2.2 #TODO Get Density of CBD Units are Newtons
		elif(lType == CocoDrink.IMMUNITY_BOOST):
			liquidWeightAt100percent = 2.2 #TODO Get Density of IMMUNITY_BOOST Units are Newtons
		elif(lType == CocoDrink.DAILY_VITAMINS):
			liquidWeightAt100percent = 2.2 #TODO Get Density of DAILY_VITAMINS Units are Newtons
		elif(lType == CocoDrink.RUM):
			liquidWeightAt100percent = 2.2 #TODO Get Density of RUM Units are Newtons
		elif(lType == CocoDrink.PINA_COLADA):
			liquidWeightAt100percent = 2.2 #TODO Get Density of PINA_COLADA Units are Newtons
		elif(lType == CocoDrink.ORANGE_FLAVOR):
			liquidWeightAt100percent = 2.2 #TODO Get Density of ORANGE_JUICE Units are Newtons		
	
		percentage = GetForce(lType)/liquidWeightAt100percent

		bottleLocation = FindLiquidForceSensor(lType)
		
		#TODO MissionControl.ReportLiquidLevel(lType, percentage, MissionControl.KIOSK_ID)
		
		if(percentage < LOW_LEVEL):
			#TODO MissionControl.ReportLowLiquidLevel(lType, bottleLocation, MissionControl.KIOSK_ID)
    
		return percentage

	def GetForce(lType):
		"""
		Get force as measured by hx711 connected to a 5 kg analog strain gauge. Most Sign Bit first amd 25 (to 27) pulses 
		
		@link https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf
		@link https://github.com/aguegu/ardulibs/
		@link https://www.amazon.com/dp/B075317R45/ref=cm_sw_r_cp_api_i_Ph7JEb5A1F12M

		Degraw 5kg Load Cell and HX711 Combo Pack Kit - Load Cell Amplifier ADC Weight Sensor for Arduino Scale - Everything Needed for Accurate Force Measurement 

		Keyword arguments:
		lType - Type (name) of liquid being measured as defined in CocoDrink.py 
		
		Return value:
		forceInNewtons - The weight of liquid type in Newtons 
		"""

		forceSensorID = FindLiquidForceSensor(lType)

		print("TODO")
		#SCK = 
		#DT = 

		forceInlbs = DT 
		forceInNewtons = forceInlbs * 0.2248
		
		return forceInNewtons

	def FindLiquidForceSensor(lType):
	"""
	Correlate a dynamic interger drink ID (from QR code scan) with static internal force sensor ID 
	
	Keyword arguments:
	lType -- Type (name) of the liquid inside a 750 ml bottle

	Return value:
	ID -- ID number of the force sensor a bottle is pushing against
	"""		
		if(lType == CocoDrink.CBD):
			ID = FORCE_SENSOR_1
		elif(lType == CocoDrink.IMMUNITY_BOOST):
			ID = FORCE_SENSOR_2
		elif(lType == CocoDrink.DAILY_VITAMINS):
			ID = FORCE_SENSOR_3
		elif(lType == CocoDrink.RUM):
			ID = FORCE_SENSOR_4
		elif(lType == CocoDrink.PINA_COLADA):
			ID = FORCE_SENSOR_5 
		elif(lType == CocoDrink.ORANGE):
			ID = FORCE_SENSOR_6

		return ID


	def IsLaserSafetyGridSafe():
	"""
	Determine if any object (e.g. human hand, dog, chopstick, etc) is within 1 of 3 rectanglur danger zones
	TODO This may require upto 24 LASER sensors (S) unless we use mirrors or ultrasonics

	Top View of DANGER ZONES (D) and LASER Sensors (S)
	   S S SS S S
	0 25cm 50cm 75cm (x-axis)
	|    |    |    |
	_----_----_----_   - 0 cm
	|  SDSDSSDSDS  | S - 5 cm
    |  DDDDDDDDDD  |   - 10 cm
	|  DSDDSSDDSD  | S - 15 cm
	|  DDDDDDDDDD  |   - 20 cm
	|  SDSDSSDSDS  | S - 25 cm
	|  DDDDSSDDDD  | S - 30 cm (y-axis)

	Keyword arguments:
	None

	Return value:
	safe -- True if danger zones are clear; Otherwise False
	"""		
    	    safe = True
    	    # Zone (15,0) to (60,-29) cm 
			# Flip between X-axis S#1 and S#2
			# Check (ZS#1, YS#1) then (ZS#2, YS#1) 
			# Check (ZS#5, YS#2) 
			# Check (ZS#9, YS#3) then (ZS#10, YS#3) 
			for xAxisSensor in range(0, NUM_X_AXIS_PING_SENSORS): 
				for yAxix in range(0, NUM_Y_AXIS_PING_SENSORS):
					xDist = GetLASERpingDistance(PING_Xaxis_Pin)
					yDist = GetLASERpingDistance(PING_Yaxis_Pin)
					zDist = GetLASERpingDistance(PING_Zaxis_Pin)
					if(xDist <= 29): # 29 cm
						if(15 <= yDist and yDisy <= 60):
							if(zDist <= 22):
								safe = False 
											
																Debug.Dprint(DebugObject, "X-Axis LASER pin: " + PING_Xaxis_Pin) 
			Debug.Dprint(DebugObject, "Y-Axis LASER pin: " + PING_Yaxis_Pin) 
			Debug.Dprint(DebugObject, "Z-Axis LASER pin: " + PING_Zaxis_Pin) 
					
    	    return safe
    	
	def GetLASERpingDistance(pingPinNumber, units):
	"""
	Get distance to the closet object in direct line of sight of a PING LASER or ultrasonic rangefinder
	
	Keyword arguments:
	pingPinNumber -- Interger Broadcom (BCM) pin number (NOT physical BOARD #) on Raspberry Pi that PING sensor is connected to
	units -- Unit of measure that distance should be returned in millimeter (default) or inches
	
	Return value:
	range -- Interger distance in millimeters (default) or inches
	"""
		if(units == "in" or units == "IN" or units == "In" or units = "iN" of units== "Inches"):
			range = Ping.GetInches(pingPinNumber) 
		else:
			range = Ping.GetMillimeters(pingPinNumber) 
		
		return range 