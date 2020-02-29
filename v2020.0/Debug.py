#!/usr/bin/env python

__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-02-29"
__doc__     = "Code to make print() debuggging and data logging easier"

# Allow program to create GMT and local timestamps
from time import gmtime, strftime

class Debug:

    def __init__(self):
        self.f = open('DataLog.txt','r+')
        self.DEBUG_STATEMENTS_ON = False	# Toogle debug statements on and off for this python file

    def GetMode(self):
	    return self.DEBUG_STATEMENTS_ON

    def TurnOnDebugMode(self):
        self.DEBUG_STATEMENTS_ON = True

    def TurnOffDebugMode(self):
        self.DEBUG_STATEMENTS_ON = False

    def CloseFile(self):
        self.f.close()

    ###
    # Debug print to terminal only
    # Calls standard Python 3 print("X") statement if global variable is TRUE
    #
    ###
    def Dprint(self, logMessage):
        if(self.DEBUG_STATEMENTS_ON):
            print("MESSAGE: " + logMessage)
        else:
            print("/n") # PRINT NEW LINE / DO NOTHING

    ###
    # Log print to both a datalog.txt file and the terminal
    #
    # @link - https://docs.python.org/3/library/time.html#time.strftime
    #
    # return NOTHING
    ###
    def Lprint(self, logMessage):
        self.Dprint("DAY & TIME: " +  strftime("%c")) # Sat Feb 29 13:48:05 2020 
        self.Dprint(logMessage)

        self.f.write("DAY & TIME: " +  strftime("%c"))
        self.f.write("MESSAGE: " + logMessage)


if __name__ == "__main__":
    print("UNIT TESTING:")
    test = Debug()

    print(test.GetMode())
    test.Dprint("This should not print :)")
    test.TurnOnDebugMode()
    print(test.GetMode())

    test.Dprint("Hello World")
    test.Lprint("Goodbye World data logging is NOT fun")
    test.Lprint("Just kidding :)")
    test.TurnOffDebugMode()
    test.Dprint("This should not print either :)")
    test.CloseFile()
