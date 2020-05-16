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

UDP_HOST = socket.gethostname()
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.bind((UDP_HOST, UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print('received message:', data)
