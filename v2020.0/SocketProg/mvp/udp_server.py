#!/usr/bin/env python
#In Tapomatic v2020.0 the server in the GUI Pi
# GUI Pi send the txt file.
import socket

UDP_IP = "192.168.225.56"
UDP_PORT = 5005
MESSAGE = "Hello, World!"


# print ("UDP target IP:", UDP_IP)
# print  ("UDP target port:", UDP_PORT)
# print  ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))