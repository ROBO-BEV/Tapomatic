#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import pyautogui

import cv2

import serial

HIGH = 1
LOW = 0

BACARDI_LOGO = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV0.png'
COCOTAPS_LOGO ='/home/pi/Tapomatic/v2020.0/static/images/CocoTapsLogoV0.png'
WHITE_LOGO = '/home/pi/Tapomatic/white.png'

DWELL_CONSTANT = 0.02132 #0.015 or 0.150 or 0.02132 ms
CARRIAGE_RETURN_DELAY_DURATION = 5.33
MID_GRAY_VALUE = 127

LASER_FIRE_PIN = 7
ORANGE_FLAVOR_PIN = 15
PINEAPPLE_FLAVOR_PIN = 31
PINA_COLADA_FLAVOR_PIN = 37

PUMP_CONSTANT = 2

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

def WriteImage(path):
	"""
	Convert any .PNG or .JPEG image to Grayscale and write image data to harddrive

	Key arguments:
	path -- Full filename pathway on  Raspberry pi (i.e. /home/pi/???)

	Return Value:
	Grayscale image object
	"""

	img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
	cv2.imwrite('SavedImage.png', img)

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

	cv2.imshow('Color', originalImage)
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

	#path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV0.png'
	path = WHITE_LOGO
	grayScaleImage = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	print('Dimensions: ', grayScaleImage.shape)
	imgHeight, imgWidth =  grayScaleImage.shape
	print('Height: ', imgHeight)
	print('Width: ', imgWidth)

	cv2.imshow('GrayScale', grayScaleImage)
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

	cv2.imshow('B&W', bwImage)
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

	imgHeight, imgWidth =  img.shape
	totalPixels = imgHeight * imgWidth
	highPixel = 0
	medPixel = 0
	lowPixel = 0
	print('Total Number Of Pixels: ', totalPixels)

	endOfRow = False
	ser = serial.Serial()
	#ser.baudrate = 115200
	#ser.port = '/dev/ttyUSB0'
	#ser.open()
	#serDrill = '/dev/ttylUSB1'
	#print(ser.name)

	#ser.write("?".encode)

	totalTime = 0

	for yPixel in range(50, 167):  #(imgHeight)
		#print("yPixel: ", yPixel)

		for xPixel in range(imgWidth):
			bwColor = img[yPixel, xPixel]

			#print('xPixel: ', xPixel)
			#if(60 < xPixel and xPixel < 160):
				#if(yPixel== 93):
					#print('X: ', xPixel)
					#print('Y: ', yPixel)
					#print('B&W Shade: ', bwColor)

			if((imgWidth - 1) == xPixel):
				endOfRow = True

			pixelDwellDuration = ((255 - bwColor) / 255) * DWELL_CONSTANT

			if(bwColor >= MID_GRAY_VALUE):
				#print('NOT BURN: ', bwColor)
				GPIO.output(LASER_FIRE_PIN, LOW)
				MoveLaserStepperMotor(ser, DWELL_CONSTANT, endOfRow, yPixel, imgWidth)
				lowPixel = lowPixel + 1
			else:
				#print('PIXEL BURN: ', bwColor)
				GPIO.output(LASER_FIRE_PIN, HIGH)
				MoveLaserStepperMotor(ser, pixelDwellDuration, endOfRow, yPixel, imgWidth)
				highPixel = highPixel + 1

			#if(pixelDwellDuration <= 55 * DWELL_CONSTANT):
			#	totalTime = totalTime + DWELL_CONSTANT
			#else:
			#	totalTime = totalTime + pixelDwellDuration
			#print('Subtotal LASER Time: ', totalTime)
			endOfRow = False

	ser.close()
	print('LOW PERCENTAGE: ', lowPixel/totalPixels)
	print('MED PERCENTAGE: ', medPixel/totalPixels)
	print('HIGH PERCENTAGE: ', highPixel/totalPixels)
	print('TOTAL LASER ON TIME: ', totalTime)


def MoveLaserStepperMotor(ser, dwellDuration, endOfRow, yPixel, imgWidth):
	"""
	Send G-Code command our serial USB to CNC motor controller

	Key arguments:
	ser  -- serial port object to send G-Code command to
	dwellDuration -- Duration of time in seconds to pause movement of LASER head on each pixel
	endOfRow -- Boolean variable to determine when LASER head is at end of x (or column) equal to imgWidth
	yPixel -- Current y (or row) location of LASER head
	imgWidth -- Final x (or column) location LASER head should move to

	Return value:
	NOTHING
	"""
	if(endOfRow):
		#print('PERFORM CARRIAGE RETURN')
		gCode = "G0 X0 Y" + str(yPixel+1)
		print(gCode)
		time.sleep(CARRIAGE_RETURN_DELAY_DURATION)
	else:
		#print('MOVE HORIZTONAL')
		gCode = "G0 X" + str(imgWidth) + "Y" + str(yPixel)
		time.sleep(dwellDuration)

	# https://www.cnc4fun.com/wp-content/uploads/2019/12/Grbl-Commands-v1.1-2.pdf
	# https://www.robotshop.com/community/forum/t/can-one-arduino-resent-serial-com-to-another-arduino/10602/7
	# https://github.com/grbl/grbl/wiki/Interfacing-with-Grbl
	# http://www.bachinmaker.com/index.php?p=85&a=view&r=23
	
	##ser.write(gCode.encode()) 		# Encode G0 X? Y? string into byte data

def FindFirstBurnPixel(img):
	imgHeight, imgWidth =  img.shape
	doneSearching = False

	for yPixel in range(imgHeight):
		for xPixel in range(imgWidth):
			bwColor = img[yPixel, xPixel]
			if(bwColor < MID_GRAY_VALUE and (not doneSearching)): #BURN PIXEL
				doneSearching = True
				firstX = xPixel
				firstY = yPixel

	return firstX, firstY


def FindLastBurnPixel(img):
	imgHeight, imgWidth =  img.shape

	for yPixel in range(imgHeight):
		for xPixel in range(imgWidth):
			bwColor = img[yPixel, xPixel]
			if(bwColor < MID_GRAY_VALUE): # BURN PIXEL
				lastX = xPixel
				lastY = yPixel

	return lastX, lastY



def PumpFlavor(flavorPin, volume):
	"""
	Turn on pump corresponding to select flavor

	Key arguments:
	flavorPin -- GPIO pin to toggle high
	volume - Amount of liquid to pump in units of Ounces

	Return value:
	NOTHING
	"""
	GPIO.output(flavorPin, HIGH)
	time.sleep(volume*PUMP_CONSTANT)
	GPIO.output(flavorPin, LOW)


if __name__ == "__main__":

	screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.
	print('SCREEN SIZE: ', screenWidth, screenHeight )
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LASER_FIRE_PIN, GPIO.OUT, initial=GPIO.LOW)

	##OpenColorImage()
	#OpenGrayScaleImage()
	##OpenBlackWhiteImage()

	print('FIRST PIXEL: ', FindFirstBurnPixel(LoadImage(BACARDI_LOGO)))
	print('LAST PIXEL: ', FindLastBurnPixel(LoadImage(BACARDI_LOGO)))

	#BurnImage(LoadImage(WHITE_LOGO))
	#WriteImage(BACARDI_LOGO)
 	pyautogui.click(100, 200)  # Move the mouse to XY coordinates in Candle GUI and click  it
 	BurnImage(LoadImage(BACARDI_LOGO))

	# Relays
	GPIO.setup(ORANGE_FLAVOR_PIN, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PINEAPPLE_FLAVOR_PIN, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PINA_COLADA_FLAVOR_PIN, GPIO.OUT, initial=GPIO.LOW)

	PumpFlavor(ORANGE_FLAVOR_PIN, 1.5)

	time.sleep(3)

	GPIO.cleanup()
