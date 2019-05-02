import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helpers_configs import dropdown_style, color_palette, update_dates
from ..layouts import (
    center_team_dropdown_col,
    select_date_col,
    month_quarter_radio,
    graph_drop_with_filter_amnt,
    equal_graph_row,
    small_trend_graph,
    card_col,
)
from ..incidents_utils import (
    drop_downs,
    total_incidents,
    incidents_per100mm,
    update_graph,
    card_three_title,
    repeat_ppts,
    percent_without_incident,
    update_trending_graph,
    incident_details_options,
    incident_types_dropdown,
    create_card_three,
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
                            id="incident-drop",
                            options=incident_types_dropdown,
                            value="falls",
                            style=dropdown_style,
                        ),
                        Row(
                            [
                                Col(
                                    [
                                        dcc.RadioItems(
                                            id="measure-radio",
                                            options=[
                                                {"label": "Total", "value": "total"},
                                                {"label": "Per100", "value": "pmpm"},
                                            ],
                                            value="total",
                                        )
                                    ],
                                    bp="md",
                                    size=6,
                                    mobile_size=6,
                                    style={
                                        "padding-right": 0,
                                        "display": "flex",
                                        "flex-direction": "column",
                                        "justify-content": "center",
                                    },
                                ),
                                Col(
                                    [month_quarter_radio()],
                                    bp="md",
                                    size=6,
                                    mobile_size=6,
                                    style={
                                        "padding-left": 0,
                                        "display": "flex",
                                        "flex-direction": "column",
                                        "justify-content": "center",
                                    },
                                ),
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
                    "graph-one-drop", "location", "graph-one-radio", "incident-options"
                ),
                graph_drop_with_filter_amnt(
                    "graph-two-drop",
                    "activity_at_time_of_fall",
                    "graph-two-radio",
                    "incident-options-two",
                ),
            ],
            className="options-row",
        ),
        equal_graph_row("graph-one", "graph-two"),
        Row(
            [
                small_trend_graph("incident-trending-graph"),
                Col(
                    [
                        Row(
                            [
                                card_col(
                                    "Total",
                                    "total-card",
                                    color_palette[3],
                                    size=4,
                                    height="100%",
                                ),
                                card_col(
                                    "Per 100MM",
                                    "pmpm-card",
                                    color_palette[3],
                                    size=4,
                                    height="100%",
                                ),
                                card_col(
                                    "",
                                    "level-2-card",
                                    color_palette[3],
                                    size=4,
                                    title_id="level-2-card-title",
                                    height="100%",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                        Row(
                            [
                                card_col(
                                    "Repeat Ppts",
                                    "repeat-ppts-card",
                                    color_palette[1],
                                    size=4,
                                    height="100%",
                                ),
                                card_col(
                                    "% No Incidents",
                                    "without-incident-card",
                                    color_palette[1],
                                    size=4,
                                    height="100%",
                                ),
                                Col(
                                    [
                                        dcc.RadioItems(
                                            id="outlier-radio",
                                            options=[
                                                {"label": "All", "value": False},
                                                {
                                                    "label": "Exclude Outliers",
                                                    "value": True,
                                                },
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
                                    size=4,
                                    mobile_size=4,
                                    style={
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "justify-content": "center",
                                        "align-items": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                                "align-items": "center",
                                "margin-top": "1vh",
                            },
                        ),
                    ],
                    size=6,
                ),
            ],
            className="bottom-row",
        ),
    ]
)


@app.callback(Output("graph-one-drop", "options"), [Input("incident-drop", "value")])
def graph_one_dd_options(selected_incident):
    """
    Returns dropdown options that
    can be used to group the data
    based on the indicent type
    """
    return [
        {"label": i.replace("_", " ").title(), "value": i}
        for i in drop_downs[selected_incident]
    ]


@app.callback(Output("graph-one-drop", "value"), [Input("graph-one-drop", "options")])
def graph_one_dd_value(available_options):
    """
    Returns the default value for the selected
    drop down grouping option
    """
    return available_options[0]["value"]


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
    Retuns a dictionary of additional incident options if there
    are more options than the selected amount to be plotted
    """
    start_date, end_date = update_dates(start_date, end_date, "Q")

    return incident_details_options(
        start_date, end_date, selected_incident, selected_cols, amount, center
    )


@app.callback(Output("incident-options", "value"), [Input("graph-one-drop", "value")])
def incident_one_value(arg):
    """
    Retuns None for additional incident options when graph option dropdown is changed
    """

    return None


@app.callback(
    Output("incident-options-two", "options"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("incident-drop", "value"),
        Input("graph-two-drop", "value"),
        Input("graph-two-radio", "value"),
        Input("center-drop", "value"),
    ],
)
def incident_two_details(
    start_date, end_date, selected_incident, selected_cols, amount, center
):
    """
    Retuns a dictionary of additional incident options if there
    are more options than the selected amount to be plotted
    """
    start_date, end_date = update_dates(start_date, end_date, "Q")
    return incident_details_options(
        start_date, end_date, selected_incident, selected_cols, amount, center
    )


@app.callback(
    Output("incident-options-two", "value"), [Input("graph-two-drop", "value")]
)
def incident_two_value(arg):
    """
    Retuns None for additional incident options when graph option dropdown is changed
    """

    return None


@app.callback(Output("graph-two-drop", "options"), [Input("incident-drop", "value")])
def graph_two_dd_options(selected_incident):
    """
    Returns dropdown options that
    can be used to group the data
    based on the indicent type
    """
    return [
        {"label": i.replace("_", " ").title(), "value": i}
        for i in drop_downs[selected_incident]
    ]


@app.callback(Output("graph-two-drop", "value"), [Input("graph-two-drop", "options")])
def graph_two_dd_value(available_options):
    """
    Returns the default value for the selected
    drop down grouping option
    """
    return available_options[1]["value"]


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


@app.callback(
    Output("graph-two", "figure"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("graph-two-drop", "value"),
        Input("incident-options-two", "value"),
        Input("graph-two-radio", "value"),
        Input("center-drop", "value"),
        Input("outlier-radio", "value"),
    ],
)
def update_graph_two(
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
    Updates right graph based on dates, selected incident, and
    grouping drop down choices
    """
    start_date, end_date = update_dates(start_date, end_date, freq)
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


@app.callback(
    Output("incident-trending-graph", "figure"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
        Input("measure-radio", "value"),
        Input("center-drop", "value"),
        Input("outlier-radio", "value"),
    ],
)
def update_graph_trending(
    incident, start_date, end_date, freq, measure, center, remove_outliers
):
    """
    Updates trend graph in bottom row based on dates, selected incident,
    freq and total vs pmpm choices
    """
    start_date, end_date = update_dates(start_date, end_date, freq)
    return update_trending_graph(
        incident, start_date, end_date, freq, measure, center, remove_outliers
    )


@app.callback(
    Output("total-card", "children"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
        Input("outlier-radio", "value"),
    ],
)
def update_total_card(selected_incident, start_date, end_date, center, remove_outliers):
    """
    Updates total incidents card value based on user choices
    """
    return total_incidents(
        selected_incident, start_date, end_date, center, remove_outliers
    )


@app.callback(
    Output("pmpm-card", "children"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
        Input("outlier-radio", "value"),
    ],
)
def update_pmpm_card(selected_incident, start_date, end_date, center, remove_outliers):
    """
    Updates incidents per member per month card value based on user choices
    """
    return incidents_per100mm(
        selected_incident, start_date, end_date, center, remove_outliers
    )


@app.callback(
    Output("level-2-card-title", "children"), [Input("incident-drop", "value")]
)
def card3_name(selected_incident):
    """
    Updates last card in row title based on selected incident
    """
    return card_three_title[selected_incident]


@app.callback(
    Output("level-2-card", "children"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_level2_card(incident, start_date, end_date, center):
    """
    Updates last card in row value based on user choices
    """
    return create_card_three(incident, start_date, end_date, center)


@app.callback(
    Output("repeat-ppts-card", "children"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_repeat_card(selected_incident, start_date, end_date, center):
    """
    Updates ppts with multiple incidents card
    based on user choices
    """
    repeats, percent_by_repeaters, outlier, outlier_num = repeat_ppts(
        selected_incident, start_date, end_date, center
    )
    return f"{repeats} / {percent_by_repeaters}% / {outlier}({int(outlier_num)}+)"


@app.callback(
    Output("without-incident-card", "children"),
    [
        Input("incident-drop", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_no_incident_card(selected_incident, start_date, end_date, center):
    """
    Updates ppts without an incident card
    based on user choices
    """
    return (
        f"{percent_without_incident(selected_incident, start_date, end_date, center)}%"
    )

