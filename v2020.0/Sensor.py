import time

from MissionControl import *

class Sensor():	

	FORCE_SENSOR_1 = 1
	FORCE_SENSOR_2 = 2
	FORCE_SENSOR_3 = 3
	FORCE_SENSOR_4 = 4
	FORCE_SENSOR_5 = 5
	FORCE_SENSOR_6 = 6


	def __init__(self, currentNumOfSensors, sType, pins, partNumber):
			wires = numpy.empty(len(pins), dtype=object)   # TODO wires = ndarray((len(pins),),int) OR wires = [None] * len(pins) 				# Create an array on same length as pins[?, ?, ?]
			for i in pins:
				self.wires[i] = pins[i]
			self.sensorType = sType
			currentNumOfActuators += 1
			self.sensorID = currentNumOfSensors# Auto-incremented interger class variable
			self.partNumber = partNumber
		
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
		elif(lType == CocoDrink.ORANGE_JUICE):
			liquidWeightAt100percent = 2.2 #TODO Get Density of ORANGE_JUICE Units are Newtons		
	
		percentage = GetForce(lType)/liquidWeightAt100percent

		if(percentage < 10):
			MissionControl.SendLiquidLevelMessage(lType,  MissionControl.MESSAGE_1)
    
		return percentage

	def GetForce(lType):
		"""
		Get force as measured by hx711 connected to a 5 kg analog strain gauge. Most Sign Bit first amd 25 (to 27) pulses 

		@lType - Type of liquid being measured as defined in CocoDrink.py 

		@link https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf
		 
		return forceInNewtons - The weight of liquid in Newtons
		"""
		forceSensorID = FindLiquidForceSensor(lType)

		SCK = 
		DT = 

		forceInlbs = DT 
		forceInNewtons = forceInlbs * 0.2248
		

    	return forceInNewtons

	def FindLiquidForceSensor(lType):

		if(lType == CocoDrink.CBD):
			ID = FORCE_SENSOR_1
		elif(lType == CocoDrink.IMMUNITY_BOOST):
			ID = FORCE_SENSOR_2
		elif(lType == CocoDrink.IMMUNITY_BOOST):
			ID = FORCE_SENSOR_3
		elif(lType == CocoDrink.IMMUNITY_BOOST):
			ID = FORCE_SENSOR_4
		elif(lType == CocoDrink.IMMUNITY_BOOST):
			ID = FORCE_SENSOR_5
		elif(lType == CocoDrink.IMMUNITY_BOOST):
			ID = FORCE_SENSOR_6

		return ID


	def IsLaserSafetyGridSafe():
    	status = false
		print("TODO") 

    	return status


