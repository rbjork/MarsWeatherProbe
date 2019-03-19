__author__ = 'ronaldbjork'

import urllib.request, json
import requests
import pandas as pd


from datetime import datetime,timedelta
import numpy as np
import os
import time
import boto
import botocore

from WeatherDataParser import WeatherDataParser

from ConfigParser import ConfigParser

ONEC2 = True

NASA_WEATHER_PROBE_URL = "https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0"
TEST_PROBE_URL = "http://localhost:5000"
LOG_FOLDER = "logs"

BUCKET_NAME = 's3-to-es-bucket' # replace with your bucket name
#KEY = 'my_image_in_s3.jpg' # replace with your object key

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


    def readFromLog(self, date): # this could be either from NASA or sensors written from here or KP remote
        s3 = boto.resource('s3')
        data = False
        try:
            allfileobjects = s3.list_objects(Bucket=BUCKET_NAME, Prefix="logs/", Delimiter='/')
            for key in allfileobjects:
                obj = allfileobjects[key].get()
                body = obj['Body'].read()
                logdata = json.loads(str(body, 'utf-8'))
                datestamp = logdata['DATETIME']
                if date == datestamp:
                    data = logdata
                    break

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                pass

        return data


    def writeToLog(self, data, toS3=False, fromEC2=False):
        today = datetime.today()
        logfilepath = "{}/Sensordata5Day_{}.json".format(LOG_FOLDER, str(today.date()))
        if toS3:
            s3 = boto.resource('s3')
            bucket = s3.Bucket(BUCKET_NAME)
            bucket.put_object(
                ACL='public-read',
                ContentType='application/json',
                Key=logfilepath,
                Body=json.dumps(data),
            )
        else:
            if os.path.exists(logfilepath):
                with open(logfilepath,'a') as fp:
                    fp.write(str(data))
                    fp.close()
            else:
                with open(logfilepath,'w') as fp:
                    fp.write(str(data))
                    fp.close()

    def setAlarmTempeture(self,mintempeture):
        self.minTemperature = mintempeture

    def getSensorDataAndSaveToLog(self,urlvalue):
        with urllib.request.urlopen(urlvalue) as url:
            data = json.loads(url.read().decode())
            self.writeToLog(json.dumps(data))
            with open("./logs/currentSensorData.json",'w') as fp:
                json.dump(data, fp)
                fp.close()
        return data

    def getMarsWeatherForLastFiveDays(self,fromNasa):
        if fromNasa:
            self.getSensorDataAndSaveToLog(NASA_WEATHER_PROBE_URL)

        today = datetime.today().date()
        weather = []
        for i in range(5):

            dayIn5 = today - timedelta(days=i+1)
            month = str(dayIn5.month) if dayIn5.month > 9 else '0'+ str(dayIn5.month)
            day = str(dayIn5.day) if dayIn5.day > 9 else '0' + str(dayIn5.day)
            date = "{}-{}-{}".format(dayIn5.year, month, day)
            if fromNasa:
                res = self.weatherDataParser.parseLog4Weather(date) # Direct From NASA with url call
            else:
                res = self.readFromLog(date) # from sensors data posted to AWS S3

            if res and res['Temperature'] and res['Wind']:
                print(res)
                av = res['Temperature'][0]['AT']['av']
                mn = res['Temperature'][0]['AT']['mn']
                mx = res['Temperature'][0]['AT']['mx']
                wnd = res['Wind'][0]['WD']['0']['ct']
                val = {"DATE":date,"DAY":day,"TEMPavg":av,"TEMPmin":mn,"TEMPmax":mx,"WIND":wnd}
                weather.append(val)
        df = pd.DataFrame(weather)
        mean = df['TEMPavg'].mean()
        maxtemp = df['TEMPmax'].max()
        mintemp = df['TEMPmin'].min()
        print(mean,maxtemp,mintemp)
        return (df, mean, maxtemp, mintemp)


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
    ONEC2 = False
    earthConsole = EarthCommandConsole()
    result = earthConsole.getMarsWeatherForLastFiveDays(True)
    df = result[0]
    with open("./logs/Sensordata5DayDF.json",'w') as fp:
        df.to_json(fp)
        fp.close()
    df.to_json()
    print(result)
    #result = earthConsole.parseLog4Tempeture("2019-03-04")
    #print(result)
