import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import (
    enrollment,
    demographics,
    quality,
    card_value
)
from ..settings import color_palette
from ..layouts import (
    card_col,
    indicator_header,
    left_number_right_spark,
    top_number_bottom_spark,
)


layout = html.Div(
    [
        Row(indicator_header("Demographics"), className="header-row"),
        Row(
            [
                card_col(
                    card_title="Avg. Age",
                    card_val_id="card-1-demographics",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Avg. Years Enrolled",
                    card_val_id="card-2-demographics",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Living in the Community(%)",
                    card_val_id="card-3-demographics",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Below 65 Years Old(%)",
                    card_val_id="card-4-demographics",
                    color=color_palette[1],
                    size=3,
                ),
            ],
            className="first-row",
        ),
        Row(
            [
                card_col(
                    card_title="Non-English(%)",
                    card_val_id="card-5-demographics",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Non-White(%)",
                    card_val_id="card-6-demographics",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Female(%)",
                    card_val_id="card-7-demographics",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Dual(%)",
                    card_val_id="card-8-demographics",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Medicaid Only(%)",
                    card_val_id="card-9-demographics",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Private Pay(%)",
                    card_val_id="card-10-demographics",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
            ],
            className="second-row",
        ),
        Row(
            [
                card_col(
                    card_title="BH Diagnosis(%)",
                    card_val_id="card-11-demographics",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="6+ Chronic Conditions(%)",
                    card_val_id="card-12-demographics",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Pneumo. Rate",
                    card_val_id="card-13-demographics",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Influenza Rate",
                    card_val_id="card-14-demographics",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Avg. Days Until NF Admit",
                    card_val_id="card-15-demographics",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="No Hosp. Last Year(%)",
                    card_val_id="card-16-demographics",
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


@app.callback(Output("card-1-demographics", "children"), [Input("time_range", "value")])
def card_val_1_demographics(time_range):
    return card_value(
        time_range,
        demographics.avg_age,
        "demographics",
        "avg_age",
        top_number_bottom_spark,
    )


@app.callback(Output("card-2-demographics", "children"), [Input("time_range", "value")])
def card_val_2_demographics(time_range):
    return card_value(
        time_range,
        enrollment.avg_years_enrolled,
        "enrollment",
        "avg_years_enrolled",
        top_number_bottom_spark,
    )


@app.callback(Output("card-3-demographics", "children"), [Input("time_range", "value")])
def card_val_3_demographics(time_range):
    return card_value(
        time_range,
        demographics.living_in_community_percent,
        "demographics",
        "percent_living_in_community",
        top_number_bottom_spark,
    )


@app.callback(Output("card-4-demographics", "children"), [Input("time_range", "value")])
def card_val_4_demographics(time_range):
    return card_value(
        time_range,
        demographics.percent_age_below_65,
        "demographics",
        "percent_below_65",
        top_number_bottom_spark,
    )


@app.callback(Output("card-5-demographics", "children"), [Input("time_range", "value")])
def card_val_5_demographics(time_range):
    return card_value(
        time_range,
        demographics.percent_primary_non_english,
        "demographics",
        "percent_primary_non_english",
        left_number_right_spark,
    )


@app.callback(Output("card-6-demographics", "children"), [Input("time_range", "value")])
def card_val_6_demographics(time_range):
    return card_value(
        time_range,
        demographics.percent_non_white,
        "demographics",
        "percent_non_white",
        left_number_right_spark,
    )


@app.callback(Output("card-7-demographics", "children"), [Input("time_range", "value")])
def card_val_7_demographics(time_range):
    return card_value(
        time_range,
        demographics.percent_female,
        "demographics",
        "percent_female",
        left_number_right_spark,
    )


@app.callback(Output("card-8-demographics", "children"), [Input("time_range", "value")])
def card_val_8_demographics(time_range):
    return card_value(
        time_range,
        demographics.percent_dual,
        "demographics",
        "percent_dual_enrolled",
        left_number_right_spark,
    )


@app.callback(Output("card-9-demographics", "children"), [Input("time_range", "value")])
def card_val_9_demographics(time_range):
    return card_value(
        time_range,
        demographics.percent_medicaid_only,
        "demographics",
        "percent_medicaid_only",
        left_number_right_spark,
    )


@app.callback(
    Output("card-10-demographics", "children"), [Input("time_range", "value")]
)
def card_val_10_demographics(time_range):
    return card_value(
        time_range,
        demographics.percent_private_pay,
        "demographics",
        "percent_private_pay",
        left_number_right_spark,
    )


@app.callback(
    Output("card-11-demographics", "children"), [Input("time_range", "value")]
)
def card_val_11_demographics(time_range):
    return card_value(
        time_range,
        demographics.behavorial_dx_percent,
        "demographics",
        "bh_dx_percent",
        top_number_bottom_spark,
    )


@app.callback(
    Output("card-12-demographics", "children"), [Input("time_range", "value")]
)
def card_val_12_demographics(time_range):
    return card_value(
        time_range,
        demographics.over_six_chronic_conditions_percent,
        "demographics",
        "six_chronic_conditions",
        top_number_bottom_spark,
    )


@app.callback(
    Output("card-13-demographics", "children"), [Input("time_range", "value")]
)
def card_val_13_demographics(time_range):
    return card_value(
        time_range,
        quality.pneumo_rate,
        "quality",
        "pneumo_rate",
        top_number_bottom_spark,
    )


@app.callback(
    Output("card-14-demographics", "children"), [Input("time_range", "value")]
)
def card_val_14_demographics(time_range):
    return card_value(
        time_range, quality.influ_rate, "quality", "influ_rate", top_number_bottom_spark
    )


@app.callback(
    Output("card-15-demographics", "children"), [Input("time_range", "value")]
)
def card_val_15_demographics(time_range):
    return card_value(
        time_range,
        quality.avg_days_until_nf_admission,
        "quality",
        "avg_days_until_nf_admission",
        top_number_bottom_spark,
    )


@app.callback(
    Output("card-16-demographics", "children"), [Input("time_range", "value")]
)
def card_val_16_demographics(time_range):
    return card_value(
        time_range,
        quality.no_hosp_admission_last_year,
        "quality",
        "no_hosp_admission_last_year",
        top_number_bottom_spark,
    )

