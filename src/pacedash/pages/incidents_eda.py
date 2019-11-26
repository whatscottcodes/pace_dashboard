import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import update_dates
from ..settings import dropdown_style

from ..layouts import (
    center_dropdown_col,
    select_date_col,
    month_quarter_radio,
    graph_drop_with_filter_amnt,
    graph_row,
)
from ..incidents_eda_utils import (
    drop_downs,
    update_graph,
    update_trending_graph,
    incident_details_options,
    incident_types_dropdown,
)

layout = html.Div(
    [
        Row(
            [
                center_dropdown_col(),
                select_date_col(),
                Col(
                    [
                        dcc.Dropdown(
                            id="incident-drop",
                            options=incident_types_dropdown,
                            value="falls",
                            style=dropdown_style,
                        ),
                        Row(
                            [
                                Col(
                                    [month_quarter_radio()],
                                    bp="md",
                                    size=6,
                                    mobile_size=6,
                                    style={
                                        "display": "flex",
                                        "flex-direction": "column",
                                        "justify-content": "center",
                                    },
                                )
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "flex-start",
                                "align-items": "center",
                            },
                        ),
                    ],
                    bp="md",
                    size=3,
                    style={
                        "padding-top": "0.5vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                    },
                ),
                graph_drop_with_filter_amnt(
                    "graph-one-drop", None, "graph-one-radio", "incident-options"
                ),
                Col(
                    [
                        dcc.RadioItems(
                            id="outlier-radio",
                            options=[
                                {"label": "All", "value": False},
                                {"label": "Exclude Outliers", "value": True},
                            ],
                            value=False,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "flex-end",
                                "align-items": "center",
                            },
                        )
                    ],
                    bp="md",
                    size=3,
                    mobile_size=4,
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                ),
            ],
            className="options-row",
        ),
        graph_row("graph-one"),
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


@app.callback(Output("graph-one-drop", "options"), [Input("incident-drop", "value")])
def graph_one_dd_options(selected_incident):
    """
    Returns dropdown options that
    can be used to group the data
    based on the incident type
    """

    return [
        {"label": i.replace("_", " ").title(), "value": i}
        for i in drop_downs[selected_incident]
    ]


@app.callback(
    Output("incident-options", "options"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("incident-drop", "value"),
        Input("graph-one-drop", "value"),
        Input("graph-one-radio", "value"),
        Input("center-drop", "value"),
    ],
)
def incident_one_details(
    start_date, end_date, selected_incident, selected_cols, amount, center
):
    """
    Returns a dictionary of additional incident options if there
    are more options than the selected amount to be plotted
    """
    start_date, end_date = update_dates(start_date, end_date, "Q")
    if selected_cols is None:
        return [{"label": None, "value": None}]
    return incident_details_options(
        start_date, end_date, selected_incident, selected_cols, amount, center
    )


@app.callback(Output("incident-options", "value"), [Input("graph-one-drop", "value")])
def incident_one_value(arg):
    """
    Returns None for additional incident options when graph option dropdown is changed
    """

    return None


@app.callback(
    Output("graph-one", "figure"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("graph-one-drop", "value"),
        Input("incident-options", "value"),
        Input("graph-one-radio", "value"),
        Input("center-drop", "value"),
        Input("outlier-radio", "value"),
    ],
)
def update_graph_one(
    incident,
    start_date,
    end_date,
    freq,
    cols,
    incident_details,
    amount,
    center,
    remove_outliers,
):
    """
    Updates left graph based on dates, selected incident, and
    grouping drop down choices
    """
    start_date, end_date = update_dates(start_date, end_date, freq)

    if cols is None:
        measure = "pmpm"
        return update_trending_graph(
            incident, start_date, end_date, freq, measure, center, remove_outliers
        )

    return update_graph(
        incident,
        start_date,
        end_date,
        freq,
        cols,
        incident_details,
        amount,
        center,
        remove_outliers,
    )
