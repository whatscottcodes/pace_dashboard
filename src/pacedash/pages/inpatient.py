import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import utilization, quality, card_value
from ..settings import color_palette

from ..layouts import (
    card_col,
    utilization_header,
    left_number_right_spark,
    top_number_bottom_spark,
)

layout = html.Div(
    [
        Row(utilization_header("Inpatient"), className="header-row"),
        Row(
            [
                card_col(
                    card_title="Admissions per 100MM",
                    card_val_id="card-1-inpatient",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="ER Visits per 100MM",
                    card_val_id="card-2-inpatient",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="LOS per 100MM",
                    card_val_id="card-3-inpatient",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="30-Day Readmit Rate",
                    card_val_id="card-4-inpatient",
                    color=color_palette[1],
                    size=3,
                ),
            ],
            className="first-row",
        ),
        Row(
            [
                card_col(
                    card_title="Admissions",
                    card_val_id="card-5-inpatient",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Discharges",
                    card_val_id="card-6-inpatient",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="ER Visits",
                    card_val_id="card-7-inpatient",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Psych Admissions",
                    card_val_id="card-8-inpatient",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="ALOS",
                    card_val_id="card-9-inpatient",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Psych ALOS",
                    card_val_id="card-10-inpatient",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
            ],
            className="second-row",
        ),
        Row(
            [
                card_col(
                    card_title="Psych 30-Day Readmit Rate",
                    card_val_id="card-11-inpatient",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="ER 30-Day Revisit Rate",
                    card_val_id="card-12-inpatient",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="No Hosp. Since Enrolled(%)",
                    card_val_id="card-13-inpatient",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Ppts with Admission",
                    card_val_id="card-14-inpatient",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Weekend Utilization(%)",
                    card_val_id="card-15-inpatient",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Admitted from ER",
                    card_val_id="card-16-inpatient",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
            ],
            className="third-row",
        ),
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


@app.callback(Output("card-1-inpatient", "children"), [Input("time_range", "value")])
def card_val_1_inpatient(time_range):
    return card_value(
        time_range,
        utilization.admissions_per_100MM,
        "utilization",
        "acute_admissions_per_100MM",
        top_number_bottom_spark,
        ["acute"],
    )


@app.callback(Output("card-2-inpatient", "children"), [Input("time_range", "value")])
def card_val_2_inpatient(time_range):
    return card_value(
        time_range,
        utilization.admissions_per_100MM,
        "utilization",
        "er_visits_per_100MM",
        top_number_bottom_spark,
        ["er_only"],
    )


@app.callback(Output("card-3-inpatient", "children"), [Input("time_range", "value")])
def card_val_3_inpatient(time_range):
    return card_value(
        time_range,
        utilization.los_per_100mm,
        "utilization",
        "acute_los_per_100MM",
        top_number_bottom_spark,
        ["acute"],
    )


@app.callback(Output("card-4-inpatient", "children"), [Input("time_range", "value")])
def card_val_4_inpatient(time_range):
    return card_value(
        time_range,
        utilization.readmits_30day_rate,
        "utilization",
        "acute_30_day_readmit_rate",
        top_number_bottom_spark,
        ["acute"],
    )


@app.callback(Output("card-5-inpatient", "children"), [Input("time_range", "value")])
def card_val_5_inpatient(time_range):
    return card_value(
        time_range,
        utilization.admissions_count,
        "utilization",
        "acute_admissions",
        left_number_right_spark,
        ["acute"],
    )


@app.callback(Output("card-6-inpatient", "children"), [Input("time_range", "value")])
def card_val_6_inpatient(time_range):
    return card_value(
        time_range,
        utilization.discharges_count,
        "utilization",
        "acute_discharges",
        left_number_right_spark,
        ["acute"],
    )


@app.callback(Output("card-7-inpatient", "children"), [Input("time_range", "value")])
def card_val_7_inpatient(time_range):
    return card_value(
        time_range,
        utilization.admissions_count,
        "utilization",
        "er_visits",
        left_number_right_spark,
        ["er_only"],
    )


@app.callback(Output("card-8-inpatient", "children"), [Input("time_range", "value")])
def card_val_8_inpatient(time_range):
    return card_value(
        time_range,
        utilization.admissions_count,
        "utilization",
        "psych_admissions",
        left_number_right_spark,
        ["psych"],
    )


@app.callback(Output("card-9-inpatient", "children"), [Input("time_range", "value")])
def card_val_9_inpatient(time_range):
    return card_value(
        time_range,
        utilization.alos,
        "utilization",
        "acute_alos",
        left_number_right_spark,
        ["acute"],
    )


@app.callback(Output("card-10-inpatient", "children"), [Input("time_range", "value")])
def card_val_10_inpatient(time_range):
    return card_value(
        time_range,
        utilization.alos,
        "utilization",
        "psych_alos",
        left_number_right_spark,
        ["psych"],
    )


@app.callback(Output("card-11-inpatient", "children"), [Input("time_range", "value")])
def card_val_11_inpatient(time_range):
    return card_value(
        time_range,
        utilization.readmits_30day_rate,
        "utilization",
        "psych_30_day_readmit_rate",
        top_number_bottom_spark,
        ["psych"],
    )


@app.callback(Output("card-12-inpatient", "children"), [Input("time_range", "value")])
def card_val_12_inpatient(time_range):
    return card_value(
        time_range,
        utilization.readmits_30day_rate,
        "utilization",
        "er_only_30_day_readmit_rate",
        top_number_bottom_spark,
        ["er_only"],
    )


@app.callback(Output("card-13-inpatient", "children"), [Input("time_range", "value")])
def card_val_13_inpatient(time_range):
    return card_value(
        time_range,
        quality.no_hosp_admission_since_enrollment,
        "quality",
        "no_hosp_admission_since_enrollment",
        top_number_bottom_spark,
    )


@app.callback(Output("card-14-inpatient", "children"), [Input("time_range", "value")])
def card_val_14_inpatient(time_range):
    return card_value(
        time_range,
        utilization.unique_admissions_count,
        "utilization",
        "acute_unique_admissions",
        top_number_bottom_spark,
        ["acute"],
    )


@app.callback(Output("card-15-inpatient", "children"), [Input("time_range", "value")])
def card_val_15_inpatient(time_range):
    return card_value(
        time_range,
        utilization.weekend_admission_percent,
        "utilization",
        "acute_weekend_percent",
        top_number_bottom_spark,
        ["acute"],
    )


@app.callback(Output("card-16-inpatient", "children"), [Input("time_range", "value")])
def card_val_16_inpatient(time_range):
    return card_value(
        time_range,
        utilization.er_to_inp_rate,
        "utilization",
        "er_to_inp_rate",
        top_number_bottom_spark,
    )

