#!/usr/bin/env python3
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-06-30"
__doc__     = "Class to define OTA commuications architecture for 30K+ Tapomatic kiosk"
"""

# Allow program to create GMT and local timestamps
from time import gmtime, strftime

# Allow program to READ Comma Separated Value files
import csvreader 

LOW_LIQUID_MESSAGE = 0
PHYSICAL_DAMAGE_MESSAGE = 1
LOW_POWER_MESSAGE = 2
DULL_KNIFE_MESSAGE = 3
VERISON_MESSAGE = 4


class MissionControl():	

	totalCoconutsVended = 0
	totalTapsUsed = 0
	totalFlavorOzUsed = 0
	totalHealthOzUsed = 0
	totalCoirFiberRemoved = 0
	currentHealthPercentage = 100.0
	

    def __init__(self, kioskID, version, key):
		"""
		
		Key arguments:
		kioskID -- Unique ID for every prototype or production Tapomatic manufactured
		version -- Verison on software that should be running on a Tapomatic
		key -- Security key for ALL Tapoamtics to allow Over-The-Air (OTA) updates
		
		Return value:
		New MissionControl() object
		"""

        self.DebugObject = Debug(True, "MissionControl.py")

		self.kioskID = kioskID    
		self.version = version
		self.key = key 			

    def ReportLiquidLevel(lType, internalBottleLocation, kioskID):
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
    	
    	
    	
    def ReportLowLiquidLevel(lType, internalBottleLocation, kioskID):
    	"""
    	High priority alert that the current liquid level is below 20%
    	    	
    	Key arguments:
        lType -- Type of liquid add-on to inject into thr coconut
        internalBottleLocation -- Position starting with 0 that a bottle is from the left side of kiosk as you move right
kioskID -- Unique ID for every prototype or production Tapomatic manufactured

    	Return value:
    	liqPercentage -- Percent (less then 20%) that a 750 mL botle is full
    	"""
    	
    	
    	return liqPercentage
    
    def GetKioskGPSlocation(kioskID):
    	"""
    	Determine the GPS location using celluar towers (not a GPS satilite receiver) or a hard coded value in non-volitile memory 
    	
    	Key arguments:
    	kioskID -- Unique ID for every prototype or production Tapomatic manufactured
    	
    	Return value:
    	gpsData -- Lattitude, Longitude, and Altitude data 
    	
    	Update to RavenDB Implemention in August 20200
    	"""
    	
    	# Hard coded locations that have TERRIBLE cell service 
    	try:
    		f = open(kioskLocation.csv, 'rb')  # open only in read mode.
    		data = f.read(DATA_BUFFER_SIZE) # Read for Buffer Size.
    	except:
    		this.DebugObject.Dprint("Could not open {}, ensure the filepath is correct.")
    	
    	
    	print("TODO RavenDB or TextFile?")
    	
    
    def GetKioskLocationName(kioskID):
        """
    
    	
    	Key arguments:
    	kioskID -- Unique ID for every prototype or production Tapomatic manufactured
    	
    	Return value:
    	locationName -- Human readable String variable describing the location
    	"""
    	#Read CVS and take 2nd entry (0, Vinny's Home, 2728 Brookstone Court Las Vegas NV 89117, 36.1416584, -115.2958079;)
    	
    	return locationName
    	
    	
    	
    def ReportHealthPercentage():
	    """
    	
    	
    	Key arguments:
    	
    	Return value:
    	
    	"""
    	
    	return currentHealthPercentage
    	
    def ReportPowerState():
    	"""
    	
    	
    	Key arguments:
    	
    	Return value:
    	
    	"""
	
    def ReportTapUsage():
    	"""
    	
    	Return value:
    	totalTapsUsed -- Total number of CoirTek taps removed from tap ring since last count. Power cycling machine should NOT reset this variable.
    	"""
    	
    	return totalTapsUsed
	
    def ReportCoconutUsage():
		"""
    	
    	Return value:
    	totalCoconutsUsed -- Total number coconuts tapped since last count. Power cycling machine should NOT reset this variable.
    	"""
    	
    	return totalCoconutsUsed
    
    def ReportKnifeStatus():
    	"""
    	
  
    	Key arguments:
    	
    	Return value:
    	
    	"""
    	#TODO Jan 2021
    	
	def ConnectToDSDservive():
		"""
		Rob's sale CRM and accounting sysytem EDI 944
		https://www.jobisez.com/edi/tp/guide.aspx?doc=/edi-igs/3m/Wins-944-3060.pdf
		"""
		
	def SetEDI944():
	
	def GetEDI944():
		
		
    def StartOTA(verison):
    	"""
		Update kiosk to version specified or newish version if invalid version number is given
		
		"""
	if(verison > 2020.0):
	    DebugObject.Dprint(,"Tracking your IP address, this in not public code :)")
	elif(version == 2020.0):
	    #OLD Tapomatic CodeBase FilePath
	    oldFilepath = "~/Tapomatic/v" + version
	    #NEW Tapomatic CodeBase FilePath
	    newVersion = version + 0.1
            check_call("mkdir newVersion", shell=True)
	    newFilepath = "~/Tapomatic/v" + version
	    check_call("cd newVersion", shell=True)
	    
	   #TODO Start downloading code
	   #curl ???o
	
	elif(verison < 2020.0):
		self.DebugObject.Dprint(,"This is old code that ia on longer supported on this hardware.")
	else:
		self.DebugObject.Dprint(,"Invalid version number updating to v2020.0")
		

	
    def StopOTA():
    	"""
    	
    	
    	Key arguments:
    	
    	Return value:
    	
    	"""
	
	
