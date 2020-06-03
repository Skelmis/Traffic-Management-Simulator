#!/usr/local/bin/python3

from controllers import Controller as TrafficLightController
import os
from termcolor import colored
import threading
import time
from cars import Car
import random
import sys
from pprint import pprint

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

"""
    A function which generates a random set of cars depending on the number provided.
"""


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


""" A function which generates the display of the Traffic Lights as a string. """


def controllerDisplay():
    formatString = "{:<25}{:<25}{:<25}{:<25}"
    header = formatString.format(
        northController.getName(),
        eastController.getName(),
        southController.getName(),
        westController.getName(),
    )
    line1 = formatString.format(" - - ", " - - ", " - - ", " - - ")
    line2 = colored(
        formatString.format(
            northController.getTL().redStr(),
            eastController.getTL().redStr(),
            southController.getTL().redStr(),
            westController.getTL().redStr(),
        ),
        "red",
    )
    line3 = colored(
        formatString.format(
            northController.getTL().orangeStr(),
            eastController.getTL().orangeStr(),
            southController.getTL().orangeStr(),
            westController.getTL().orangeStr(),
        ),
        "yellow",
    )
    line4 = colored(
        formatString.format(
            northController.getTL().greenStr(),
            eastController.getTL().greenStr(),
            southController.getTL().greenStr(),
            westController.getTL().greenStr(),
        ),
        "green",
    )
    return (
        header
        + "\n"
        + line1
        + "\n"
        + line2
        + "\n"
        + line3
        + "\n"
        + line4
        + "\n"
        + line1
        + "\n"
    )


"""
    A function which displays the traffic lights, cars, and timer to the console window.
"""


def displayControllers():
    while True:
        # os.system('clear') # Doesnt work on windows lol
        os.system("cls")
        print(controllerDisplay())
        displayCars()
        timer()
        PrintMax()
        time.sleep(1)
        # break # Only want one iterationn lol


""" A function to display the car lanes to the console window."""


def displayCars():
    print("NORTH:", end="")
    print(northLane)  # pprint prints lists n shit nicely
    print("EAST:", end="")
    print(eastLane)
    print("SOUTH:", end="")
    print(southLane)
    print("WEST:", end="")
    print(westLane)


""" A function to remove cars from a lane based on their intended direction. """


def removeCars(lane, direction):
    for i in range(0, len(lane)):
        car = lane[i]
        if car.getDirection() == direction:
            lane.remove(car)
            break


""" A function which tells the car to move depending on the sensor. """


def sensor(controller, lane):
    # If there are still more cars in the lane
    if len(lane) > 0:
        # Find out which lights are on
        matrix = controller.getTL().whatsOn()
        # If the green light and turning green light are on, or the orange light and turning orange light are on, remove the next car in the lane
        if (matrix[2] == True and matrix[3] == True) or (
            matrix[4] == True and matrix[5] == True
        ):
            del lane[0]
        # If the green turning light or the orange turning light are on, remove the next car in the lane which is turning right
        elif matrix[3] == True or matrix[5] == True:
            removeCars(lane, "RIGHT")
        # If the green light or the orange light are on, remove the cars which are going straight or turning left from the lane
        elif matrix[2] == True or matrix[4] == True:
            removeCars(lane, "STRAIGHT")
            removeCars(lane, "LEFT")


""" A function which tells cars to move depending on the controller of the traffic light."""


def carsGo(controller, lane):
    while True:
        sensor(controller, lane)
        # Pause to allow "car to leave intersection"
        time.sleep(1)


""" A function which generates a new set of random cars when all the lanes become empty. """


def resetCars():
    while True:
        if (
            len(northLane) == 0
            and len(southLane) == 0
            and len(eastLane) == 0
            and len(westLane) == 0
        ):
            # generateCars(random.randint(10, 100))

            # Use 50 as our set testcase for comparsions
            # to our baseline
            generateCars(50)


""" A function which counts the number of cars going a certain direction in the given lane. """


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


""" A function which displays the time elapsed and number of generated cars to the user. """


def timer():
    """
    Displays the current runtime and also how many cars have
    been generated for the user so far.
    """
    current_time = time.perf_counter()
    time_elapsed = current_time - start
    minutes, seconds = divmod(time_elapsed, 60)
    hours, minutes = divmod(minutes, 60)
    seconds = int(seconds)
    minutes = int(minutes)
    hours = int(hours)
    print("----------")
    print(
        "TIME ELAPSED: {:0>2d}:{:0>2d}:{:0>2d}".format(hours, minutes, seconds),
        "| Total cars:",
        all_cars,
    )
    # Removed the kickout function to test higher limits
    # agaisnt our baseline test simulator


""" A function which determines which lightSignals to set off and when. """


def ResetAllWaits():
    """
    Resets the wait times for all controllers
    """
    northController.ResetRightWait()
    northController.ResetOtherWait()

    eastController.ResetRightWait()
    eastController.ResetRightWait()

    southController.ResetRightWait()
    southController.ResetOtherWait()

    westController.ResetRightWait()
    westController.ResetOtherWait()


def IncrementAllWaits():
    """
    Increments all waits by 1
    """
    northController.IncrementRightWait()
    northController.IncrementOtherWait()

    eastController.IncrementRightWait()
    eastController.IncrementOtherWait()

    southController.IncrementRightWait()
    southController.IncrementOtherWait()

    westController.IncrementRightWait()
    westController.IncrementOtherWait()


def RunDualOtherControllers(controllerOne, controllerTwo):
    """
    Used to shorten up the code needed within lightSignals()
    by simply running the code here with the required things
    Runs the STRAIGHT & LEFT lights

    Params:
     - controllerOne, controllerTwo (controller) : The controllers needed
    """
    threadOne = threading.Thread(target=controllerOne.OtherCycle)
    threadTwo = threading.Thread(target=controllerTwo.OtherCycle)
    threadOne.start()
    threadTwo.start()
    threadOne.join()
    threadTwo.join()
    controllerOne.ResetOtherWait()
    controllerTwo.ResetOtherWait()


def RunDualRightControllers(controllerOne, controllerTwo):
    """
    Used to shorten up the code needed within lightSignals()
    by simply running the code here with the required things
    Runs the RIGHT lights

    Params:
     - controllerOne, controllerTwo (controller) : The controllers needed
    """
    threadOne = threading.Thread(target=controllerOne.RightCycle)
    threadTwo = threading.Thread(target=controllerTwo.RightCycle)
    threadOne.start()
    threadTwo.start()
    threadOne.join()
    threadTwo.join()
    controllerOne.ResetRightWait()
    controllerTwo.ResetRightWait()


def PrintMax():
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
    print(data[longestLight])


def lightSignals():
    # thread = threading.Thread(target=PrintMax)
    # thread.start()
    while True:
        # We need to know how many cars need what light per side
        # The other is LEFT & STRAIGHT going cars
        northRight, northOther = CountAllCars(northLane)
        eastRight, eastOther = CountAllCars(eastLane)
        southRight, southOther = CountAllCars(southLane)
        westRight, westOther = CountAllCars(westLane)

        # TODO
        # Implement a way to get the largest out of the 8 above then run the rule
        # set to figure out what one to use
        # WE need to know the lane so we use a dict
        # Dunno how it handles double ups
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
                print("North Other Wait exceeded, running north & south")
                RunDualOtherControllers(northController, southController)
            else:
                # All north should go
                print("North other wait exceeded, running all north")
                northController.AllCycle()
                northController.ResetBothWaits()
        elif eastController.GetOtherWait() > 7 and eastOther != 0:
            # means the east left & straight cars need to go
            if eastRight < westOther:
                # west other should go
                print("east Other Wait exceeded, running east & west")
                RunDualOtherControllers(eastController, westController)
            else:
                # All east should go
                print("east other wait exceeded, running all east")
                eastController.AllCycle()
                eastController.ResetBothWaits()
        elif southController.GetOtherWait() > 7 and southOther != 0:
            # Means the south left & straight cars need to go
            if southRight < northOther:
                # north other should go
                print("south Other Wait exceeded, running south & north")
                RunDualOtherControllers(southController, northController)
            else:
                # All south should go
                print("south other wait exceeded, running all south")
                southController.AllCycle()
                southController.ResetBothWaits()
        elif westController.GetOtherWait() > 7 and westOther != 0:
            # means the west left & straight cars need to ggit commito
            if westRight < eastOther:
                # east other should go
                print("west Other Wait exceeded, running west & east")
                RunDualOtherControllers(westController, eastController)
            else:
                # All west should go
                print("west other wait exceeded, running all west")
                westController.AllCycle()
                westController.ResetBothWaits()
        elif northController.GetRightWait() > 7 and northRight != 0:
            # Means the north right Need to go
            if northOther < southRight:
                # south right should go
                print("North right Wait exceeded, running north & south")
                RunDualRightControllers(northController, southController)
            else:
                # All north should go
                print("North right wait exceeded, running all north")
                northController.AllCycle()
                northController.ResetBothWaits()
        elif eastController.GetRightWait() > 7 and eastRight != 0:
            if eastOther < westRight:
                # west right should go
                print("east right Wait exceeded, running east & west")
                RunDualRightControllers(eastController, westController)
            else:
                # All east should go
                print("east right wait exceeded, running all east")
                eastController.AllCycle()
                eastController.ResetBothWaits()
        elif southController.GetRightWait() > 7 and southRight != 0:
            if southOther < northRight:
                # north right should go
                print("south right Wait exceeded, running south & north")
                RunDualRightControllers(southController, northController)
            else:
                # All south should go
                print("south right wait exceeded, running all south")
                southController.AllCycle()
                southController.ResetBothWaits()
        elif westController.GetRightWait() > 7 and westRight != 0:
            if westOther < eastRight:
                # west other should go
                print("west right Wait exceeded, running west & east")
                RunDualRightControllers(westController, eastController)
            else:
                # All east should go
                print("west right wait exceeded, running all west")
                westController.AllCycle()
                westController.ResetBothWaits()
        # The next 8 are our actual logic steps which pick the lane to run with
        elif data[longestLight] == "no":
            # North other is longest lane
            if northRight < southOther:
                print("Dual north & south other")
                # south other should go
                RunDualOtherControllers(northController, southController)
            else:
                # All north should go
                print("All north")
                northController.AllCycle()
                northController.ResetBothWaits()
        elif data[longestLight] == "eo":
            # East other is longest lane
            if eastRight < westOther:
                # west other should go
                print("Both east & west other")
                RunDualOtherControllers(eastController, westController)
            else:
                # All east should go
                print("All east")
                eastController.AllCycle()
                eastController.ResetBothWaits()
        elif data[longestLight] == "so":
            # South other is longest lane
            if southRight < northOther:
                # north other should go
                print("Dual south & north other")
                RunDualOtherControllers(southController, northController)
            else:
                # All south should go
                print("All south")
                southController.AllCycle()
                southController.ResetBothWaits()
        elif data[longestLight] == "wo":
            # West other is longest lane
            if westRight < eastOther:
                # east other should go
                print("Both west & east other")
                RunDualOtherControllers(westController, eastController)
            else:
                # All west should go
                print("All west")
                westController.AllCycle()
                westController.ResetBothWaits()
        elif data[longestLight] == "nr":
            # North right is longest lane
            if northOther < southRight:
                # south right should go
                print("Both north & south right")
                RunDualRightControllers(northController, southController)
            else:
                # All north should go
                print("All north")
                northController.AllCycle()
                northController.ResetBothWaits()
        elif data[longestLight] == "er":
            # East right is longest lane
            if eastOther < westRight:
                # west other should go
                print("Both east & west right")
                RunDualRightControllers(eastController, westController)
            else:
                # All east should go
                print("All east")
                eastController.AllCycle()
                eastController.ResetBothWaits()
        elif data[longestLight] == "sr":
            # South right is longest lane
            if southOther < northRight:
                # north right should go
                print("Both south & north right")
                RunDualRightControllers(southController, northController)
            else:
                # All south should go
                print("All south")
                southController.AllCycle()
                southController.ResetBothWaits()
        elif data[longestLight] == "wr":
            # West right is longest lane
            if westOther < eastRight:
                # west other should go
                print("Both west & east right")
                RunDualRightControllers(westController, eastController)
            else:
                # All west should go
                print("All west")
                westController.AllCycle()
                westController.ResetBothWaits()
        else:
            # If our logic cannot figure out what light
            # we need to do, just cycle through all of them
            print("All cycle")
            northController.AllCycle()
            eastController.AllCycle()
            southController.AllCycle()
            westController.AllCycle()
            ResetAllWaits()

        IncrementAllWaits()
        # time.sleep(5)


""" A function which allows us to start the simulation. """


def main():
    # The following lines of code are used to set up the simulation
    # Start the timer
    timerThread = threading.Thread(target=timer)
    timerThread.start()
    # Initially generate 10 cars
    generateCars(10)
    # Start the reset function to listen for when the lanes are empty
    resetThread = threading.Thread(target=resetCars)
    resetThread.start()
    # Start the display of the simulation
    x = threading.Thread(target=displayControllers)
    x.start()
    # Start the traffic light controllers using your design
    lights = threading.Thread(target=lightSignals)
    lights.start()
    # Start the cars in the north lane moving, listening for north traffic light changes
    northCars = threading.Thread(target=carsGo, args=(northController, northLane,))
    northCars.start()
    # Start the cars in the south lane moving, listening for south traffic light changes
    southCars = threading.Thread(target=carsGo, args=(southController, southLane,))
    southCars.start()
    # Start the cars in the east lane moving, listening for east traffic light changes
    eastCars = threading.Thread(target=carsGo, args=(eastController, eastLane,))
    eastCars.start()
    # Start the cars in the west lane moving, listening for west traffic light changes
    westCars = threading.Thread(target=carsGo, args=(westController, westLane,))
    westCars.start()


if __name__ == "__main__":
    main()
