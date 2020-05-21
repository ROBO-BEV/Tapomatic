#!/usr/bin/env python
__author__  = "Murali Dulla"
__email__   = "jeevanmurali@gmail.mvp"
__company__ = "COCOTAPS"
__status__  = "Development"
__date__    = "Late Updated: 2020-05-14"
__doc__     = "UDP Client to receive the kiosk orders from the UDP Server running on GUI PI4."

#In Tapomatic v2020.0 the Client is the Backend Pi
#Backedn Pi receives the csv file.
import socket
import sys, logging

#Buffer Size , change this if want to receive the data in a different size.
DATA_BUFFER_SIZE = 1024
def raspberryClientProgram():
    """
        Initiate the UDP Socket bind to the local host and sepcified port,
        waits for the UDP Server message from GUI PI.
       	Key arguments: Nothing.
        #Return Value: Nothing.
    """
    # Client binds to the local host.
    UDP_HOST = socket.gethostname()
    UDP_PORT = 5005
    try:
        #Initiate the socket for the UDP Protocol.
        udpClientSocket = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        # Bind the udp socket to the HOST AND PORT.
        udpClientSocket.bind((UDP_HOST, UDP_PORT))
        logging.info('Client is running to start receiving the order files.')
    except udpClientSocket.error:
        logging.error('Error in creating the udpClientSocket')
        ## INVOKE A SMS MESSAGE TO THE OWNER? or To the Cloud?
        sys.exit(1)

    while True:
        # Receiving data from the UDP Server.
        data, addr = udpClientSocket.recvfrom(DATA_BUFFER_SIZE) # buffer size is 1024 bytes
        logging.info('received message:', data) #TODO LOGGING NOT WORKING, HAVE TO FIX
        print ('received message: ', data)
        ##TODO Write code to handle this data

if __name__ == '__main__':
    raspberryClientProgram()