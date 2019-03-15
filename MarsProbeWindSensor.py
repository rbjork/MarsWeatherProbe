__author__ = 'ronaldbjork'

import time
import numpy as np
from string import Template
from ConfigParser import ConfigParser

responseTime = None
minTemp = None
testEnabled = False

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)

responsetemplate = Template('''{

    "WD":{
        "0": {
				"compass_degrees": ${cd},
				"compass_point": ${cp},
				"compass_right": ${cr},
				"compass_up": ${cu},
				"ct": ${ct}
			},
    }}''')

class MarsProbeWindSensor():

    # Gets tempeture over last hour
    # av: average over hour, ct: current temp, mn : min temp, mx: max temp

    def __init__(self, testEnable):
        self.testEnabled = testEnable
        parser = ConfigParser("./sysconfig.json")
        self.ip = parser.parseParamFromConfig('devices/hub/ip')
        self.host = parser.parseParamFromConfig('devices/hub/host')

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Server 
            s.bind((self.ip, self.host))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    winddata = self.getCurrentSensorReadings()
                    conn.sendall(winddata)

	def getCurrentSensorReadings(self):
		ctv = np.random.normal()
		tvalues = np.random.normal(-50.0,10.0,5)
		avv = tvalues.mean()
		mnv = min(ctv,min(tvalues))
		mxv = max(ctv,max(tvalues))
		readvalues = responsetemplate.substitute(av=avv,mn=mnv,mx=mxv,ct=ctv)
		return readvalues

	def setTestResponseTimeAndMinTemp(self,rt,mt):
		global responseTime, minTemp, testEnabled
		responseTime = rt
		minTemp = mt
		testEnabled = True

	def reset(self):
		global responseTime, minTemp , testEnabled
		responseTime = None
		minTemp = None
		testEnabled = False
