import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from ..app import app
from ..components import Col, Row
from ..helpers_configs import dropdown_style, color_palette
from ..census_utils import (
    enrollment_df,
    get_census,
    graph_choice,
    total_census,
    growth_rate,
    churn_rate,
    retention_graph,
    census_data_options,
)

from ..layouts import (
    card_num_style,
    center_team_dropdown_col,
    select_date_col,
    small_clear_card,
    month_quarter_radio,
    sixty_forty_graph_row,
    card_col,
    small_trend_graph,
)

layout = html.Div(
    [
        Row(
            [
                center_team_dropdown_col(),
                select_date_col(),
                Col(
                    [
                        Row(
                            [
                                small_clear_card("Census", get_census()),
                                small_clear_card(
                                    "Providence",
                                    get_census("AND center = 'Providence'"),
                                ),
                                small_clear_card(
                                    "Westerly", get_census("AND center = 'Westerly'")
                                ),
                                small_clear_card(
                                    "Woonsocket",
                                    get_census("AND center = 'Woonsocket'"),
                                ),
                            ],
                            style={
                                "flex-direction": "row",
                                "justify-content": "center",
                                "text-align": "center",
                                "align-items": "center",
                            },
                        )
                    ],
                    size=5,
                    mobile_size=12,
                    style={
                        "flex-direction": "row",
                        "justify-content": "center",
                        "text-align": "center",
                        "align-items": "center",
                    },
                ),
                Col(
                    [
                        dcc.Dropdown(
                            id="graph1-drop",
                            options=census_data_options,
                            value=census_data_options[0]["value"],
                            searchable=False,
                            style=dropdown_style,
                        ),
                        dcc.Dropdown(
                            id="graph2-drop",
                            options=census_data_options,
                            value=census_data_options[1]["value"],
                            searchable=False,
                            style=dropdown_style,
                        ),
                    ],
                    bp="md",
                    size=3,
                    mobile_size=6,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                    },
                ),
                Col(
                    [month_quarter_radio()],
                    bp="md",
                    size=1,
                    mobile_size=6,
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-content": "center"
                    },
                ),
            ],
            className="options-row",
        ),
        sixty_forty_graph_row("trend-graph", "bar-graph"),
        Row(
            [
                card_col("Total Census", "total_census", color_palette[3]),
                card_col("Growth", "growth", color_palette[1]),
                card_col("Churn", "churn", color_palette[3]),
                small_trend_graph("retention-graph"),
            ],
            className="bottom-row",
        ),
    ]
)


@app.callback(
    Output("trend-graph", "figure"),
    [
        Input("graph1-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph(graph, start_date, end_date, freq, center):
    """Updates larger left graph based on user selected options"""
    return graph_choice[graph](start_date, end_date, freq, center)


@app.callback(
    Output("bar-graph", "figure"),
    [
        Input("graph2-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph2(graph, start_date, end_date, freq, center):
    """Updates smaller right graph based on user selected options"""
    return graph_choice[graph](start_date, end_date, freq, center)


@app.callback(
    Output("total_census", "children"),
    [
        Input("center-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
    ],
)
def update_total_census(center, start_date, end_date):
    """
    Updates total census card value based on user choices
    """
    return total_census(center, start_date, end_date)


@app.callback(
    Output("growth", "children"),
    [
        Input("center-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
    ],
)
def growth_rate_card(center, start_date, end_date):
    """
    Updates growth rate card value based on user choices
    """
    # might want to make this a SQL queries
    df = enrollment_df(center, ["enrollment_date", "disenrollment_date"])
    return f"{round(growth_rate(df, start_date, end_date),2)}%"


@app.callback(
    Output("churn", "children"),
    [
        Input("center-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
    ],
)
def churn_rate_card(center, start_date, end_date):
    """
    Updates churn rate card value based on user choices
    """
    # might want to make this a SQL queries
    df = enrollment_df(center, ["enrollment_date", "disenrollment_date"])
    return f"{round(churn_rate(df, start_date, end_date),2)}%"


@app.callback(
    Output("growth", "style"),
    [
        Input("center-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("growth", "children"),
        Input("churn", "children"),
    ],
)
def update_growth_style(_, __, ___, growth, churn):
    """
    Updates color of gorwth card value based on user choices and 
    if the growth is greater than the churn
    """
    if float(growth[:-1]) > float(churn[:-1]):
        color = color_palette[0]
    else:
        color = "#FF4136"
    colored_num_style = card_num_style.copy()
    colored_num_style["color"] = color
    return colored_num_style


@app.callback(
    Output("retention-graph", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_retention_graph(start_date, end_date, center):
    """
    Updates sparkline type graph in bottom row with trending
    growth and churn based on user choices
    """
    return retention_graph(start_date, end_date, center)
