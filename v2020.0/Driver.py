#!/usr/bin/env python

__author__ =  "Blaze Sanders"
__email__ =   "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-04-06"
__doc__ =     "Logic to run Tapomatic back-end services (i.e. not GUI)"

# Useful standard Python system jazz
import sys, time, traceback, argparse, string

# Allow UDP communication between different CPUs (e.g. Raspberry Pi, NVIVDIA TX2, etc) using Ethernet
import socket

# Allow keyboard to control program flow and typing to terminal window
import pynput.keyboard
from pynput.keyboard import Key, Controller

# Custom Robotic Beverage Technologies Inc code
from CoCoDrink import *         	# Store valid CoCoTaps drink configurations
from Actuator import *         	# Modular plug and play control of motors, servos, and relays
from Debug import *		    	# Configure datalogging parameters and debug printing control

# Create a command line parser
parser = argparse.ArgumentParser(prog = "Tapomatic v2020.0", description = __doc__, add_help=True)
parser.add_argument("-i", "--piIP_Address", type=str, default="192.168.1.135", help="IPv4 address of the Tapomatic V0 ID0 backend Raspberry Pi 4.")
parser.add_argument("-r", "--rx_Socket", type=int, default=30000, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-s", "--tx_Socket", type=int, default=30100, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-u", "--unit", type=str, default= FIELD_MODE, choices=[TESTING_MODE, FIELD_MODE, PRODUCT_MODE], help="Select boot up mode for BARISTO kiosk.")
parser.add_argument("-t", "--trace", type=int, default=0, help="Program trace level.")
parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on kiosk.")
parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
args = parser.parse_args()

	# Raspberry Pi B+ refernce pin CONSTANTS as defined in ???rc.local script???
	NUM_GPIO_PINS = 15                       # Outputs: GPO0 to GPO3 Inputs: GPI0 to GPI3
	MAX_NUM_A_OR_B_PLUS_GPIO_PINS = 40      # Pins 1 to 40 on Raspberry Pi A+ or B+ or ZERO W
	MAX_NUM_A_OR_B_GPIO_PINS = 26           # Pins 1 to 26 on Raspberry Pi A or B
	NUM_OUTPUT_PINS = 8                     # This software instance of Raspberry Pi can have up to eight output pins
	NUM_INPUT_PINS = 7                      # This software instance of Raspberry Pi can have up to seven input pins

# External WWW IP addresses
LINODE_MYSQL_IP = "45.79.104.3?"
RAVEN_DB_IP = "TODO"

# Internal local network IP addresses and ports
GUI_PI_IP = "127.168.1.69"
VEND_PI_IP = "127.168.1.42"
UDP_PORT = 5005

# Over The Air (OTA) Updating Configurations
VERSION = "2020.0"
PRODUCT_MODE = "PRODUCT"        		# Final product configuration
FIELD_MODE   = "FIELD"					# Non-Techanical repair person configuration
TESTING_MODE = "TESTING"				# Internal developer configuration

# Tapomatic v2020.0 kiosk can process upto 2 coconuts in parallel
MAX_VEND_QUEUE_SIZE = 2

# Max time (in seconds) each of the three processes (Drilling, Tapping, Top Off) takes
MAX_DRILLING_TIME    = 15
MAX_TAPPING_TIME     = 10
MAX_TOPPING_OFF_TIME = 5

# Exit case CONSTANTS for debug logs
TORQUE_EXIT_CASE = -1
DEPTH_EXIT_CASE  = -2
TIME_EXIT_CASE   = -3

# Raspberry Pi 4B refernce pin constants as defined in ???rc.local script???
NUM_PI_GPIO_PINS = 8              		# Outputs: GPO0 to GPO3 Inputs: GPI0 to GPI3
MAX_NUM_PI_A_OR_B_PLUS_GPIO_PINS = 40 	# Pins 1 to 40 on Raspberry Pi A+ or B+ or ZERO W
MAX_NUM_PI_A_OR_B_GPIO_PINS = 26      	# Pins 1 to 26 on Raspberry Pi A or B
NUM_PI_OUTPUT_PINS = 4                	# This software instance of Raspberry Pi can have up to four output pins
NUM_PI_INPUT_PINS = 4                 	# This software instance of Raspberry Pi can have up to four input pins
#UART pins in BCM mode are: 14, 15 /dev/ttyAMA0

#The TODO?17? actuators CONSTANTS
ROTATIONTAL_TOOL_MOTOR = 0
Z_LINEAR_TOOL_MOTOR    = -1
X_LINEAR_TOOL_MOTOR    = -2
Y_LINEAR_TOOL_MOTOR    = -3
Z1_LINEAR_LIFT_MOTOR   = -4
Z2_LINEAR_LIFT_MOTOR   = -5
TODO

# Tool change CONSTANTS
NO_TOOL = 0
DRILL_BIT_TOOL = -1
TAPPING_SOCKET_TOOL = -2
#TODO Not needed LASER_BRANDING_TOOL = -3

# If force on top off knive is greater than CONSTANT below it is probably dull
DULL_KNIFE_FORCE = 100	# Units are Newtons
SHARP = 1
DULL = 0
# Array elements 
# [Side A Section 1, Side A Section 2, Side A Section 3, Side B Section 4, Side B Section 5, Side B Section 6]
KNIVE_SECTIONS[6] = [SHARP, SHARP, SHARP, SHARP, SHARP, SHARP]


def ConfigureKnife():
    if(Sensor.GetForce(Sensor.FORCE_SENSOR) > DULL_KNIFE_FORCE):
        KNIVE_SECTIONS[currentKnifeSectionInUse] == DULL
        currentKnifeSectionInUse += 1
        MoveKnifePostion(currentKnifeSectionInUse)

def MoveKnifePostion(currentKnifeSectionInUse):
    print("TODO")

###
# Actuate N number of actuators to LIFT coconuts into the drilling, tapping, and toping off system
#
# @actuatorObjects - Array of linear actuators() objects to control
#
# return NOTHING
###
def LiftCoconut(actuatorObjects):
	for i in actuatorObjects:			# Move ALL actuators to LIFT cocoonut to max position at the same time
		actuatorObjects[i].max()		# OLD WAY cupSeparatorServo1.min()

	#time.sleep(MAX_DRILLING_TIME + MAX_TAPPING_TIME + MAX_TOPPING_OFF_TIME) #TODO REAL LIFE TESTING ~30 seconds

###
# Actuate N number of actuators to LOWER coconuts into the drilling, tapping, and toping off system
#
# @actuatorObjects - Array of linear actuators() objects to control
#
# return NOTHING
###
def LowerCoconut(actuatorObjects):
	for j in actuatorObjects:			# Move ALL actuators to LOWER coconut to min position at the same time
		actuatorObjects[j].min()		# OLD WAY cupSeparatorServo1.min()


###
# Turn ON rotational motor to spin drill bit at high speed until a stopSignal is given
#
# @stopSignal - Input signal that can cause drill to stop OTHERWISW MAX_DRILLING_TIME causes drill to stop
# @actuatorObjects - Array of linear actuators() objects to control
#
# return Exit case CONSTANT describing why drill stopped
###
def RunDrill(stopSignal, actuatorObjects):
	torqueBelowLimit = True
	drillDepthNotAtMax = True
	timeDelta = 0.0

	while(torqueBelowLimit or drillDepthNotAtMax and timeDelta < MAX_DRILLING_TIME):
		actuatorObjects[0].max()			# Turn on ONE rotational motor at max speed
		timeDelta += 0.001					#TODO REAL LIFE TESING OF LOOP SPEED ~1 ms

	if(not torqueBelowLimit):
		return TORQUE_EXIT_CASE
	elif(not drillDepthNotAtMax):
		return DEPTH_EXIT_CASE
	else:
		return TIME_EXIT_CASE


###
# Emergency stop of rotational motor instantly
#
# return NOTHING
###
def StopDrill(actuatorObjects):
	actuatorObjects[0].min()			# Turn off ONE rotational motor (TODO Is min == off?)
	actuatorObjects[1].min()			# Pull linear Z axis motor back to start position


###
# Change end effector tool connected to the 3-axis + rotational motor crane system
#
# @newTool - Name of new tool to cennect to the crane system
#
# return NOTHING
###
def SwapTool(newTool):
    if(currentTool == newTool):
        Debug.Dprint("DO NOTHING")
    elif(newTool == DRILL_BIT_TOOL):
        GoToToolHome()
        LockOldTool()
        UnlockNewTool()
    elif(newTool == TAPPING_SOCKET_TOOL):
        GoToToolHome()
        LockOldTool()
        UnlockNewTool()
    else:
        Debug.Dprint("ERROR: You attempted to use a tool not supported by Tapomatic v" + VERSION)

###
# Top off coconut by cutting striaght across with horizontal knive
#
# @direction - Plus or minus X axis direction to cut towards.
# @actuatorObjects - Array of linear actuators() objects to control
#
# return false if top off knive is dull and needs service
###
def AcutateDoubleSidedKnive(direction, actuatorObjects):

    if(direction == PLUS):
        Debgug.Dprint("TODO")
    elif(direction == MINUS):
        Debgug.Dprint("TODO")
    else:
        Debgug.Dprint("TODO")

    if(GetForce() > DULL_KNIVE_FORCE):
        isKniveSharp = false
        Debug.Lprint("Topping off knive is dull, service ASAP")
    else:
        isKniveSharp = true

    return isKniveSharp

# Actuate peristaltic pump to dispense liquid milk into cup
#
# @powderType - Product name of powder add-on to dispense (e.g. CINNAMON)
# @powderLevel - Amount of powder units to dispense 1 unit = 0.1 oz
# @actuatorObjects - Array of Actuator.py objects to control
#
# return NOTHING
###
def actuateFlavorPump(flavorType, flavorLevel, actuatorObjects):

	if(CoCoDrink.NONE < flavorLevel and flavorLevel <= CoCoDrink.MAX_FLAVOR_LEVEL):
		actuationTime = flavorLevel / CoCoDrink.FLAVOR_FLOW_RATE  #Units of Seconds based on flow rate per second of pump
		if(flavorType == CoCoDrink.RUM):
			Debug.Dprint("Pumping RUM into coconut for " + actuationTime  +" seconds")
			actuatorObjects[0].run(actuationTime, Actuator.N_A, 0.5, Actuator.FORWARD) #PROBABLY CORRECT
			#simpleSyrupSugarMotor.run(actuationTime, Actuator.N_A, 0.5, Actuator.FORWARD) #PROBABLY WRONG
		elif(flavorType == CoCoDrink.PINA_COLADA):
			Debug.Dprint("Pumping PINA COLADA into coconut for " + actuationTime  +" seconds")
			#actuatorObjects[1].
			self.run(actuationTime, Actuator.N_A, 0.5, Actuator.FORWARD) #PROBABLY WRONG
		elif(flavorType == CoCoDrink.CBD):
			Debug.Dprint("Pumping CBD into coconut for " + actuationTime  +" seconds")
			#actuatorObjects[2].
			#time.sleep(actuationTime)
		elif(flavorType == Drink.CHOCOLATE):
			print("TODO")
			#actuatorObjects[1].
			#ONE OF ABOVE METHODS
		else:
			print("INVALID SUGAR TYPE PASSED TO FUNCTION - TRY SIMPLE_SYRUP CONSTANT")
	elif(sugarLevel == Drink.NONE):
		time.sleep(0.001) # DO NOTHING expect pause for 1 millisecond

	else:
		print("INVALID SUGAR LEVEL PASSED TO FUNCTION - TRY VALUE 0 TO 8")

###
# Move belt conveyor to position cups under add-on product pumps
#
# @direction - Clockwise or Counter Clockwise rotation on main conveyor belt
# @numOfPositions - Number of unit steps to move conveyor belt
#
# return NOTHING
###
def moveConveyor(actuatorObjects, direction, numOfPositions):
	if(direction == Actuator.FORWARD):
		for posNum in range(1, numOfPositions+1):
			for i in actuatorObjects: 			# Move ALL actuators to drop cup to min position at the same time
				actuatorObjects[i].run(Actuator.CW) 	#or Actuator.FORWARD
			time.sleep(MAX_ADDON_DISPENSE_TIME)		#Units are Seconds
	elif(direction == Actuator.BACKWARDS):
		for posNum in range(1, numOfPositions+1):
			for i in actuatorObjects: 			# Move ALL actuators to drop cup to min position at the same time
				actuatorObjects[i].run(Actuator.CCW) 	#or Actuator.BACKWARD
			time.sleep(MAX_ADDON_DISPENSE_TIME)		#Units are Seconds
	else:
		print("INVALID CONVEYOR DIRECTION PASSED TO FUNCTION - TRY FORWARD OR BACKWARDS")

if __name__ == "__main__":

    # TODO Does this work? or do I need to call actuatoObjects[i].???
    ROTATIONTAL_TOOL_MOTOR = actuatorObjects[0]

    Z_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[1]
    X_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[2]
    Y_LINEAR_TOOL_STEPPER_MOTOR  = actuatorObjects[3]

    Z1_LINEAR_LIFT_MOTOR = actuatorObjects[4]
    Z2_LINEAR_LIFT_MOTOR = actuatorObjects[5]

    Y1_LINEAR_CUT_MOTOR = actuatorObjects[6]
    Y2_LINEAR_CUT_MOTOR = actuatorObjects[7]
    X1_LINEAR_POSITION_MOTOR = actuatorObjects[8]

    Y1_LINEAR_COVER_MOTOR = actuatorObjects[9]
    Y2_LINEAR_COVER_MOTOR = actuatorObjects[10]

    FLAVOR1_PERISTALTIC_PUMP = actuatorObjects[11]
    FLAVOR2_PERISTALTIC_PUMP = actuatorObjects[12]
    FLAVOR3_PERISTALTIC_PUMP = actuatorObjects[13]
    FLAVOR4_PERISTALTIC_PUMP = actuatorObjects[14] # TODO REMOVE AND RENUMBER? 

    Z_LINEAR_LASER_STEPPER_MOTOR = actuatorObjects[15]
    X_LINEAR_LASER_STEPPER_MOTOR = actuatorObjects[16]
    Y_LINEAR_LASER_STEPPER_MOTOR  = actuatorObjects[17]

    ROTATIONAL_DISK_STEPPER_MOTOR = actuatorObjects[18]

    currentTool = NO_TOOL           # Default is having no tool attached to 3-axis system
    currentKnifeSectionInUse = 0    # Always attempt to used section 0 when code restarts

    currentNumberOfOrders = 0
    numOfOrdersInProgress = 1

    tempDrink = Drink(Drink.NONE, Drink.NONE, Drink.NONE)
    vendQueue[MAX_VEND_QUEUE_SIZE] =  [tempDrink, tempDrink, tempDrink]

    # DEFINE ALL ACTUATORS INSIDE TAPOMATIC ATTACH TO ADAFRUIT DC & STEPPER MOTOR HAT 2348
    cupSepServo1Pins = [VCC_5V, GND, 5]  		# GPIO5 = BOARD29 = DC_STEPPER_HAT???
    cupSeparatorServo1 = Actuator("S", cupSepServo1Pins, "Cup Separator Servo 1: Seamuing MG996R", Actuator.CW)
    cupSepServo2Pins = [VCC_5V, GND, 6]  		# GPIO6 = BOARD31 = DC_STEPPER_HAT???
    cupSeparatorServo2 = Actuator("S", cupSepServo2Pins, "Cup Separator Servo 2: Seamuing MG996R", Actuator.CCW)

    coldBrewCoffeePins = [PWR_12V, GND, ??]	#TODO GPIO?? = BOARD?? = DC_STEPPER_HAT???
    coldBrewCoffeeMotor1 =  Actuator("R", coldBrewCoffeePins, "Cold Brew Coffee Motor: Zjchao 202", Actuator.CW)

    simpleSyrupSugarPins = [PWR_12V, GND, 4]	#TODO GPIO4 = BOARD7 = DC_STEPPER_HAT???
    simpleSyrupSugarMotor =  Actuator("R", simpleSyrupSugarPins, "Simple Syrup Sugar Motor: Zjchao 202", Actuator.CW)
    carmelSugarPins = [PWR_12V, GND, 17]		#TODO GPIO17 = BOARD11 = DC_STEPPER_HAT???
    carmelSugarMotor =  Actuator("R", carmelSugarPins, "Carmel Sugar Motor: Zjchao 202", Actuator.CW)
    vanillaSugarPins = [PWR_12V, GND, 27]		#TODO GPIO27 = BOARD? = DC_STEPPER_HAT???
    vanillaSugarMotor = Actuator("R", vanillaSugarPins, "Vanilla Sugar Motor: Zjchao 202", Actuator.CW)
    chocolateSugarPins = [PWR_12V, GND, 22]		#TODO GPIO22 =
    chocolateSugarMotor =  Actuator("R", chocolateSugarPins, "Chocolate Sugar Motor: Zjchao 202", Actuator.CW)

    halfHalfMilkPin = [PWR_12V, GND, 18]		#TODO GPIO18 =
    halfHalfMilkMotor = Actuator("R", halfHalfMilkPin, "Half & Half Milk Motor: Zjchao 202", Actator.CW)
    almondMilkPin = [PWR_12V, GND, 23]		#TODO GPIO23 =
    almondMilkMotor = Actuator("R", almondMilkPin, "Almond Milk Motor: Zjchao 202", Actator.CW)
    oatlyMilkPin = [PWR_12V, GND, 24]		#TODO GPIO24 =
    oatlyMilkMotor = Actuator("R", oatlyMilkPin, "Oatly Milk Motor: Zjchao 202", Actator.CW)

    #TODO GPIO12 = BOARD? = DC_STEPPER_HAT???   / GPIO16 = BOARD? = DC_STEPPER_HAT???
    conveyorMotor1Pins = [PWR_12V, GND, VCC_5V, GND, NO_PIN, NO_PIN, 12, 16]
    conveyorMotor1 = Actuator("M", conveyorMotor1Pins, "Conveyor Motor 1: Mountain ARK Mini T100 Tank SR-Series")
    conveyorMotor2Pins = [PWR_12V, GND, VCC_5V, GND, NO_PIN, NO_PIN, 12, 16]
    conveyorMotor2 = Actuator("M", conveyorMotor2Pins, "Conveyor Motor 1: Mountain ARK Mini T100 Tank SR-Series")

    #TODO GPIO20 = BOARD? = DC_STEPPER_HAT?   / GPIO21 = BOARD? = DC_STEPPER_HAT?
    liftMotor1Pins = [PWR_12V, GND, 20, 21]
    liftMotor1 = Actuator("M", liftMotor1Pins, "Lift Motor 1: ECO L11TGF900NB100-T1")
    liftMotor2Pins = [PWR_12V, GND, 20, 21]
    liftMotor2 = Actuator("M", liftMotor2Pins, "Lift Motor 2: ECO L11TGF900NB100-T1")

    powderServo1Pins = [VCC_5V, GND, 13]		#TODO GPIO13 = BOARD? = DC_STEPPER_HAT?
    powderServo1 = Actuator("S", powderServo1Pins, "Powder Servo 1: Seamuing MG996R")
    powderServo2Pins = [VCC_5V, GND, 19]		#TODO GPIO19 = BOARD? = DC_STEPPER_HAT?
    powderServo2 = Actuator("S", powderServo2Pins, "Powder Servo 2: Seamuing MG996R")
    powderServo3Pins = [VCC_5V, GND, 26]		#TODO GPIO26 = BOARD? = DC_STEPPER_HAT?
    powderServo3 = Actuator("S", powderServo3Pins, "Powder Servo 3: Seamuing MG996R")

    # SEPARATE FULL LIST OF ACTUATOR OBJECTS INTO MORE SPECIFIC ARRAY GROUPINGS
    actuatorObjects = [cupSeparatorServo1, cupSeparatorServo2, simpleSyrupSugarMotor, carmelSugarMotor, vanillaSugarMotor, chocolateSugarMotor, halfHalfMilkMotor, almondMilkMotor, oatlyMilkMotor, conveyorMotor1, conveyorMotor2, liftMotor1, lifeMotor2, powderServo1, powderServo2, powderServo3, coldBrewCoffeeMotor1]
    dropCupActuators = [actuatorObjects[0], actuatorObjects[1]]
    sugarActuators = [actuatorObjects[2], actuatorObjects[3], actuatorObjects[4], actuatorObjects[5]]
    milkActuators = [actuatorObjects[6], actuatorObjects[7], actuatorObjects[8]]
    conveyorActuators = [actuatorObjects[9], actuatorObjects[10]]
    liftActuators = [actuatorObjects[11], actuatorObjects[12]]
    powderActuators = [actuatorObjects[13], actuatorObjects[14], actuatorObjects[15]]
    coffeeActuators = [actuatorObjects[16]]

	while(True):
		for drinkNum in range(0, MAX_VEND_QUEUE_SIZE-1):
			vendQueue[drinkNum] = getOrder(UDP_FOR_OTHER_PI)
			if(vendQueue[drinkNum] != Drink.NONE):
				# VEND SUGAR ADD-ON
				dropCup(dropCupActuators)
				moveConveyor(conveyorActuators, Actuator.FORWARD, 1)
				actuateSugarMotor(sugarActuators, vendQueue[drinkNum].getSugarType, vendQueue[drinkNum].getSugarLevel)

				# VEND MILK ADD-ON
				vendQueue[drinkNum+1] = getOrder(UDP_FOR_OTHER_PI)
				dropCup(dropCupActuators)
				moveConveyor(conveyorActuators, Actuator.FORWARD, 1)
				actuateMilkMotor(milkActuators, vendQueue[drinkNum].getMilkType, vendQueue[drinkNum].getMilkLevel)
				actuateSugarMotor(sugarActuators, vendQueue[drinkNum+1].getSugarType, vendQueue[drinkNum+1].getSugarLevel)

				# VEND POWDER ADD-ON
				vendQueue[drinkNum+2] = getOrder(UDP_FOR_OTHER_PI)
				dropCup(dropCupActuators)
				moveConveyor(conveyorActuators, Actuator.FORWARD, 1)
				actuatePowderServo(powderActuators vendQueue[drinkNum].getPowderType)
				actuateMilkMotor(milkActuators, vendQueue[drinkNum+1].getMilkType, vendQueue[drinkNum].getMilkLevel)
				actuateSugarMotor(sugarActuators, vendQueue[drinkNum+2].getSugarType, vendQueue[drinkNum+1].getSugarLevel)

				# LIFT CUP TO USER VEND PORT(S)
				moveConveyor(conveyorActuators, Actuator.FORWARD, 1)
				liftCup(liftActuator)
