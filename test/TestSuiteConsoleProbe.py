import unittest
from TestConsolesResponseTimeMeasurement import TestConsolesResponseTimeMeasurement
from TestMeasurementAddressingAccuracy import TestMeasurementAddressingAccuracy

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConsolesResponseTimeMeasurement('test request response cycle time against spec'))
    suite.addTest(TestMeasurementAddressingAccuracy('test request message deciphering and accuracy'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
