#!/usr/bin/env python3
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-07-23"
__doc__     = "Class to define OTA commuications architecture for 30K+ Tapomatic kiosk"
"""

# Allow program to create GMT and local timestamps
from time import gmtime, strftime

# Allow program to READ Comma Separated Value files
import csv
import RaspPi
import Actuator


class MissionControl():

	# Message CONSTANTS
	LOW_LIQUID_MESSAGE = 0
	PHYSICAL_DAMAGE_MESSAGE = 1
	LOW_POWER_MESSAGE = 2
	DULL_KNIFE_MESSAGE = 3
	VERISON_MESSAGE = 4

	# EDI 944 Interface CONSTANTS from filepath:
	# Tapomatic/v2020.0/static/apiDocumentation/Wins-944-3060.pdf
	# Describes Warehouse Stock Transfer Receipt Advice Transaction Set (944)
	# for use within the context of an Electronic Data Interchange (EDI) environment.
	ST_HEADING  = "Transaction Set Header"
	W17_HEADING = "Warehouse Receipt Identification"
	N1_HEADING  = "Name"

	W07_DETAIL  = "Item Detail For Stock Receipt"
	N9_DETAIL   = "Reference Identification"

	W14_SUMMARY = "Total Receipt Information"
	SE_SUMMARY  = "Transaction Set Trailer"


	# Power CONSTANTS
	ON = 1
	OFF = 0


	# Global Class Variables
	totalCoconutsVended = 0
	totalTapsUsed = 0
	totalFlavorOzUsed = 0.0
	totalHealthOzUsed = 0.0
	totalCoirFiberKgRemoved = 0.0
	currentHealthPercentage = 100.0


	def __init__(self, kioskID, version, key):
		"""
		Constructor to setup a data connection between centrol server (Mission Control) and robot out in field

		Key arguments:
		self -- Newly created object
		kioskID -- Unique ID for every prototype or production Tapomatic manufactured
		version -- Verison of software that is running on remote device
		key -- Security key for devices to allow Over-The-Air (OTA) updates

		Return value:
		New MissionControl() object
		"""

		currentProgramFilename = os.path.basename(__file__)
		self.DebugObject = Debug(True, currentProgramFilename)

		self.kioskID = kioskID
		self.version = version
		self.key = key

		# Definition for sensors sending data back to Mission Control (internal sensors not included)
		pins = [Actuator.VCC_3_3V, RaspPi.BOARD, RaspPi.PWM0, Actuator.GND]
		self.ForceSensorObject = Sensor(Sensor.FORCE_SENSOR,pins, Sensor.FORCE_SENSOR_PART_NUMBER)
		pins = [Actuator.VCC_3V, RaspPi.BOARD, Actuator.GND]
		self.laserRangerFinderObject = Sensor(Sensor.LASER_RANGE_SENSOR, pins, Sensor.LASER_RANGE_PART_NUMBER)


	def ReportLiquidLevel(self, lType, internalBottleLocation, kioskID):
		"""
		Report the current liquid level as percentage

		Key arguments:
		lType -- Type of liquid add-on to inject into thr coconut
		internalBottleLocation -- Position starting with 0 that a bottle is from the left side of kiosk as you move right
		kioskID -- Unique ID for every prototype or production Tapomatic manufactured

		Return value:
		liqPercentage -- Percent that a 750 mL botle is full
		"""
		return liqPercentage


	def ReportLowLiquidLevel(self, lType, internalBottleLocation, kioskID):
		"""
		High priority alert that the current liquid level is below 20%

		Key arguments:
		lType -- Type of liquid add-on to inject into the coconut
		internalBottleLocation -- Position starting with 0 that a bottle is from the left side of kiosk as you move right
		kioskID -- Unique ID for every prototype or production Tapomatic manufactured

		Return value:
		liqPercentage -- Percent (less then 20%) that a 750 mL botle is full
		"""

		return liqPercentage


	def GetKioskGPSlocation(self, kioskID):
		"""
		Determine the GPS location using celluar towers (not a GPS satilite receiver) or a hard coded value in non-volitile memory
		Update to RavenDB Implemention in August 20200

		Key arguments:
		kioskID -- Unique ID for every prototype or production Tapomatic manufactured

		Return value:
		gpsData -- Lattitude, Longitude, and Altitude data
		"""

		# Hard coded locations that have TERRIBLE cell service
		try:
			print("TODO RavenDB or TextFile?")
			##TODO Blaze , Until END OF 2020 Better to have textfile only.
			f = open(kioskLocation.csv, 'rb')   # Open only in read mode.
			# data = f.read(DATA_BUFFER_SIZE)     # Read for Buffer Size.
			if(data[0] == kioskID):
				gpsData = [data[3],  data[4]]   # Latitude & Longitude
			else:
				gpsData = Sensor.GetLocation()
		except:
			this.DebugObject.Dprint("Could not open {kioskLocation.txt}, ensure the filepath is correct.")
			gpsDATA = [Debug.BAD, DEBUG.BAD]
		return gpsData


	def GetKioskLocationName(self, kioskID):
		"""
		#TODO Description

		Key arguments:
		kioskID -- Unique ID for every prototype or production Tapomatic manufactured

		Return value:
		locationName -- Human readable String variable describing the location
		"""

		#Read CVS and take 2nd entry (0, Vinny's Home, 2728 Brookstone Court Las Vegas NV 89117, 36.1416584, -115.2958079;)
		return locationName


	def ReportHealthPercentage(self):
		"""
		#TODO Description

		Key arguments:

		Return value:

		"""

		return currentHealthPercentage


	def ReportPowerState(self):
		"""
		TODO

		Key arguments:

		Return values:
		ON -- if Tapomatic is plugged in and main relay is ON; OFF otherwise
		"""

		if(gpiozero.mainPowerRelay.isActive()):
			powerState = ON
		else:
			powerState = OFF

		return powerState

	def ReportTapUsage(self):
		"""
		#TODO Description

		Return value:
		totalTapsUsed -- Total number of CoirTek taps removed from tap ring since last count. Power cycling machine should NOT reset this variable.
		"""

		return totalTapsUsed


	def ReportCoconutUsage(self):
		"""
		#TODO Description

		Return value:
		totalCoconutsUsed -- Total number coconuts tapped since last count. Power cycling machine should NOT reset this variable.
		"""

		return totalCoconutsUsed


	def ReportKnifeStatus(self):
		"""
		TODO REMOVE in v2020.1

		Return value:
		sharpness -- Interger, from 0 to MAX_CUTTING_SURFACES
		"""

		return -1


	def ConnectToDSDservive(self, serviceName):
		"""
		Rob's sale CRM and accounting sysytem EDI 944
		https://www.jobisez.com/edi/tp/guide.aspx?doc=/edi-igs/3m/Wins-944-3060.pdf

		Key arguments:
		serviceName -- String,

		Return value:
		status -- Interger, HTML error code
		"""


	def SetEDI944(self):
		"""
		Write to EDI 944 text file using interface defined at:
		https://www.jobisez.com/edi/tp/guide.aspx?doc=/edi-igs/3m/Wins-944-3060.pdf

		"""
		try:
			f = open(CocoEDI944.txt, 'rb')   # Open only in read mode.
			data = f.read(self.DATA_BUFFER_SIZE)     # Read for Buffer Size.
			if(data[0] == self.W7_HEADER):
				stockData = [data[3],  data[4]]   # Latitude & Longitude
			else:
				print('In else block')
		except:
			self.DebugObject.Dprint("Could not open {CocoEDI944.txt}, ensure the filepath is correct.")
			stockData = [Debug.BAD, DEBUG.BAD]
		return -1


	def GetEDI944(self):
		"""
		Read from  EDI 944 text file using interface defined at:
		https://www.jobisez.com/edi/tp/guide.aspx?doc=/edi-igs/3m/Wins-944-3060.pdf


		"""

		return -1


	def StartOTA(self, verison):
		"""
		Update kiosk to version specified or newish version if invalid version number is given

		Key arguments:
		version -- Verison on software that should be running on a Tapomatic

		Return value:
		??? --	    
		"""

		if(verison > 2020.0):
			self.DebugObject.Dprint("Tracking your IP address, this in not public code :)")
		elif(version == 2020.0):
			#OLD Tapomatic CodeBase FilePath
			oldFilepath = "~/Tapomatic/v" + version
			#NEW Tapomatic CodeBase FilePath
			newVersion = version + 0.1
			check_call("mkdir newVersion", shell=True)
			newFilepath = "~/Tapomatic/v" + version
			check_call("cd newVersion", shell=True)

			#TODO Start downloading code with wget or CURL (CURL is most likely not useful)
			# https://curl.haxx.se/docs/manpage.html
			# https://stackoverflow.com/questions/15034471/using-git-and-curl-command-line
			# curl https://github.com/ROBO-BEV/Tapomatic

			check_call("wget https://github.com/ROBO-BEV/Tapomatic/tree/master/v2020.1", shell=True)
			#TODO USE THIS url = "https://github.com/ROBO-BEV/Tapomatic/tree/master/" + newVersion
			#TODO wget url

		elif(verison < 2020.0):
			self.DebugObject.Dprint("This is old code that ia on longer supported on this hardware.")
		else:
			self.DebugObject.Dprint("Invalid version number updating to v2020.0")


	def StopOTA(self):
		"""

		Key arguments:

		Return value:

		"""

		return -1


	def UnitTest():
		"""
		Test object creatation and .key file reading

		Return value:
		DEBUG.OK if all tests pass

		"""

		print("START MissionControl.py UnitTest()")

		try:
			filename = ".key"
			f = open(filename, 'rb')            # Open only in read mode.
			data = f.read(DATA_BUFFER_SIZE)     # Read for Buffer Size.
		except:
			this.DebugObject.Dprint("Could not open {}, ensure the filepath is correct.")

		prototypeKioskID = 0
		GoodMissionControlObject = MissionControl(prototypeKioskID, 2020.0, f)
		GoodMissionControlObject.ReportLiquidLevel(CocoDrink.ORANGE_FLAVOR, 0, prototypeKioskID)

		#BadMissionControlObject = MissionControl(1, 2020.2, ".key")
		GoodMissionControlObject.GetKioskGPSlocation(prototypeKioskID)
		print("END UnitTest()")

		return DEBUG.OK


if __name__ == "__main__":

	try:
		passedTest = MissionControl.UnitTest()
	except NameError:
		print("UnitTest() failed - Have a nice day :)")

	print("END MissionControl.py MAIN")
