import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ..app import app
from ..components import Col, Row
from ..settings import dropdown_style
from ..enrollment_eda_utils import get_census, graph_choice

from ..layouts import (
    center_dropdown_col,
    select_date_col,
    small_clear_card,
    month_quarter_radio,
    graph_row,
)

layout = html.Div(
    [
        Row(
            [
                center_dropdown_col(),
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
                            options=[
                                {"label": "Census", "value": "enroll"},
                                {"label": "Enrollment Changes", "value": "changes"},
                                {"label": "Conversions", "value": "conv"},
                                {
                                    "label": "Voluntary Disenrollment Reasons",
                                    "value": "disenroll",
                                },
                                {
                                    "label": "Avg. Time Until Disenrollment",
                                    "value": "avg_time",
                                },
                            ],
                            value="enroll",
                            searchable=False,
                            style=dropdown_style,
                        )
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
                        "align-content": "center",
                    },
                ),
            ],
            className="options-row",
        ),
        graph_row("trend-graph"),
        Row(
            [
                Col(
                    [
                        Col(
                            [
                                dcc.Link(
                                    html.H6("Demo. EDA", style={"font-size": "1vmax"}),
                                    href="/demographics-eda",
                                )
                            ],
                            size=2,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                            },
                        ),
                        Col(
                            [
                                dcc.Link(
                                    html.H6(
                                        "Enroll. EDA", style={"font-size": "1vmax"}
                                    ),
                                    href="/enrollment-eda",
                                )
                            ],
                            size=2,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                            },
                        ),
                        Col(
                            [
                                dcc.Link(
                                    html.H6(
                                        "Incidents EDA", style={"font-size": "1vmax"}
                                    ),
                                    href="/incidents-eda",
                                )
                            ],
                            size=2,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                            },
                        ),
                        Col(
                            [
                                dcc.Link(
                                    html.H6("Utl. EDA", style={"font-size": "1vmax"}),
                                    href="/utilization-eda",
                                )
                            ],
                            size=2,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                            },
                        ),
                        Col(
                            [
                                dcc.Link(
                                    html.H6("Town Table", style={"font-size": "1vmax"}),
                                    href="/town_count",
                                )
                            ],
                            size=2,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                            },
                        ),
                    ],
                    size=6,
                    mobile_size=12,
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "center",
                        "align-items": "flex-end",
                    },
                )
            ],
            style={
                "margin-top": "0.5vh",
                "height": "4vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "flex-end",
                "align-items": "flex-end",
            },
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
    """Updates graph based on user selected options"""
    return graph_choice[graph](start_date, end_date, freq, center)
