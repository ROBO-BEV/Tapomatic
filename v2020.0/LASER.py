#!/usr/bin/env python
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.mvp"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-06-26"
__doc__     = "Class to control and move LASER system"
"""

# Allow program to create GMT and local timestamps and pause program execution
from time import gmtime, strftime, sleep

# Computer Vision modules to edit / warp images
#import numpy as np
#import cv2 as cv
#TODO ADD BACK? import cv

#TODO REMOVE IF NOT USING ARRASY ANY MORE?
#import numpy as np

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

class LASER:

	# Preset LASER power level CONSTANTS (units are Watts)
	HIGH_POWER = 10.00
	STANDARD_POWER = 5.00
	LOW_POWER = 2.50
	DEFAULT_LASER_CONSTANT = 0.05264472  	#TODO Adjust this until LASER branding looks good

	# LASER branding PNG filename CONSTANTS
	RESORT_WORLD_LOGO = "ResortWorldLogoV0.png"
	COCOTAPS_LOGO = "CocoTapsLogoV0.png"
	WYNN_HOTEL_LOGO = "WynnHotelLogoV0.png"
	RED_BULL_LOGO = "RedBullLogoV0.png"
	BACARDI_LOGO = "BacardiLogoV0.png"
	ROYAL_CARRIBBEAN_LOGO = "RoyalCarribbeanLogoV0.png"

	# Coconut sizing CONSTANTS
	SIZE_102MM = 102
	SIZE_80MM = 88

    # Global class variable
	laserConstant = -1
	laserConfig = -1


	def __init__(self, gpioFirePin, supplierPartNumber, cocoPartNumber, powerLevel, maxPowerLevel, brandingArt):
	    """
	    Create a LASER object with power settings, part numbers, and image data to used when fired via GPIO pin

	    Key arguments:
        gpioFirePin -- 5V GPIO pin used to control a LASER or a 12V relay connected to a LASER
	    supplierPartNumber -- External supplier part number (i.e. PA-07-12-5V)
	    cocoPartNumber -- Internal part number (i.e XXX-YYYYY-Z)) linked to one supplier part number
	    powerLevel -- Power in Wats to intialize a LASER module first fire to
	    maxPowerLevel -- Max power in Watts that LASER can support in continous operation (> 30 seconds)
	    brandingArt -- Black & White PNG image to brand / burn into an object

	    Return value:
	    New LASER() object
	    """

	    self.DebugObject = Debug(True, "LASER.py")

	    self.gpioFirePin = gpiozero.DigitalOutputDevice(gpioFirePin)

	    self.supplierPartNumber = supplierPartNumber

	    if(cocoPartNumber.length() != 10):
	        self.DebugObject.Dprint("Invalid part number format, please verify part number looks like XXX-YYYYY-Z")

	    # List of current valid internal LASER part numbers
	    if(cocoPartNumner == "?00-????-?" or cocoPartNumber == "?00-????-?"):
	        self.cocoPartNumber = cocoPartNumber
	    else:
	        self.DebugObject.Dprint("Invalid part number format")

	    if(0 > powerLevel or powerLevel > self.maxPowerLevel):
	        # Check for valid power level and default to 10 Watts if invalid
	        Debug.Dprint(DebugOject, "Invalid power. I'm  setting the LASER power to " + repr(self.maxPowerLevel/2) + " Watts")
	        self.powerLevel = self.maxPowerLevel/2
	    else:
	        self.powerLevel = powerLevel


	    self.brandingArt = WarpImage(LoadImage(COCOTAPS_LOGO), SIZE_100MM) # Initialize to standard CocoTaps logo

	    ConfigureLaserForNewImage()


	def LoadImage(fileName):
		"""
		Load a PNG image on the local harddrive into RAM

		Key arguments:
		filename -- PNG file to load into memory

		Return value:
		bwImg -- Black & White PNG image
		"""

		filenameLength = len(filename)
		fileExtension = substring((filenameLength - 3), filenameLength)

		if(fileExtension.toLower() == png):
			path = "../static/images/" + fileNam
			img = cv.imread(path)

			# Convert to gray scale first to apply better thresholding which will create a better black and white image
			grayImg = cv.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

			# Anything above 127 on a scale from 0 to 255 is WHITE
			(thresh, bwImg) = cv.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
		else:
			self.DebugObject.Dprint("Please pass a .png file to the LoadImage() function in LASER.py code")

		return bwImg


	def WarpImage(self, currentImage, coconutSize):
		"""
		Wrap a straight / square image so that after LASER branding on coconut its straight again

		Key arguments:
		currentImage -- Starting PNG image (TODO max size in ? x ? pixels / ?? MB)
		coconutSize -- Horizontal diameter of coconut in millimeters

		Return value:
		newImage -- A new image that has been warpped to to display correctly after LASER branding 
		"""
		# https://docs.opencv.org/2.4/doc/tutorials/core/mat_the_basic_image_container/mat_the_basic_image_container.html
        # https://pythonprogramming.net/loading-images-python-opencv-tutorial/

		img = cv.imread(currentImage)
		imgWidth = img.width
		imgHeight = img.height

		for xPixel in range(imgWidth):
			for yPixel in range(imgHeight):
				rgbColor = img.at<Vec3b>(xPixel,yPixel)
				# Split image into three part vertically and horizonatlly
				##TODO Why we need the below line? Blaze?
				### Murali this makes a new image which will be warped and we can NOT use img variable name
				# img.at<Vec3b>(xPixel,yPixel) = rgbColor
				#warppedImg.at<Vec3b>(xPixel,yPixel) = rgbColor
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


	def __ConfigureLaserForNewImage(self):
		"""
		PRIVATE FUNCATION (See __)

		Calculate pixel dwell duration based on LASER power level and image size

        Key arguments:
        filename -- PNG file to load into memory

        Return value:
        pixelBurnDuration -- Time in seconds that LASER should dwell on coconut pixel
		"""

		numOfPixels = GetNumOfPixels()
		moistureLevel = GetCoconutMoistureLevel()

		if(0 < self.powerLevel or self.powerLevel <= LOW_POWER):
			laserConstant = DEFAULT_LASER_CONSTANT * 0.5
		elif(LOW < self.powerLevel or  self.powerLevel < STANDARD_POWER):
			laserConstant = DEFAULT_LASER_CONSTANT * 1.0
		elif(self.powerLevel >= STANDARD_POWER):
			laserConstant = DEFAULT_LASER_CONSTANT * 1.5
		else:
			Debug.Lprint("ERROR: Invalid power level choosen in ConfigureLaserForNewImage() function")
		pixelBurnDuration = laserConstant * moistureLevel/100.0 * numOfPixels/1000000

		return pixelBurnDuration


	def StopLaser(self):
	    """
	    Toogle GPIO pin connected to high power relay LOW to turn OFF a LASER

	    Key arguments:
	    NONE

	    Return value:
	    NOTHING
	    """
	    gpiozero.off(self.gpioFirePin)

	def BurnImage(self, laserConfig):
		"""
		Toogle GPIO pin possibly connected to a high power relay HIGH to turn ON a LASER
		Puts CPU to sleep so NOT a threadable function yet

		Key arguments:
		laserConfig -- TODO REMOVE?

		Return value:
		NOTHING
		"""

		pixelBurnDuration = self.__ConfigureLaserForNewImage

		dutyCycle = self.powerLevel/self.maxPowerLevel
		imageBurnComplete = False
		frequency = 100                                         # Desired LASER pulse in Hz
		while(not imageBurnComplete):
			# laserConstant is a class variable
			highTime = 1/frequency  * dutyCycle * laserConstant
			sleep(highTime)                                     # Sleep upto 10 ms and keep LASER ON
			gpiozero.on(self.gpioFirePin)
			sleep(0.010 - highTime)                             # Sleep 10 ms minus time is HIGH
			gpiozero.off(self.gpioFirePin)

		imageBurnComplete = MoveLaserStepperMotor(pixelDwellDuration, frequency)


	def MoveLaserStepperMotor(frequency, motorID):
		"""

		Return value:
		NOTHING
		"""

		for pixelNum in range (0, GetNumOfPixels(filename) - 1):
			sleep(pixelDwellDuration + 1/frequency)
			#TODO if(pixelNum = )


	def SetPowerLevel(watts, cocoPartNumber):
		"""
		Set the power level based on LASER part number being used

		Key arguments:
		watts -- Power in Watts to set LASER output to
		cocoPartNumber -- Internal XXX-YYYYY-Z part number linked to a vendor part number
		"""

		if(cocoPartNumber == "205-00003-A"):
		    if(0 > watts or watts > 10):
		        Debug.Dprint(self.DebugObject, "The 400067260113 LASER must have power level between or equal to 0.1 and 10 Watts")
		    else:
		        self.powerLevel = watts
		else:
		    self.DebugObject.Dprint("This LASER supplier part number is not supported in LASER.py code base")


	def GetNumOfPixels():
		"""
		Calculate the total number of (pixels / 1,000,000) that is in an image file

		Key argument:
        NONE

		Return value:
		totalNumOfPixels -- Total number of megapixels (million pixels) in an image
		"""

		#img = LoadLImage(self.brandingArt #TODO DOES LoadImage RETURN a img variable)
		img = cv.imread(self.brandingArt)
		imgWidth = img.width
		imgHeight = img.height
		totalNumOfPixels = imgWidth * imgHeight

		return totalNumOfPixels


	def GetCoconutMoistureLevel():
		"""
		Moisture level from 0 to 100 corresponing to % humidity

    	Key arguments:
    	NONE

    	Return value:
    	moisturePercentage -- An float from 0.0 to 100.0
		"""

	    #TODO Moisture sensor in fridge
		print("TODO I2C sensor")
		moisturePercentage = 100
		return moisturePercentage


	if __name__ == "__main__":
		LaserDebugObject = Debug(True, "LASER.py")
		LaserDebugObject.Dprint("Running LASER.py main unit test")

		laserConfig = 1
		#TestLASERobject = LASER(RaspPi.BOARD7, "40004672601138", "205-0003-A", STANDARD_POWER, 10, COCOTAPS_LOGO)

		TestLASERobject.ConfigureLaserForNewImage()
		TestLASERobject.BurnImage(laserConfig)
		time.sleep(10) 										# Pause 10 seconds

		StopLASER()
