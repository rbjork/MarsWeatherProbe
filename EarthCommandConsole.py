__author__ = 'ronaldbjork'

import urllib.request, json
import requests


from datetime import datetime,timedelta
import numpy as np
import os
import time

from ConfigParser import ConfigParser

NASA_WEATHER_PROBE_URL = "https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0"
TEST_PROBE_URL = "http://localhost:5000"
LOG_FOLDER = "./logs"

NORMALRANGE = {'min':-140, 'max':50}  # tempeture Fahrenheit

# INSPIRED FROM https://qiita.com/bmj0114/items/db9f7b9486769940c422

class EarthCommandConsole():

    def parse_sensor_json(self, input_json, target_key, target_date):
        if type(input_json) is dict and input_json:
            matching = []
            for key in input_json:
                if key == target_key and target_date in input_json[key]:
                    return {'DATETIME':input_json[key], 'AT':input_json['AT']}
                res = self.parse_sensor_json(input_json[key], target_key, target_date)
                if res:
                    matching.append(res)
            if len(matching) > 0:
                return matching
            else:
                return False
        elif type(input_json) is list and input_json:
            matching = []
            for entity in input_json:
                res = self.parse_sensor_json(entity, target_key, target_date)
                if res:
                    matching.append(res)
            if len(matching) > 0:
                return matching
            else:
                return False


    def parseLog4Tempeture(self, date):
        with open("./logs/currentSensorData.json",'r') as fp:
            data = json.loads(fp.read())
            fp.close()
        First_UTCResult = self.parse_sensor_json(data,'First_UTC',date)
        Last_UTCResult = self.parse_sensor_json(data,'Last_UTC',date)
        return {"First_UTCResult":First_UTCResult,"Last_UTCResult":Last_UTCResult}




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
        self.writeToLog(json.dump(data))
        with open("currentSensorData.json",'w') as fp:
            json.dump(data, fp)
            fp.close()
        return data


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


    def getMarsWeatherForLastFiveDays(self):
        getSensorDataAndSaveToLog(self,NASA_WEATHER_PROBE_URL)
        today = datetime.today().date()
        weather = []
        for i in range(5):
            yesturday = today - timedelta(days=i)
            date = "{}-{}-{}".format(yesturday.year,yesturday.month,yesturday.day)
            res = self.parseLog4Tempeture(date)
            weather.append(res)
        for w in weather:
            wfirst = w['First_UTCResult']
            wlast = w['Last_UTCResult']
            if wfirst:
                temp = wfirst[0]['AT']['mn']
            elif wlast:
                temp = wlast[0]['AT']['mx']

    def setup(self):
        parser = ConfigParser("./sysconfig.json")
        self.awsurl = parser.parseParamFromConfig('aws/url')



#if __name__ == "__main__":

    # result =parseLog4Tempeture("2019-03-04")
    # print('2019-03-04',result)
    # result =parseLog4Tempeture("2019-03-05")
    # print('2019-03-05',result)
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
