__author__ = 'ronaldbjork'

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import requests
import json 

from EarthCommandConsole import EarthCommandConsole

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF',
    'graph_bg': '#666666'
}
fontsizes = {
    'title':'20'
}

earthCommandConsole = None

df = pd.DataFrame({'day':[1,2,3,4,5],'temperature':[-30,-23,-22,-40,10],'wind':[5,4,54,20,14]})

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor':colors['background']}, children=[
    html.H1(children='Mars Probe Master Control',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-size':fontsizes['title']
        }),

    dcc.Graph(
        id='five-day-mars-weather',
        figure={
            'data': [
                go.Scatter(
                    x=df['day'],
                    y=df['temperature'],
                    mode='lines',
                    opacity=0.7,
                    name='Temperature'
                ),
                go.Scatter(
                    x=df['day'],
                    y=df['wind'],
                    mode='lines',
                    opacity=0.7,
                    name='Wind'
                )
            ],
            'layout': go.Layout(
                xaxis={'type': 'linear', 'title': 'Day', 'showgrid':True, 'showline':True},
                yaxis={'title': 'Temperature', 'showgrid':True, 'showline':True},
                margin={'l': 60, 'b': 60, 't': 10, 'r': 50},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                plot_bgcolor='rgba(70,70,70,1)',
                paper_bgcolor='rgba(70,70,70,1)',
                font = dict(
                  color = "white",
                  size = 12
                )
            )
        }
    ),

    html.Button('Get 5 Day Tempetures', id='read5DayTemp_btn'),
    html.Div(id='current-temp-readout'),
    html.Button('Get Current Tempeture', id='readcurrenttemp_btn')

])

@app.callback(Output('five-day-mars-weather', 'figure'),[Input('read5DayTemp_btn','n_clicks' )])
def getTempData(n_clicks):
    print("click")
    df = earthCommandConsole.getMarsWeatherForLastFiveDays()
    print(json.dumps(df))

@app.callback(Output(component_id='current-temp-readout', component_property='children'),[Input('readcurrenttemp_btn','n_clicks')])
def getCurrentTemp(n_clicks):
    pass

def setup():
    global earthCommandConsole
    earthCommandConsole = EarthCommandConsole()


if __name__ == "__main__":
    setup()
    app.run_server(debug=True)