import unittest
import unittest
import MarsProbeTemperatureSensor
import EarthCommandConsole
import MarsProbeWindSensor
import MarsProbeRadioTransceiver
import numpy as np
from datetime import datetime

TEST_PROBE_URL = "localhost:5000"

class TestMeasurementLowTemperatureAlarm(unittest.TestCase):

    def setup(self):
        self.minTemperature = np.random.normal(-80,50,1)
        self.tempAbove = self.minTemperature + 10
        self.tempBelow = self.minTemperature - 10
        self.marsProbeTemperatureSensor = MarsProbeTemperatureSensor()
        self.marsProbeRadioTransceiver = MarsProbeRadioTransceiver()
        self.marsProbeTemperatureSensor.setTestResponseTimeAndMinTemp(self.responseTime, self.minTempeture)

    def testLowTempAlarmWithTempBelow(self):
        res = self.marsProbeRadioTransceiver.checkTempeture({[{'AT':{"mn":self.tempBelow}}]})
        self.assertEqual(res,"Temp below normal range","Good")

    def testLowTempAlarmWithTempAbove(self):
        res = self.marsProbeRadioTransceiver.checkTempeture({[{'AT':{"mn":self.tempAbove}}]})
        self.assertEqual(res,"Temp in normal range","Good")
