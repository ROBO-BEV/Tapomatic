#!/usr/bin/env python

__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.mvp"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-06-22"
__doc__     = "Logic to run Flask based GUI front-end for CoCoTaps"

# Useful system jazz
import sys, traceback, argparse, string

from time import sleep #TODO REMOVE?

# Allows for the creation of a GUI web app that communicates with python backend code
# Saves HTML files in a folder called "templates" in the same folder as your Flask code
# Saves user state / data across page refreshes and crashes, by using browser cookies
from flask import Flask, render_template, session

# Allow BASH command to be run inside Python3 code like this file
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_call

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *
#TODO import Drink

#
from flask import request
# Make a Flask application and start running code from __main__
app = Flask(__name__)
app.secret_key = 'FreshCoConuts@42'			# TODO Select STRONG key for production code
app.config['SESSION_TYPE'] = 'filesystem'	# TODO Fix Image URL filepath code in welcome.html

@app.route('/')
def WelcomeScreen():
	HTMLtoDisplay = "welcome.html"
	return render_template(HTMLtoDisplay)

@app.route('/TapOrCut', methods=['GET'])
def TapOrCutScreen():
	"""
	GUI for displaying options to the user Cancel order or  1. Tap 2. Cutoff.
	HTTP GET Method
	:return: HTML template to display TaporCut
	"""
	# userSelection = request.args.get('userselection')
	# print('userSelection:: ' + str(userSelection))
	HTMLtoDisplay = "tapOrCut.html"
	return render_template(HTMLtoDisplay)


@app.route('/Branding', methods=['GET'])
def Branding():
	"""
	GUI for displaying options to the user for selecting a brand to get printed on the coconut.
	HTTP GET Method
	@userselection from the tapOrCut userselection. Depending on userselection, will prepare the order. (Tap or Cutoff)
	:return: HTML template to display branding.html
	"""
	userSelection = request.args.get('userselection')
	print('userSelection:: ' + str(userSelection))
	HTMLtoDisplay = "branding.html"
	return render_template(HTMLtoDisplay)

@app.route('/Health', methods=['GET'])
def Health():
	"""
	GUI for displaying options to the user for selecting Health Supplements
	 HTTP GET Method
	 @userselection from the branding.html , Depending on userselection, will print the brand on the coconut.
	:return: HTML template to display health.html
	"""
	userSelection = request.args.get('userselection')
	print('userSelection:: ' + str(userSelection))
	HTMLtoDisplay = "health.html"
	return render_template(HTMLtoDisplay)


@app.route('/Flavor', methods=['GET'])
def Flavor():
	"""
	GUI for displaying options to the user for selecting different flavors.
	HTTP GET Method
	@userselection from the health.html , Depending on userselection, will mix the selected healthy supplement to the order.
	:return: HTML template to display flavor.html
	"""
	userSelection = request.args.get('userselection')
	print('userSelection:: ' + str(userSelection))
	HTMLtoDisplay = "flavor.html"
	return render_template(HTMLtoDisplay)


@app.route('/Waiting', methods=['GET'])
def Waiting():
	"""
	TODO This function will get a signal from the SYSTEM???? to move on to the next screen.
	GUI to display WAITING.
    HTTP GET Method
    @userselection from the flavor.html , Depending on userselection, will mix the selected flavor to the order.
	:return: HTML template to display waiting.html
	"""
	userSelection = request.args.get('userselection')
	print('userSelection:: ' + str(userSelection))
	HTMLtoDisplay = "waiting.html"
	return render_template(HTMLtoDisplay)

@app.route('/Complete')
def CompleteScreen():
	"""
	GUI to display COMPLETE.
	HTTP GET Method
	:return: HTML template to display complete.html
	"""
	HTMLtoDisplay = "complete.html"
	return render_template(HTMLtoDisplay)

if __name__ == '__main__':
    DebugOject = Debug(True, "GUI.py")
    app.run(debug=True)
    if(DebugOject.GetMode == True):
	    # Allow URLs to be refreshed (F5) without restarting web server after code changes
	    app.run(debug=True)
	    check_call("export FLASK_DEBUG=1", shell=True)
    else:
	    app.run(debug=False) # check_call("export FLASK_DEBUG=0", shell=True)
	    app.run(host='0.0.0.0')

    # #WelcomeScreen()
    # #TODO Add button code
    # #sleep(3)
    # TapOrCutScreen()
    #
    # print("Sleeping Worked")
    # #FlavorScreen()
    # #sleep(3)
    # #BrandScreen()
    # #sleep(3)
    # #WaitingScreen()
    # #sleep(3)
    # #CompleteScreen()
