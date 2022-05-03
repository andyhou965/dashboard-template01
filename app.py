import pathlib
import dash
from dash import dcc
from dash import html
from components import *

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

# This is for gunicorn
server = app.server

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
