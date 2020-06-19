from termcolor import colored

""" A class which stores the information for a traffic light. """


class Traffic:

    # Each light is set to True or False depending on whether it is on or off
    def __init__(self):
        self.red = True
        self.orange = False
        self.green = False
        self.tred = True  # T red is turning right light?
        self.torange = False
        self.tgreen = False

    # Function which allow you to switch lights on and off
    def redOn(self):
        self.red = True

    def redOff(self):
        self.red = False

    def orangeOn(self):
        self.orange = True

    def orangeOff(self):
        self.orange = False

    def greenOn(self):
        self.green = True

    def greenOff(self):
        self.green = False

    def tredOn(self):
        self.tred = True

    def tredOff(self):
        self.tred = False

    def torangeOn(self):
        self.torange = True

    def torangeOff(self):
        self.torange = False

    def tgreenOn(self):
        self.tgreen = True

    def tgreenOff(self):
        self.tgreen = False

    # This function allows us to reset all the lights
    def switchOff(self):
        self.redOff()
        self.orangeOff()
        self.greenOff()
        self.tredOff()
        self.torangeOff()
        self.tgreenOff()

    # Return the value as a matrix to determine which lights are on or off
    def whatsOn(self):
        return [self.red, self.tred, self.orange, self.torange, self.green, self.tgreen]

    # The following functions are for displaying the light in the simulation
    def displayLight(self, light, type):
        if light and type == "S":
            return "O"
        elif light and type == "T":
            return ">"
        else:
            return " "

    def redStr(self):
        return (
            "|"
            + self.displayLight(self.red, "S")
            + "|"
            + self.displayLight(self.tred, "T")
            + "|"
        )

    def orangeStr(self):
        return (
            "|"
            + self.displayLight(self.orange, "S")
            + "|"
            + self.displayLight(self.torange, "T")
            + "|"
        )

    def greenStr(self):
        return (
            "|"
            + self.displayLight(self.green, "S")
            + "|"
            + self.displayLight(self.tgreen, "T")
            + "|"
        )
