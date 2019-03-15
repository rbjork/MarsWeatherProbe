__author__ = 'ronaldbjork'

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import requests

from EarthCommandConsole import EarthCommandConsole

earthCommandConsole = None

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor':colors['background']}, children=[
    html.H1(children='Mars Probe Master Control',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    dcc.Graph(
        id='five-day-mars-weather',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    ),
    
    html.Button('Get 5 Day Tempetures', id='read5DayTemp_btn'),
    html.Div(id='current-temp-readout'),
    html.Button('Get Current Tempeture', id='readcurrenttemp_btn')

])

@app.callback(Output(component_id='five-day-mars-weather', component_property='children'),[Input('read5DayTemp_btn','n_clicks' )])
def getTempData(n_clicks):
    data = earthCommandConsole.getMarsWeatherForLastFiveDays()

@app.callback(Output(component_id='current-temp-readout'), component_property='children'),[Input('readcurrenttemp_btn','n_clicks')]
def getCurrentTemp(n_clicks):
    pass

def setup():
    global earthCommandConsole
    earthCommandConsole = EarthCommandConsole()


if __name__ == "__main__":
    setup()
    app.run_server(debug=True)
