#!/usr/bin/python3

import  RPi.GPIO as GPIO
import time

HIGH = 1
LOW = 0


if __name__ == "__main__":
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

	##GPIO.cleanup(7)
	##GPIO.cleanup(15)
	##GPIO.cleanup(19)
	##GPIO.cleanup(22)

	GPIO.output(7, LOW)
	GPIO.output(37, LOW)
