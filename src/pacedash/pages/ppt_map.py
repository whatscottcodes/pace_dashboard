import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from ..app import app
from ..components import Row
from ..helper_functions import enrollment
from ..settings import color_palette, graph_config

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
                    interval=604_800 * 1000,  # in milliseconds
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
    Updates participant map
    """
    mapbox_access_token = "pk.eyJ1Ijoic2NvdHRhdHBhY2UiLCJhIjoiY2pxODJ5Y2g3MDFleDN4dGxobnk0MzY1ayJ9.OwmFKDj12Z9m5PT4QVXWcg"

    enrolled_df, disenrolled_df = enrollment.address_mapping_df()

    fig_data = [
        go.Scattermapbox(
            lat=disenrolled_df.lat,
            lon=disenrolled_df.lon,
            mode="markers",
            name="Disenrolled",
            marker=dict(color=color_palette[0], size=10),
            line=dict(width=0),
            text=disenrolled_df.name + "<br>" + disenrolled_df.full_address,
            hoverinfo="text",
        ),
        go.Scattermapbox(
            lat=enrolled_df.lat,
            lon=enrolled_df.lon,
            mode="markers",
            name="Enrolled",
            marker=dict(color=color_palette[2], size=10),
            line=dict(width=0),
            text=enrolled_df.name + "<br>" + enrolled_df.full_address,
            hoverinfo="text",
        ),
    ]

    fig_layout = go.Layout(
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"pad": 5, "l": 50, "r": 55, "t": 35, "b": 35},
        hovermode="closest",
        showlegend=True,
        legend=dict(orientation="h", y=-0.015, traceorder="reversed"),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(lat=41.700, lon=-71.4128),
            pitch=0,
            zoom=8.75,
            style="streets",
        ),
        annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=1.035,
                x=0,
                text=f"<b>Map of Participants</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ],
    )
    return dict(data=fig_data, layout=fig_layout)

