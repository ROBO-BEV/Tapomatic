#!/usr/bin/env python

___author__ = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-02-29"
__doc__     = "Install script to setup development enviroment for CoCoTaps Tapomatic v2020.0"

CURRENT_CONFIG = "PI_4_B"
#POSSIBLE_CONFIGS = "NVIDIA_TX2" or "NVIDIA_NANO" # Hard code CURRENT_CONFIG by swapping with one of these

# Allow program to pause operation and create local timestamps
from time import sleep

# Allow BASH command to be run inside Python3 code like this file
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_call

if __name__ == "__main__":
	check_call("clear",shell=True)              # Clear terminal

	# Check and update your system
	check_call("sudo apt update", shell=True)
	check_call("sudo apt upgrade", shell=True)
	sleep(5) 			                        # Pause program to allow user to read upgrade output
	check_call("clear",shell=True)


	### Follow these steps to get initial Tapomatic software running

	# Flask requires Python 3 to work
	check_call("sudo apt install python3-pip", shell=True)

	# Use Python Virtual Environment packaging tool PIPENV by installing homebrew on Linux
	#TODO check_call("brew install pipenv", shell=True)
	#TODO check_call("git clone https://github.com/Homebrew/brew ~/.linuxbrew/Homebrew", shell=True)
	#TODO check_call("mkdir ~/.linuxbrew/bin", shell=True)
	#TODO lcheck_call("vn -s ~/.linuxbrew/Homebrew/bin/brew ~/.linuxbrew/bin", shell=True)
	#TODO check_call("eval $(~/.linuxbrew/bin/brew shellenv)", shell=True)
	#TODO check_call("brew install pipenv", shell=True)

	# Flask is the GUI front-end to that runs in parallel with python back-end controlling pumps
	# Remember to run flask with "python3" NOT "python" command, or you will get weird errors :)
	# @link https://aryaboudaie.com/python/technical/educational/web/flask/2018/10/17/flask.html
	check_call("pip3 install flask", shell=True)
	#TODO check_call("pipenv install flask", shell=True)

	# Set enviroment variable to select GUI.py file as the Flask application
	check_call("export FLASK_APP=GUI.py", shell=True)
