import time

import cv2

import Debug

class LASER:

	powerLevel = 0

	HIGH_POWER = 16
	STANDARD_POWER = 8
	LOW_POWER = 4

	LASER_CONSTANT = 0.05264472  	#TODO Adjust this until LASER branding looks good

	def __init__(self, powerLevel):
		self.powerLevel = 8.0 	# Initialize to 8.0 Watts

	def LoadLaserImage(fileName):

	def ConfigureLaserForNewImage(powerLevel):
		#TODO Calculate firing duration based on LASER power level and image size
		if(powerLevel != STANDARD_POWER):
			numOfPixels = GetNumOfPixels()
			moistureLevel = GetCocoNutMoistureLevel()
			duration = LASER_CONSTANT * moistureLevel * numOfPixels 
		elif():
			#TODO CHANGE POWER LEVEL HERE
		elif():

		else:
			Debug.Dprint("ERROR: Invalid power level choosen in COnfigureLaserForNewImage() function")

		return duration

	def StopLaser():

	def FireLaser(duration):

	def SetPowerLevel():
