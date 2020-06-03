#!/usr/local/bin/python3

from lights import Traffic as trafficLight
import time

""" A class which stores the logic of the controller that you are going to implement """


class Controller:

    # The name of the controller, associated with the road and traffic direction, can be either NORTH, EAST, SOUTH or WEST
    # The time delay between light switching
    INTERVAL = 3

    def __init__(self, name):
        self.name = name or None
        self.trafficLight = trafficLight() or None
        self.wait_right = 0  # Used to check traffic hasnt been sitting too long
        self.wait_other = 0

    def GetOtherWait(self):
        """
        Returns self.wait
        """
        return self.wait_other

    def ResetOtherWait(self):
        """
        Sets the current controllers wait to 0
        """
        self.wait_other = 0

    def IncrementOtherWait(self):
        """
        Increase wait by 1
        """
        self.wait_other += 1

    def GetRightWait(self):
        """
        Returns self.wait
        """
        return self.wait_right

    def ResetRightWait(self):
        """
        Sets the current controllers wait to 0
        """
        self.wait_right = 0

    def IncrementRightWait(self):
        """
        Increase wait by 1
        """
        self.wait_right += 1

    def ResetBothWaits(self):
        """
        Resets both the waits
        """
        self.ResetRightWait()
        self.ResetOtherWait()

    def getName(self):
        return self.name

    def getTL(self):
        return self.trafficLight

    # An example of defining a traffic light phase as a function
    def phaseStop(self):
        self.trafficLight.switchOff()
        self.trafficLight.redOn()
        self.trafficLight.tredOn()

    # Define further phases for your traffic light here

    def AllCycle(self):
        """
        Cycles through all of the lights turning them on and off
        """
        # All green lights on
        self.trafficLight.switchOff()
        self.trafficLight.greenOn()
        self.trafficLight.tgreenOn()
        # Pause the light before the change for the length of the interval
        time.sleep(self.INTERVAL)
        # All orange lights on
        self.trafficLight.switchOff()
        self.trafficLight.orangeOn()
        self.trafficLight.torangeOn()
        time.sleep(self.INTERVAL)
        # All red lights on
        self.phaseStop()

    def RightCycle(self):
        """
        Cycles through the right traffic lights
        Leaves S/L off
        """
        # All green lights on
        self.trafficLight.switchOff()
        self.trafficLight.redOn()
        self.trafficLight.tgreenOn()
        # Pause the light before the change for the length of the interval
        time.sleep(self.INTERVAL)
        # All orange lights on
        self.trafficLight.switchOff()
        self.trafficLight.redOn()
        self.trafficLight.torangeOn()
        time.sleep(self.INTERVAL)
        # All red lights on
        self.phaseStop()

    def OtherCycle(self):
        """
        Cycles through the straight/left traffic lights
        Leaves right off
        """
        # All green lights on
        self.trafficLight.switchOff()
        self.trafficLight.greenOn()
        self.trafficLight.tredOn()
        # Pause the light before the change for the length of the interval
        time.sleep(self.INTERVAL)
        # All orange lights on
        self.trafficLight.switchOff()
        self.trafficLight.orangeOn()
        self.trafficLight.tredOn()
        time.sleep(self.INTERVAL)
        # All red lights on
        self.phaseStop()
