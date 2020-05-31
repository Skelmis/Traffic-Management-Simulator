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
        time.sleep(1)
        # break # Only want one iterationn lol


""" A function to display the car lanes to the console window."""


def displayCars():
    print("NORTH:", end="")
    pprint(northLane)  # pprint prints lists n shit nicely
    print("EAST:", end="")
    pprint(eastLane)
    print("SOUTH:", end="")
    pprint(southLane)
    print("WEST:", end="")
    pprint(westLane)


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
            generateCars(random.randint(10, 100))


""" A function which counts the number of cars going a certain direction in the given lane. """


def countCars(lane, direction):
    count = 0
    for car in lane:
        if car.getDirection() == direction:
            count += 1
    return count


""" A function which displays the time elapsed and number of generated cars to the user. """


def timer():
    current_time = time.perf_counter()
    time_elapsed = current_time - start
    hours = int(time_elapsed // 360)
    time_elapsed %= 360
    minutes = int(time_elapsed // 60)
    time_elapsed %= 60
    seconds = int(time_elapsed)
    print("----------")
    print(
        "TIME ELAPSED: {:0>2d}:{:0>2d}:{:0>2d}".format(hours, minutes, seconds),
        "| Total cars:",
        all_cars,
    )
    if int(time_elapsed) == 60:
        sys.exit()


""" A function which determines which lightSignals to set off and when. """


def lightSignals():
    while True:
        northController.allCycle()
        southController.allCycle()
        eastController.allCycle()
        westController.allCycle()
        pass
        # Your signal design goes here


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
