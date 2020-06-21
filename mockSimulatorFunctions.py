from controllers import Controller as TrafficLightController
import os
from termcolor import colored
import threading
import time
from cars import Car
import random
import sys

# Get the starting time to determine time elapsed
start = time.perf_counter()
# Store the number of cars generated
all_cars = 0

# Initialise each controller, one for each direction
northController = TrafficLightController("NORTH")
eastController = TrafficLightController("EAST")
southController = TrafficLightController("SOUTH")
westController = TrafficLightController("WEST")

# Create a lane as a list to store cars for each direction
northLane = []
eastLane = []
southLane = []
westLane = []

# For if the lights break and flash orange
lightsAreBroken = False


def generateCars(number):
    global all_cars
    all_cars += number
    roads = ["NORTH", "SOUTH", "EAST", "WEST"]
    directions = ["LEFT", "RIGHT", "STRAIGHT"]
    for i in range(1, number + 1):
        name = "Car" + str(i)
        enter = random.choice(roads)
        direction = random.choice(directions)
        car = Car(name, enter, direction)
        if enter == "NORTH":
            northLane.append(car)
        elif enter == "EAST":
            eastLane.append(car)
        elif enter == "WEST":
            westLane.append(car)
        elif enter == "SOUTH":
            southLane.append(car)
        else:
            print("ERROR:", "direction", direction, "does not exist.")


def countCars(lane, direction):
    count = 0
    for car in lane:
        if car.getDirection() == direction:
            count += 1
    return count


def CountAllCars(lane):
    """
    Counts all the cars in the lane onto two sides so we can get numbers

    Returns:
     - right, other (int, int) : The count of cars going right or other way
    """
    right = 0
    other = 0
    for car in lane:
        if car.getDirection() == "RIGHT":
            right += 1
        else:
            other += 1

    return right, other


def lightSignals():
    """
    A modified light signals function to suit our testing plan
    """
    try:
        # We need to know how many cars need what light per side
        # The other is LEFT & STRAIGHT going cars
        northRight, northOther = CountAllCars(northLane)
        eastRight, eastOther = CountAllCars(eastLane)
        southRight, southOther = CountAllCars(southLane)
        westRight, westOther = CountAllCars(westLane)

        data = {
            northRight: "nr",
            northOther: "no",
            eastRight: "er",
            eastOther: "eo",
            southRight: "sr",
            southOther: "so",
            westRight: "wr",
            westOther: "wo",
        }
        longestLight = max(data)

        """
        The first 8 if statements purely work based off of if the
        maximum wait time is exceeded. Each loop here is counted as 1 time
        so if you have to wait 8 times then you get priority next loop
        given we have 8 sets of lights I feel this is only fair
        """
        if northController.GetOtherWait() > 7 and northOther != 0:
            # works as intended
            # Means the left & straight cars need to go
            if northRight < southOther:
                # south other should go
                return ("no", "so")
            else:
                # All north should go
                return ("no", "nr")
        elif eastController.GetOtherWait() > 7 and eastOther != 0:
            # means the east left & straight cars need to go
            if eastRight < westOther:
                # west other should go
                return ("eo", "wo")
            else:
                # All east should go
                return ("eo", "er", 9)
        elif southController.GetOtherWait() > 7 and southOther != 0:
            # Means the south left & straight cars need to go
            if southRight < northOther:
                # north other should go
                return ("so", "no")
            else:
                # All south should go
                return ("so", "sr")
        elif westController.GetOtherWait() > 7 and westOther != 0:
            # means the west left & straight cars need to ggit commito
            if westRight < eastOther:
                # east other should go
                return ("wo", "eo")
            else:
                # All west should go
                return ("wo", "wr")
        elif northController.GetRightWait() > 7 and northRight != 0:
            # Means the north right Need to go
            if northOther < southRight:
                # south right should go
                return ("nr", "sr")
            else:
                # All north should go
                return ("nr", "no")
        elif eastController.GetRightWait() > 7 and eastRight != 0:
            if eastOther < westRight:
                # west right should go
                return ("er", "wr")
            else:
                # All east should go
                return ("er", "eo")
        elif southController.GetRightWait() > 7 and southRight != 0:
            if southOther < northRight:
                # north right should go
                return ("sr", "nr")
            else:
                # All south should go
                return ("sr", "so")
        elif westController.GetRightWait() > 7 and westRight != 0:
            if westOther < eastRight:
                # east right should go
                return ("wr", "er")
            else:
                # All east should go
                return ("wr", "wo")
        # The next 8 are our actual logic steps which pick the lane to run with
        elif data[longestLight] == "no":
            # North other is longest lane
            if northRight < southOther:
                # south other should go
                return ("no", "so")
            else:
                # All north should go
                return ("no", "nr")
        elif data[longestLight] == "eo":
            # East other is longest lane
            if eastRight < westOther:
                # west other should go
                return ("eo", "wo")
            else:
                # All east should go
                return ("eo", "er")
        elif data[longestLight] == "so":
            # South other is longest lane
            if southRight < northOther:
                # north other should go
                return ("so", "no")
            else:
                # All south should go
                return ("so", "sr")
        elif data[longestLight] == "wo":
            # West other is longest lane
            if westRight < eastOther:
                # east other should go
                return ("wo", "eo")
            else:
                # All west should go
                return ("wo", "wr")
        elif data[longestLight] == "nr":
            # North right is longest lane
            if northOther < southRight:
                # south right should go
                return ("nr", "sr")
            else:
                # All north should go
                return ("nr", "no")
        elif data[longestLight] == "er":
            # East right is longest lane
            if eastOther < westRight:
                # west right should go
                return ("er", "wr")
            else:
                # All east should go
                return ("er", "eo")
        elif data[longestLight] == "sr":
            # South right is longest lane
            if southOther < northRight:
                # north right should go
                return ("sr", "nr")
            else:
                # All south should go
                return ("sr", "so")
        elif data[longestLight] == "wr":
            # West right is longest lane
            if westOther < eastRight:
                # west other should go
                return ("wr", "er")
            else:
                # All west should go
                return ("wr", "wo")
        else:
            # If our logic cannot figure out what light
            # we need to do, just cycle through all of them
            return "All Cycle"

    except Exception as e:
        """
        This should never trip, but if it 'does' break we need to be
        able to handle that in a manner which is safe to drivers, so we
        will cycle every light to orange for 1 time 'interval'.

        Refer to the comment in the car removal area for how
        lightsAreBroken works cool thankies :)
        """
        return "Broken Cycle"
    # finally:
    # In accordance with the road rules we sleep here
    # so there is an 'all red' time between light sets
    # time.sleep(1)
    # No need to sleep as this is used for logic tests
