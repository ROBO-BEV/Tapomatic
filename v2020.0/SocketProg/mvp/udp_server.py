#!/usr/bin/env python
#In Tapomatic v2020.0 the server in the GUI Pi
# GUI Pi send the txt file.
import socket

# localIP = socket.gethostname()
# localPort = 5000
# udpServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
# udpServerSocket.bind((localIP, localPort))
# print("UDP server up and listening")

# Find a way to get the client PI address here.
UDP_CLIENT_IP = socket.gethostname()
UDP_CLIENT_PORT = 5005
udpClientSocket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

filename= 'coco_orders.csv'
#LOOP CONDITIONS????
while (True):
    f = open(filename, 'rb')
    l = f.read(1024)
    while (l):
        udpClientSocket.sendto(l,(UDP_CLIENT_IP, UDP_CLIENT_PORT))
        print('Sent ',repr(l))
        l = f.read(1024)
    f.close()
