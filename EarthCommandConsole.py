__author__ = 'ronaldbjork'

import urllib.request, json
import requests


from datetime import datetime,timedelta
import numpy as np
import os
import time

from WeatherDataParser import WeatherDataParser

from ConfigParser import ConfigParser

NASA_WEATHER_PROBE_URL = "https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0"
TEST_PROBE_URL = "http://localhost:5000"
LOG_FOLDER = "./logs"

NORMALRANGE = {'min':-140, 'max':50}  # tempeture Fahrenheit

# INSPIRED FROM https://qiita.com/bmj0114/items/db9f7b9486769940c422

class EarthCommandConsole():

    def __init__(self):
        parser = ConfigParser("./sysconfig.json")
        self.weatherDataParser = WeatherDataParser()
        self.awsapi = parser.parseParamFromConfig('cloud/aws_apigateway/url')


    def checkTempeture(self, sensordata):
        data = json.loads(sensordata)
        air_temp_data_1 = data['First_UTCResult']
        air_temp_data_2 = data['Last_UTCResult']
        tempeture = None
        if air_temp_data_1:
            tempeture = air_temp_data_1[0]['AT']['mn']
        elif air_temp_data_2:
            tempeture = air_temp_data_2[0]['AT']['mx']

        if tempeture is None:
            message = "reading failed"
        elif tempeture < NORMALRANGE.min:
            message = "Temp in normal range"
        else:
            message = "Temp below normal range"

        return {'tempeture':tempeture,'message':message}


    def getSensorData(self,urlvalue):
        with urllib.request.urlopen(urlvalue) as url:
            sensorData = url.read().decode()
        self.checkTempeture(sensorData)
        return sensorData


    def writeToLog(self, data):
        today = datetime.today()
        logfile = "{}/log_{}.txt".format(LOG_FOLDER, str(today.date()))
        if os.path.exists(logfile):
            with open(logfile,'a') as fp:
                fp.write(str(data))
                fp.close()
        else:
            with open(logfile,'w') as fp:
                fp.write(str(data))
                fp.close()

    def setAlarmTempeture(self,mintempeture):
        pass

    def getSensorDataAndSaveToLog(self,urlvalue):
        with urllib.request.urlopen(urlvalue) as url:
            data = json.loads(url.read().decode())
            self.writeToLog(json.dumps(data))
            with open("./logs/currentSensorData1.json",'w') as fp:
                json.dump(data, fp)
                fp.close()

        return data

    def getMarsWeatherForLastFiveDays(self):
        self.getSensorDataAndSaveToLog(NASA_WEATHER_PROBE_URL)
        today = datetime.today().date()
        weather = []
        for i in range(5):
            dayIn5 = today - timedelta(days=i+1)
            month = str(dayIn5.month) if dayIn5.month > 9 else '0'+ str(dayIn5.month)
            day = str(dayIn5.day) if dayIn5.day > 9 else '0' + str(dayIn5.day)
            date = "{}-{}-{}".format(dayIn5.year, month, day)
            res = self.weatherDataParser.parseLog4Weather(date)
            weather.append(res)
        return weather


    def testCasehalfSecond(self,urlvalue):
        timedrequests = []
        for i in range(10):
            start = datetime.today()
            urllib.request.urlopen(urlvalue)
            end = datetime.today()
            dif = end - start
            timedrequests.append(dif.microseconds/1000)
            time.sleep(.5)
        mean = np.array(timedrequests).mean()
        return mean


if __name__ == "__main__":
    earthConsole = EarthCommandConsole()
    result = earthConsole.getMarsWeatherForLastFiveDays()
    print(result)
    #result = earthConsole.parseLog4Tempeture("2019-03-04")
    #print(result)
    #result =earthConsole.parseLog4Tempeture("2019-03-05")
    #print(result)
    # result =parseLog4Tempeture("2019-03-06")
    # print("2019-03-06",result)
    # result =parseLog4Tempeture("2019-03-07")
    # print("2019-03-07",result)
    # result =parseLog4Tempeture("2019-03-08")
    # print('2019-03-08',result)
    # result =parseLog4Tempeture("2019-03-09")
    # print("2019-03-09",result)
    # result =parseLog4Tempeture("2019-03-10")
    # print("2019-03-10",result)
    # result =parseLog4Tempeture("2019-03-11")
    # print("2019-03-11",result)
    #loadJson2file()
    #mean = testCasehalfSecond()
    #print("mean request time:",str(mean))
