#!/usr/bin/env python
"""
___author__ = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-04-17"
__doc__     = "Install script to setup development enviroment for CoCoTaps Tapomatic v2020.0"
"""

CURRENT_CONFIG = "PI_4_B"
#POSSIBLE_CONFIGS = "NVIDIA_TX2" or "NVIDIA_NANO" # Hard code CURRENT_CONFIG by swapping with one of these

# Allow program to pause operation and create local timestamps
from time import sleep

# Allow BASH command to be run inside Python3 code like this file
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_call

# Useful standard Python system jazz
import sys, time, traceback, argparse, string

# Create a command line parser
parser = argparse.ArgumentParser(prog = "Tapomatic v2020.0", description = __doc__, add_help=True)
parser.add_argument("PC_username", type=str, default="Admin", help="Windows 10 username for account you are logged into.")
parser.add_argument("Computer_Type", type=str, default="Admin", help="Please type (PC, Mac, or Pi).")
parser.add_argument("-r", "--rx_Socket", type=int, default=30000, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-s", "--tx_Socket", type=int, default=30100, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-t", "--trace", type=int, default=0, help="Program trace level.")
parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on kiosk.")
parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
args = parser.parse_args()

if __name__ == "__main__":

	# When using Windows 10 code flows here
	if(args.Computer_Type == "PC" or args.Computer_Type == "pc"):
		# Tapomatic v2020.0: error: the following arguments are required: PC_username
		# PS C:\Users\Owner\OneDrive\Documents\GitHub\Tapomatic> python .\install.py Owner
		# 'clear' is not recognized as an internal or external command, operable program or batch file. Traceback (most recent call last):
  		# File ".\install.py", line 35, in <module>
    	# check_call("clear",shell=True)              # Clear terminal
 		# File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.8_3.8.752.0_x64__qbz5n2kfra8p0\lib\subprocess.py", line 364, in check_call
    	# raise CalledProcessError(retcode, cmd)
		# subprocess.CalledProcessError: Command 'clear' returned non-zero exit status 1.
		# TODO Fix above ```try: except CalledProcessError: ``` around the windows code
		
		# @link https://stackoverflow.com/questions/46041719/windows-reports-error-when-trying-to-install-package-using-pipenv
		# @link https://medium.com/@mahmudahsan/how-to-use-python-pipenv-in-mac-and-windows-1c6dc87b403e
		print("Please install Python3.7 or higher from www.python.org/downloads/windows/ before running install.py")
		check_call("pip install pipenv", shell=True)    							#TODO Does this work with PowerShell?
		filepath = 'c:\\users\\' + args.PC_username + '\\appdata\\local\\programs\\python\\python36-32\\Scripts'
		check_call("set PATH=%PATH%;set PATH=%PATH%;'" + filepath +"'", shell=True) #TODO Does this work with PowerShell?

	# When using Linux / Rapsberry Pi code flows here 
	if(args.Computer_Type == "Pi" or args.Computer_Type == "pi"):
		check_call("clear",shell=True)              # Clear terminal
		check_call("sudo apt update", shell=True) 	# Check and update your system
		check_call("sudo apt upgrade", shell=True)
		sleep(5) 			                        # Pause program to allow user to read upgrade output
		check_call("clear",shell=True)
		check_call("sudo apt install python3-pip", shell=True) 	# Flask requires Python 3 to work
		check_call("pip install pipenv", shell=True)

	# When using Mac code flows here 
	if(args.Computer_Type == "Mac" or args.Computer_Type == "mac" or args.Computer_Type == "MAC"):
		# Install a real package manager (Homebrew) on the Mac :) https://brew.sh
		check_call("/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
", shell=True)
		#check_call("git clone https://github.com/Homebrew/brew ~/.linuxbrew/Homebrew", shell=True)
		#check_call("mkdir ~/.linuxbrew/bin", shell=True)
		#check_call("vn -s ~/.linuxbrew/Homebrew/bin/brew ~/.linuxbrew/bin", shell=True)
		#check_call("eval $(~/.linuxbrew/bin/brew shellenv)", shell=True)
		# Flask requires Python 3 to work
		check_call("brew install python3", shell=True)
		check_call("brew install pipenv", shell=True)
		check_call("brew install docutils", shell=True)
		check_call("brew install numpy", shell=True) 
		check_call("brew install opencv-python", shell=True) 

	# Start PIPENV Python Virtual Environment packaging tool installs 
	# @link https://pipenv.readthedocs.io/en/latest/basics/
	# Communicate with sensors
	# TODO DO WE NEEDED THIS? check_call("pipenv install pyserial", shell=True)
	
	# Flask is the GUI front-end to that runs in parallel with python back-end controlling pumps
	# Remember to run flask with "python3" NOT "python" command, or you will get weird errors :)
	# @link https://aryaboudaie.com/python/technical/educational/web/flask/2018/10/17/flask.html
	check_call("pipenv install flask", shell=True) 		# Python microframework for GUI creation 
	check_call("export FLASK_APP=GUI.py", shell=True)   # Set enviroment variable to select GUI.py file as the Flask application

	# Install a documentation library
	check_call("pipenv install docutils", shell=True) 	
	
	# Install a numby library for array creation
	check_call("pipenv install numpy", shell=True)		

	# Install computer vision library to wrap images around coconuts and load photos
	check_call("pip install opencv-python", shell=True)
	
	# Activate PIPENV
	check_call("pipenv shell", shell=True) 				
	
	# Start GUI
	check_call("pipenv run python GUI.py", shell=True)	
	
	# exit # deactivate and quit
