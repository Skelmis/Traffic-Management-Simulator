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
    def test_controllerAttr(self):
        """
        Test the attributes are set correctly
        """
        controller = TrafficLightController("WEST")
        self.assertEqual(controller.getName(), "WEST")
        self.assertTrue(controller.getTL() != None)

    # Add further tests for your controller class here
    def test_wait(self):
        """
        Tests our wait increment functions
        """
        controller = TrafficLightController("WEST")
        self.assertEqual(controller.GetRightWait(), 0)
        controller.IncrementRightWait()
        controller.IncrementRightWait()
        self.assertEqual(controller.GetRightWait(), 2)
        controller.ResetRightWait()
        self.assertEqual(controller.GetRightWait(), 0)

    def test_waitReset(self):
        """
        Tests our wait reset functions
        """
        controller = TrafficLightController("WEST")
        self.assertEqual(controller.GetRightWait(), 0, msg="Right wait")
        controller.IncrementRightWait()
        controller.ResetRightWait()
        self.assertNotEqual(controller.GetRightWait(), 1, msg="Right wait")
        controller.ResetRightWait()
        controller.ResetRightWait()
        self.assertEqual(controller.GetRightWait(), 0, msg="Right wait")

        self.assertEqual(controller.GetOtherWait(), 0, msg="Other wait")
        controller.IncrementOtherWait()
        controller.ResetOtherWait()
        self.assertNotEqual(controller.GetOtherWait(), 1, msg="Other wait")
        controller.ResetOtherWait()
        controller.ResetOtherWait()
        self.assertEqual(controller.GetOtherWait(), 0, msg="Other wait")

    def test_dualWaitReset(self):
        """
        Test wait functions which do both at once
        """
        controller = TrafficLightController("WEST")
        controller.IncrementBothWaits()
        self.assertEqual(controller.GetRightWait(), 1, msg="Right wait")
        self.assertEqual(controller.GetOtherWait(), 1, msg="Other wait")

    def test_otherInitWait(self):
        """
        Makes sure waits are set right on init
        """
        controller = TrafficLightController("WEST")
        self.assertEqual(controller.GetRightWait(), 0, msg="Right wait")
        self.assertEqual(controller.GetOtherWait(), 0, msg="Other wait")

    ### Simulator class tests ###

    def test_generateCars(self):
        """
        Test car generation
        """
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

    def test_displayCars(self):
        """
        Test the display functions
        """
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        simulator.displayCars()
        sys.stdout = sys.__stdout__
        self.assertEqual(
            capturedOutput.getvalue(),
            "NORTH: "
            + str(simulator.northLane)
            + "\nEAST: "
            + str(simulator.eastLane)
            + "\nSOUTH: "
            + str(simulator.southLane)
            + "\nWEST: "
            + str(simulator.westLane)
            + "\n",
        )

    def test_timer(self):
        """
        Test the timer is correct
        """
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
        """
        Test the controller output is correct
        """
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

    def test_removeCars(self):
        """
        Test for removing cars
        """
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.removeCars(lane, "LEFT")
        self.assertEqual(lane, [car1, car2, car3])

    def test_sensorAllGo(self):
        """
        Tests for the sensor
        """
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
        """
        Test all sensors are orange
        """
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
        """
        Test right lights
        """
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
        """
        Test right light is orange
        """
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
        """
        Test straight lights
        """
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
        """
        Test straight orange lights
        """
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
        """
        Test car counting function
        """
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        answer = simulator.countCars(lane, "LEFT")
        self.assertEqual(answer, 2)

    ### Car class tests ###

    def test_carAttr(self):
        """
        Test the attributes are set correctly
        """
        car = Car("Car1", "WEST", "LEFT")
        self.assertEqual(car.getName(), "Car1")
        self.assertEqual(car.getEnter(), "WEST")
        self.assertEqual(car.getDirection(), "LEFT")

    def test_carDisplayDirLeft(self):
        """
        Test display direction is left
        """
        car = Car("Car1", "WEST", "LEFT")
        self.assertEqual(car.displayDirection(), "<")

    def test_carDisplayDirRight(self):
        """
        Test display direction is right
        """
        car = Car("Car1", "WEST", "RIGHT")
        self.assertEqual(car.displayDirection(), ">")

    def test_carDisplayDirStraight(self):
        """
        Test display direction is straight
        """
        car = Car("Car1", "WEST", "STRAIGHT")
        self.assertEqual(car.displayDirection(), "^")

    def test_carStr(self):
        """
        Test str function
        """
        car = Car("Car1", "WEST", "STRAIGHT")
        self.assertEqual(str(car), "Car1: STRAIGHT")

    ### Traffic Light Tests ###

    def test_TLAttr(self):
        """
        Test the attributes are set correctly
        """
        trafficLight = TrafficLight()
        self.assertEqual(
            trafficLight.whatsOn(), [True, True, False, False, False, False]
        )

    def test_redOn(self):
        """
        Test red on
        """
        trafficLight = TrafficLight()
        trafficLight.redOn()
        self.assertTrue(trafficLight.whatsOn()[0])

    def test_redOff(self):
        """
        Test red off
        """
        trafficLight = TrafficLight()
        trafficLight.redOff()
        self.assertFalse(trafficLight.whatsOn()[0])

    def test_tredOn(self):
        """
        test right red on
        """
        trafficLight = TrafficLight()
        trafficLight.tredOn()
        self.assertTrue(trafficLight.whatsOn()[1])

    def test_tredOff(self):
        """
        test right red off
        """
        trafficLight = TrafficLight()
        trafficLight.tredOff()
        self.assertFalse(trafficLight.whatsOn()[1])

    def test_orangeOn(self):
        """
        test orange on
        """
        trafficLight = TrafficLight()
        trafficLight.orangeOn()
        self.assertTrue(trafficLight.whatsOn()[2])

    def test_orangeOff(self):
        """
        test orange off
        """
        trafficLight = TrafficLight()
        trafficLight.orangeOff()
        self.assertFalse(trafficLight.whatsOn()[2])

    def test_torangeOn(self):
        """
        test right orange on
        """
        trafficLight = TrafficLight()
        trafficLight.torangeOn()
        self.assertTrue(trafficLight.whatsOn()[3])

    def test_torangeOff(self):
        """
        test right orange off
        """
        trafficLight = TrafficLight()
        trafficLight.torangeOff()
        self.assertFalse(trafficLight.whatsOn()[3])

    def test_greenOn(self):
        """
        test green on
        """
        trafficLight = TrafficLight()
        trafficLight.greenOn()
        self.assertTrue(trafficLight.whatsOn()[4])

    def test_greenOff(self):
        """
        test green off
        """
        trafficLight = TrafficLight()
        trafficLight.greenOff()
        self.assertFalse(trafficLight.whatsOn()[4])

    def test_tgreenOn(self):
        """
        test right green on
        """
        trafficLight = TrafficLight()
        trafficLight.tgreenOn()
        self.assertTrue(trafficLight.whatsOn()[5])

    def test_tgreenOff(self):
        """
        test right green off
        """
        trafficLight = TrafficLight()
        trafficLight.tgreenOff()
        self.assertFalse(trafficLight.whatsOn()[5])

    def test_displayLightOnS(self):
        """
        Test light display function straight light on
        """
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.displayLight(True, "S"), "O")

    def test_displayLightOnT(self):
        """
        Test light display function t lights on
        """
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.displayLight(True, "T"), ">")

    def test_displayLightOff(self):
        """
        Test light display function t lights off
        """
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.displayLight(False, "T"), " ")

    def test_redStr(self):
        """
        Test light display function red str
        """
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.redStr(), "|O|>|")

    def test_orangeStr(self):
        """
        Test light display function orange str
        """
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.orangeStr(), "| | |")

    def test_greenStr(self):
        """
        Test light display function green str
        """
        trafficLight = TrafficLight()
        self.assertEqual(trafficLight.greenStr(), "| | |")


if __name__ == "__main__":
    unittest.main()
