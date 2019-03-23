__author__ = 'ronaldbjork'

from flask import Flask, render_template
import os

from EarthCommandConsole import EarthCommandConsole

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
    return render_template('weathergraph.html', name = user,  wvalues = df.to_json())

@app.route('/getweatherlast5days/<string:choice>/')
def getweatherlast5days(choice):
    df = earthCommandConsole.getMarsWeatherForLastFiveDays(choice=="NASA")
    return {'weatherdata':df.to_json()}

@app.route('/get5daysweather/<string:datevalue>/')
def getweatherlast5days(datevalue):
    df = earthCommandConsole.getMarsWeatherForFiveDays(False,datevalue)
    return {'weatherdata':df.to_json()}

@app.route('/')
def render_home():
    user = "ron bjork"
    return render_template('weathergraph.html', name = user,  wvalues = df.to_json())

if __name__ == '__main__':
    print(os.getcwd())
    app.run()
