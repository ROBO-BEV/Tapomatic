#!/usr/bin/env python3
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-06-21"
__doc__     = "Logic to run Tapomatic back-end services (i.e. not GUI)"
"""

# Useful standard Python system jazz
import sys, traceback, argparse, string

# Allow UDP communication between computers
import socket

# TODO DOWNSELECT LIBRARIES Allow program to create GMT and local timestamps
from time import sleep, gmtime, strftime
from datetime import datetime, timezone, timedelta

# Allow keyboard to control program flow and typing to terminal window
#import pynput.keyboard
#from pynput.keyboard import Key, Controller

# Create array
#TODO REMOVE import numpy as np

# Custom CocoTaps and Robotic Beverage Technologies Inc code
from CocoDrink import *        	# Store valid CoCoTaps drink configurations
from Actuator import *         	# Modular plug and play control of motors, servos, and relays
from Debug import *		        # Configure datalogging parameters and debug printing control
from RaspPi import *            # Contains usefull GPIO pin CONSTANTS and setup configurations
#from LASER import *		        # Enable LASER movement and image warping around coconut

# Over The Air (OTA) Updating Configurations
VERSION = "2020.0"
PRODUCT_MODE = "PRODUCT"        		# Final product configuration
FIELD_MODE   = "FIELD"					# Non-Techanical repair person configuration
TESTING_MODE = "TESTING"				# Internal developer configuration

# Create a command line parser
parser = argparse.ArgumentParser(prog = "Tapomatic v2020.0", description = __doc__, add_help=True)
parser.add_argument("-i", "--piIP_Address", type=str, default="127.168.1.42", help="IPv4 address of the Tapomatic V0 ID0 backend Raspberry Pi 4.")
parser.add_argument("-r", "--rx_Socket", type=int, default=505, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-s", "--tx_Socket", type=int, default=505, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-u", "--unit", type=str, default= FIELD_MODE, choices=[TESTING_MODE, FIELD_MODE, PRODUCT_MODE], help="Select boot up mode for BARISTO kiosk.")
parser.add_argument("-t", "--trace", type=int, default=0, help="Program trace level.")
parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on kiosk.")
parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
args = parser.parse_args()


# Tapomatic v2020.0 kiosk can process upto 2 coconuts in parallel
MAX_VEND_QUEUE_SIZE = 1

# Max time (in seconds) each of the three processes (Drilling, Tapping, Top Off) takes
MAX_DRILLING_TIME    = 15
MAX_TAPPING_TIME     = 10
MAX_TOPPING_OFF_TIME = 5
MAX_LASER_TIME = MAX_DRILLING_TIME + MAX_TAPPING_TIME + MAX_TOPPING_OFF_TIME

#The TODO?19? actuators CONSTANTS
MAX_NUM_OF_ACTUATORS = 19    		#TODO DOUBLE CHECK THIS
IMMUNITY_ADDITIVE_SERVO = 0         #IMMUNITY_ADDITIVE_PUMP = 0
VITAMIN_ADDITIVE_SERVO = 1          #VITAMIN_ADDITIVE_PUMP = 1
RUM_PUMP = 2
PINA_COLADA_FLAVOR_PUMP = 3
PINEAPPLE_FLAVOR_PUMP = 4
ORANGE_FLAVOR_PUMP = 5
Z1_LINEAR_LIFT_MOTOR = 6
Z2_LINEAR_LIFT_MOTOR = 7
X1_CUTTING_MOTOR = 8
X2_CUTTING_MOTOR = 9
Y1_CUTTING_MOTOR = 10
Y1_LINEAR_COVER_MOTOR = 11
Y2_LINEAR_COVER_MOTOR = 12

ROTATIONTAL_TOOL_MOTOR = 13
Z_LINEAR_TOOL_MOTOR    = 14
Y_LINEAR_TOOL_MOTOR    = 15
X_LINEAR_TOOL_MOTOR    = 16

Z_LINEAR_LASER_MOTOR = 17
Y_LINEAR_LASER_MOTOR = 18
X_LINEAR_LASER_MOTOR = 19

# Tool change CONSTANTS
NO_TOOL = 0
DRILL_BIT_TOOL = -1
TAPPING_SOCKET_TOOL = -2
LASER_BRANDING_TOOL = -3

#TODO REMOVE FOR v2020.1 If force on topping off knife is greater than DULL_KNIFE_FORCE it is probably dull
DULL_KNIFE_FORCE = 100	# Units are Newtons
SHARP = 1
DULL = 0
DULL_KNIFE = -1
NUM_OF_KNIFE_CUTTING_AREAS = 6
#FIX ARRAY CREATION KNIVE_SECTIONS[NUM_OF_KNIFE_CUTTING_AREAS] = [SHARP, SHARP, SHARP, SHARP, SHARP, SHARP]
# [Side A Section 1, Side A Section 2, Side A Section 3, Side B Section 4, Side B Section 5, Side B Section 6]

# Global variables in the Driver.py

previousCuttingForce = SHARP    # Boolean storing status of knife edge during the last occurring count
currentKnifeSectionInUse = 0    # Interger 0 to (NUM_OF_KNIFE_CUTTING_AREAS - 1) describing part of knife being used


def CheckKnifeSharpness():
    """
    Determine if a cutting area is sharp or dull using the cutting force needed during the previous cut

    Key arguments:
    NONE

    Return value:
    previuosCuttingForce -- A float between 0.0 and 220.0 Newtons inclusively
    """

    if(previousCuttingForce > DULL_KNIFE_FORCE):
        KNIVE_SECTIONS[currentKnifeSectionInUse] == DULL
        currentKnifeSectionInUse += 1
        MoveKnifePostion(currentKnifeSectionInUse)

    previousCuttingForce = Sensor.GetForce(Sensor.CUTTING_FORCE_SENSOR)

    return previuosCuttingForce


def MoveKnifePostion():
    """
    Use linear actuator to slide knife left or right and expose new cutting surface / section

    Key arguments:
    NONE

    Return value:
    knifeSectionNowInUse -- The new knife cutting section; otherwise retrun DULL_KNIFE so vendor can be informed    
    """

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
	actuatorObjects -- Array of linear actuators() objects to contro

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


def RunDrill(stopSignal, actuatorObjects):
    """

    Turn ON rotational motor to spin drill bit at high speed until a stopSignal is given

    Key arguments:
    stopSignal - Input signal that can cause drill to stop OTHERWISW MAX_DRILLING_TIME causes drill to stop
    actuatorObjects - Array of linear actuators() objects to control

    return Exit case CONSTANT describing why drill stopped
    """

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


def StopDrill(actuatorObjects):
    """"
    Emergency stop of rotational motor instantly

    return NOTHING
    """
    actuatorObjects[0].min()			# Turn off ONE rotational motor (TODO Is min == off?)
    actuatorObjects[1].min()			# Pull linear Z axis motor back to start position


def SwapTool(newTool):
    """
    Change end effector tool connected to the 3-axis + rotational motor crane system

    newTool - Name of new tool to cennect to the crane system

    return NOTHING
    """

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


def AcutateDoubleSidedKnive(direction, actuatorObjects):
    """
    Top off coconut by cutting striaght across with horizontal knive

    Key arguments:
    direction - Plus or minus X axis direction to cut towards.
    actuatorObjects - Array of linear actuators() objects to control

    Return values:
    return false if top off knive is dull and needs service
    """

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


def ActuateFlavorPump(flavorType, flavorLevel, actuatorObjects):
    """
    Actuate peristaltic pump to dispense liquid milk into cup

    powderType - Product name of powder add-on to dispense (e.g. CINNAMON) 
    powderLevel - Amount of powder units to dispense 1 unit = 0.1 oz
    actuatorObjects - Array of Actuator.py objects to control

    return NOTHING
    """

    if(CoCoDrink.NONE < flavorLevel and flavorLevel <= CoCoDrink.MAX_FLAVOR_LEVEL):
	    actuationTime = flavorLevel / CoCoDrink.FLAVOR_FLOW_RATE  #Units of Seconds based on flow rate per second of pump

    if(flavorType == CoCoDrink.RUM):
	    Debug.Dprint("Pumping RUM into coconut for " + actuationTime  +" seconds")
	    actuatorObjects[0].run(actuationTime, Actuator.N_A, 0.5, Actuator.FORWARD) #PROBABLY CORRECT
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


def GetOrder(timeout):
    """
    Allow UDP communiation over an Ethernet cable between two computers by sending a CSV file from the server / computer running GUI.py and to the client / computer running Driver.py back-end code

    In Tapomatic v2020.0 the Client is the Backend Pi abd the Backedn Pi receives the csv file.

    Key arguments:
    timeout -- Time in milliseconds GetOrder() function should wait for all UDP datapacket to arrive. Suggested timeout is 750 ms or less

    Return value:
    NOTHING
    """

    # Packet buffer size, change this if data seems to be cutoff or missing
    DATA_BUFFER_SIZE = 1024
    UDP_HOST = socket.gethostname()
    UDP_PORT = 5005

    try:
        #Initiate the socket for the UDP Protocol.
        udpClientSocket = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        # Bind the udp socket to the HOST AND PORT.
        udpClientSocket.bind((UDP_HOST, UDP_PORT))
        #TODO Debug.Dprint("Client is running to start receiving the order files.")
        logging.info('Client is running to start receiving the order files.')
    except udpClientSocket.error:
        #TODO Debug.Dprint(driverDebugObject, "Error in creating the udpClientSocket.")
        logging.error('Error in creating the udpClientSocket')

    #TODO TIMESTAMP OBJECT
    #TODO while(timeout > 0):
    while True:
        now = datetime.now(timezone.utc)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)   # Use POSIX epoch with TODO 1, 1
        startTimeStampMicroSec = (now - epoch)//timedelta(microsecond=1)

        # Receiving data from the UDP Server.
        data, addr = udpClientSocket.recvfrom(DATA_BUFFER_SIZE)
        # TODO Debug.Dprint(driverDebugObject, "received message: " + data)
        logging.info('received message:', data) #TODO LOGGING NOT WORKING, HAVE TO FIX
        #TODO Write code to handle this data

        now = datetime.now(timezone.utc)
        endTimeStampMicroSec = (now - epoch)//timedelta(microsecond=1)

        timeout = timeout - (endTimeStampMicroSec/1000 - startTimeStampMicroSec/1000)


if __name__ == "__main__":

    driverDebugObject = Debug(True, "Driver.py")

    #actuatorObjects = np.array(MAX_NUM_OF_ACTUATORS)

    currentTool = NO_TOOL           # Default is having no tool attached to 3-axis system
    currentKnifeSectionInUse = 0    # Always attempt to used section 0 when code restarts

    numberOfOrdersCompleted = 0
    numberOfOrdersInProgress = 0
    #TODO tempDrink = CocoDrink2(CocoDrink2.NONE, CocoDrink2.NONE, CocoDrink2.NONE, CocoDrink2.NONE, CocoDrink2.NONE, CocoDrink2.NONE, CocoDrink2.NONE, CocoDrink2.NONE)
    #TODO tempDrink = CocoDrink(CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE, CocoDrink.NONE)
    vendQueue = np.array(MAX_VEND_QUEUE_SIZE)

    GuiPi = RaspPi()
    BackendPi = RaspPi()


    # Actuators as define in schematic tab at https://upverter.com/design/blazesandersinc/tapomatic-v2020-1
    immunityHealthAdditivePins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.BOARD7]
    vitaminsHealthAdditivePins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.BOARD11]
    actuatorList = [Actuator('S', IMMUNITY_ADDITIVE_SERVO, immunityHealthAdditivePins, "Immunity Boost Servo: Seamuing MG996R", Actuator.CW)]
    actuatorList.append(Actuator('S', VITAMIN_ADDITIVE_SERVO, vitaminsHealthAdditivePins, "Daily Vitamins Servo: Seamuing MG996R", Actuator.CW))
    powderActuatorList = actuatorList

    rumFlavorPins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    pinaColadaFlavorPins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    pineappleFlavorPins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    orangeFlavorPins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    fluidActuatorList =  [Actuator('R', RUM_PUMP, rumFlavorPins, "Rum Flavor Motor: Zjchao 202", Actuator.CW)]
    fluidActuatorList.append(Actuator('R', PINA_COLADA_FLAVOR_PUMP, pinaColadaFlavorPins, "Pina Colada Flavor Motor: Zjchao 202", Actuator.CW))
    fluidActuatorList.append(Actuator('R', PINEAPPLE_FLAVOR_PUMP, pineappleFlavorPins, "Orange Flavor Motor: Zjchao 202", Actuator.CW))
    fluidActuatorList.append(Actuator('R', ORANGE_FLAVOR_PUMP, orangeFlavorPins, "Orange Flavor Motor: Zjchao 202", Actuator.CW))
    # Add fluid actuators to the full system actuator list
    actuatorList.append(fluidActuatorList)

    liftMotor1Pins = [Actuator.HIGH_PWR_12V, Actuator.GND]
    liftMotor2Pins = [Actuator.HIGH_PWR_12V, Actuator.GND]
    liftingActuatorList = [Actuator('L', Z1_LINEAR_LIFT_MOTOR, liftMotor1Pins, "Lift Motor 1: PA-07-12-5V", Actuator.LINEAR_OUT)]
    liftingActuatorList.append(Actuator('L', Z2_LINEAR_LIFT_MOTOR, liftMotor2Pins, "Lift Motor 2: PA-07-12-5V", Actuator.LINEAR_OUT))
    # Add lifting actuators to the full system actuator list
    actuatorList.append(liftingActuatorList)

    cuttingMotor1Pins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    cuttingMotor2Pins = [Actuator.HIGH_PWR_12V, Actuator.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    knifePositionMotorPins = [Actuator.HIGH_PWR_5V, Actuator.GND, BackendPi.I2C_SDA1_NAME, BackendPi.I2C_SCL1_NAME]
    cuttingActuatorList = [Actuator('L', X1_CUTTING_MOTOR, cuttingMotor1Pins, "Cutting Motor 1: PA-04-6-100", Actuator.LINEAR_OUT)]
    cuttingActuatorList.append(Actuator('L', X2_CUTTING_MOTOR, cuttingMotor2Pins, "Cutting Motor 2: PA-04-6-100", Actuator.LINEAR_OUT))
    cuttingActuatorList.append(Actuator('L', Y1_CUTTING_MOTOR, knifePositionMotorPins, "Knife Position Motor: PA-07-?TODO?-5V", Actuator.LINEAR_OUT))
    # Add cutting actuators to the full system actuator list
    actuatorList.append(cuttingActuatorList)

    coveringMotor1Pins = [Actuator.HIGH_PWR_12V, Actuator.GND]
    coveringMotor2Pins = [Actuator.HIGH_PWR_12V, Actuator.GND]
    coveringActuatorList = [Actuator('L', Y1_LINEAR_COVER_MOTOR, coveringMotor1Pins, "Covering Motor 1: PA-07-?TODO?-5V", Actuator.LINEAR_OUT)]
    coveringActuatorList.append(Actuator('L', Y2_LINEAR_COVER_MOTOR, coveringMotor2Pins, "Covering Motor 2: PA-07-?TODO?-5V", Actuator.LINEAR_OUT))
    # Add cocering actuators to the full system actuator list
    actuatorList.append(coveringActuatorList)

    #TODO FIX Vec3b laserObject = LASER("40004672600113", LASER.HIGH_POWER)

    guiReady = False

    while(True):
        for drinkNum in range(0, MAX_VEND_QUEUE_SIZE-1):
    	    try:
    	        vendQueue[drinkNum] = GetOrder(UDP_GUI_PI)
    	        guiReady = True
    	    except socket.timeout:		    # Network connection to GUI down or busy
    	        guiReady = False

    	    finally:
    	    	if(guiReady == True and vendQueue[drinkNum] != Drink.NONE):
                    Run(lifingActuators)    # Raise cocont platform

                    artFilename = vendQueue[drinkNum].GetBrandingArt()
                    LaserObject.LoadImage(artFilename)

                    if(vendQueue[drinkNum].GetFlow() == CocoDrink.TAPPED):
                        Run(tappingAcutors)
                        ActuateAddon(vendQueue[drinkNum].GetAddOn())
                        #TODO actuateSugarMotor(sugarActuators, vendQueue[drinkNum+1].getSugarType, vendQueue[drinkNum+1].getSugarLevel)
                    else:
                        Run(cuttingActuators)

                    Run(lifingActuators)    # Lower cocont platform

    	    	else:
                    Debug.Dprint(driverDebugObject, "No orders in queue")

                    MissionControl()

                    time.sleep(0.1) #Pause for 100 ms to slow down while loop and reduce CPU usage
