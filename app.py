import time
import pathlib
import os

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import State, Input, Output
import dash_daq as daq

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

# This is for gunicorn
server = app.server

# Dash_DAQ elements

utc = html.Div(
    id="control-panel-utc",
    children=[
        daq.LEDDisplay(
            id="control-panel-utc-component",
            value="16:23",
            label="Time",
            size=40,
            color="#fec036",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

speed = html.Div(
    id="control-panel-speed",
    children=[
        daq.Gauge(
            id="control-panel-speed-component",
            label="Speed",
            min=0,
            max=40,
            showCurrentValue=True,
            value=27.859,
            size=175,
            units="1000km/h",
            color="#fec036",
        )
    ],
    n_clicks=0,
)

elevation = html.Div(
    id="control-panel-elevation",
    children=[
        daq.Tank(
            id="control-panel-elevation-component",
            label="Elevation",
            min=0,
            max=1000,
            value=650,
            units="kilometers",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

temperature = html.Div(
    id="control-panel-temperature",
    children=[
        daq.Tank(
            id="control-panel-temperature-component",
            label="Temperature",
            min=0,
            max=500,
            value=290,
            units="Kelvin",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

fuel_indicator = html.Div(
    id="control-panel-fuel",
    children=[
        daq.GraduatedBar(
            id="control-panel-fuel-component",
            label="Fuel Level",
            min=0,
            max=100,
            value=76,
            step=1,
            showCurrentValue=True,
            color="#fec036",
        )
    ],
    n_clicks=0,
)

battery_indicator = html.Div(
    id="control-panel-battery",
    children=[
        daq.GraduatedBar(
            id="control-panel-battery-component",
            label="Battery-Level",
            min=0,
            max=100,
            value=85,
            step=1,
            showCurrentValue=True,
            color="#fec036",
        )
    ],
    n_clicks=0,
)

longitude = html.Div(
    id="control-panel-longitude",
    children=[
        daq.LEDDisplay(
            id="control-panel-longitude-component",
            value="0000.0000",
            label="Longitude",
            size=24,
            color="#fec036",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

latitude = html.Div(
    id="control-panel-latitude",
    children=[
        daq.LEDDisplay(
            id="control-panel-latitude-component",
            value="0050.9789",
            label="Latitude",
            size=24,
            color="#fec036",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

solar_panel_0 = daq.Indicator(
    className="panel-lower-indicator",
    id="control-panel-solar-panel-0",
    label="Solar-Panel-0",
    labelPosition="bottom",
    value=True,
    color="#fec036",
    style={"color": "#black"},
)

solar_panel_1 = daq.Indicator(
    className="panel-lower-indicator",
    id="control-panel-solar-panel-1",
    label="Solar-Panel-1",
    labelPosition="bottom",
    value=True,
    color="#fec036",
    style={"color": "#black"},
)

camera = daq.Indicator(
    className="panel-lower-indicator",
    id="control-panel-camera",
    label="Camera",
    labelPosition="bottom",
    value=True,
    color="#fec036",
    style={"color": "#black"},
)

thrusters = daq.Indicator(
    className="panel-lower-indicator",
    id="control-panel-thrusters",
    label="Thrusters",
    labelPosition="bottom",
    value=True,
    color="#fec036",
    style={"color": "#black"},
)

motor = daq.Indicator(
    className="panel-lower-indicator",
    id="control-panel-motor",
    label="Motor",
    labelPosition="bottom",
    value=True,
    color="#fec036",
    style={"color": "#black"},
)

communication_signal = daq.Indicator(
    className="panel-lower-indicator",
    id="control-panel-communication-signal",
    label="Signal",
    labelPosition="bottom",
    value=True,
    color="#fec036",
    style={"color": "#black"},
)

map_toggle = daq.ToggleSwitch(
    id="control-panel-toggle-map",
    value=True,
    label=["Off", "On"],
    color="#ffe102",
    style={"color": "#black"},
)

minute_toggle = daq.ToggleSwitch(
    id="control-panel-toggle-minute",
    value=True,
    label=["Past Hour", "Past Minute"],
    color="#ffe102",
    style={"color": "#black"},
)

# Side panel

dropdown = dcc.Dropdown(
    id="dropdown-component",
    options=[
        {"label": "Option01", "value": "value01"},
        {"label": "Option02", "value": "value02"},
    ],
    clearable=False,
    value="value01",
)

dropdown_text = html.P(id="dropdown-text", children=["Main Title"])

title = html.H1(id="name", children="")

body = html.P(className="description", id="description", children=[""])

side_panel_layout = html.Div(
    id="panel-side",
    children=[
        dropdown_text,
        html.Div(id="dropdown", children=dropdown),
        html.Div(id="panel-side-text", children=[title, body]),
    ],
)

# Helper to straighten lines on the map
def flatten_path(xy1, xy2):
    diff_rate = (xy2 - xy1) / 100
    res_list = []
    for i in range(100):
        res_list.append(xy1 + i * diff_rate)
    return res_list


map_data = [
    {
        "type": "scattermapbox",
        "lat": [0],
        "lon": [0],
        "hoverinfo": "text+lon+lat",
        "text": "Satellite Path",
        "mode": "lines",
        "line": {"width": 2, "color": "#707070"},
    },
    {
        "type": "scattermapbox",
        "lat": [0],
        "lon": [0],
        "hoverinfo": "text+lon+lat",
        "text": "Current Position",
        "mode": "markers",
        "marker": {"size": 10, "color": "#fec036"},
    },
]

map_layout = {
    "showlegend": False,
    "autosize": True,
    "paper_bgcolor": "#1e1e1e",
    "plot_bgcolor": "#1e1e1e",
    "margin": {"t": 0, "r": 0, "b": 0, "l": 0},
}

map_graph = html.Div(
    id="world-map-wrapper",
    children=[
        map_toggle,
        dcc.Graph(
            id="world-map",
            figure={"data": map_data, "layout": map_layout},
            config={"displayModeBar": False, "scrollZoom": False},
        ),
    ],
)

# Histogram

histogram = html.Div(
    id="histogram-container",
    children=[
        html.Div(
            id="histogram-header",
            children=[
                html.H1(
                    id="histogram-title", children=["Select A Property To Display"]
                ),
                minute_toggle,
            ],
        ),
        dcc.Graph(
            id="histogram-graph",
            figure={
                "data": [
                    {
                        "x": [i for i in range(60)],
                        "y": [i for i in range(60)],
                        "type": "scatter",
                        "marker": {"color": "#fec036"},
                    }
                ],
                "layout": {
                    "margin": {"t": 30, "r": 35, "b": 40, "l": 50},
                    "xaxis": {"dtick": 5, "gridcolor": "#636363", "showline": False},
                    "yaxis": {"showgrid": False},
                    "plot_bgcolor": "#2b2b2b",
                    "paper_bgcolor": "#2b2b2b",
                    "font": {"color": "gray"},
                },
            },
            config={"displayModeBar": False},
        ),
    ],
)

# Control panel + map
main_panel_layout = html.Div(
    id="panel-upper-lower",
    children=[
        dcc.Interval(id="interval", interval=1 * 2000, n_intervals=0),
        map_graph,
        html.Div(
            id="panel",
            children=[
                histogram,
                html.Div(
                    id="panel-lower",
                    children=[
                        html.Div(
                            id="panel-lower-0",
                            children=[elevation, temperature, speed, utc],
                        ),
                        html.Div(
                            id="panel-lower-1",
                            children=[
                                html.Div(
                                    id="panel-lower-led-displays",
                                    children=[latitude, longitude],
                                ),
                                html.Div(
                                    id="panel-lower-indicators",
                                    children=[
                                        html.Div(
                                            id="panel-lower-indicators-0",
                                            children=[solar_panel_0, thrusters],
                                        ),
                                        html.Div(
                                            id="panel-lower-indicators-1",
                                            children=[solar_panel_1, motor],
                                        ),
                                        html.Div(
                                            id="panel-lower-indicators-2",
                                            children=[camera, communication_signal],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    id="panel-lower-graduated-bars",
                                    children=[fuel_indicator, battery_indicator],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Data generation

# Pandas
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# Root
root_layout = html.Div(
    id="root",
    children=[
        dcc.Store(id="store-placeholder"),
        dcc.Store(
            id="store-data",
            data={},
        ),
        # For the case no components were clicked, we need to know what type of graph to preserve
        dcc.Store(id="store-data-config", data={"info_type": "", "satellite_type": 0}),
        side_panel_layout,
        main_panel_layout,
    ],
)

app.layout = root_layout

if __name__ == "__main__":
    app.run_server(debug=True)
