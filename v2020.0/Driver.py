#!/usr/bin/env python

"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-04-30"
__doc__     = "Logic to run Tapomatic back-end services (i.e. not GUI)"
"""

# Useful standard Python system jazz
import sys, time, traceback, argparse, string

# Allow UDP communication between compu
import socket

# Allow keyboard to control program flow and typing to terminal window
import pynput.keyboard
from pynput.keyboard import Key, Controller

# Custom CocoTaps and Robotic Beverage Technologies Inc code
from CocoDrink import *         # Store valid CoCoTaps drink configurations
from Actuator import *         	# Modular plug and play control of motors, servos, and relays
from Debug import *		# Configure datalogging parameters and debug printing control
from UDP import *		# Allow UDP communiation over an Ethernet cable between two computers 
from RaspPi import *            # Contains usefull GPIO pin CONSTANTS and setup configurations
from LASER import *		# Enable LASER movement and image warping around coconut

# Create a command line parser
parser = argparse.ArgumentParser(prog = "Tapomatic v2020.0", description = __doc__, add_help=True)
parser.add_argument("-i", "--piIP_Address", type=str, default="127.168.1.42", help="IPv4 address of the Tapomatic V0 ID0 backend Raspberry Pi 4.")
parser.add_argument("-r", "--rx_Socket", type=int, default=30000, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-s", "--tx_Socket", type=int, default=30100, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-u", "--unit", type=str, default= FIELD_MODE, choices=[TESTING_MODE, FIELD_MODE, PRODUCT_MODE], help="Select boot up mode for BARISTO kiosk.")
parser.add_argument("-t", "--trace", type=int, default=0, help="Program trace level.")
parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on kiosk.")
parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
args = parser.parse_args()

# Over The Air (OTA) Updating Configurations
VERSION = "2020.0"
PRODUCT_MODE = "PRODUCT"        		# Final product configuration
FIELD_MODE   = "FIELD"					# Non-Techanical repair person configuration
TESTING_MODE = "TESTING"				# Internal developer configuration

# Tapomatic v2020.0 kiosk can process upto 2 coconuts in parallel
MAX_VEND_QUEUE_SIZE = 1

# Max time (in seconds) each of the three processes (Drilling, Tapping, Top Off) takes
MAX_DRILLING_TIME    = 15
MAX_TAPPING_TIME     = 10
MAX_TOPPING_OFF_TIME = 5
MAX_LASER_TIME = MAX_DRILLING_TIME + MAX_TAPPING_TIME + MAX_TOPPING_OFF_TIME

#The TODO?17? actuators CONSTANTS
TOTAL_NUM_OF_ACTUATORS = 17    		#TODO DOUBLE CHECK THIS
ROTATIONTAL_TOOL_MOTOR = 0
Z_LINEAR_TOOL_MOTOR    = 1
X_LINEAR_TOOL_MOTOR    = 2
Y_LINEAR_TOOL_MOTOR    = 3
Z1_LINEAR_LIFT_MOTOR   = 4
Z2_LINEAR_LIFT_MOTOR   = 5
#TODO

# Tool change CONSTANTS
NO_TOOL = 0
DRILL_BIT_TOOL = -1
TAPPING_SOCKET_TOOL = -2
#TODO Not needed LASER_BRANDING_TOOL = -3

# If force on topping off knife is greater than DULL_KNIFE_FORCE it is probably dull
DULL_KNIFE_FORCE = 100	# Units are Newtons
SHARP = 1
DULL = 0
DULL_KNIFE = -1
NUM_OF_KNIFE_CUTTING_AREAS = 6
KNIVE_SECTIONS[NUM_OF_KNIFE_CUTTING_AREAS] = [SHARP, SHARP, SHARP, SHARP, SHARP, SHARP]
# [Side A Section 1, Side A Section 2, Side A Section 3, Side B Section 4, Side B Section 5, Side B Section 6]

def ConfigureKnife(currentKnifeSectionInUse):
    if(Sensor.GetForce(Sensor.FORCE_SENSOR) > DULL_KNIFE_FORCE):
        KNIVE_SECTIONS[currentKnifeSectionInUse] == DULL
        currentKnifeSectionInUse += 1
        MoveKnifePostion(currentKnifeSectionInUse)


def MoveKnifePostion():
    """
    Use linear actuator to slide knife left or right and expose new cutting surface / section

    Key arguments:
    NONE

    Return value:
    knifeSectionNowInUse -- The new knife cutting section; otherwise retrun DULL_KNIFE so vendor can be informed    
    """
    
    # currentKnifeSectionInUse is a global variable in the Driver.py

    if(0 <= currentKnifeSectionInUse or currentKnifeSectionInUse < NUM_OF_KNIFE_CUTTING_AREAS - 1): 	
        Debug.Drpint(DebugObject, "Moving knife to next cutting surface / section")
	knifeSectionNowInUse = currentKniifeSectionInUse + 1
    elif(currentKnifeSectionInUse == NUM_OF_CUTTING_AREAS - 1):
        Debug.Drpint(DebugObject, "Message Code:" + MissionControl.DULL_KNIFE_MESSAGE + "Tapomatic has used up all the cutting surfaces on the current knife")
	MissionControl.SendMessage(MissionControl.DULL_KNIFE_MESSAGE)
	knifeSectionNowInUse = DULL_KNIFE
    else:
	print("BAD PARAMETERS")

    return knifeSectionNowInUse


def LiftCoconut(actuatorObjects):
	"""
	Actuate N number of actuators to LIFT coconuts into the drilling, tapping, and toping off system
	
	Key Arguments:
	actuatorObjects -- Array of linear actuators() objects to control
	
	Return value:
	NOTHING
	"""

	for i in actuatorObjects:			# Move ALL actuators to LIFT cocoonut to max position at the same time
		ActuatorObjects[i].max()		# OLD WAY cupSeparatorServo1.min()

	#time.sleep(MAX_DRILLING_TIME + MAX_TAPPING_TIME + MAX_TOPPING_OFF_TIME) #TODO REAL LIFE TESTING ~30 seconds


def LowerCoconut(actuatorObjects):
	"""
	Actuate N number of actuators to LOWER coconuts into the drilling, tapping, and toping off system

	Key arguments:
	actuatorObjects -- Array of linear actuators() objects to control

	Retrun vlaue:
	NOTHING
	"""

	for j in ActuatorObjects:			# Move ALL actuators to LOWER coconut to min position at the same time
		ActuatorObjects[j].min()		# OLD WAY cupSeparatorServo1.min()


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
        Debug.Dprint(Debug(True), "DO NOTHING")
    elif(newTool == DRILL_BIT_TOOL):
        GoToToolHome()
        LockOldTool()
        UnlockNewTool()
    elif(newTool == TAPPING_SOCKET_TOOL):
        GoToToolHome()
        LockOldTool()
        UnlockNewTool()
    else:
        Debug.Dprint(Debug(True), "ERROR: You attempted to use a tool not supported by Tapomatic v" + VERSION)

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

def MoveConveyor(actuatorObjects, direction, numOfPositions):
    """
    Move conveyor / ring to position product under the actuator

    Key arguments:
    actuatorObjects --
    direction -- Clockwise or Counter Clockwise rotation on main conveyor belt
    numOfPositions - Number of unit steps to move conveyor / ring

    Key values:
    NOTHING
    """
	
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


def GetOrder():
    print("TODO UDP communications")
		
if __name__ == "__main__":

    DebugObject = Debug(True)  #https://github.com/ROBO-BEV/Tapomatic/issues/8

    # TODO Does this work? or do I need to call actuatoObjects[i].???
    ROTATIONTAL_TOOL_MOTOR = actuatorObjects[0]

    Z_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[1]
    X_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[2]
    Y_LINEAR_TOOL_STEPPER_MOTOR = actuatorObjects[3]

    Z1_LINEAR_LIFT_MOTOR = actuatorObjects[4]
    Z2_LINEAR_LIFT_MOTOR = actuatorObjects[5]

    Y1_LINEAR_CUT_MOTOR = actuatorObjects[6]
    Y2_LINEAR_CUT_MOTOR = actuatorObjects[7]
    X1_LINEAR_KNIFE_POSITION_MOTOR = actuatorObjects[8]

    Y1_LINEAR_COVER_MOTOR = actuatorObjects[9]
    Y2_LINEAR_COVER_MOTOR = actuatorObjects[10]

    LIQ_1_PERISTALTIC_PUMP = actuatorObjects[11]
    LIQ_2_PERISTALTIC_PUMP = actuatorObjects[12]
    LIQ_3_PERISTALTIC_PUMP = actuatorObjects[13]
    LIQ_4_PERISTALTIC_PUMP = actuatorObjects[14] 
    LIQ_5_PERISTALTIC_PUMP = actuatorObjects[14]
    LIQ_6_PERISTALTIC_PUMP = actuatorObjects[15] 

    Z_LINEAR_LASER_STEPPER_MOTOR = actuatorObjects[16]
    X_LINEAR_LASER_STEPPER_MOTOR = actuatorObjects[17]
    Y_LINEAR_LASER_STEPPER_MOTOR = actuatorObjects[18]

    ROTATIONAL_DISK_STEPPER_MOTOR = actuatorObjects[19]

    currentTool = NO_TOOL           # Default is having no tool attached to 3-axis system
    currentKnifeSectionInUse = 0    # Always attempt to used section 0 when code restarts

    numberOfOrdersCompleted = 0
    numberOfOrdersInProgress = 0

    TempDrink = CocoDrink(CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE)
    vendQueue[MAX_VEND_QUEUE_SIZE] =  [tempDrink]

    # TODO REMOVE? GuiPi = RaspPi()
    # REMOVE? BackendPi = RaspPi()

    # DEFINE ALL ACTUATORS INSIDE TAPOMATIC ATTACH TO ADAFRUIT DC & STEPPER MOTOR HAT 2348
    # SEPARATE FULL LIST OF ACTUATOR OBJECTS INTO MORE SPECIFIC ARRAY GROUPINGS   
    # https://upverter.com/design/blazesandersinc/tapomatic-v2020-1/
    ActuatorObjects[TOTAL_NUM_OF_ACTUATORS] = Actuator("TODO", BackendPi.NO_PIN, "Non-Configured Actutator") 

    immunityHealthAdditivePins = [BackendPi.PWR_12V, BackendPi.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]	
    ImmunityHealthAdditiveMotor = Actuator("R", ImmunityHealthAdditivePins, "Immunity Boost Motor: Zjchao 202", Actuator.CW)
    ActuatorObject[0] = ImmunityHealthAdditiveMotor
    vitaminsHealthAdditivePins = [BackendPi.PWR_12V, BackendPi.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    VitaminsHealthAdditiveMotor = Actuator("R", vitaminsHealthAdditivePins, "Daily Vitamins Motor: Zjchao 202", Actuator.CW)
    ActuatorObject[1] = VitaminsHealthAdditiveMotor

    rumFlavorPins = [BackendPi.PWR_12V, BackendPi.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    RumFlavorMotor = Actuator("R", rumFlavorPins, "Rum Flavor Motor: Zjchao 202", Actuator.CW)
    ActuatorObject[2] = RumFlavorMotor
    pinaColadaFlavorPins = [BackendPi.PWR_12V, BackendPi.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    PinaColadaFlavorMotor = Actuator("R", pinaColadaFlavorPins, "Pina Colada Flavor Motor: Zjchao 202", Actuator.CW)
    ActuatorObject[3] = PinaColadaFlavorMotor
    pineappleFlavorPins = [BackendPi.PWR_12V, BackendPi.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    PineappleFlavorMotor = Actuator("R", orangeFlavorPins, "Orange Flavor Motor: Zjchao 202", Actuator.CW)	
    ActuatorObject[4] = PineappleFlavorMotor
    orangeFlavorPins = [BackendPi.PWR_12V, BackendPi.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    OrangeFlavorMotor = Actuator("R", orangeFlavorPins, "Orange Flavor Motor: Zjchao 202", Actuator.CW)
    ActuatorObject[5] = OrangeFlavorMotor
    FluidActuators = [ActuatorObject[0], ActuatorObject[1], ActuatorObject[2], ActuatorObject[3], ActuatorObject[4], ActuatorObject[5]]
 
    liftMotor1Pins = [BackendPi.PWR_12V, BackendPi1.GND, BackendPi1.TODO]
    LiftMotor1 = Actuator("M", liftMotor1Pins, "Lift Motor 1: TODO")
    ActuatorObject[6] = LiftMotor1
    liftMotor2Pins = [BackendPi1.PWR_12V, BackendPi1.GND, BackendPi1.TODO]
    LiftMotor2 = Actuator("M", liftMotor2Pins, "Lift Motor 2: TODO ECO L11TGF900NB100-T1")
    ActuatorObject[7] = LiftMotor2
    LiftingActuators = [ActuatorObject[6], ActuatorObjects[7]]

    powderServo1Pins = [VCC_5V, GND, BOARD7]
    PowderServo1 = Actuator("S", powderServo1Pins, "Powder Dispensing Servo: Seamuing MG996R")
    ActuatorObject[8] = PowerServo1
    powderServo2Pins = [VCC_5V, GND, BOARD11]
    PowderServo2 = Actuator("S", powderServo2Pins, "Powder Dispensing Servo: Seamuing MG996R")
    ActuatorObject[9] = PowerServo2
    powderMixingServo1Pins = [VCC_5V, GND, BOARD13]
    PowderMixngServo1 = Actuator("S", powderServo1Pins, "Powder Mixing Servo: Seamuing MG996R")
    ActuatorObject[10] = PowerMixingServo1
    powderMixingServo2Pins = [VCC_5V, GND, BOARD15]
    PowderMixngServo2 = Actuator("S", powderServo2Pins, "Powder Mixing Servo: Seamuing MG996R")
    ActuatorObject[11] = PowerMixingServo2
    PowderActuators = [ActuatorObject[8], ActuatorObject[9], ActuatorObject[10], ActuatorObject[11]]

    cuttingMotor1Pins = [BackendPi.PWR_12V, BackendPi1.GND, BackendPi1.TODO]
    
    cuttingMotor2Pins = [BackendPi.PWR_12V, BackendPi1.GND, BackendPi1.TODO]
    
    knifePositionMotorPins [RaspPi.PWR_12V, RaspPi.GND, RaspPi.TODO]
    
    CuttingActuators = [ActuatorObject[12], ActuatorObject[13], ActuatorObject[14]]

    coveringMotor1Pins = [BackendPi.PWR_12V, BackendPi1.GND, BackendPi1.TODO]
    
    coveringMotor2Pins = [BackendPi.PWR_12V, BackendPi1.GND, BackendPi1.TODO]
    
    CoverActuators = [ActuatorObject[15], ActuatorObject[16]]

    
    LaserObject = LASER(LASER.HIGH_POWER)
    guiReady = False 

   #TODO DELETE [ImmunityHealthAdditiveMotor, VitaminsHealthAdditiveMotor, RumFlavorMotor, PinaColadaFlavorMotor, PineappleFlavorMotor, OrangeFlavorMotor LiftMotor1, LiftMotor2, PowderServo1, PowderServo2, PowderMixingServo1, PowderMixingServo2, ]

    while(True):
    	for drinkNum in range(0, MAX_VEND_QUEUE_SIZE-1):
    	    try:
                vendQueue[drinkNum] = GetOrder(UDP_GUI_PI)
    		guiReady = True
    	    except socket.timeout:		# Network connection to GUI down or busy
    	        guiReady = False
    			
    	    finally:	
    	    	if(guiReady == True and vendQueue[drinkNum] != Drink.NONE):
    		    artFilename = vendQueue[drinkNum].GetBrandingArt()
    		    LaserObject.LoadImage(artFilename)
    		    ActuateAddon(vendQueue[drinkNum].GetAddOn())
    	    	    if(vendQueue[drinkNum].GetFlow() == CocoDrink.TAPPED):
    		    	Run(TappingAcutors)
    	            else:
    	            	Run(CuttingActuators)
		else:
		    Debug.Dprint(Debug(True), "No orders in queue")
		    time.sleep(0.1) #Pause for 100 ms to slow down while loop and reduce CPU usage 
				
				
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
