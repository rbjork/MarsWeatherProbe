import unittest
import sys

from test.TestConsolesResponseTimeMeasurement import TestConsolesResponseTimeMeasurement
from test.TestTransceiverWeatherPosting import TestTransceiverWeatherPosting

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConsolesResponseTimeMeasurement())
    #suite.addTest(TestMeasurementLowTemperatureAlarm('test request message deciphering and accuracy'))
    suite.addTest(TestTransceiverWeatherPosting())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
