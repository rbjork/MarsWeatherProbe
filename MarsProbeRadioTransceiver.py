__author__ = 'ronaldbjork'

from flask import Flask, render_template
from flask import request, make_response
import requests
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
WINDSENSORPORT = 65433  # The port used by the server
TEMPSENSORPORT = 65432

from MarsProbeTemperatureSensor import MarsProbeTemperatureSensor
from MarsProbeWindSensor import MarsProbeWindSensor
from ConfigParser import ConfigParser

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
marsProbeTemperatureSensor = None
marsProbeWindSensor = None

AWS_ELASTIC_SEARCH_ENDPOINT = ""
AWS_APIGATEWAY = ""



@app.route("/getsensorreading", methods=['GET'])
def getsensorreading():
    tempreading = marsProbeTemperatureSensor.getCurrentSensorReadings()  # Version 1.0
    windreading = marsProbeWindSensor.getCurrentSensorReadings()  # Version 1.0



def sendHourlyTempeturesV1():
    tempreading = marsProbeTemperatureSensor.getCurrentSensorReadings()  # Version 1.0
    r = requests.post(AWS_ELASTIC_SEARCH_ENDPOINT, data=tempreading)
    r = requests.post(AWS_APIGATEWAY, data=tempreading)

def sendHourlyTempeturesV2(tempreading):
    r = requests.post(AWS_ELASTIC_SEARCH_ENDPOINT, data=tempreading)
    r = requests.post(AWS_APIGATEWAY, data=tempreading)


def setup():
    global marsProbeTemperatureSensor,AWS_ELASTIC_SEARCH_ENDPOINT,AWS_APIGATEWAY, temp_ip, temp_host
    marsProbeTemperatureSensor = MarsProbeTemperatureSensor()
    marsProbeWindSensor = MarsProbeWindSensor()  # not used
    parser = ConfigParser("./sysconfig.json")
    temp_ip = parser.parseParamFromConfig('devices/tempsensor/ip')
    temp_host = parser.parseParamFromConfig('devices/tempsensor/host')
    bysocket = parser.parseParamFromConfig('devices/tempsensor/hassocket')
    AWS_ELASTIC_SEARCH_ENDPOINT = parser.parseParamFromConfig('cloud/aws_es/url')
    AWS_APIGATEWAY = parser.parseParamFromConfig('cloud/aws_apigateway/url')
    while True:
        time.sleep(10)
        if bysocket:
            connectTempetureSensor()
        else:
            sendHourlyTempeturesV1()


# UPGRADE Version 2.0
def connectTempetureSensor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # client
        s.connect((HOST, TEMPSENSORPORT))
        s.sendall(b'Send Temperature')
        tempdata = s.recv(1024)
        sendHourlyTempeturesV2(tempdata)
    print('Received', repr(data))


# UPGRADE Version 2.0
def connectWindowSensor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, WINDSENSORPORT))
        s.sendall(b'Send Wind')
        winddata = s.recv(1024)
    print('Received', repr(data))


if __name__ == "__main__":
    setup()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    ipaddress = "http://" + ip
    print(ipaddress)
    app.run(host=ip, port=5000, threaded=True)
