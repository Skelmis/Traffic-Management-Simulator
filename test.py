#!/usr/local/bin/python3

import unittest
from cars import Car
from controllers import Controller as TrafficLightController
from lights import Traffic as TrafficLight
import simulator
import threading
import io
import sys
from termcolor import colored


class TestSimulation(unittest.TestCase):

    """
    Test the functionality of each simulator class.
    """

    ### Controller class tests ###
    # Test the attributes are set correctly
    def test_controllerAttr(self):
        controller = TrafficLightController("WEST")
        self.assertEqual(controller.getName(), "WEST")
        self.assertTrue(controller.getTL() != None)

    # Add further tests for your controller class here

    ### Simulator class tests ###

    # Add further tests for your simulation functions that you have modified here

    # Test the car generator
    def test_generateCars(self):
        simulator.generateCars(10)
        self.assertTrue(
            len(simulator.northLane) > 0
            or len(simulator.southLane) > 0
            or len(simulator.eastLane) > 0
            or len(simulator.westLane) > 0
        )
        self.assertEqual(
            (
                len(simulator.northLane)
                + len(simulator.southLane)
                + len(simulator.eastLane)
                + len(simulator.westLane)
            ),
            10,
        )

    # Test the display functions
    def test_displayCars(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        simulator.displayCars()
        sys.stdout = sys.__stdout__
        self.assertEqual(
            capturedOutput.getvalue(),
            "NORTH:"
            + str(simulator.northLane)
            + "\nEAST:"
            + str(simulator.eastLane)
            + "\nSOUTH:"
            + str(simulator.southLane)
            + "\nWEST:"
            + str(simulator.westLane)
            + "\n",
        )

    def test_timer(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        simulator.start = 0
        simulator.timer()
        sys.stdout = sys.__stdout__
        self.assertEqual(
            capturedOutput.getvalue(),
            "----------\nTIME ELAPSED: 00:00:00 | Total cars: "
            + str(simulator.all_cars)
            + "\n",
        )

    def test_controllerDisplay(self):
        string = (
            "NORTH                    EAST                     SOUTH                    WEST                     \n - -                      - -                      - -                      - -                     \n"
            + colored(
                "|O|>|                    |O|>|                    |O|>|                    |O|>|                    ",
                "red",
            )
            + "\n"
            + colored(
                "| | |                    | | |                    | | |                    | | |                    ",
                "yellow",
            )
            + "\n"
            + colored(
                "| | |                    | | |                    | | |                    | | |                    ",
                "green",
            )
            + "\n - -                      - -                      - -                      - -                     \n"
        )
        self.assertEqual(simulator.controllerDisplay(), string)

    # Test for removing cars
    def test_removeCars(self):
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.removeCars(lane, "LEFT")
        self.assertEqual(lane, [car1, car2, car3])

    # Tests for the sensor
    def test_sensorAllGo(self):
        controller = TrafficLightController("MOCK")
        tl = controller.getTL()
        tl.switchOff()
        tl.greenOn()
        tl.tgreenOn()
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.sensor(controller, lane)
        self.assertEqual(lane, [car2, car3, car3])

    def test_sensorAllOrange(self):
        controller = TrafficLightController("MOCK")
        tl = controller.getTL()
        tl.switchOff()
        tl.orangeOn()
        tl.torangeOn()
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.sensor(controller, lane)
        self.assertEqual(lane, [car2, car3, car3])

    def test_sensorRightGo(self):
        controller = TrafficLightController("MOCK")
        tl = controller.getTL()
        tl.switchOff()
        tl.redOn()
        tl.tgreenOn()
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.sensor(controller, lane)
        self.assertEqual(lane, [car1, car3, car3])

    def test_sensorRightOrange(self):
        controller = TrafficLightController("MOCK")
        tl = controller.getTL()
        tl.switchOff()
        tl.redOn()
        tl.torangeOn()
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.sensor(controller, lane)
        self.assertEqual(lane, [car1, car3, car3])

    def test_sensorStraightGo(self):
        controller = TrafficLightController("MOCK")
        tl = controller.getTL()
        tl.switchOff()
        tl.tredOn()
        tl.greenOn()
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.sensor(controller, lane)
        self.assertEqual(lane, [car2, car3])

    def test_sensorStraightOrange(self):
        controller = TrafficLightController("MOCK")
        tl = controller.getTL()
        tl.switchOff()
        tl.tredOn()
        tl.orangeOn()
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.sensor(controller, lane)
        self.assertEqual(lane, [car2, car3])

    # A test for the count cars function
    def test_countCars(self):
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        answer = simulator.countCars(lane, "LEFT")
        self.assertEqual(answer, 2)

    ### Car class tests ###
    # Test the attributes are set correctly
    def test_carAttr(self):
        car = Car("Car1", "WEST", "LEFT")
        self.assertEqual(car.getName(), "Car1")
        self.assertEqual(car.getEnter(), "WEST")
        self.assertEqual(car.getDirection(), "LEFT")

    # Test display direction
    def test_carDisplayDirLeft(self):
        car = Car("Car1", "WEST", "LEFT")
        self.assertEqual(car.displayDirection(), "<")

    def test_carDisplayDirRight(self):
        car = Car("Car1", "WEST", "RIGHT")
        self.assertEqual(car.displayDirection(), ">")

    def test_carDisplayDirStraight(self):
        car = Car("Car1", "WEST", "STRAIGHT")
        self.assertEqual(car.displayDirection(), "^")

    # Test str function
    def test_carStr(self):
        car = Car("Car1", "WEST", "STRAIGHT")
        self.assertEqual(str(car), "Car1: STRAIGHT")

    ### Traffic Light Tests ###
    # Test the attributes are set correctly
    def test_TLAttr(self):
        trafficLight = TrafficLight()
        self.assertEqual(
            trafficLight.whatsOn(), [True, True, False, False, False, False]
        )

    # Test the on and off light functions
    def test_redOn(self):
        trafficLight = TrafficLight()
        trafficLight.redOn()
        self.assertTrue(trafficLight.whatsOn()[0])

    def test_redOff(self):
        trafficLight = TrafficLight()
        trafficLight.redOff()
        self.assertFalse(trafficLight.whatsOn()[0])

    def test_tredOn(self):
        trafficLight = TrafficLight()
        trafficLight.tredOn()
        self.assertTrue(trafficLight.whatsOn()[1])

    def test_tredOff(self):
        trafficLight = TrafficLight()
        trafficLight.tredOff()
        self.assertFalse(trafficLight.whatsOn()[1])

    def test_orangeOn(self):
        trafficLight = TrafficLight()
        trafficLight.orangeOn()
        self.assertTrue(trafficLight.whatsOn()[2])

    def test_orangeOff(self):
        trafficLight = TrafficLight()
        trafficLight.orangeOff()
        self.assertFalse(trafficLight.whatsOn()[2])

    def test_torangeOn(self):
        trafficLight = TrafficLight()
        trafficLight.torangeOn()
        self.assertTrue(trafficLight.whatsOn()[3])

    def test_torangeOff(self):
        trafficLight = TrafficLight()
        trafficLight.torangeOff()
        self.assertFalse(trafficLight.whatsOn()[3])

    def test_greenOn(self):
        trafficLight = TrafficLight()
        trafficLight.greenOn()
        self.assertTrue(trafficLight.whatsOn()[4])

    def test_greenOff(self):
        trafficLight = TrafficLight()
        trafficLight.greenOff()
        self.assertFalse(trafficLight.whatsOn()[4])

    def test_tgreenOn(self):
        trafficLight = TrafficLight()
        trafficLight.tgreenOn()
        self.assertTrue(trafficLight.whatsOn()[5])

    def test_tgreenOff(self):
        trafficLight = TrafficLight()
        trafficLight.tgreenOff()
        self.assertFalse(trafficLight.whatsOn()[5])

    # Test the light display functions
    def test_displayLightOnS(self):
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.displayLight(True, "S"), "O")

    def test_displayLightOnT(self):
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.displayLight(True, "T"), ">")

    def test_displayLightOff(self):
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.displayLight(False, "T"), " ")

    def test_redStr(self):
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.redStr(), "|O|>|")

    def test_orangeStr(self):
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.orangeStr(), "| | |")

    def test_greenStr(self):
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.greenStr(), "| | |")


if __name__ == "__main__":
    unittest.main()
