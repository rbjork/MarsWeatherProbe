__author__ = 'ronaldbjork'

from flask import Flask, render_template, Response
from flask import request, make_response
import requests
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address

from MarsProbeTemperatureSensor import MarsProbeTemperatureSensor
from MarsProbeWindSensor import MarsProbeWindSensor
from WeatherDataParser import WeatherDataParser
from ConfigParser import ConfigParser

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

marsProbeTemperatureSensor = None
marsProbeWindSensor = None
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
    return json.dumps({"status":200})

def sendDailyTempeturesV1():
    tempreading = marsProbeTemperatureSensor.getCurrentSensorReadings()  # Version 1.0
    r = requests.post(AWS_APIGATEWAY, data=tempreading)

def sendDailyTempeturesV2(tempreading):
    r = requests.post(AWS_APIGATEWAY, data=tempreading)

@app.route("/post5daysweatherdata", methods=['GET'])
def post5daysWeatherData(nasa=False):
    headers = {"Content-Type":"application/json", "x-api-key":"fbgAxsG1pr3H7WQrUPoWz4V0aDzF5Knua938WYja"}
    if nasa:
        with urllib.request.urlopen(urlvalue) as url:
            weatherdata = json.loads(url.read().decode())
            with open("./logs/currentSensorData.json",'w') as fp:
                json.dump(data, fp)
                fp.close()

    daycount = 0
    today = datetime.today().date()

    weaterdata5day = []

    while daycount < 5:
        time.sleep(1)
        dayIn5 = today - timedelta(days=daycount+1)
        month = str(dayIn5.month) if dayIn5.month > 9 else '0'+ str(dayIn5.month)
        day = str(dayIn5.day) if dayIn5.day > 9 else '0' + str(dayIn5.day)
        date = "{}-{}-{}".format(dayIn5.year, month, day)
        if nasa:
            weatherdata4date = weatherDataParser.parseLog4Weather(date)
            weatherdata4date["DATETIME":date]
        else:
            weatherdata4date = {"DATETIME":date}
            if onboardsensors:
                sensortempreadings = marsProbeTemperatureSensor.getCurrentSensorReadings()
                sensorwindreadings = marsProbeWindSensor.getCurrentSensorReadings()
            else:
                sensortempreadings = connectTempetureSensor()
                sensorwindreadings = connectWindSensor()

            weatherdata4date["Temperature"] = sensortempreadings
            weatherdata4date["Wind"] = sensorwindreadings})

        r = requests.post(AWS_APIGATEWAY, data=weatherdata4date, headers=headers)
        weaterdata5day.append(weatherdata4date)
        daycount += 1
    r = requests.post(AWS_APIGATEWAY, data=weaterdata5day, headers=headers)
    return


def setup():
    global marsProbeTemperatureSensor, marsProbeWindSensor, AWS_APIGATEWAY, temp_ip, temp_port, wind_ip, wind_port, onboardsensors
    marsProbeTemperatureSensor = MarsProbeTemperatureSensor()
    marsProbeWindSensor = MarsProbeWindSensor()  # not used
    weatherDataParser = WeatherDataParser()
    parser = ConfigParser("./sysconfig.json")
    temp_ip = parser.parseParamFromConfig('devices/tempsensor/ip')
    temp_port = parser.parseParamFromConfig('devices/tempsensor/port')
    wind_ip = parser.parseParamFromConfig('devices/windsensor/ip')
    wind_port = parser.parseParamFromConfig('devices/windsensor/port')
    onboardsensors = parser.parseParamFromConfig('devices/tempsensor/onboardsensors')
    AWS_APIGATEWAY = parser.parseParamFromConfig('cloud/aws_apigateway/url')


# UPGRADE Version 2.0
def connectTempetureSensor():
    tempdata = {}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # client
        s.connect((temp_ip, temp_port))
        s.sendall(b'Send Temperature')
        tempdata = s.recv(1024)
    return tempdata


# UPGRADE Version 2.0
def connectWindowSensor():
    winddata = {}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((wind_ip, wind_port))
        s.sendall(b'Send Wind')
        winddata = s.recv(1024)
    return winddata


if __name__ == "__main__":
    setup()
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    ipaddress = "http://" + HOST
    print(ipaddress)
    app.run(host=HOST, port=5000, threaded=True)
