#!/usr/bin/env python3
"""
__author__ =  "Murali Krishna Dulla"
__email__ =   "jeevanmurali@gmail.com"
__company__ = "Robotic Beverage Technologies Inc"
__status__ =  "Development"
__date__ =    "Late Updated: 2020-08-11"
__doc__ =     "Class Contains Motor Operations"
"""
from builtins import super
from time import sleep
from Actuator import Actuator

class Motor(Actuator):
    def __init__(self, pins, partNumber, direction):
        # https://gist.github.com/johnwargo/ea5edc8516b24e0658784ae116628277
        # https://gpiozero.readthedocs.io/en/stable/api_output.html
        # https://stackoverflow.com/questions/14301967/bare-asterisk-in-function-arguments/14302007#14302007
        super(Motor).__init__()
        # The last two wires in array are the INPUT control pins
        #tempMotorObject = Motor(wires[len(wires)-2], wires[len(wires)-1])
        #self.actuatorObject = tempMotorObject

    def Run(self, duration, newPosition, speed, direction):
        # TODO Write motor control code

        Motor.enable()  # TODO CHANGE TO self.acutatorObject
        currentPosition = self.actuatorObject.value

        while (currentPosition != newPosition):
            if (self.actuatorObject.forwardDirection == Actuator.CW):
                Motor.forward(speed)
            else:
                Motor.reverse(speed)

            currentPosition = self.actuatorObject.value

        sleep(duration)  # TODO signal.pause(duration)
        Motor.disable()

    def setAngularPosition(self, newAngle):
        """
            Set the rotational position of a AngularServo() or Motor() object

            Key arguments:
            newAngle - Rotational angle to set actuator to, more exact for Servo() objects then Motor() object

            Return value:
            NOTHING
        """

        print("Settinng angular position for the motor")


    def getPosition(self):
        """
        Read the linear or rotational positon on an actuator

        Return value:
        The position of actuator, with value between -1.0 and 1.0 inclusively
        """
        print("Get position for the motor")
