#!/usr/bin/env python

___author__ = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-02-18"
__doc__     = "Install script to setup run and dev enviroment for CoCoTaps Tapomatic v2020.0"

CURRENT_CONFIG = "Pi4B"
#POSSIBLE_CONFIGS = "UnbuntuOnWindows" of "UbuntuMateOnPC" or "NvidiaTX2" or "NvidiaNano"

# Allow program pausing and timestamp creation
import time

# Allow BASH command to be run inside Python3 code like this file
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_call

if __name__ == "__main__":
	check_call("clear",shell=True)  # Clear terminal

	# Check and update your system
	check_call("sudo apt update", shell=True)
	check_call("sudo apt upgrade", shell=True)
	time.sleep(5) 			#Pause program to allow user to read upgrae info
	check_call("clear",shell=True)  # Clear terminal


	### Follow these steps to get initial cafeBEEP software running

	# Flask requires Python 3 to work
	check_call("sudo apt install python3-pip", shell=True)

	# Use Python Virtual Environment Packaging Tool
	#TODO check_call("pip install pipenv", shell=True)

	# Flask is the GUI frontend to that runs in parallel with python backend controling pumps
	# Remember to run flask with "python3" NOT "python" command, or you will get weird errors :)
	# https://aryaboudaie.com/python/technical/educational/web/flask/2018/10/17/flask.html
	check_call("pip3 install flask", shell=True)
	#TODO check_call("pipenv install flask", shell=True)
