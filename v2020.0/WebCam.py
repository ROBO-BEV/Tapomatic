#!/usr/bin/env python3
"""
__author__ =  "Muralikrishna Dulla"
__email__ =   "m@beepbeeptechinc.com"
__company__ = "CocoTaps"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-07-22"
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
	# Directory To Save the Generated QR Codes.
	QRCODES_DIR = os.getcwd() + '/QRCodes'
	# Directory where Source Images to embed behind the QR code.
	QRImages_DIR = 'static/QRImages/'

	# Source Images to embed behind the QR code.
	IMMUNITY_BOOST_IMG = 'immunity_boost.png'
	DAILY_VITAMINS_IMG = 'daily_vitamins.jpg'
	ENERGY_BOOST_IMG = 'energy_boost.jpg'
	PINA_COLADA_IMG = 'pina_colada.jpg'
	PINEAPPLE_FLAVOR_IMG = 'pineapple_flavor.jpg'
	ORANGE_FLAVOR_IMG = 'orange_flavor.jpg'

	# Dictionary to store the mappings of cocodrink codes with the images to embed behind the QR code.
	qrDictionary = {}
	qrDictionary[CocoDrink.IMMUNITY_BOOST]   =    IMMUNITY_BOOST_IMG
	qrDictionary[CocoDrink.DAILY_VITAMINS]   =    DAILY_VITAMINS_IMG
	qrDictionary[CocoDrink.ENERGY_BOOST]     =    ENERGY_BOOST_IMG
	qrDictionary[CocoDrink.PINA_COLADA]      =    PINA_COLADA_IMG
	qrDictionary[CocoDrink.PINEAPPLE_FLAVOR] =    PINEAPPLE_FLAVOR_IMG
	qrDictionary[CocoDrink.ORANGE_FLAVOR]    =    ORANGE_FLAVOR_IMG


	def generateQR(self, qrWord, picture):
			"""
			Generate a word based  MYQR code
			Key arguments:
			QRword -- Data to encode into QR code dots
			picture -- Background image to embed behind QR code dots

			Return value:
			None
			"""
			version, level, qr_name = myqr.run(
				qrWord,
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


	def generateQRCode(self, drinkCode):
		"""
		Generate QR code with CONSTANT INT Drink Code and embed the mapped source images behind the code.
		Key argmuments:
		drinkCode: CocoDrink Code.
		Return value:
		None.
		"""
		qrImage = self.QRImages_DIR + self.qrDictionary.get(drinkCode)
		qrWord  = self.COCOTAPS_URL  + str(drinkCode)
		self.generateQR(qrWord, qrImage)
		return

if __name__ == "__main__":
	
	object = WebCam()
	## TODO : Blaze you can use this code block to generate the QR codes.
	list = [CocoDrink.ORANGE_FLAVOR, CocoDrink.PINEAPPLE_FLAVOR, CocoDrink.PINA_COLADA, CocoDrink.ENERGY_BOOST, CocoDrink.IMMUNITY_BOOST, CocoDrink.DAILY_VITAMINS]
	for i in list:
		object.generateQRCode(i)
	# testObject2 = WebCam()
	# testObject2.generateQR(CocoDrink.ORANGE_FLAVOR,'static/QRImages/'+'orange_flavor2.jpg')




