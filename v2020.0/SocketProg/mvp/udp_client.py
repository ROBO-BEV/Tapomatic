#!/usr/bin/env python

#In Tapomatic v2020.0 the Client is the Backend Pi
#Backedn Pi receives the csv file.
import socket
import socket

UDP_HOST = socket.gethostname()
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
socket.SOCK_DGRAM) # UDP
sock.bind((UDP_HOST, UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print('received message:', data)
