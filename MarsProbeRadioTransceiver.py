__author__ = 'ronaldbjork'

from flask import Flask

import requests
import socket
import json
import urllib
from datetime import datetime, timedelta
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
NASA_WEATHER_PROBE_URL = "https://mars.nasa.gov/rss/api/?feed=weather&category=insight&feedtype=json&ver=1.0"

from MarsProbeTemperatureSensor import MarsProbeTemperatureSensor
from MarsProbeWindSensor import MarsProbeWindSensor
from WeatherDataParser import WeatherDataParser
from ConfigParser import ConfigParser

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

marsProbeTemperatureSensor = None
marsProbeWindSensor = None
weatherDataParser = None
temp_port = ""
temp_ip = ""
wind_port = ""
wind_ip = ""
onboardsensors = False

AWS_APIGATEWAY = ""


@app.route("/getsensorreading", methods=['GET'])
def getsensorreading():
    tempreading = marsProbeTemperatureSensor.getCurrentSensorReadings()  # Version 1.0
    windreading = marsProbeWindSensor.getCurrentSensorReadings()  # Version 1.0
    return json.dumps({"Temperature": tempreading, "Wind": windreading})


def sendDailyTempeturesV1():
    tempreading = marsProbeTemperatureSensor.getCurrentSensorReadings()  # Version 1.0
    r = requests.post(AWS_APIGATEWAY, data=tempreading)


def setAlarmTempeture(self, mintempeture):
    self.minTemperature = mintempeture


def checkTempeture(self, sensordata):
    data = json.loads(sensordata)
    air_temp_data_1 = data['First_UTCResult']
    air_temp_data_2 = data['Last_UTCResult']
    temperature = None
    if air_temp_data_1:
        temperature = air_temp_data_1[0]['AT']['mn']
    elif air_temp_data_2:
        temperature = air_temp_data_2[0]['AT']['mx']

    if temperature is None:
        message = "reading failed"
    elif temperature > self.minTemperature:
        message = "Temp in normal range"
    else:
        message = "Temp below normal range"

    return {'tempeture': temperature, 'message': message}


def sendDailyTempeturesV2(tempreading):
    r = requests.post(AWS_APIGATEWAY, data=tempreading)


@app.route("/post5daysweatherdata", methods=['GET'])
def post5daysWeatherData(nasa=False):
    headers = {"Content-Type": "application/json", "x-api-key": "fbgAxsG1pr3H7WQrUPoWz4V0aDzF5Knua938WYja"}
    if nasa:
        with urllib.request.urlopen(NASA_WEATHER_PROBE_URL) as url:
            weatherdata = json.loads(url.read().decode())
            with open("./logs/currentSensorData.json", 'w') as fp:
                json.dump(weatherdata, fp)
                fp.close()

    daycount = 0
    today = datetime.today().date()

    weaterdata5day = []

    while daycount < 5:
        time.sleep(1)
        dayIn5 = today - timedelta(days=daycount + 1)
        month = str(dayIn5.month) if dayIn5.month > 9 else '0' + str(dayIn5.month)
        day = str(dayIn5.day) if dayIn5.day > 9 else '0' + str(dayIn5.day)
        date = "{}-{}-{}".format(dayIn5.year, month, day)
        if nasa:
            weatherdata4date = weatherDataParser.parseLog4Weather(date)
            weatherdata4date["DATETIME"] = date
        else:
            weatherdata4date = {"DATETIME": date}
            if onboardsensors:
                sensortempreadings = marsProbeTemperatureSensor.getCurrentSensorReadings()
                sensorwindreadings = marsProbeWindSensor.getCurrentSensorReadings()
            else:
                sensortempreadings = connectTempetureSensor()
                sensorwindreadings = connectWindSensor()

            weatherdata4date["Temperature"] = sensortempreadings
            weatherdata4date["Wind"] = sensorwindreadings

        r = requests.post(AWS_APIGATEWAY, data=weatherdata4date, headers=headers)
        print(weatherdata4date)
        print(r.status_code)
        #weaterdata5day.append(weatherdata4date)
        daycount += 1
    #r = requests.post(AWS_APIGATEWAY, data=weaterdata5day, headers=headers)
    return


def setup():
    global marsProbeTemperatureSensor, marsProbeWindSensor, weatherDataParser, AWS_APIGATEWAY, temp_ip, temp_port, wind_ip, wind_port, onboardsensors
    marsProbeTemperatureSensor = MarsProbeTemperatureSensor(False)
    marsProbeWindSensor = MarsProbeWindSensor(False)  # not used
    weatherDataParser = WeatherDataParser()
    parser = ConfigParser("./sysconfig.json")
    temp_ip = parser.parseParamFromConfig('devices/tempsensor/ip')
    temp_port = parser.parseParamFromConfig('devices/tempsensor/port')
    wind_ip = parser.parseParamFromConfig('devices/windsensor/ip')
    wind_port = parser.parseParamFromConfig('devices/windsensor/port')
    onboardsensors = parser.parseParamFromConfig('onboardsensors')
    AWS_APIGATEWAY = parser.parseParamFromConfig('cloud/aws_apigateway/url')


# UPGRADE Version 2.0
def connectTempetureSensor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # client
        s.connect((temp_ip, temp_port))
        s.sendall(b'Send Temperature')
        tempdata = s.recv(1024)
    return tempdata


# UPGRADE Version 2.0
def connectWindSensor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((wind_ip, wind_port))
        s.sendall(b'Send Wind')
        winddata = s.recv(1024)
    return winddata


if __name__ == "__main__":
    setup()
    post5daysWeatherData(True)
    exit()


    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    ipaddress = "http://" + HOST
    print(ipaddress)
    app.run(host=HOST, port=5000, threaded=True)
