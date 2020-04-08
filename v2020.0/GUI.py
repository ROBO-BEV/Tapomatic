#!/usr/bin/env python

__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-04-08"
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

# Make a Flask application and start running code from __main__
app = Flask(__name__)
app.secret_key = 'FreshCoConuts@42'			# TODO Select STRONG key for production code
app.config['SESSION_TYPE'] = 'filesystem'	# TODO Fix Image URL filepath code in welcome.html

@app.route('/')
def WelcomeScreen():
	HTMLtoDisplay = "welcome.html"
	return render_template(HTMLtoDisplay)

@app.route('/Waiting')
def WaitingScreen():
	HTMLtoDisplay = "waiting.html"
	return render_template(HTMLtoDisplay)

@app.route('/TapOrCut')
def TapOrCutScreen():
	HTMLtoDisplay = "tapOrCut.html"
	return render_template(HTMLtoDisplay)

@app.route('/Complete')
def CompleteScreen():
	HTMLtoDisplay = "complete.html"
	return render_template(HTMLtoDisplay)

if __name__ == '__main__':
    DebugOject = Debug(True)
    if(DebugOject.GetMode == True):
	    # Allow URLs to be refreshed (F5) without restarting web server after code changes
	    #app.run(debug=True)
	    check_call("export FLASK_DEBUG=1", shell=True)
    else:
	    app.run(debug=False) # check_call("export FLASK_DEBUG=0", shell=True)
	    app.run(host='0.0.0.0')

    #WelcomeScreen()
    #TODO Add button code
    #sleep(3)
    TapOrCutScreen()
    sleep(3)
    print("Sleeping Worked")
    #FlavorScreen()
    #sleep(3)
    #BrandScreen()
    #sleep(3)
    #WaitingScreen()
    #sleep(3)
    #CompleteScreen()
