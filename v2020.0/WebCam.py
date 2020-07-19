#!/usr/bin/env python3
"""
__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-07-05"
__doc__ =     "Class to define flavors and health additivies in a CocoTaps coconut drink"
"""
from MyQR import myqr
# Allow program to extract filename of the current file
import os

class WebCam():
	#COCOTAPS URL
	COCOTAPS_URL = 'https://www.cocotaps.com/'




	# Drink Name CONSTANTS
	NONE = "NONE"
	NO_DRINK = 0
	COCONUT = 1
	MAX_DRINK_NAME = COCONUT
	
	# Coconut sizing CONSTANTS
	SIZE_102MM = 102
	SIZE_88MM = 88
	
	# Addon Name CONSTANTS                  #TODO CONVERT INTERGERS TO STRINGS???
	IMMUNITY_BOOST = 1
	DAILY_VITAMINS = 2
	ENERGY_BOOST = 3
	PINA_COLADA = 4
	PINEAPPLE_FLAVOR = 5
	ORANGE_FLAVOR = 6
	MAX_ADD_ON_NAME = ORANGE_FLAVOR

	# QR Strings
	IMMUNITY_BOOST = 'IMMUNITY_BOOST'
	DAILY_VITAMINS = 'DAILY_VITAMINS'
	ENERGY_BOOST = 'ENERGY_BOOST'
	PINA_COLADA = 'PINA_COLADA'
	PINEAPPLE_FLAVOR = 'PINEAPPLE_FLAVOR'
	ORANGE_FLAVOR = 'ORANGE_FLAVOR'

	QRCODES_DIR = os.getcwd()+'/QRCodes'


	def generateQR(self, QRWord, picture):
		#Generate the MYQR code word based.
		version, level, qr_name = myqr.run(
			QRWord,
			version=10,
			level='H',
			picture=picture,
			colorized=True,
			contrast=1.5,
			brightness=1.6,
			save_name=None,
			save_dir=self.QRCODES_DIR
		)
		return

	def generateQRCodeForImmunityBoost(self):
		self.generateQR(self.COCOTAPS_URL + self.IMMUNITY_BOOST,'static/QRImages/'+'immunity_boost.png')
		return

	def generateQRCodeForDailyVitamins(self):
		self.generateQR(self.COCOTAPS_URL + self.DAILY_VITAMINS,'static/QRImages/'+'daily_vitamins.jpg')
		return

	def generateQRCodeForEnergyBoost(self):
		self.generateQR(self.COCOTAPS_URL + self.ENERGY_BOOST,'static/QRImages/'+'energy_boost.jpg')
		return

	def generateQRCodeForPinaColada(self):
		self.generateQR(self.COCOTAPS_URL + self.PINA_COLADA,'static/QRImages/'+'pina_colada.jpg')
		return

	def generateQRCodeForPineappleFlavor(self):
		self.generateQR(self.COCOTAPS_URL + self.PINEAPPLE_FLAVOR,'static/QRImages/'+'pineapple_flavor.jpg')
		return

	def generateQRCodeForOrangeFlavor(self):
		self.generateQR(self.COCOTAPS_URL + self.ORANGE_FLAVOR,'static/QRImages/'+'orange_flavor.jpg')
		return

if __name__ == "__main__":
	object = WebCam()
	object.generateQRCodeForImmunityBoost()
	object.generateQRCodeForDailyVitamins()
	object.generateQRCodeForEnergyBoost()
	object.generateQRCodeForPinaColada()
	object.generateQRCodeForPineappleFlavor()
	object.generateQRCodeForOrangeFlavor()




