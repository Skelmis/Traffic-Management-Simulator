#!/usr/local/bin/python3

import unittest
from cars import Car
from controllers import Controller as TrafficLightController
from lights import Traffic as TrafficLight
import simulator
import mockSimulatorFunctions as testFunctions
import threading
import io
import sys
from termcolor import colored
import time


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
        controller = TrafficLightController("TEST")
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
        controller = TrafficLightController("TEST")
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
        controller = TrafficLightController("TEST")
        controller.IncrementBothWaits()
        self.assertEqual(controller.GetRightWait(), 1, msg="Right wait")
        self.assertEqual(controller.GetOtherWait(), 1, msg="Other wait")

        controller.ResetBothWaits()
        self.assertEqual(controller.GetRightWait(), 0, msg="Right wait")
        self.assertEqual(controller.GetOtherWait(), 0, msg="Other wait")

    def test_otherInitWait(self):
        """
        Makes sure waits are set right on init
        """
        controller = TrafficLightController("TEST")
        self.assertEqual(controller.GetRightWait(), 0, msg="Right wait")
        self.assertEqual(controller.GetOtherWait(), 0, msg="Other wait")

    def test_dualWaitIncrement(self):
        """
        Test the method handling incrementing both waits
        """
        controller = TrafficLightController("TEST")
        controller.IncrementBothWaits()
        self.assertEqual(controller.GetRightWait(), 1, msg="Right wait")
        self.assertEqual(controller.GetOtherWait(), 1, msg="Other wait")

    def test_phaseStop(self):
        """
        test the phase stop function
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.phaseStop()
        self.assertEqual(tl.whatsOn(), [True, True, False, False, False, False])

    def test_phaseOrange(self):
        """
        test the phase orange function
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.phaseOrange()
        self.assertEqual(tl.whatsOn(), [False, False, True, True, False, False])

    def test_phaseGreen(self):
        """
        test the phase green function
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.phaseGreen()
        self.assertEqual(tl.whatsOn(), [False, False, False, False, True, True])

    def test_partialRightCycle(self):
        """
        Test a part of our right cycle
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.trafficLight.switchOff()
        controller.trafficLight.redOn()
        controller.trafficLight.tgreenOn()
        self.assertEqual(tl.whatsOn(), [True, False, False, False, False, True])

    def test_partialRightCycleTwo(self):
        """
        Test the other part of our right cycle
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.trafficLight.switchOff()
        controller.trafficLight.redOn()
        controller.trafficLight.torangeOn()
        self.assertEqual(tl.whatsOn(), [True, False, False, True, False, False])

    def test_partialOtherCycle(self):
        """
        Test a part of our other cycle
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.trafficLight.switchOff()
        controller.trafficLight.greenOn()
        controller.trafficLight.tredOn()
        self.assertEqual(tl.whatsOn(), [False, True, False, False, True, False])

    def test_partialOtherCycleTwo(self):
        """
        Test the other part of our other cycle
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.trafficLight.switchOff()
        controller.trafficLight.orangeOn()
        controller.trafficLight.tredOn()
        self.assertEqual(tl.whatsOn(), [False, True, True, False, False, False])

    def test_partialBrokenCycle(self):
        """
        Test the broken cycle logic, minus timings
        """
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        controller.trafficLight.switchOff()
        self.assertEqual(tl.whatsOn(), [False, False, False, False, False, False])

        controller.trafficLight.orangeOn()
        controller.trafficLight.torangeOn()
        self.assertEqual(tl.whatsOn(), [False, False, True, True, False, False])

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
        eastLane = [car1, car2, car3, car3]
        simulator.removeCars(eastLane, "LEFT")
        self.assertEqual(eastLane, [car1, car2, car3])

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

    # <-- Custom simulator tests begin -->
    def test_lightsBrokenVar(self):
        """
        Tests if the variable is initialized correct
        """
        self.assertFalse(simulator.lightsAreBroken)

    def test_lightsBrokenLogic(self):
        """
        Tests lightsAreBroken works as intended
        """
        simulator.lightsAreBroken = True
        controller = TrafficLightController("TEST")
        tl = controller.getTL()
        tl.switchOff()
        tl.greenOn()
        tl.tgreenOn()
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        simulator.sensor(controller, lane)
        self.assertEqual(lane, [car1, car2, car3, car3])

        # Reset the variable so as not to break anything
        simulator.lightsAreBroken = False

    def test_countAllCars(self):
        """
        Used to test the counnt all cars method
        """
        controller = TrafficLightController("TEST")
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        lane = [car1, car2, car3, car3]
        self.assertEqual(simulator.CountAllCars(lane), (1, 3))

    def test_bulkWaitChanges(self):
        """
        Tests both IncrementAllWaits() and ResetAllWaits()
        """
        self.assertEqual(simulator.northController.GetOtherWait(), 0)
        self.assertEqual(simulator.eastController.GetOtherWait(), 0)
        self.assertEqual(simulator.southController.GetOtherWait(), 0)
        self.assertEqual(simulator.westController.GetOtherWait(), 0)

        simulator.IncrementAllWaits()
        self.assertEqual(simulator.northController.GetOtherWait(), 1)
        self.assertEqual(simulator.eastController.GetOtherWait(), 1)
        self.assertEqual(simulator.southController.GetOtherWait(), 1)
        self.assertEqual(simulator.westController.GetOtherWait(), 1)

        simulator.ResetAllWaits()
        self.assertEqual(simulator.northController.GetOtherWait(), 0)
        self.assertEqual(simulator.eastController.GetOtherWait(), 0)
        self.assertEqual(simulator.southController.GetOtherWait(), 0)
        self.assertEqual(simulator.westController.GetOtherWait(), 0)

    def test_lightSignalsLogic(self):
        """
        Tests our logic for our light signals
        """
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        car4 = Car("Car4", "NORTH", "RIGHT")
        testFunctions.eastLane = [car1, car2, car3]
        testFunctions.northLane = [car4, car4]
        self.assertEqual(testFunctions.lightSignals(), ("eo", "er"))

    def test_lightSignalWaitLogic(self):
        """
        Tests the logic being wait times in light signals
        """
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        car4 = Car("Car4", "NORTH", "RIGHT")
        car5 = Car("Car5", "NORTH", "STRAIGHT")
        testFunctions.eastLane = [car1, car2, car3]
        testFunctions.northLane = [car4, car5, car4]
        for i in range(10):
            # Force wait to be tripped
            testFunctions.northController.IncrementOtherWait()

        self.assertEqual(testFunctions.lightSignals(), ("no", "nr"))

    def test_lightSignalWaitLogicTwo(self):
        """
        Test further logic behind the wait times
        """
        car1 = Car("Car1", "EAST", "STRAIGHT")
        car2 = Car("Car2", "EAST", "RIGHT")
        car3 = Car("Car3", "EAST", "LEFT")
        car4 = Car("Car4", "NORTH", "RIGHT")
        car5 = Car("Car5", "NORTH", "STRAIGHT")
        testFunctions.eastLane = [car1, car2, car3]
        testFunctions.northLane = [car4, car5]
        testFunctions.northController.wait_other = 7  # test border value

        self.assertEqual(testFunctions.lightSignals(), ("eo", "er"))

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
        Test car str function
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
