#!/usr/bin/python3

import  RPi.GPIO as GPIO
import time
import numpy

import cv2
#from CocoDrink import *

HIGH = 1
LOW = 0

def LoadColorImage():
	path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV1.png'
	originalImage = cv2.imread(path)

	print('Dimensions: ', originalImage.shape)
	imgHeight, imgWidth, colorChannels = originalImage.shape
	print('Height: ', imgHeight)
	print('Width: ', imgWidth)
	print('Color Channels: ', colorChannels)

	#cv2.imshow('image',originalImage)

	return originalImage

def LoadGrayScaleImage():
	path = '/home/pi/Tapomatic/v2020.0/static/images/BacardiLogoV1.png'
	grayScaleImage = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	print('Dimensions: ', grayScaleImage.shape)
	imgHeight, imgWidth =  grayScaleImage.shape
	print('Height: ', imgHeight)
	print('Width: ', imgWidth)

	#cv2.imshow('image',originalImage)

	return grayScaleImage


if __name__ == "__main__":

	LoadColorImage()
	LoadGrayScaleImage()

	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
	#GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
	#GPIO.setup(31, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(37, GPIO.OUT, initial=GPIO.LOW)

	GPIO.output(7, HIGH)
	#GPIO.output(15, HIGH)
	#GPIO.output(31, HIGH)
	GPIO.output(37, HIGH)

	time.sleep(3)

	GPIO.cleanup()
	##GPIO.cleanup(15)
	##GPIO.cleanup(31)
	##GPIO.cleanup(37)
