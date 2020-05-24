
#!/usr/bin/env python
import cv as cv

__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.mvp"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development" 
__date__    = "Late Updated: 2020-05-15"
__doc__     = "Class to control and move LASER system"

# Allow program to create GMT and local timestamps
from time import gmtime, strftime

# Computer Vision module to 
import cv2

import numpy as np

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

class LASER:

	# Preset LASER power level CONSTANTS (units are Watts)
	HIGHEST_POWER = 10.01
	HIGH_POWER = 10.00
	STANDARD_POWER = 5.00
	LOW_POWER = 2.50
	LOWEST_POWER = 0.01 

	# LASER branding PNG filename CONSTANTS
	RESORT_WORLD_LOGO = "ResortWorldLogoV0.png"
	COCOTAPS_LOGO = "CocoTapsLogoV0.png"
	WYNN_HOTEL_LOGO = "WynnHotelLogoV0.png"
	RED_BULL_LOGO = "RedBullLogoV0.png"
	BACARDI_LOGO = "BacardiLogoV0.png"
	ROYAL_CARRIBBEAN_LOGO = "RoyalCarribbeanLogoV0.png"

	LASER_CONSTANT = 0.05264472  	#TODO Adjust this until LASER branding looks good

	def __init__(self, partNumber, powerLevel):
	    """
	    TODO
	    
	    Key arguments:
	    partNumber -- Supplier part number (i.e. ?????)
	    powerLevel -- Power in Wats to intialize LASER module to
	    brandingArt -- Black & White PNG image ro brand / burn into an object
	    """
	    self.DebugObject = Debug(True)
	    
	    self.powerLevel = powerLevel        # Initialize to 8.0 Watts
	    if(LOWEST_POWER > powerLevel or powerLevel > HIGHEST_POWER):
	        # Check for valid power level and default to 10 Watts if invalid
	        Debug.Dprint(DebugOject, "Invalid power setting LASER power set to " + repr(HIGH_POWER))
	        self.powerLevel = HIGH_POWER
	    
	    self.partNumber = partNumber
	    self.brandingArt = COCOTAPS_LOGO	# Initialize to standard CocoTaps logo

	def LoadLImage(fileName):
		"""
		Load a PNG image on the local harddrive into RAM
		
		Key arguments:
		filename -- PNG file to load into memory
		
		Return value:
		img -- Black & White PNG image
		"""
		print("TODO: CHECK FOR >PNG?")		
		path = "../static/images/" + fileName
		img = cv2.imread(path)
		return img

	def WarpImage(currentImage, coconutSize):
		"""
		Wrap a straight / square image so that after LASER branding on coconut its straight again

		Key arguments:
		currentImage -- Starting PNG image (max size in ? x ? pixels / ?? MB)
		coconutSize -- Horizontal diameter of coconut in millimeters

		Return value:
		newImage -- A new image that has been warpped to to display correctly after LASER branding 
		"""
		# https://docs.opencv.org/2.4/doc/tutorials/core/mat_the_basic_image_container/mat_the_basic_image_container.html
        # https://pythonprogramming.net/loading-images-python-opencv-tutorial/

		#Mat m = Mat() #... // some RGB image
		img = cv.imread(currentImage)
		imgWidth = img.width
		imgHeight = img.height

		for xPixel in range(imgWidth):
			for yPixel in range(imgHeight):
				rgbColor = img.at<Vec3b>(xPixel,yPixel)
				#TODO TRANSLATION
				#Split image into three part vertically and horizonatlly
				##TODO Why we need the below line? Blaze?
				# img.at<Vec3b>(xPixel,yPixel) = rgbColor
				if(xPixel < (imgWidth/5)):
					xPixel = xPixel + 8		# Skip EIGHT pixels since ends warps more at ends
				elif((imgWidth/5) <= xPixel and xPixel < (imgWidth*2/5)):
					xPixel = xPixel + 4		# Skip FOUR pixels since ends warps more at ends
				elif((imgWidth*2/5) <= xPixel and xPixel < (imgWidth*3/5)):
					xPixel = xPixel + 0
				elif((imgWidth*3/5) <= xPixel and xPixel < (imgWidth*4/5)):
					xPixel = xPixel + 4		# Skip FOUR pixels since ends warps more at ends
				elif((imgWidth*4/5) <= xPixel and xPixel < (imgWidth)):
					xPixel = xPixel + 8		# Skip EIGHT pixels since ends wraps more at ends
						

	def ConfigureLaserForNewImage(powerLevel, filename):
		"""
		Calculate firing duration based on LASER power level and image size
		"""
		#TODO 
		if(powerLevel != STANDARD_POWER):
			numOfPixels = GetNumOfPixels(filename)
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

	def SetPowerLevel(watts, cocoPartNumber):
		"""
		Set the power level based on LASER part number being used
		
		Key arguments: 
		watts -- 
		"""
		self.powerLevel = watts
		


	def GetNumOfPixels(filename):
		"""
		Calculate the total number of (pixels / 1,000,000) that is in an image file 
		
		Key argument:
		filename -- PNG file to load into memory
		
		Return value:
		totalNumOfPixels -- Total number of megapixels (million pixels) in an image
		"""
		img = LoadLImage(filename)
		Mat m = ... // some RGB image
		imgWidth = m.width
		imgHeight = m.height
		totalNumOfPixels = imgWidth * imgHeight
		
		return totalNumOfPixels
    
	def GetCoconutMoistureLevel():
		"""
		Moisture level from 0 to 100 corresponing to % humidity
    	Return value:
    	moisturePercentage -- An float from 0.0 to 100.0 
		"""
	    #idTODO Moisture sensor in fridge
		print("TODO I2C sensor")
		moisturePercentage = 5
		return moisturePercentage
