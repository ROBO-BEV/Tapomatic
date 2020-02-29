import sys

import Writer		#TODO Find correct name

class Debug:

	def __init__(self):
		self.DEBUG_STATEMENTS_ON = False	# Toogle debug statements on and off for this python file

	def GetMode():
		return DEBUG_STATEMENTS_ON

	def TurnOnDebugMode():
		DEBUG_STATEMENTS_ON = True

	def TurnOffDebugMode():
		DEBUG_STATEMENTS_ON = False

###
# Debug print to terminal only
# Calls standard Python 3 print("X") statement if global variable is TRUE
#
###
def Dprint(logMessage):
	if(DEBUG_STATEMENTS_ON):
    	print("MSG: " + logMessage)
	else:
		print("/n") # PRINT NEW LINE / DO NOTHING

###
# Log print to both a datalog.txt file and the terminal
#
# @link - https://docs.python.org/3/library/time.html#time.strftime
#
# return NOTHING
###
def Lprint(logMessage):
	Dprint("TIME: " +  time.strftime(%xX,time.localtime))
	Dprint(logMessage)
	file.Write("TIME: " +  time.strftime(%xX,time.localtime))
	file.Write("MSG: " + logMessage)
