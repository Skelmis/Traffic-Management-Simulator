#A class which stores information about a specific car
class Car:

    name = None
    #Which road did the car enter from
    enter = None
    #Which direction would the car like to go in
    direction = None

    def __init__(self, name, enter, direction):
        self.name = name
        self.enter = enter
        self.direction = direction

    def getEnter(self):
        return self.enter

    def getDirection(self):
        return self.direction

    def getName(self):
        return self.name

    """
        A function which displays the direction of the car in the simulation.
    """
    def displayDirection(self):
        if self.direction=="LEFT":
            return "<"
        elif self.direction=="RIGHT":
            return ">"
        else:
            return "^"

    def __str__(self):
        return self.name + ": " + self.direction # It looks nicer on the eyes   #displayDirection()

    def __repr__(self):
        return self.name + ": " + self.direction # It looks nicer on the eyes   #displayDirection()
