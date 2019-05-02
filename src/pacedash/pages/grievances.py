import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from ..app import app
from ..components import Col, Row
from ..helpers_configs import dropdown_style, color_palette, update_dates
from ..layouts import (
    center_team_dropdown_col,
    select_date_col,
    month_quarter_radio,
    equal_graph_row,
    small_trend_graph,
    card_col,
)

from ..griev_utils import (
    build_grievance_graphs,
    trend_graph,
    grievance_dropdown_options,
    total_grievances,
    grievances_pmpm,
    most_common_griev_cat,
)

layout = html.Div(
    [
        Row(
            [
                center_team_dropdown_col(),
                select_date_col(),
                Col(
                    [
                        dcc.Dropdown(
                            id="griev-one-drop",
                            options=grievance_dropdown_options,
                            value="category",
                            style=dropdown_style,
                        ),
                        Row([html.P("")]),
                    ],
                    bp="md",
                    size=3,
                    style={
                        "padding-top": "0.5vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "flex-start",
                        "align-content": "flex-start",
                    },
                ),
                Col(
                    [
                        dcc.Dropdown(
                            id="griev-two-drop",
                            options=grievance_dropdown_options,
                            value="providers",
                            style=dropdown_style,
                        ),
                        Row([html.P("")]),
                    ],
                    bp="md",
                    size=3,
                    style={
                        "padding-top": "0.5vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "flex-start",
                        "align-content": "flex-start",
                    },
                ),
                Col([], size=1),
                Col(
                    [month_quarter_radio()],
                    bp="md",
                    size=2,
                    style={
                        "padding-left": 0,
                        "display": "flex",
                        "justify-content": "flex-end",
                        "align-content": "flex-end",
                    },
                ),
            ],
            className="options-row",
        ),
        equal_graph_row("griev-graph-one", "griev-graph-two"),
        Row(
            [
                small_trend_graph("griev-trend-graph"),
                card_col("Total", "total_griev-card", color_palette[3]),
                card_col("Per 100MM", "griev_per_100", color_palette[1]),
                card_col("Most Common", "common-griev-card", color_palette[3]),
            ],
            className="bottom-row",
        ),
    ]
)


@app.callback(
    Output("griev-graph-one", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("griev-one-drop", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph_one(start_date, end_date, freq, col_group, center):
    """
    Updates left graph based on dates, center, and
    grouping drop down choices
    """
    return build_grievance_graphs(start_date, end_date, freq, col_group, center)


@app.callback(
    Output("griev-graph-two", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("griev-two-drop", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph_two(start_date, end_date, freq, col_group, center):
    """
    Updates right graph based on dates, center, and
    grouping drop down choices
    """
    return build_grievance_graphs(start_date, end_date, freq, col_group, center)


@app.callback(
    Output("griev-trend-graph", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph_trending(start_date, end_date, freq, center):
    """
    Updates trend graph in bottom row based on dates, center,
    and freq
    """
    return trend_graph(start_date, end_date, freq, center)


@app.callback(
    Output("total_griev-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_griev_total_card(start_date, end_date, center):
    """
    Updates the total grievances number
    based on user selected options
    """
    return total_grievances(start_date, end_date, center)


@app.callback(
    Output("griev_per_100", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_griev_100_card(start_date, end_date, center):
    """
    Updates the grievances per 100 member months
    based on user selected options
    """
    return grievances_pmpm(start_date, end_date, center)


@app.callback(
    Output("common-griev-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_common_griev_card(start_date, end_date, center):
    """
    Updates the most common girevance area
    based on user selected options
    """
    return most_common_griev_cat(start_date, end_date, center)
