import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ..app import app
from ..components import Row, Col
from ..town_table_utils import enrollment_by_town_table

import pandas as pd


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
                        dcc.Input(
                            id="start_date",
                            type="text",
                            size=13,
                            value=(
                                pd.to_datetime("today") - pd.DateOffset(years=1)
                            ).strftime("%m/%d/%Y"),
                            style={
                                "text-align": "center",
                                "width": "100%",
                                "min-height": "3vh",
                                "border-color": "#ccc",
                                "border-style": "solid",
                                "border-width": "1px",
                                "border-radius": "4px",
                            },
                        ),
                        dcc.Input(
                            id="end_date",
                            type="text",
                            size=13,
                            value=pd.to_datetime("today").strftime("%m/%d/%Y"),
                            style={
                                "text-align": "center",
                                "width": "100%",
                                "min-height": "3vh",
                                "border-color": "#ccc",
                                "border-style": "solid",
                                "border-width": "1px",
                                "border-radius": "4px",
                            },
                        ),
                        dcc.Interval(
                            id="interval-component",
                            interval=12 * 60 * 60 * 1000,  # in milliseconds
                            n_intervals=0,
                        ),
                    ],
                    bp="md",
                    size=2,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "flex-start",
                        "margin-bottom": "2vh",
                    },
                ),
                Col(
                    id="town-table",
                    size=10,
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


@app.callback(
    Output("town-table", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_town_table(start_date, end_date, center):
    """
    Updates table of the count of participants
    from each city/town based on user choices
    """
    return enrollment_by_town_table(start_date, end_date, center)
