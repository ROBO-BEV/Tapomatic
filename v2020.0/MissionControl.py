#!/usr/bin/env python

"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-04-29"
__doc__     = "Class to define OTA commuications architecture of 30K+ Tapomatic kiosk"
"""

# Allow program to create GMT and local timestamps
from time import gmtime, strftime

LOW_LIQUID_MESSAGE = 0
PHYSICAL_DAMAGE_MESSAGE = 1
LOW_POWER_MESSAGE = 2
DULL_KNIFE_MESSAGE = 3


class MissionControl():	

    def __init__(self, currentNumOfSensors, currentNumOfActuators, kioskID, version):
	"""

	"""

        self.DebugObject = Debug(True)

	self.kioskID = kioskID    

    def ReportLiquidLevel(lType, percentage, kioskID):
		
    def ReportLowLiquidLevel(lType, bottleLocation, kioskID):
    
    def ReportDamage():
	
    def ReportPowerState():
	
    def ReportCoconutUsage():
	
    def ReportTapUsage():
	 
    def ReportKnifeStatus()

    def StartOTA(verison):
	# Check for valid version number
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
	   #curl ???
	
	else:
	   print("TODO") 

	
    def StopOTA():
	
	
