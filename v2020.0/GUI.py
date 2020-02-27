#!/usr/bin/env python

__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-02-18"
__doc__     = "Logic to run Flask based GUI front-end for CoCoTaps"

#TODO import Drink

# Useful system jazz
import sys, time, traceback, argparse, string

# Allows for the creation of a GUI web app that communicates with python backend code
# Saves HTML files in a folder called "templates" in the same folder as your Flask code
# Saves user state / data across page refreshes and crashes, by using browser cookies
from flask import Flask, render_template, session

# Make a Flask application and start running code from __main__
app = Flask(__name__)
app.secret_key = 'FreshCoConuts@42'			# TODO Select STRONG key for production code
app.config['SESSION_TYPE'] = 'filesystem'	# TODO Fix Image URL filepath code in welcome.html

@app.route('/')
def HomeScreen():
	HTMLtoDisplay = "welcome.html"
	return render_template(HTMLtoDisplay)

def WaitingScreen():
	HTMLtoDisplay = "waiting.html"
	return render_template(HTMLtoDisplay)

def CompleteScreen():
	HTMLtoDisplay = "complete.html"
	return render_template(HTMLtoDisplay)

if __name__ == '__main__':
	if(Debug.GetMode()):
		# Allow URLs to be refreshed (F5) without restarting web server after code changes
		app.run(debug=True) # check_call("export FLASK_DEBUG=1", shell=True)
	else::
		check_call("export FLASK_DEBUG=0", shell=True)
		app.run(host='0.0.0.0')

	HomeScreen()
	#TODO IF BUTTON PRESSED
	#WaitingScreen()
	#CompleteScreen()
