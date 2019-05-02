import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row, Card

from ..helpers_configs import card_num_style, color_palette
from ..layouts import (
    center_team_dropdown_col,
    select_date_col,
    data_drop_with_graph_radios,
    three_graph_row,
    card_col,
)
from ..demographic_utils import (
    graph_types,
    chart_functions,
    dx_rate,
    avg_age,
    avg_years_enrolled,
    attnd_day_center,
    non_english_percent,
    non_white_percent,
    dual_enrolled_percent,
    pneumo_vacc_rate,
    influ_vacc_rate,
    demographic_attribute_options,
)


layout = html.Div(
    [
        Row(
            [
                center_team_dropdown_col(),
                select_date_col(),
                data_drop_with_graph_radios(
                    "graph-one-drop-demo",
                    demographic_attribute_options,
                    "age",
                    "graph-one-type",
                    "age_dist",
                ),
                data_drop_with_graph_radios(
                    "graph-two-drop-demo",
                    demographic_attribute_options,
                    "gender",
                    "graph-two-type",
                    "gen_dist",
                ),
                data_drop_with_graph_radios(
                    "graph-three-drop-demo",
                    demographic_attribute_options,
                    "race",
                    "graph-three-type",
                    "race_bar",
                ),
            ],
            className="options-row",
        ),
        three_graph_row("graph-one-demo", "graph-two-demo", "graph-three-demo"),
        Row(
            [
                card_col("Avg. Age", "avg-age-card", color_palette[3]),
                card_col("Avg. PACE Yrs", "avg-years-enrolled-card", color_palette[3]),
                card_col("Attending DC", "attnd-dc-card", color_palette[3]),
                card_col("% Non-English", "non-eng-card", color_palette[3]),
                card_col("% Non-White", "non-white-card", color_palette[3]),
                card_col("% Dual", "dual-card", color_palette[3]),
            ],
            className="demo-row",
            
        ),
        Row(
            [
                card_col("Acuity", "acuity-card", color_palette[1]),
                card_col("% Dementia Dx", "dementia-card", color_palette[1]),
                card_col("% BH Dx", "bh-card", color_palette[1]),
                card_col("Pneumo Vac.", "pneumo-card", color_palette[1]),
                card_col("Flu Vac.", "influ-card", color_palette[1]),
                Col(
                    [
                        html.H5(
                            [
                                dcc.Link(html.H4("Map of Ppts "), href="/map"),
                                "\n",
                                dcc.Link(html.H4("Ppts by Town"), href="/town_count"),
                            ]
                        )
                    ],
                    bp="md",
                    size=2,
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "center",
                        "align-items": "center",
                        "margin-top": "0.5vh",
                    },
                ),
            ],
            className="bottom-row",
            style={"height": "11.5vh", "margin-top": "0.5vh"},
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
    Output("graph-three-type", "options"), [Input("graph-three-drop-demo", "value")]
)
def update_graph_three_type(attr):
    """
    Updates graph display option in a radio based on
    demographic attribute selected by the user
    """
    return graph_types[attr]


@app.callback(
    Output("graph-three-type", "value"), [Input("graph-three-type", "options")]
)
def update_graph_three_type_val(available_options):
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
    Updates middle graph based on user selected options
    """
    return chart_functions[graph_type](start_date, end_date, center)


@app.callback(
    Output("graph-three-demo", "figure"),
    [
        Input("graph-three-type", "value"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_graph_three_demos(graph_type, start_date, end_date, center):
    """
    Updates right graph based on user selected options
    """
    return chart_functions[graph_type](start_date, end_date, center)


@app.callback(
    Output("avg-age-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def avg_age_card(start_date, end_date, center):
    """
    Updates average age card based on user selected options
    """
    return avg_age(start_date, end_date, center)


@app.callback(
    Output("avg-years-enrolled-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def avg_years_enrolled_card(start_date, end_date, center):
    """
    Updates average years enrolled card based on user selected options
    """
    return avg_years_enrolled(start_date, end_date, center)


@app.callback(
    Output("attnd-dc-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def attnd_day_card(start_date, end_date, center):
    """
    Updates participants attending the day center
    card based on user selected options
    """
    return attnd_day_center(start_date, end_date, center)


@app.callback(
    Output("non-eng-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def non_english_card(start_date, end_date, center):
    """
    Updates the percent of participants who do not
    speak english as thier primary language
    card based on user selected options
    """
    return non_english_percent(start_date, end_date, center)


@app.callback(
    Output("non-white-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def non_white_card(start_date, end_date, center):
    """
    Updates the percent of participants who are not
    white/Caucasian card based on user selected options
    """
    return non_white_percent(start_date, end_date, center)


@app.callback(
    Output("dual-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def dual_enrolled_card(start_date, end_date, center):
    """
    Updates the percent of participants with both
    Medicare and Medicaid card based on user selected options
    """
    return dual_enrolled_percent(start_date, end_date, center)


@app.callback(Output("acuity-card", "children"), [Input("end_date", "values")])
def acuity_card(end_date):
    """
    Updates the average acuity of participants
    card based on user selected options
    """
    return "WIP"


@app.callback(
    Output("dementia-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def dementia_card(start_date, end_date, center):
    """
    Updates the percent of participants with a dementia
    related dx card based on user selected options
    """
    return dx_rate("dementia", start_date, end_date, center)


@app.callback(
    Output("bh-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def bhdx_card(start_date, end_date, center):
    """
    Updates the percent of participants with a behavioral
    health related dx card based on user selected options
    """
    return dx_rate("bh", start_date, end_date, center)


@app.callback(
    Output("pneumo-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def pneumo_card(start_date, end_date, center):
    """
    Updates the pneumococcal vaccination rate
    based on user selected options
    """
    return pneumo_vacc_rate(start_date, end_date, center)


@app.callback(
    Output("influ-card", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def influ_card(start_date, end_date, center):
    """
    Updates the influenza vaccination rate
    based on user selected options
    """
    return influ_vacc_rate(start_date, end_date, center)
