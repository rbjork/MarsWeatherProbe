__author__ = 'ronaldbjork'
import unittest
import MarsProbeTemperatureSensor
import EarthCommandConsole
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

class TestConsolesResponseTimeMeasurement(unittest.TestCase):

    def setUp(self):
        self.responseTime = max(0.0,np.random.normal(.5,.1,1))
        self.minTemperature = np.random.normal(-80,50,1)
        self.tempAbove = self.minTemperature + 10
        self.tempBelow = self.minTemperature - 10
        self.marsProbeTemperatureSensor = MarsProbeTemperatureSensor()
        self.earthCommandConsole = EarthCommandConsole()
        self.marsProbeTemperatureSensor.setTestResponseTimeAndMinTemp(self.responseTime, self.minTempeture)

    def test_responseMeasurement(self):
        start = datetime.now()
        self.earthCommandConsole.getSensorData(True) # True means test only
        end = datetime.now()
        dif = end - start
        self.assertLessEqual(dif,1.1*self.responseTime)

    def test_minTempetureReading(self):
        pass