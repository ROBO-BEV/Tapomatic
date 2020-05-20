#!/usr/bin/env python

__author__  = "Murali Dulla"
__email__   = "jeevanmurali@gmail.mvp"
__company__ = "COCOTAPS"
__status__  = "Development"
__date__    = "Late Updated: 2020-05-14"
__doc__     = "UDP Server to send the kiosk orders to the UDP Client running on PI4."

import socket
from time import sleep
import sys, logging

#Buffer Size , change this if want to send the data in a different size.
# Make sure to change the same variable in client as well.
DATA_BUFFER_SIZE = 1024

##In Tapomatic v2020.0 the server in the GUI Pi
# GUI Pi send the CSV file format.
class UDPServer:
    def raspberryServerProgram(self,filename):
            """
               Initiate the UDP Socket and send CSV file to the Client.
               Key arguments: file to send to the raspberry PI Client.
               #Return Value: Nothing
            """

            # localIP = socket.gethostname()
            # localPort = 5000
            # udpServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
            # udpServerSocket.bind((localIP, localPort))

            #TODO Find a way to get the client PI address here.
            UDP_CLIENT_IP = socket.gethostname()
            UDP_CLIENT_PORT = 5005
            try:
                # Initiate the socket for the UDP Protocol.
                udpClientSocket = socket.socket(socket.AF_INET,  # Address Family.
                                                socket.SOCK_DGRAM)  # UDP
                logging.info('Running the server program to start sending order files.')
            except udpClientSocket.error:
                logging.error('Error in creating the udpClientSocket')
                #TODO INVOKE A SMS MESSAGE TO THE OWNER? or To the Cloud?
                sys.exit(1)
            #LOOP CONDITIONS????
            while (True):
                try:
                    f = open(filename, 'rb')  # open only in read mode.
                    l = f.read(DATA_BUFFER_SIZE) # Read for Buffer Size.
                except:
                    logging.error("Could not open {}, ensure the filepath is correct.".format(
                        self.raspberryServerProgram))
                    sys.exit(1)
                while (l):
                    udpClientSocket.sendto(l,(UDP_CLIENT_IP, UDP_CLIENT_PORT)) # Send Data to the UDP Client using the clinet IP and PORT.
                    logging.info('Sent ',repr(l)) #TODO LOGGING NOT WORKING, HAVE TO FIX
                    print('Sent' ,  repr(l))
                    # Read the file with DATA BUFFER SIZE.
                    l = f.read(DATA_BUFFER_SIZE)
                #Close the file, once done with file content.
                f.close()
                sleep(15) ##TODO Refractor this Code, USE THREADING ?

if __name__ == '__main__':
    #TODO: Accept file path and name via args from command line?
    filename= 'coco_orders.csv'
    object = UDPServer()
    UDPServer.raspberryServerProgram(object, filename)