#!/usr/local/bin/python3

from lights import Traffic as trafficLight
import time

""" A class which stores the logic of the controller that you are going to implement """
class Controller:

    #The name of the controller, associated with the road and traffic direction, can be either NORTH, EAST, SOUTH or WEST
    #The time delay between light switching
    INTERVAL = 3

    def __init__(self, name):
        self.name = name or None
        self.trafficLight = trafficLight() or None

    def getName(self):
        return self.name

    def getTL(self):
        return self.trafficLight

    #An example of defining a traffic light phase as a function
    def phaseStop(self):
        self.trafficLight.switchOff()
        self.trafficLight.redOn()
        self.trafficLight.tredOn()

    #Define further phases for your traffic light here

    #An example of defining a traffic light cycle as a function
    def allCycle(self):
        #All green lights on
        #Pause the light before the change for the length of the interval
        time.sleep(self.INTERVAL)
        #All orange lights on
        time.sleep(self.INTERVAL)
        #All red lights on
        self.phaseStop()
