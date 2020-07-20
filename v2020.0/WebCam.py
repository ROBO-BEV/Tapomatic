#!/usr/bin/env python3
"""
__author__ =  "Murali ???"
__email__ =   "m@beepbeeptechinc.com"
__company__ = "CocoTaps"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-07-19"
__doc__ =     "Class to create QR codes for drinks and control USB camera to scan them"
"""

# See https://github.com/sylnsfar/qrcode
from MyQR import myqr

# Allow program to extract filename of the current file
import os

# Custom CocoTaps and Robotic Beverage Technologies Inc code
from CocoDrink import *         # Store valid CoCoTaps drink configurations


class WebCam:

	# CocoTaps  URL
	COCOTAPS_URL = 'https://www.cocotaps.com/'

	# QR Strings
	# IMMUNITY_BOOST = 'IMMUNITY_BOOST'
	# DAILY_VITAMINS = 'DAILY_VITAMINS'
	# ENERGY_BOOST = 'ENERGY_BOOST'
	# PINA_COLADA = 'PINA_COLADA'
	# PINEAPPLE_FLAVOR = 'PINEAPPLE_FLAVOR'
	# ORANGE_FLAVOR = 'ORANGE_FLAVOR'

	QRCODES_DIR = os.getcwd()+'/QRCodes'


	def generateQR(self, QRword, picture):
		"""
		Generate a word based  MYQR code 
		
		Key arguments:
		QRword -- Data to encode into QR code dots
		picture -- Background image to embed behind QR code dots 
		
		Return value:
		??? --
		"""
		
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
		"""
		I think we can delete all these functions and add swtich statement to main generateQR function -BLAZE
		
		Generate QR code with CONSTANT INT IMMUNITY_BOOST encoded into dots
		
		Key argmuments:
		NONE
		
		Return value:
		immunity_boost.png -- Image created and stored in "static/QRImages" directory 
		"""
		
		self.generateQR(CocoDrink.IMMUNITY_BOOST,'static/QRImages/'+'immunity_boost.png')
		
		return


	def generateQRCodeForDailyVitamins(self):
		"""
		Adding URL makes data more ???
		
		"""
		self.generateQR(self.COCOTAPS_URL + CocoDrink.DAILY_VITAMINS,'static/QRImages/'+'daily_vitamins.jpg')
		return          #WHY EMPTY RETURN

	def generateQRCodeForEnergyBoost(self):
		self.generateQR(self.COCOTAPS_URL + CocoDrink.ENERGY_BOOST,'static/QRImages/'+'energy_boost.jpg')
		return

	def generateQRCodeForPinaColada(self):
		self.generateQR(self.COCOTAPS_URL + CocoDrink.PINA_COLADA,'static/QRImages/'+'pina_colada.jpg')
		return

	def generateQRCodeForPineappleFlavor(self):
		self.generateQR(self.COCOTAPS_URL + CocoDrink.PINEAPPLE_FLAVOR,'static/QRImages/'+'pineapple_flavor.jpg')
		return

	def generateQRCodeForOrangeFlavor(self):
		self.generateQR(self.COCOTAPS_URL + CocoDrink.ORANGE_FLAVOR,'static/QRImages/'+'orange_flavor.jpg')
		return


if __name__ == "__main__":
	
	object = WebCam()

	object.generateQRCodeForImmunityBoost()
	object.generateQRCodeForDailyVitamins()
	object.generateQRCodeForEnergyBoost()
	object.generateQRCodeForPinaColada()
	object.generateQRCodeForPineappleFlavor()
	object.generateQRCodeForOrangeFlavor()


    testObject2 = WebCam()
	testObject2.generateQR(CocoDrink.ORANGE_FLAVOR,'static/QRImages/'+'orange_flavor2.jpg')




