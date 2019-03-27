import unittest
import MarsProbeRadioTransceiver
from ConfigParser import ConfigParser
import json
from datetime import datetime
RESPONSE_TIME = 0.1


class TestTransceiverWeatherPosting(unittest.TestCase):

    def setup(self):
        print("TestTransceiverWeatherPosting setup")
        parser = ConfigParser("sysconfig.json")
        self.responseTime = parser.parseParamFromConfig('test/responsetime')
        self.tranceiver = MarsProbeRadioTransceiver
        self.tranceiver.setup()

    def test_post(self):
        data = self.tranceiver.getsensorreading()
        #datajson = json.loads(data)
        res = self.tranceiver.sendDailyTempeturesV2(data)
        self.assertEqual(res.status_code,200,"Failed send daily temperature")

    def test_post_time(self):
        data = self.tranceiver.getsensorreading()
        #datajson = json.loads(data)
        start = datetime.now()
        res = self.tranceiver.sendDailyTempeturesV2(data)
        end = datetime.now()
        dif = end - start
        self.assertLessEqual(dif.seconds, int(self.responseTime), "Failed post time requirement")

    def test_5_day_post_from_nasa(self):
        res = self.tranceiver.post5daysWeatherData(True)
        self.assertEqual(res.status_code,200,"Failed post 5 Day weather data")

    def runTest(self):
        print("running tranceiver tests")
        self.setup()
        self.test_post()
        self.test_post_time()
        self.test_5_day_post_from_nasa()

    if __name__ == "__main__":
        unittest.main()
