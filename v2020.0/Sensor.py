#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-04-15"
__doc__ =     "Class to communicate with all sensors inside the Tapomatic kiosk" 

# Allow program to pause operation and create local timestamps
from time import sleep

# Allow communication (Read and write) to senors via the serial port 
#TODO if gpiozero doesn't support import serial

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

except ImportError:
	
	# Allow BASH command to be run inside Python3 code like this file
	import subprocess
	from subprocess import Popen, PIPE
	from subprocess import check_call

	# This import SHOULD work on both Mac & PC to allow software dev work (no hardware in the loop testing)
	check_call("pip3 install gpiozero pigpio", shell=True)

	DebugObject = Debug(True)
	DebugObject.Dprint(DebugObject, "WARNING: You are running code on Mac or PC (NOT a Raspberry Pi)")

class Sensor():	

	# TODO Define all pins in schematic
	FORCE_SENSOR_1 = 1
	FORCE_SENSOR_2 = 2
	FORCE_SENSOR_3 = 3
	FORCE_SENSOR_4 = 4
	FORCE_SENSOR_5 = 5
	FORCE_SENSOR_6 = 6
	
	# TODO Define all pins in schematic
	PING_Xaxis_Pin = 12
	PING_Xaxis_Pin_Name = "Board12"
	PING_Yaxis_Pin = 13
	PING_Yaxis_Pin_Name = "Board13"
	PING_Zaxis_Pin = 14
	PING_Zaxis_Pin_Name = "Board14"
	
	def __init__(self, currentNumOfSensors, sType, pins, partNumber):
		wires = numpy.empty(len(pins), dtype=object)   # TODO wires = ndarray((len(pins),),int) OR wires = [None] * len(pins) 				# Create an array on same length as pins[?, ?, ?]
		for i in pins:
			self.wires[i] = pins[i]
		self.sensorType = sType
		currentNumOfActuators += 1
		self.sensorID = currentNumOfSensors# Auto-incremented interger class variable
		self.partNumber = partNumber
		
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

	
	def GetLevel(self, lType):
		"""
		Determine level / percentage of liquid left in a 750 ml glass bottle to notify service employee refill needed at 10%

		@self - Instance of object being called
		@lType - Type of liquid being measured as defined in CocoDrink.py (Weight of liquid and bottle is define in Sensor.py)

		return percentage - The amount of liquid left as percentage
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

		if(percentage < 10.0):
			print("TODO")
			#MissionControl.SendLiquidLevelMessage(lType,  MissionControl.MESSAGE_1)
    
		return percentage

	def GetForce(lType):
		"""
		Get force as measured by hx711 connected to a 5 kg analog strain gauge. Most Sign Bit first amd 25 (to 27) pulses 

		@lType - Type of liquid being measured as defined in CocoDrink.py 

		@link https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf
		
		@link https://github.com/aguegu/ardulibs/
		
		Degraw 5kg Load Cell and HX711 Combo Pack Kit - Load Cell Amplifier ADC Weight Sensor for Arduino Scale - Everything Needed for Accurate Force Measurement https://www.amazon.com/dp/B075317R45/ref=cm_sw_r_cp_api_i_Ph7JEb5A1F12M

		return forceInNewtons - The weight of liquid in Newtons
		"""

		forceSensorID = FindLiquidForceSensor(lType)

		print("TODO")
		#SCK = 
		#DT = 

		forceInlbs = DT 
		forceInNewtons = forceInlbs * 0.2248
		
		return forceInNewtons

	def FindLiquidForceSensor(lType):
		
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
    	    status = False
    	    for pin in range(PING_Xaxis_Pin, PING_Zaxis_Pin+1):
    	    	if(GetLASERpingDistance(pin) >= OBJECT_IN_THE_WAY):
    	        	status = True 

    	    return status
    	
	def GetLASERpingDistance(pingPinNumber):
		range = Ping.GetMillimeters(pingPinNumber) 
		
		return range 
   
