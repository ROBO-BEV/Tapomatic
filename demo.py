#!/usr/bin/python3

import  RPi.GPIO as GPIO
import time
import numpy

import cv2
#from CocoDrink import *

import multiprocessing as mp

HIGH = 1
LOW = 0

def LoadColorImage():
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

	#return originalImage

def LoadGrayScaleImage():
	path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV0.png'
	grayScaleImage = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	print('Dimensions: ', grayScaleImage.shape)
	imgHeight, imgWidth =  grayScaleImage.shape
	print('Height: ', imgHeight)
	print('Width: ', imgWidth)

	#cv2.imshow('Gray Image', grayScaleImage)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	return grayScaleImage

def LoadBlackWhiteImage():
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

	return bwImage


def BurnImage(img, laserConstant):
	"""
	Toogle GPIO pin possibly connected to a high power relay HIGH to turn ON a LASER
	Puts CPU to sleep so NOT a threadable function yet

	Key arguments:
	laserConfig -- TODO REMOVE?

	Return value:
	NOTHING
	"""
	pixelBurnDuration = 0.015

	dutyCycle = 100
	frequency = 100                                         # Desired LASER pulse in Hz

	imageBurnComplete = False
	pixelNum = 1

	path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV0.png'
	grayScaleImage = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	imgHeight, imgWidth =  grayScaleImage.shape
	totalPixels = imgHeight * imgWidth
	print('Total Number Of Pixels: ', totalPixels)

	highTime = 1/frequency  * dutyCycle * laserConstant
	print('High Time: ', highTime)
	print('Low Time: ', highTime - (1/frequency))

	while(not imageBurnComplete):

		#https://www.machinelearningplus.com/python/parallel-processing-python/
		pool = mp.Pool(2)
		results = pool.apply(MoveLaserStepperMotor, args=(totalPixels, pixelDwellDuration, frequency))

	pool.close

		time.sleep(highTime)
		GPIO.output(7, HIGH)
		time.sleep(highTime - (1/frequency))
		GPIO.output(7, LOW)

		#imageBurnComplete = MoveLaserStepperMotor(pixelDwellDuration, frequency)
		pixelNum = pixelNum + 1
		if(pixelNum >= totalPixel):
			imageBurnComplete = True


def MoveLaserStepperMotor(pixelDwellDuration, frequency):
	print('NOT DONE')

if __name__ == "__main__":

	print("Number of processors: ", mp.cpu_count())

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)

	LoadColorImage()
	LoadGrayScaleImage()
	LoadBlackWhiteImage()
	BurnImage(LoadGrayScaleImage, 1.0)

	# Relays
	#GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
	#GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW)
	#GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

	GPIO.output(7, HIGH)
	#GPIO.output(15, HIGH)
	#GPIO.output(31, HIGH)
	GPIO.output(37, HIGH)

	time.sleep(3)

	GPIO.cleanup()
	##GPIO.cleanup(15)
	##GPIO.cleanup(31)
	##GPIO.cleanup(37)
