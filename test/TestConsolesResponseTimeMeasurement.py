__author__ = 'ronaldbjork'
import unittest
import sys

from MarsProbeTemperatureSensor import MarsProbeTemperatureSensor
from EarthCommandConsole import EarthCommandConsole
from ConfigParser import ConfigParser
import numpy as np
from datetime import datetime
TEST_PROBE_URL = "localhost:5000"

#   Test Suite 1
#   Test Case 1
#       Summary: This test case overall system data acquisition and
#       transmission speed. This test measures full cycle time from
#       the initial request made by the control console, arrival of
#       the request signal at the sensor probe(through NASA data
#       center), the probes retrieval of its sensor measurements,
#       and finally the arrival of the returned data to the
#       controller console(CommandConsole)
#
#       Related Requirements: The system needs to have proven data
#       integrity and mapping of requests to responses.

NASA_WEATHER_PROBE_URL = "https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0"

class TestConsolesResponseTimeMeasurement(unittest.TestCase):

    def setUp(self):
        print("setUp")
        parser = ConfigParser("sysconfig.json")
        self.minTemperature = float(parser.parseParamFromConfig("test/mintemperature"))
        self.responseTime = int(parser.parseParamFromConfig("test/responsetime"))
        self.tempAbove = self.minTemperature + 10
        self.tempBelow = self.minTemperature - 10
        self.earthCommandConsole = EarthCommandConsole()
        self.marsProbeTemperatureSensor = MarsProbeTemperatureSensor(True)

    def test_responseMeasurement(self):
        start = datetime.now()
        self.earthCommandConsole.getSensorData(NASA_WEATHER_PROBE_URL) # True means test only
        end = datetime.now()
        dif = end - start
        self.assertLessEqual(dif.seconds, self.responseTime)

    def runTest(self):
        print("running Sensor tests")
        self.test_responseMeasurement()

        #assert(True == True)

    #def test_minTempetureReading(self):
    #    pass

    if __name__ == "__main__":
        unittest.main()
