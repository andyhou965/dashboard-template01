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
