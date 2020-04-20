#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-04-09"
__doc__ =     "Class to define flavors and health additivies in a CocoDrink"

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

class CocoDrink:

    # Drink Name CONSTANTS
    NONE = -1
    CBD = 0
    IMMUNITY_BOOST = 1
    DAILY_VITAMINS = 2
    RUM = 3
    PINA_COLADA = 4
    ORANGE_JUICE = 5
    PINEAPPLE_FLAVOR = 6
    VANILLA = 7
    ENERGY_BOOST = 8
    ORGINAL_RED_BULL = 9


    ##

	def __init__(self, drinkName, addOnFlavor, addOnFlavorLevels, addOnHealthAdditive, addOnHealthAdditiveLevels):
        """
        Constructor to initialize an Drink object
        
        @self - Newly created object
	    @drinkName - CONSTANT product name of drink (e.g. IMMUNITY_BOOST, PINA_COLADA, etc)
	    @addOnTypes - Array holding product names to be added to a drink
	    	addOnTypes[0] is CONSTANT product name of ??? being added to drink
	    	addOnTypes[1] is CONSTANT product name of ??? being added to drink
	    	addOnTypes[2] is .png filename of art being added on top of drink
	        @addOnLevels - Array holding amount / level of product to be added to a drink
    
        lidColor - For v2020.0 lid color defaults to tan
                   For v2020.1 web app with allow user to select personalized color
	    size - For v2020.0 size defaults to 10 ounces
	           For v2020.1 and later may default larger or smaller, depending on user feedback
    
        return NOTHING
        """