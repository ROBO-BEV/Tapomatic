#!/usr/bin/python3

import  RPi.GPIO as GPIO
import time
#import numpy

import cv2

import serial
#from CocoDrink import *


HIGH = 1
LOW = 0

BACARDI_LOGO = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV0.png'
COCOTAPS_LOGO ='/home/pi/Tapomatic/v2020.0/static/images/CocoTapsLogoV0.png'

LASER_FIRE_PIN = 7
ORANGE_FLAVOR_PIN = 15
PINEAPPLE_FLAVOR_PIN = 31
PINA_COLADA_FLAVOR_PIN = 37


def LoadImage(path):
	"""
	Convert any .PNG or .JPEG image to Grayscale and return image data

	Key arguments:
	path -- Full filename pathway on  Raspberry pi (i.e. /home/pi/???)

	Return Value:
	Grayscale image object
	"""

	img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	return img

def OpenColorImage():
	"""
	Open any .PNG or .JPEG  image without conversion in new window until keyboard press

	Key arguments:
	NONE

	Return value:
	Grayscale  image object
	"""
	path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV0.png'
	originalImage = cv2.imread(path)

	print('Dimensions: ', originalImage.shape)
	imgHeight, imgWidth, colorChannels = originalImage.shape
	print('Height: ', imgHeight)
	print('Width: ', imgWidth)
	print('Color Channels: ', colorChannels)

	cv2.imshow('Color Image', originalImage)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def OpenGrayScaleImage():
	"""
	Convert Color image to Grayscale and display in new window until keyboard press

	Key arguments:
	NONE

	Return value:
	Grayscale  image object
	"""

	path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV0.png'
	grayScaleImage = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	print('Dimensions: ', grayScaleImage.shape)
	imgHeight, imgWidth =  grayScaleImage.shape
	print('Height: ', imgHeight)
	print('Width: ', imgWidth)

	cv2.imshow('Gray Image', grayScaleImage)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def OpenBlackWhiteImage():
	"""
	Convert Color image to Grayscale to Black & White and display in new window until keyboard button press

	Key arguments:
	NONE

	Return value:
	Black and White image object
	"""

	path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV1.png'
	originalImage = cv2.imread(path, cv2.IMREAD_UNCHANGED)


	# Convert to gray scale first to apply better thresholding which will create $                        grayImg = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
	grayImg = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

	# Anything above 127 on a scale from 0 to 255 is WHITE
	(thresh, bwImage) = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)

	print('Dimensions: ', bwImage.shape)
	imgHeight, imgWidth =  bwImage.shape
	print('Height: ', imgHeight)
	print('Width: ', imgWidth)

	cv2.imshow('B & W Image', bwImage)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def BurnImage(img):
	"""
	Toogle GPIO pin connected to a high power relay HIGH to turn ON a LASER
	Puts CPU to sleep so NOT a threadable function yet

	Key arguments:
	img -- GrayScale (two return parameter) image to load into RAM and analysis using OpenCV

	Return value:
	NOTHING
	"""
	pixelDwellDuration = 0.0015			# 1.5 ms

	imgHeight, imgWidth =  img.shape
	totalPixels = imgHeight * imgWidth
	print('Total Number Of Pixels: ', totalPixels)

	endOfRow = False
	ser = serial.Serial('/dev/ttyUSB0')
	print(ser.name)

	for yPixel in range(imgHeight):
		#print('yPixel: ', yPixel)

		for xPixel in range(imgWidth):
			#print('xPixel: ', xPixel)

			bwColor = img[yPixel, xPixel]
			if((imgWidth - 1) == xPixel):
				endOfRow = True

			if(bwColor >= 170):
				#print('IMAGE BURN: ', bwColor)
				MoveLaserStepperMotor(ser, pixelDwellDuration, endOfRow, yPixel, xPixel)
			elif(bwColor >= 85):
				#print('IMAGE BURN 50%: ', bwColor)
				MoveLaserStepperMotor(ser, pixelDwellDuration/2, endOfRow, yPixel, xPixel)
			else:
				#print('NOT BURN', bwColor)
				MoveLaserStepperMotor(ser, 0, endOfRow, yPixel, xPixel)

			endOfRow = False

def MoveLaserStepperMotor(ser, dwellDuration, endOfRow, yPixel, xPixel):
	"""
	Send G-Code command our serial USB to CNC motor controller

	Key arguments:
	ser  -- serial port object to send G-Code command to
	dwellDuration -- Duration of time in seconds to pause movement of LASER head on each pixel
	endOfRow -- Boolean variable to determine when LASER head is at end of image row
	yPixel -- Current y (or row) location of LASER head
	xPixel -- Current x or (column) location of LASER head

	Return value:
	NOTHING
	"""
	if(endOfRow):
		#print('PERFORM CARRIAGE RETURN')
		gCode = "G0 X0 Y" + str(yPixel)
		#print(gCode)
		time.sleep(dwellDuration)
	else:
		#print('MOVE HORIZTONAL')
		gCode = "G0 X" + str(xPixel) + "Y" + str(yPixel)
		time.sleep(dwellDuration)

	ser.write(gCode.encode()) 		# Encode G0 X? Y? string into byte data


def PumpFlavor(flavorID):


if __name__ == "__main__":

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LASER_FIRE_PIN, GPIO.OUT, initial=GPIO.LOW)

	##LoadColorImage()
	##LoadGrayScaleImage()
	##LoadBlackWhiteImage()
	BurnImage(LoadImage(BACARDI_LOGO))

	# Relays
	##GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
	##GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
	##GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW)
	##GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

	##GPIO.output(7, HIGH)
	##GPIO.output(15, HIGH)
	##GPIO.output(31, HIGH)
	##GPIO.output(37, HIGH)

	time.sleep(3)

	GPIO.cleanup()
	##GPIO.cleanup(15)
	##GPIO.cleanup(31)
	##GPIO.cleanup(37)
