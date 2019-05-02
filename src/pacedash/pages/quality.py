import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from ..app import app
from ..components import Col, Row
from ..helpers_configs import (
    card_num_style,
    graph_config,
    create_daterange
)
from ..quality_utils import quality_table, qapi_table

layout = html.Div(
    [
        Row(
            [
                Col(
                    [
                        dcc.Dropdown(
                            id="center-drop",
                            options=[
                                {"label": "All Centers", "value": "all"},
                                {"label": "Providence", "value": "Providence"},
                                {"label": "Westerly", "value": "Westerly"},
                                {"label": "Woonsocket", "value": "Woonsocket"},
                            ],
                            value="all",
                            searchable=False,
                        ),
                        dcc.Dropdown(
                            id="team-drop",
                            options=[
                                {"label": "All Teams", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "South", "value": "south"},
                                {"label": "East", "value": "east"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            placeholder="Select a team",
                            searchable=False,
                        ),
                        dcc.Link(
                            html.H5("Grievances"),
                            href="/grievances",
                            style={'margin-top': '2vh',
                                   'margin-left': '0.5vw', 'width': '35%'}
                        ),
                        dcc.Link(
                            html.H5("Incidents"),
                            href="/incidents",
                            style={'margin-left': '0.5vw', 'width': '35%'}

                        ),
                        dcc.Link(
                            html.H5("Utilization"),
                            href="/utilization",
                            style={'margin-left': '0.5vw', 'width': '35%'}
                        )
                    ],
                    bp="md",
                    size=2, mobile_size=12,
                    style={
                        "margin-top": "1vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "flex-start",
                    },
                ),
                Col([
                    Row([Col([html.H1('Quality Measures')],
                             size=12, mobile_size=12,
                             style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "flex-start",
                        "align-items": "flex-start",
                    })]),

                    Row([Col(id="quality-table",
                             size=12, mobile_size=12,
                             style={
                                 "display": "flex",
                                 "flex-direction": "column",
                                 "justify-content": "center",
                                 "align-items": "flex-start",
                             })]),
                    Row([Col([html.H1('QAPI 2019 Measures')],
                             size=12, mobile_size=12,
                             style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "flex-start",
                    })]),
                    Row([Col(id="quality-table2",
                             size=12, mobile_size=12,
                             style={
                                 "display": "flex",
                                 "flex-direction": "column",
                                 "justify-content": "center",
                                 "align-items": "flex-start",
                             })])],
                    size=10, mobile_size=12,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "flex-start",
                },
                ),
            ],
            style={
                "margin-top": "4vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
            },
        )
    ]
)


@app.callback(Output("quality-table", "children"),
              [Input("center-drop", "value")])
def update_quality_table(center):
    """
    Updates quality table when the center dropdown is used
    """
    return quality_table(center)


@app.callback(Output("quality-table2", "children"),
              [Input("center-drop", "value")])
def update_qapi_table(center):
    """
    Updates QAPI table when the center dropdown is used
    """
    return qapi_table(center)
