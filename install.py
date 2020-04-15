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

# Useful standard Python system jazz
import sys, time, traceback, argparse, string

# Create a command line parser
parser = argparse.ArgumentParser(prog = "Tapomatic v2020.0", description = __doc__, add_help=True)
parser.add_argument("PC_username", type=str, default="Admin", help="Windows 10 username for account you are logged into.")
parser.add_argument("-r", "--rx_Socket", type=int, default=30000, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-s", "--tx_Socket", type=int, default=30100, help="UDP port / socket number for connected Ethernet device.")
parser.add_argument("-t", "--trace", type=int, default=0, help="Program trace level.")
parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on kiosk.")
parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
args = parser.parse_args()

if __name__ == "__main__":
	# Tapomatic v2020.0: error: the following arguments are required: PC_username
	# PS C:\Users\Owner\OneDrive\Documents\GitHub\Tapomatic> python .\install.py Owner
	# 'clear' is not recognized as an internal or external command, operable program or batch file. Traceback (most recent call last):
  	# File ".\install.py", line 35, in <module>
    # check_call("clear",shell=True)              # Clear terminal
 	# File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.8_3.8.752.0_x64__qbz5n2kfra8p0\lib\subprocess.py", line 364, in check_call
    # raise CalledProcessError(retcode, cmd)
	# subprocess.CalledProcessError: Command 'clear' returned non-zero exit status 1.
	# TODO Fix above ```try: except CalledProcessError: ``` around the windows code


	check_call("clear",shell=True)              # Clear terminal

	# Check and update your system
	check_call("sudo apt update", shell=True)
	check_call("sudo apt upgrade", shell=True)
	sleep(5) 			                        # Pause program to allow user to read upgrade output
	check_call("clear",shell=True)


	### Follow these steps to get initial Tapomatic software running

	# Flask requires Python 3 to work
	check_call("sudo apt install python3-pip", shell=True)

	# Use Python Virtual Environment packaging tool PIPENV 
	# When using Windows 10
	check_call("pip install pipenv", shell=True)
	filepath = 'c:\\users\\' + args.PC_username + '\\appdata\\local\\programs\\python\\python36-32\\Scripts'
	check_call("set PATH=%PATH%;set PATH=%PATH%;'" + filepath +"'", shell=True)

	# @link https://pipenv.readthedocs.io/en/latest/basics/
	# @link https://medium.com/@mahmudahsan/how-to-use-python-pipenv-in-mac-and-windows-1c6dc87b403e
	# @link https://stackoverflow.com/questions/46041719/windows-reports-error-when-trying-to-install-package-using-pipenv
	# You can use pipenv easily without issues by the following commands in Power Shell:
	# pipenv install pyserial 
	# pipenv install docutils # Install a documentation library
	# pipenv install numpy # Install a numby library for array creation
	# pipenv shell # activate pipenv
	# pipenv run python GUI.py
	# exit # deactivate and quit




	# When using Linux / Rapsberry Pi 


	# When using Mac install homebrew on Linux

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
