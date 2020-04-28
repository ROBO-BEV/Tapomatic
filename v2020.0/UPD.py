#!/usr/bin/env python

import os, sys, time, traceback, argparse
sys.path.insert(1, "../../Packages")
from swiftradio.clients import SwiftRadioEthernet
from swiftradio.clients import SwiftUDPClient
import swiftradio

__author__ = "Ethan Sharratt"
__email__ = "sharratt@tethers.com"
__company__ = "Tethers Unlimited Inc."
__status__ = "Development"
__date__ = "Late Updated: 08/02/16"
__doc__ = "Script for sending a file to the radio to be downlinked."

STX_PKTSIZE = 1115

def GetFile(radioIP_Address, port, filename, loop):
	try:
		# Ensure a file was given.
		if filename == None:
			print "No file provided, please use the -f option and provide a filepath."
			sys.exit(1)

		# Instantiate a UDP connection to the downlink port.
		try:
			udp = SwiftUDPClient(radioIP_Address, port)
			udp.connect()
		except:
			print "Could not open a udp client for the provided IPv4 address and port."
			sys.exit(1)

		# Open the transmit data file
		try:
			f = open(filename, 'rb')
			dfstats = os.stat(filename)
			dfsize = dfstats.st_size
		except:
			print "Could not open {}, ensure the filepath is correct.".format(filename)
			sys.exit(1)

		# Send file to radio
		bytes = 0
		dataLeftToRead = True
		while dataLeftToRead:
			data = f.read(STX_PKTSIZE)
			bytes += len(data)
			sys.stdout.write("\rTransferring file...{:.3f}%".format(100*float(bytes)/float(dfsize)))
			if not data:
				sys.stdout.write("\rTransferring file...100.00%\n")
				if loop == 1:
					f.seek(0,0)
					bytes = 0
					time.sleep(.1)
				else:
					dataLeftToRead = False					
					#f.close()        PROGRAM SHOULD NOT END WHEN DATA IS GONE
					#udp.disconnect()
					#sys.exit(1)     
			else:
				udp.write(data,len(data))

	except KeyboardInterrupt:
		f.close()
		udp.disconnect()
	except:
		traceback.print_exc()