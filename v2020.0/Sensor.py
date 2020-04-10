import time


class Sensor():

	# Wire value CONTSTANTS 
	# Raspberry Pi 4 Pin Layout https://pinout.xyz/pinout/pin1_3v3_power
	NO_PIN = -1  						#TODO This constant may not be needed :)
	NO_WIRE = 0
	VCC_3_3V = 1
	VCC_3_3V_NAME = "BOARD1"     		# 3.3 Volts @ upto 0.050 Amps = 0.165 Watts https://pinout.xyz/pinout/pin1_3v3_power
	VCC_5V = 2
	VCC_5V_NAME = "BOARD2"        		# 5 Volts @ upto ~1.5 Amps (Power Adapter - Pi usgae) = 7.5 Watts https://pinout.xyz/pinout/pin2_5v_power
	I2C_SDA = 3					
	I2C_SDA_NAME = "BOARD3"				# Fixed, 1.8 kohms pull-up to 3.3v https://pinout.xyz/pinout/pin3_gpio2
	I2C_SCL = 5
	I2C_SDA_NAME = "BOARD5"				# Fixed, 1.8 kohms pull-up to 3.3v https://pinout.xyz/pinout/pin5_gpio3
	TXD = 8
	TXD_NAME = "BOARD8" 				# UART transmit pin / Serial Port https://pinout.xyz/pinout/pin8_gpio14 
	RXD = 10	
	RXD_NAME = "BOARD10" 				# UART recieve pin / Serial Port https://pinout.xyz/pinout/pin10_gpio15					
	GND = "BOARD6&9&14&20&25&30&34&39"	# Digital Ground (0 Volts) https://pinout.xyz/pinout/ground
	PWM0 = 12
	PWM0_NAME = "BOARD12"				#Pulse Width Modulation https://pinout.xyz/pinout/pin12_gpio18 

def __init__(self, currentNumOfSensors, sType, pins, partNumber):
		wires = numpy.empty(len(pins), dtype=object)   # TODO wires = ndarray((len(pins),),int) OR wires = [None] * len(pins) 				# Create an array on same length as pins[?, ?, ?]
		for i in pins:
			self.wires[i] = pins[i]
		self.sensorType = sType
		currentNumOfActuators += 1
		self.sensorID = currentNumOfSensors# Auto-incremented interger class variable
		self.partNumber = partNumber
		
		
	


def GetLevel(lType):
if(lType == CocoDrink.ORANGE_JUICE):
  liquidWeightAt100percent = #Units are Newtons
GetForce/liquidWeightAt100percent
    return percentage


Degraw 5kg Load Cell and HX711 Combo Pack Kit - Load Cell Amplifier ADC Weight Sensor for Arduino Scale - Everything Needed for Accurate Force Measurement https://www.amazon.com/dp/B075317R45/ref=cm_sw_r_cp_api_i_Ph7JEb5A1F12M

https://github.com/aguegu/ardulibs/
HX711 datasheet: https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf
https://www.youtube.com/watch?v=nGUpzwEa4vg

def GetForce():
SCK
DT

    return forceInNewtons

def IsLaserSafetyGridSafe():
    status = false

    #TODO 

    return status


