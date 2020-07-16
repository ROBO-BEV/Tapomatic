#!/usr/bin/env python3
"""
__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-07-05"
__doc__ =     "Class to define flavors and health additivies in a CocoTaps coconut drink"
"""

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

# Allow program to extract filename of the current file
import os

try:
	# Robotic Beverage Technologies code for controlling many different types of motors, servos, and relays
	from Actuator import *

	# Robotic Beverage Technologies code for controlling the physical movement and power output of a LASER
	from LASER import *

except ImportError:
	#TODO DO LOW LEVEL PIN CONTROL THAT WORKS EVER WHERE? http://wiringpi.com/the-gpio-utility/
	currentProgramFilename = os.path.basename(__file__)
	TempDebugObject = Debug(True, "Try/Catch ImportError in " + currentProgramFilename)
	TempDebugObject.Dprint("WARNING - You are running code on Mac or PC (NOT a Raspberry Pi 4), thus hardware control is not possible.")


class CocoDrink:

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

	# Extra add-ons for v2021.1
	CBD = 7
	ENERGY_BOOST = 8
	ORGINAL_RED_BULL = 9
	RUM = 10

	# Add-On level CONSTANTS
	MAX_ADD_ON_LEVEL = 5
	MIN_ADD_ON_LEVEL = 0

	# User GUI.py program flow selection CONSTANTS
	TAPPED = 0
	TOPPED_OFF = 1  #TODO REMOVE - LIKELY NOT GOING TO BE SUPPORTED IN v2020.1
	FLAVOR = 2
	HEALTH_ADDITIVE = 3

	# LASER branding PNG filename CONSTANTS
	RESORT_WORLD_LOGO = "ResortWorldLogoV0.png"
	COCOTAPS_LOGO = "CocoTapsLogoV0.png"
	WYNN_HOTEL_LOGO = "WynnHotelLogoV0.png"
	RED_BULL_LOGO = "RedBullLogoV0.png"
	BACARDI_LOGO = "BacardiLogoV0.png"
	ROYAL_CARRIBBEAN_LOGO = "RoyalCarribbeanLogoV0.png"


	def __init__(self, drinkNameID, addOnFlavor, addOnFlavorLevel, addOnHealthAdditive, addOnHealthAdditiveLevel, tapOrCutFlow, brandingArt):
		"""
		Constructor to initialize an CocoDrink() object, which stores add-ons and artwork

		Key arguments:
		self -- Newly created CocoDrink object
		drinkNameID -- CONSTANT product name of drink
		addOnFlavor -- CONSTANT product name of flavoring being added to base drink (e.g. IMMUNITY_BOOST, PINA_COLADA, etc)
		addOnFlavorLevel -- The unit step amount of flavor to be added to a drink from 0 to MAX_ADD_ON_LEVEL
							Each unit is a different but constant volume (in milliLiters) for each flavor
		addOnHealthAdditive -- CONSTANT product name of  health additive being added to base liquid
		addOnHealthAdditiveLevel -- The unit step amount of additive to be added to a drink from 0 to MAX_ADD_ON_LEVEL
									Each discrete unit is a differnt but constant volume (in milliLiters) for each additive
		tapOrCutFlow -- Variable used as conditional in program flow to determin if coconut is topped off or tapped 
		brandingArt -- PNG image to LASER brand onto the side of the coconut (max size is 200 MB or ? x ? pixels / ? x ? inches)

		Return value:
		New CocoDrink() object
		"""
		
		currentProgramFilename = os.path.basename(__file__)
		self.DebugObject = Debug(True, currentProgramFilename) 
        
		self.drinkNameID = drinkNameID
		self.addOnFlavor = addOnFlavor
		self.addOnFlavorLevel = addOnFlavorLevel
		self.addOnHealthAdditive = addOnHealthAdditive
		self.addOnHealthAdditiveLevel = addOnHealthAdditiveLevel
		self.tapOrCutFlow = tapOrCutFlow   	                        #TODO REMOVE - LIKELY NOT GOING TO BE SUPPORTED IN v2020.1
		self.brandingArt = brandingArt

		if(addOnFlavorLevel > CocoDrink.MAX_ADD_ON_LEVEL or addOnHealthAdditiveLevel > CocoDrink.MAX_ADD_ON_LEVEL):
			self.DebugObject.Dprint("OBJECT CREATION ERROR: You created a CocoDrink() object with add-on level greater then " + MAX_ADD_ON_LEVEL)
			__exit__() # Destructor / memory clean up

		if(addOnFlavorLevel < 0 or addOnHealthAdditiveLevel < 0):
			self.DebugObject.Dprint( "OBJECT CREATION ERROR: You created a CocoDrink() object with add-on level less then " + MIN_ADD_ON_LEVEL)
			__exit__() # Destructor / memory clean up

		if(CocoDrink.NO_DRINK > drinkNameID or drinkNameID > CocoDrink.MAX_DRINK_NAME):
			self.DebugObject.Dprint("OBJECT CREATION ERROR: You created a CocoDrink() object with a drink name that doesn't exist. Why did you do that genius?")
			__exit__() # Destructor / memory clean up


	def __enter__(self):
		"""
		The 'with' statement clarifies code that previously would use try...finally blocks to ensure that clean-up code is executed. 
		https://docs.python.org/2.5/whatsnew/pep-343.html
		https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit

		Key arguments:
        NONE
        
		Return value:
		NOTHING
		"""

		print("in __enter__")

		return self


	def __exit__(self, exception_type, exception_value, traceback):
		"""
		Memory cleanup

		Key arguments:
		exception_type --
		exception_value --
		traceback --

		Return value:
		NOTHING
		"""

		self.DebugObject.Dprint("Cleaning up CocoDrink() object in __exit__ ")


	def GetAddOn(self, lType):
		"""
		Determine the type of add-on the user selected from GUI.py and branch code floW

		Key arguments:
		lType -- Type of liquid add-on to inject into a coconut

		Return value:
		addOn -- CocoDrink CONSTANT based on user selection
		"""

		if(lType == CocoDrink.FLAVOR):
			addOn = self.GetFlavorType()  
		elif(lType == CocoDrink.HEALTH_ADDITIVE):
			addOn = self.GetHealthAdditiveType() #TODO OR (self)

		return addOn
		
		
	def GetFlavorType(self):
	    """
	    Get product name of flavoring
	    
	    Key arguments:
	    NONE
	    
	    Return value:
	    Integer GLOBAL CONSTANT from CocoDrink.py
	    """
	    
	    return self.addOnFlavor


	def GetHealthAdditiveType(self):
		"""
		Get product name of additive fluid

    	Key arguments:
        NONE
        
    	Return value:
    	return Integer GLOBAL CONSTANT from CocoDrink.py
		"""

		return self.addOnHealthAdditive


	def GetLaserArtType(self):
		"""
		Get filename of logo LASER branding into coconut

    	Key arguments:
    	NONE

    	Return value:
    	return String GLOBAL CONSTANT from CocoDrink.py
		"""

		return self.brandingArt


	def GetFlavorLevel(self):
		"""
		Get amount / level of flavor fluid in a coco drink in User Interface units

    	Key arguments:
        NONE
        
    	Return value:
    	return Integer value between 0 and  MAX_ADD_ON_LEVEL inclusively
		"""

		return self.addOnFlavorLevel

	def GetHealthAdditiveLevel(self):
		"""
		Get amount / level of health additive fluid in a Cocodrink in User Interface units

    	Key arguments:
        NONE
        
    	Return value:
    	return Integer value between 0 and  MAX_ADD_ON_LEVEL inclusively
		"""

		return self.addOnHealthAdditiveLevel


	def ConvertLevelToVolume(self, addOnUnits):
		"""
		Since each fluid has a different flavor or health effect strength per mL this function defined what the User Interface units represent

		Key arguments:
		addOnUnits -- Integer variable, between and 0 and MAX_ADD_ON_LEVEL (inclusive)

		Reture value:
		volume -- Interger variable, in units of mL for pumps to dispense
		"""

		self.addOnFlavor = addOnFlavor
		self.addOnFlavorLevel = addOnFlavorLevel
		self.addOnHealthAdditive = addOnHealthAdditive
		self.addOnHealthAdditiveLevel = addOnHealthAdditiveLevel


		if(self.addOnHealthAdditive == IMMUNITY_BOOST):
			oneUnitToMilliLiterFactor = 15
		elif(self.addOnHealthAdditive == DAILY_VITAMINS):
			oneUnitToMilliLiterFactor = 13.3
		elif(self.addOnHealthAdditive ==ENERGY_BOOST):
			oneUnitToMilliLiterFactor = 13.3

		elif(self.addOnFlavor == PINA_COLADA):
			oneUnitToMilloiiterFactor = 12
		elif(self.addOnFlavor == PINEAPPLE_FLAVOR):
			oneUnitToMilliLiterFactor = 19
		elif(self.addOnFlavor == ORANGE_FLAVOR):
			oneUnitToMilliLiterFactor = 3
			
		else:
			self.DebugObject.Dprint("ERROR CODE (0x" + GLOBAL_CONSTANT_USAGE_ERROR + ") Verfiy that this Tapomatic unit has " + self.addOnHealthAdditice + " & " + self.addOneFlavor  + " stocked.")

		volume = addOnUnits * oneUnitToMilliLeterFactor
		
		return volume


	def ConvertVolumeToPumpRunTime(volume, cocoPartNumber):
	    """
		Since motor models can vary in dispense volume / sec this function adjusts run time 
        
        Key argument:
        volume -- Interger variable, of desired volume to be dispensed
        cocoPartNumber -- String variable, which is internal CocoTaps data in the format (XXX-YYYY-ZZ)) 
        
        Return value:
        seconds - Float variable, that pump should run in order to dispense the correct volume of liquid
        """

	    thiccBoiFactor = 1                      # Set to default value 
	    
	    if(pumpPartNumber == "202-0006-A"):
	        oneMilloLiterToSecondFactor = 2.2
	    else:
	        this.DebugObject.Dprint("ERROR CODE (0x" + PUMP_CONFIGURATION_ERROR + ") Verify that you are using the correct pump part nuumber, as defined in Actuator.py and CocoDrink.py")

	    if(self.drinkName == PINA_COLADA):
	        thiccBoiFactor = 1.75			# This flavoring is extra thick, pump longer to get correct volume

	    seconds = volume * oneMilloLiterToSecondFactor * thiccBoiFactor
	    
	    return seconds
	
	
	def UnitTest():
	    print("START CocoDrink.py UnitTest()")
	    
	    TestCocoDrinkObject = CocoDrink(CocoDrink.COCONUT, CocoDrink.NONE, 0, CocoDrink.DAILY_VITAMINS, 5, CocoDrink.TAPPED, CocoDrink.COCOTAPS_LOGO)
	    print("AddOn flavor ID # is: ", TestCocoDrinkObject.GetAddOn(CocoDrink.FLAVOR))
	    print("Flavor LEVEL (in User Interface units) selected was: ", TestCocoDrinkObject.GetFlavorLevel())

	    print("AddOn health additive ID # is: ", TestCocoDrinkObject.GetAddOn(CocoDrink.HEALTH_ADDITIVE))
	    print("Health additive LEVEL (in Use Interface units) selected was: ", TestCocoDrinkObject.GetHealthAdditiveLevel())

	    print("END CocoDrink.py UnitTest()")
	
if __name__ == "__main__":

    try:
        CocoDrink.UnitTest()
    except NameError:
        print("UnitTest() failed - Have a nice day :)")            
    
    print("END CocoDrink.py MAIN")


    
