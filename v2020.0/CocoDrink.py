#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-04-21"
__doc__ =     "Class to define flavors and health additivies in a CocoDrink"

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *


# Robotic Beverage Technologies code for controlling many different types of motors, servos, relays, amd LEDS
from Actuator import *

class CocoDrink:

    # Drink Name CONSTANTS
    NO_DRINK = -1
    IMMUNITY_BOOST = 0
    DAILY_VITAMINS = 1
    RUM_FLAVOR = 2
    PINA_COLADA = 3
    PINEAPPLE_FLAVOR = 4
    ORANGE_FLAVOR = 5
    MAX_DRINK_NAME = ORANGE_FLAVOR
    
    # Extra add-ons for v2021.0
    CBD = 7
    ENERGY_BOOST = 8
    ORGINAL_RED_BULL = 9
    
    MAX_ADD_ON_LEVEL = 5
    MIN_ADD_ON_LEVEL = 0

	def __init__(self, drinkName, addOnFlavor, addOnFlavorLevel, addOnHealthAdditive, addOnHealthAdditiveLevels, brandingArt):
        """
        Constructor to initialize an Drink object
        
        Key arguments:
        self -- Newly created object
	    drinkName -- CONSTANT product name of drink (e.g. IMMUNITY_BOOST, PINA_COLADA, etc)
        addOnFlavor -- CONSTANT product name of syrup flavoring being added to base drink
	    addOnFlavorLevel -- The amount of flavor to be added to a drink from 0 to 5 (each discrete unit is a differnt but CONSTANT voulne (units are milliLiter) of fluid 
        addOnHealthAdditive -- CONSTANT product name of  health additive being added to base liquid   
        addOnHealthAdditiveLevel -- The amount of additive to be added to a drink from 0 to 5 (each discrete unit is a differnt but CONSTANT volume (units are milliLiters) of fluid
    
        Return value:
        return new CocoDrink() object  
        """
      
        self.DebugObject = Debug(True)
        
        self.drinkName = drinkName
        self.addOnFlavor = addOnFlavor
        self.addOnFlavorLevel = addOnFlavorLevel
        self.addOnHealthAdditive = addOnHeathAdditive
        self.addOnHealthAdditiveLevel = addOnHealthAdditiveLevel
        self.brandingArt = brandingArt
        
        if(addOnFlavorLevel > MAX_ADD_ON_LEVEL or addOnHealthAdditiveLevel > MAX_ADD_ON_LEVEL):
				Debug.Dprint(DebugObject, "ERROR: You created a CocoDrink() object with add-on level greater then 5")
				__exit__() #TODO EXIT CONSTRUCTOR
	    
        if(addOnFlavorLevel < 0 or addOnHewlthAdditiveLevel < 0):
				Debug.Dprint(self.DebugObject, "ERROR: You created a CocoDrink() object with add-on level less then 0")b
				__exit__() #TODO EXIT CONSTRUCTOR
				
		if(NO_DRINK > drinkName or drinkName > MAX_DRINK_NAME):
		    Debug.Dprint(DebugObject, "ERROR: You created a CocoDrink() object with a name that doesn't exist. Why did you do that genius?")
		    	__exit__() #TODO EXIT CONSTRUCTOR
				
				
	###
	#
	#
        # @self - Instance of object being called
	#
	# return object that created exception
	####

	def __enter__(self):
	"""
	
	
	
	"""
		print("in __enter__")
		return self

	###
	#
	#
        # @self - Instance of object being called
	#
	#
	#
	####
	def __exit__(self, exception_type, exception_value, traceback):
	"""
	
	
	"""
		print("in __exit__")


        ###
        # Get product name of sugar in drink
        #
        # @self - Instance of object being called
        #
        # return String variable of product name
        ###
	def GetFlavorType(self):
	"""
	
	
	
	"""
		return self.addOnFlavor

        ###
        # Get product name of milk in drink
        #
        # @self - Instance of object being called
        #
        # return String variable of product name
        ###
	def GetHealthAdditiveType(self):
	"""
	
	
	
	"""
		return self.addOnHealthAdditive

        ###
        # Get filename for branding art on side of coconut
        #
        # @self - Instance of object being called
        #
        # return String variable of filename
        ###
	def GetLaserArtType(self):
	"""
	
	
	"""
		return self.brandingArt

   
    def GetFlavorLevel(self):
	"""
	Get amount / level of flavor fluid in a coco drink in User Interface units 
	
   
    Key arguments:
    self -- Instance of object being called
      
    Return value:
    return Integer value between 0 and  MAX_ADD_ON_LEVEL inclusively 
	"""
		return self.addOnFlavorLevel

	def ConvertLevelToVolume(self, addOnUnits):
	"""
	Since each fluid has a different flavor or health effect strength per mL this function defined what the User Interface units of mean
	
	Key arguments:
	addOnUnits -- Integer between and 0 and MAX_ADD_ON_LEVEL inclusively 
	
	
	Reture value:
	volume - In units of mL for pumps to dispense 
	"""
		if(self.drinkName == IMMUNITY_BOOST):
			oneUnitToMilliLiterFactor = 15
		elif(self.drinkName == IMMUNITY_BOOST):
			oneUnitToMilliLiterFactor = 13.3
		elif(self.drinkName == IMMUNITY_BOOST):
			oneUnitToMilloiiterFactor = 12
		elif(self.drinkName == IMMUNITY_BOOST):
			oneUnitToMilliLiterFactor = 19
		elif(self.drinkName == IMMUNITY_BOOST):
			oneUnitToMilliLiterFactor = 3
		elif(self.drinkName == IMMUNITY_BOOST):
			oneUnitToMilliLiterFactor = 9
		else:
			Debug.Dprint(self.DebugObject, "TODO define error masseging architecture")
		
		return volume = addOnUnits * oneUnitToMilliLeterFactor
		
		
	def ConvertVolumeToPumpRunTime(volume, motorName):
	"""
	Since each pump has a different flow rate(mL/Sec) this function defined how long each pump type should stay on to dispense an exact (~2 ml variance) of fluid. fudgeFactor variable enable "THICK BOI" (Search Google) fluids to be dispenses currently  
	
	Key Paramters:
	motorName -- Pump / motor name as defines ik Actuator.py
	
	Return value:
	seconds -- The amount of time a pump should operate  to dispense the correct amount of fluid
	"""
		thickBoiFactor = 1
		
		if(motorName == Actuactor.??):
			oneMilloLiterToSecondFactor = 2.2
		else:
			Debug.Dprint(self.DebugObject, "TODO define error masseging architecture")
			
		if(self.drinkName == PINA_COLADA):
			thickBoiFactor = 1.75
		
		return seconds = volume * oneMilloLiterToSecondFactor * thickBoiFactor
		
       
	def GetHealthAdditiveLevel(self):
	"""
	Get amount / level of health additive fluid in a coco drink in User Interface units
	
    Key arguments:
    self -- Instance of object being called
      
    Return value:
    return Integer value between 0 and  MAX_ADD_ON_LEVEL inclusively 
	"""
	
		return self.addOnHealthAdditiveLevel
				
				
				
				
				
				