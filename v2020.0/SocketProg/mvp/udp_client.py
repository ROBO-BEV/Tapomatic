#!/usr/bin/env python
__author__  = "Murali Dulla"
__email__   = "jeevanmurali@gmail.com"
__company__ = "COCOTAPS"
__status__  = "Development"
__date__    = "Late Updated: 2020-05-14"
__doc__     = "UDP Client to receive the kiosk orders from the UDP Server running on GUI PI4."

#In Tapomatic v2020.0 the Client is the Backend Pi
#Backedn Pi receives the csv file.
import socket
import sys, logging
def raspberryClientProgram():
    UDP_HOST = socket.gethostname()
    UDP_PORT = 5005
    try:
        udpClientSocket = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        udpClientSocket.bind((UDP_HOST, UDP_PORT))
        logging.info('Client is running to start receiving the order files.')
    except udpClientSocket.error:
        logging.error('Error in creating the udpClientSocket')
        ## INVOKE A SMS MESSAGE TO THE OWNER? or To the Cloud?
        sys.exit(1)

    while True:
        data, addr = udpClientSocket.recvfrom(1024) # buffer size is 1024 bytes
        logging.info('received message:', data)
        ##TODO Write code to handle this data

if __name__ == '__main__':
    raspberryClientProgram()