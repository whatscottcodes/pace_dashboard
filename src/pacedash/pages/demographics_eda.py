import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row

from ..layouts import (
    center_dropdown_col,
    select_date_col,
    data_drop_with_graph_radios,
    equal_graph_row,
)
from ..demographics_eda_utils import (
    graph_types,
    chart_functions,
    demographic_attribute_options,
)


layout = html.Div(
    [
        Row(
            [
                data_drop_with_graph_radios(
                    "graph-one-drop-demo",
                    demographic_attribute_options,
                    "age",
                    "graph-one-type",
                    "age_dist",
                ),
                center_dropdown_col(),
                select_date_col(),
                data_drop_with_graph_radios(
                    "graph-two-drop-demo",
                    demographic_attribute_options,
                    "gender",
                    "graph-two-type",
                    "gen_dist",
                ),
            ],
            className="options-row",
        ),
        equal_graph_row("graph-one-demo", "graph-two-demo"),
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
                "height": "6vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "flex-end",
                "align-items": "flex-end",
            },
        ),
    ]
)


@app.callback(
    Output("graph-one-type", "options"), [Input("graph-one-drop-demo", "value")]
)
def update_graph_one_type(attr):
    """
    Updates graph display option in a radio based on
    demographic attribute selected by the user
    """
    return graph_types[attr]


@app.callback(Output("graph-one-type", "value"), [Input("graph-one-type", "options")])
def update_graph_one_type_val(available_options):
    """
    Updates default value in a radio based on
    demographic attribute selected by the user
    """
    return available_options[0]["value"]


@app.callback(
    Output("graph-two-type", "options"), [Input("graph-two-drop-demo", "value")]
)
def update_graph_two_type(attr):
    """
    Updates graph display option in a radio based on
    demographic attribute selected by the user
    """
    return graph_types[attr]


@app.callback(Output("graph-two-type", "value"), [Input("graph-two-type", "options")])
def update_graph_two_type_val(available_options):
    """
    Updates default value in a radio based on
    demographic attribute selected by the user
    """
    return available_options[0]["value"]


@app.callback(
    Output("graph-one-demo", "figure"),
    [
        Input("graph-one-type", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph_one_demos(graph_type, start_date, end_date, center):
    """
    Updates left graph based on user selected options
    """
    return chart_functions[graph_type](start_date, end_date, center)


@app.callback(
    Output("graph-two-demo", "figure"),
    [
        Input("graph-two-type", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph_two_demos(graph_type, start_date, end_date, center):
    """
    Updates right graph based on user selected options
    """
    return chart_functions[graph_type](start_date, end_date, center)
