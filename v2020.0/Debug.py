import sys

import Writer		#TODO Find correct name

DEBUG_STATEMENTS_ON = True    		# Toogle debug statements on and off for this python file


def __init__():
	DEBUG_STATEMENTS_ON = False		# Toogle debug statements on and off for this python file

def TurnOnDebugMode():
	DEBUG_STATEMENTS_ON = True

def TurnOffDebugMode():
	DEBUG_STATEMENTS_ON = False

###
# Debug prini to terminal only
# Calls standard Python 3 print("X") statement if global variable is TRUE
#
###
def Dprint(logMessage):
	if(DEBUG_STATEMENTS_ON):
    	print("MSG: " + logMessage)
	else:
		print("/n") # PRINT NEW LINE / DO NOTHING

###
# Log prini to both datalog.txt file and terminal
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
