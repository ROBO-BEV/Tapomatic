#!/usr/bin/env python3
"""
__author__ =  "Murali Krishna Dulla"
__email__ =   "jeevanmurali@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-08-11"
__doc__ =     "Class Contains Relay Operations"
"""
from Actuator import Actuator
from builtins import super
from time import sleep


class Relay(Actuator):
    def __init__(self):
        super(Relay, self, pins, partNumber, direction).__init__()

        # The last wire in array is the relay control pin
        tempRelayObject = OutputDevice(wires[len(wires) - 1])

        # https://gist.github.com/johnwargo/ea5edc8516b24e0658784ae116628277
        # https://gpiozero.readthedocs.io/en/stable/api_output.html
        # https://stackoverflow.com/questions/14301967/bare-asterisk-in-function-arguments/14302007#14302007
        self.actuatorObject = tempRelayObject

    def Run(self):
        # The last wire in array is the relay control pin
        tempRelayObject = OutputDevice(wires[len(wires) - 1])
        relay.on()
        sleep(duration)  # TODO signal.pause(duration)
        relay.off()

    def getPosition(self):
        """
        Read the linear or rotational positon on an actuator

        Return value:
        The position of actuator, with value between -1.0 and 1.0 inclusively
        """
        print("Get position for the Relay")