__author__ = 'ronaldbjork'

from flask import Flask, render_template
import os
import pdb
from EarthCommandConsole import EarthCommandConsole
import json

import pandas as pd
import random

app = Flask(__name__)

earthCommandConsole = EarthCommandConsole()

tavg = [random.uniform(-100,10) for i in range(5)]
tmin = [random.uniform(-100,10) for i in range(5)]
tmax = [random.uniform(-100,10) for i in range(5)]
windspeed = [random.uniform(0,100) for i in range(5)]
winddirection = [random.uniform(0,359) for i in range(5)]

df = pd.DataFrame({'DAY':[1,2,3,4,5],'TEMPavg':tavg, 'TEMPmin':tmin, 'TEMPmax':tmax, 'WINDSPEED':windspeed, 'WINDDIRECTION':winddirection})


@app.route('/weatherlast5days/<string:datevalue>/')
def weatherlast5days(datevalue):
    global df
    user = "ron bjork"
    df = earthCommandConsole.getMarsWeatherForLastFiveDays(datevalue)
    df_json = df.to_json()
    return render_template('weathergraph.html', name = user,  wvalues = df_json)

@app.route('/getweatherlast5days/<string:choice>/')
def getweatherlast5days(choice):
    df = earthCommandConsole.getMarsWeatherForLastFiveDays(choice=="NASA")
    df_json = df.to_json()
    res = {"success":True, "weatherdata":df_json}
    return json.dumps(res)

@app.route('/get5daysweather/<string:datevalue>')
def get5daysweather(datevalue):
    df = earthCommandConsole.getMarsWeatherForFiveDays(False,datevalue)
    df_json = df.to_json()
    res = {"success":True, "weatherdata":df_json}
    return json.dumps(res)

@app.route('/')
def render_home():
    user = "Ron"
    print(df.to_json())
    return render_template('weathergraph.html', name = user,  wvalues = df.to_json())

if __name__ == '__main__':
    print(os.getcwd())
    app.run()
