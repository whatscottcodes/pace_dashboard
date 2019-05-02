import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Row
from ..helpers_configs import graph_config
from ..map_utils import ppts_address_map

mapbox_access_token = "pk.eyJ1Ijoic2NvdHRhdHBhY2UiLCJhIjoiY2pxODJ5Y2g3MDFleDN4dGxobnk0MzY1ayJ9.OwmFKDj12Z9m5PT4QVXWcg"

layout = html.Div(
    [
        Row(
            [
                dcc.Graph(
                    id="map-graph",
                    style={"height": "93vh", "width": "100vw"},
                    config=graph_config,
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=604800 * 1000,  # in milliseconds
                    n_intervals=0,
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "center",
                "align-content": "center",
            },
        )
    ]
)


@app.callback(
    Output("map-graph", "figure"), [Input("interval-component", "n_intervals")]
)
def update_map(n):
    """
    Updates participant map once a week
    """
    return ppts_address_map(mapbox_access_token)
