
#!/usr/bin/env python

__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-04-22"
__doc__     = "Class to control and move LASER system"

# Allow program to create GMT and local timestamps
from time import gmtime, strftime

# Computer Vision module to 
# TODO import cv2

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

class LASER:

	# Global variable
	currentPowerLevel = 0

	# Preset LASER power level CONSTANTS (units are Watts)
	HIGH_POWER = 16
	STANDARD_POWER = 8
	LOW_POWER = 4

	# LASER branding PNG filename CONSTANTS
	RESORT_WORLD_LOGO = "ResortWorldLogoV0.png"
	COCOTAPS_LOGO = "CocoTapsLogoV0.png"
	WYNN_HOTEL_LOGO = "WynnHotelLogoV0.png"
	RED_BULL_LOGO = "RedBullLogoV0.png"
	BACARDI_LOGO = "BacardiLogoV0.png"
	ROYAL_CARRIBBEAN_LOGO = "RoyalCarribbeanLogoV0.png"

	LASER_CONSTANT = 0.05264472  	#TODO Adjust this until LASER branding looks good

	def __init__(self, powerLevel):
		self.powerLevel = 8.0 				# Initialize to 8.0 Watts
		self.brandingArt = COCOTAPS_LOGO	# Initialize to standard CocoTaps logo

	def LoadLImage(fileName):
		print("TODO")		
		path = "../static/images/" + fileName
		img = cv2.imread(path)
		return img

	def WarpImage(currentImage):
		"""
		Wrap a straight / square image so that after LASER branding on coconut its straight again

		Key arguments:
		currentImage -- Starting PNG image (max size in ? x ? pixels / ?? MB)

		Return value:
		newImage --

		"""
		Mat m = ... // some RGB image
		imgWidth = m.width
		imgHeight = m.height

		for xPixel in range(imgWidth):
			for yPixel in range(imgHeight):
					Vec3b rgbColor = currentImage.at<Vec3b>(xPixel,yPixel)
					#TODO TRANSLATION
					#Split image into three part vertically and horizonatlly
					if(xPixel < (imgWidth/3)):
						newImage.at<Vec3b>(xPixel,yPixel) = rgbColor
						xPixel = xPixel + 5		# Skip FIVE pixels since ends wraps more at ends
					elif((imgWidth/3) <= xPixel and xPixel < (imgWidth*2/3)):
						newImage.at<Vec3b>(xPixel,yPixel) = rgbColor
						xPixel = xPixel + 0		# Skip NO pixels since ends wraps more at ends
					elif((imgWidth*2/3) <= xPixel and xPixel < (imgWidth)):	
						newImage.at<Vec3b>(xPixel,yPixel) = rgbColor
						xPixel = xPixel + 5		# Skip five pixels since ends wraps more at ends
					

	def ConfigureLaserForNewImage(powerLevel):
		#TODO Calculate firing duration based on LASER power level and image size
		if(powerLevel != STANDARD_POWER):
			numOfPixels = GetNumOfPixels()
			moistureLevel = GetCoconutMoistureLevel()
			duration = LASER_CONSTANT * moistureLevel * numOfPixels 
		elif():
			#TODO CHANGE POWER LEVEL HERE
			print("TODO")
		elif():
			print("TODO")
		else:
			Debug.Lprint("ERROR: Invalid power level choosen in ConfigureLaserForNewImage() function")

		return duration

	def StopLaser():
		print("TODO")

	def FireLaser(duration):
		print("TODO")

	def SetPowerLevel():
		print("TODO")

	def GetNumOfPixels():
		print("TODO")
    
	def GetCoconutMoistureLevel():
		"""
		Moisture level from 1 to 10 corresponing to % humidity
    
    	return Integer from 1 to 100
		"""
	    #TODO Moisture sensor in fridge
		print("TODO")
		return 5
