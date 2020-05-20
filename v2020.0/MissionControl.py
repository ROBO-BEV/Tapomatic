#!/usr/bin/env python

"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.mvp"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-05-12"
__doc__     = "Class to define OTA commuications architecture of 30K+ Tapomatic kiosk"
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
	

    def __init__(self, kioskID, version, key):
		"""
		
		Key arguments:
		kioskID -- Unique ID for every prototype or production Tapomatic manufactured
		version -- Verison on software that should be running on a Tapomatic
		key -- Security key for ALL Tapoamtics to allow Over-The-Air (OTA) updates
		
		Return value:
		Newly created MissionControl() object
		"""

        self.DebugObject = Debug(True)

		self.kioskID = kioskID    
		self.version = version
		self.key = key 			

    def ReportLiquidLevel(lType, internalBottleLocation, kioskID):
    	"""
    	Report the current liquid level as perfectage 
    	
    	"""
    	
    	
    	
    	
    	
    def ReportLowLiquidLevel(lType, internalBottleLocation, kioskID):
    	"""
    	High priority alert that the current liquid level is below 20%
    	"""
    
    def GetKioskGPSlocation(kioskID):
    	"""
    	Update to RavenDB Implemention in August 20200
    	"""
    	print("TODO RavenDB or TextFile?")
    	
    
    def GetKioskLocationName():
    
    def ReportDamage():
	
    def ReportPowerState():
	
    def ReportCoconutUsage():
	
    def ReportTapUsage():
	 
    def ReportKnifeStatus():
    	

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
		DebugObject.Dprint(,"This is old code that ia on longer supported on this hardware.")
	else:
		DebugObject.Dprint(,"Invalid version number updating to v2020.0")
		

	
    def StopOTA():
	
	
