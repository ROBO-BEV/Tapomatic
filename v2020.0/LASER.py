#!/usr/bin/env python3
"""
__author__  = "Blaze Sanders"
__email__   = "blaze@cocotaps.com"
__company__ = "CocoTaps"
__status__  = "Development"
__date__    = "Late Updated: 2020-07-05"
__doc__     = "Class to control and move LASER system"
"""

# Allow program to extract filename of the current file
import os

# Allow program to create GMT and local timestamps and pause program execution
from time import gmtime, strftime, sleep

# Custom CocoTaps and Robotic Beverage Technologies code
from Debug import *             # Configure datalogging parameters and debug printing control
from CocoDrink import *        	# Stores valid CoCoTaps drink configurations
from RaspPi import *            # Contains usefull GPIO pin CONSTANTS and setup configurations

# Computer Vision modules to edit / warp images
#import numpy as np     #TODO REMOVE SINCE IM NOT USE ARRAY ANY MORE
#import cv2 as cv       #TODO REMOVE SINCE MAKING SIMPLER IS DUMB!
import cv2


try:
    # Allow control of output devices such as LEDs and Relays
    from gpiozero import LED, OutputDevice
    #from gpiozero import Energenize #TODO REMOVE SINCE TOO SPECIFIC???

except ImportError:
    #TODO DO LOW LEVEL PIN CONTROL THAT WORKS EVER WHERE? http://wiringpi.com/the-gpio-utility/
    currentProgramFilename = os.path.basename(__file__)
    TempDebugObject = Debug(True, "Try/Catch ImportError in " + currentProgramFilename)
    TempDebugObject.Dprint("WARNING - You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")
    
    
class LASER:

	# Preset LASER power level CONSTANTS (units are Watts)
	HIGH_POWER = 10.00
	STANDARD_POWER = 5.00
	LOW_POWER = 2.50
	MAX_POWER_LEVEL = HIGH_POWER
	DEFAULT_LASER_CONSTANT = 0.05264472  	#TODO Adjust this until LASER branding looks good

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
	    
	    currentProgramFilename = os.path.basename(__file__)
	    self.DebugObject = Debug(True, currentProgramFilename)
	    
	    #self.gpioFirePin = gpiozero.OutputDevice(gpioFirePin)

	    self.supplierPartNumber = supplierPartNumber

	    if(len(cocoPartNumber) != 10):
	        self.DebugObject.Dprint("Invalid part number format, please verify part number looks like XXX-YYYYY-Z")

	    # List of current valid internal LASER part numbers
	    if(cocoPartNumber == "205-0003-A" or cocoPartNumber == "???-????-?"):
	        self.cocoPartNumber = cocoPartNumber
	    else:
	        self.DebugObject.Dprint("Invalid part number format")

	    if(0 > powerLevel or powerLevel > LASER.MAX_POWER_LEVEL):
	        # Check for valid power level and default to 10 Watts if invalid
	        Debug.Dprint(DebugOject, "Invalid power. I'm  setting the LASER power to " + repr(self.maxPowerLevel/2) + " Watts")
	        self.powerLevel = self.MAX_POWER_LEVEL/2
	    else:
	        self.powerLevel = powerLevel

	    self.brandingArt = LASER.__WarpImage(CocoDrink.COCOTAPS_LOGO, CocoDrink.SIZE_102MM) # Initialize to standard CocoTaps logo
	    
	    LASER.__ConfigureLaserForNewImage(self.brandingArt)


	def LoadImage(fileName):
		"""

		Key arguments:
		filename -- PNG file to load into memory

		Return value:
		bwImg -- Black & White PNG image
		"""

		return bwImg


	def __WarpImage(fileName, coconutSize):
		"""
		Load a PNG image on the local harddrive into RAM
		Wrap a straight / square image so that after LASER branding on coconut its straight again

		Key arguments:
		fileName -- PNG file to load into memory (TODO max size in ? x ? pixels / ?? MB)
		coconutSize -- Horizontal diameter of coconut in millimeters

		Return value:
		newImage -- A new image that has been warpped to to display correctly after LASER branding 
		"""
		
		# https://docs.opencv.org/2.4/doc/tutorials/core/mat_the_basic_image_container/mat_the_basic_image_container.html
        # https://pythonprogramming.net/loading-images-python-opencv-tutorial/

		fileNameLength = len(fileName)
		periodIndex = fileNameLength - 3
		fileExtension = fileName[periodIndex:]

		if(fileExtension.lower() == "png"):
			path = "static/images/" + fileName
			originalImage = cv2.imread(path)

			# Convert to gray scale first to apply better thresholding which will create a better black and white image
			grayImg = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

			# Anything above 127 on a scale from 0 to 255 is WHITE
			(thresh, bwImg) = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)
		else:
			self.DebugObject.Dprint("Please pass a .png file to the LoadImage() function in LASER.py code")


		imgWidth = originalImage.size
		imgHeight = originalImage.size


		for xPixel in range(imgWidth):
		    print("xPixel = ", xPixel)
		    for yPixel in range(imgHeight):
   			    print("yPixel = ", yPixel)
   			    print(" of ", imgHeight)
   			    #TODO rgbColor = originalImage.at<Vec3b>(xPixel,yPixel)
				# Split image into three part vertically and horizonatlly
				### TODO SyntaxError: can't assign to comparison 
				# warppedImg.at<Vec3b>(xPixel,yPixel) = rgbColor

   			    if(xPixel < (imgWidth/5)):
   			        xPixel = xPixel + 8		# Skip EIGHT pixels since ends warps more at ends
   			    elif((imgWidth/5) <= xPixel and xPixel < (imgWidth*2/5)):
   			    	xPixel = xPixel + 4		# Skip EIGHT pixels since ends wraps more at ends
   			    elif((imgWidth*2/5) <= xPixel and xPixel < (imgWidth*3/5)):
   			    	xPixel = xPixel + 0		# Skip EIGHT pixels since ends wraps more at ends
   			    elif((imgWidth*3/5) <= xPixel and xPixel < (imgWidth*4/5)):
   			    	xPixel = xPixel + 4		# Skip EIGHT pixels since ends wraps more at ends
   			    elif((imgWidth*4/5) <= xPixel and xPixel < (imgWidth)):
   			        xPixel = xPixel + 8		# Skip EIGHT pixels since ends wraps more at ends


	def __ConfigureLaserForNewImage(img):
		"""
		PRIVATE FUNCATION (See __)

		Calculate pixel dwell duration based on LASER power level and image size

        Key arguments:
        img -- PNG file to load into memory

        Return value:
        pixelBurnDuration -- Time in seconds that LASER should dwell on coconut pixel
		"""

		numOfPixels = LASER.__GetNumOfPixels(img)
		moistureLevel = GetCoconutMoistureLevel()

		if(0 < self.powerLevel or self.powerLevel <= LOW_POWER):
			laserConstant = DEFAULT_LASER_CONSTANT * 0.5
		elif(LOW < self.powerLevel or  self.powerLevel < STANDARD_POWER):
			laserConstant = DEFAULT_LASER_CONSTANT * 1.0
		elif(self.powerLevel >= STANDARD_POWER):
			laserConstant = DEFAULT_LASER_CONSTANT * 1.5
		else:
			self.DebugObject.Lprint("ERROR: Invalid power level choosen in ConfigureLaserForNewImage() function")

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
	    self.gpioFirePin.off()
	    #gpiozero.off(self.gpioFirePin)


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
			self.gpioFirePin.on()
			sleep(0.010 - highTime)                             # Sleep 10 ms minus time is HIGH
			self.gpioFirePin.off()

		imageBurnComplete = MoveLaserStepperMotor(pixelDwellDuration, frequency)


	def MoveLaserStepperMotor(self, frequency, motorID):
		"""

		Return value:
		NOTHING
		"""

		for pixelNum in range (0, GetNumOfPixels(filename) - 1):
			sleep(pixelDwellDuration + 1/frequency)
			#TODO if(pixelNum = )


	def SetPowerLevel(self, watts, cocoPartNumber):
		"""
		Set the power level based on LASER part number being used

		Key arguments:
		watts -- Power in Watts to set LASER output to
		cocoPartNumber -- Internal XXX-YYYYY-Z part number linked to a vendor part number
		"""

		if(cocoPartNumber == "205-00003-A"):
		    if(0 > watts or watts > 10):
		        self.DebugObject.Dprint(self.DebugObject, "The 400067260113 LASER must have power level between or equal to 0.1 and 10 Watts")
		    else:
		        self.powerLevel = watts
		else:
		    self.DebugObject.Dprint("This LASER supplier part number is not supported in LASER.py code base")


	def __GetNumOfPixels(inputImage):
		"""
		Calculate the total number of (pixels / 1,000,000) that is in an image file

		Key argument:
        inputImage

		Return value:
		totalNumOfPixels -- Total number of megapixels (million pixels) in an image
		"""

		#img = LoadLImage(self.brandingArt #TODO DOES LoadImage RETURN a img variable)
		img = cv2.imread(inputImage)
		imgWidth = img.width
		imgHeight = img.height
		totalNumOfPixels = imgWidth * imgHeight

		return totalNumOfPixels


	def GetCoconutMoistureLevel(self):
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
		
	
	def CompileImageAndStoreToEMMC():
	    """
	    
	    Key arguments:
	    NONE
	    
	    Return value:
	    NOTHING
	    """
	    
	    LASER.__WarpImage()
                
        
        

if __name__ == "__main__":

    currentProgramFilename = os.path.basename(__file__)
    LaserDebugObject = Debug(True, currentProgramFilename)
    LaserDebugObject.Dprint("Running LASER.py main unit test")
    
    #laserConfig = -1
    TestLASERobject = LASER(RaspPi.BOARD7, "40004672601138", "205-0003-A", LASER.STANDARD_POWER, 10, CocoDrink.COCOTAPS_LOGO)
    
    TestLASERobject.ConfigureLaserForNewImage()
    TestLASERobject.BurnImage(laserConfig)
    time.sleep(10) 										# Pause 10 seconds
    
    StopLASER()
