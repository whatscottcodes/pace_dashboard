import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import (
    enrollment,
    demographics,
    incidents,
    utilization,
    agg,
    sparkline,
    arrow_direction,
    indicator_color,
    time_range_dict,
    card_value
)
from ..settings import color_palette
from ..layouts import (
    card_col,
    indicator_header,
    left_number_right_spark,
    text_val_no_sparkline
)

layout = html.Div(
    [
       Row(indicator_header("Incidents"), className="header-row"),
       Row([Col([
             html.H4("Falls",)
            ], size = 12, style = {"text-align": "left",
                                "justify-content": "center",
                                "flex-direction": "column",
                                "display": "flex"})], style={"margin-top":"1vmax", "margin-bottom":"0.5vmax"}),
        Row(
            [
                card_col(
                    card_title="Falls per 100MM",
                    card_val_id="card-1-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts with Fall",
                    card_val_id="card-2-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Falls by Repeaters(%)",
                    card_val_id="card-3-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts Without Fall(%)",
                    card_val_id="card-4-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Major Harm/Death",
                    card_val_id="card-5-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Fall per 100MM(adjusted)",
                    card_val_id="card-6-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
            ],
            className="equal-row", style={"border-bottom-style": "ridge"}
        ),
        Row([Col([
             html.H4("Infections",)
            ], size = 12, style = {"text-align": "left",
                                "justify-content": "center",
                                "flex-direction": "column",
                                "display": "flex"})], style={"margin-top":"1vmax", "margin-bottom":"0.5vmax"}),
        Row(
            [
                card_col(
                    card_title="Infections per 100MM",
                    card_val_id="card-7-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts with Infection",
                    card_val_id="card-8-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Infections by Repeaters(%)",
                    card_val_id="card-9-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts Without Infection(%)",
                    card_val_id="card-10-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Sepsis",
                    card_val_id="card-11-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="UTI per 100MM",
                    card_val_id="card-12-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
            ],
            className="equal-row", style={"border-bottom-style": "ridge"}
        ),
        Row([Col([
             html.H4("Medication Errors",)
            ], size = 12, style = {"text-align": "left",
                                "justify-content": "center",
                                "flex-direction": "column",
                                "display": "flex"})], style={"margin-top":"1vmax", "margin-bottom":"0.5vmax"}),
        Row(
            [
                card_col(
                    card_title="Med Errors per 100MM",
                    card_val_id="card-13-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts with Med Error",
                    card_val_id="card-14-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Most Common Responsibility",
                    card_val_id="card-15-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts Without Med Error(%)",
                    card_val_id="card-16-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Major Harm/Death",
                    card_val_id="card-17-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="High Risk Related",
                    card_val_id="card-18-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
            ],
            className="equal-row", style={"border-bottom-style": "ridge"}
        ),
        Row([Col([
             html.H4("Wounds",)
            ], size = 12, style = {"text-align": "left",
                                "justify-content": "center",
                                "flex-direction": "column",
                                "display": "flex"})], style={"margin-top":"1vmax", "margin-bottom":"0.5vmax"}),
        Row(
            [
                card_col(
                    card_title="Wounds per 100MM",
                    card_val_id="card-19-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts with Wound",
                    card_val_id="card-20-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Avg. Wound Healing Time",
                    card_val_id="card-21-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts Without Wound(%)",
                    card_val_id="card-22-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Unstageable",
                    card_val_id="card-23-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Pressure Ulcer per 100MM",
                    card_val_id="card-24-incidents",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
            ],
            className="equal-row", style={"border-bottom-style": "ridge"}
        ),
        Row([Col([
             html.H4("Burns",)
            ], size = 12, style = {"text-align": "left",
                                "justify-content": "center",
                                "flex-direction": "column",
                                "display": "flex"})], style={"margin-top":"1vmax", "margin-bottom":"0.5vmax"}),
        Row(
            [
                card_col(
                    card_title="Burns per 100MM",
                    card_val_id="card-25-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts with Burn",
                    card_val_id="card-26-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Burns by Repeaters(%)",
                    card_val_id="card-27-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Ppts Without Burn(%)",
                    card_val_id="card-28-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="3rd Degree+",
                    card_val_id="card-29-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="RN Assessment (%)",
                    card_val_id="card-30-incidents",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
            ],
            className="equal-row"
        ),
        Row(
            [
                Col(
                    [
                        Col(
                            [
                                dcc.Link(
                                    html.H6("Demo. EDA", style={
                                            "font-size": "1vmax"}),
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
                                    html.H6(
                                        "Utl. EDA", style={"font-size": "1vmax"}
                                    ),
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
                                    html.H6("Town Table", style={
                                            "font-size": "1vmax"}),
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
                "margin-top": "0",
                "height": "4vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "flex-end",
                "align-items": "flex-end",
            },
        ),
    ]
)


@app.callback(Output("card-1-incidents", "children"), [Input("time_range", "value")])
def card_val_1_incident(time_range):
    return card_value(time_range, incidents.incident_per_100MM, "falls", "per_100MM", left_number_right_spark, ["falls"])

@app.callback(Output("card-2-incidents", "children"), [Input("time_range", "value")])
def card_val_2_incident(time_range):
    return card_value(time_range, incidents.ppts_w_incident, "falls", "unique_ppts", left_number_right_spark, ["falls"])

@app.callback(Output("card-3-incidents", "children"), [Input("time_range", "value")])
def card_val_3_incident(time_range):
    return card_value(time_range, incidents.percent_by_repeaters, "falls", "percent_by_repeaters", left_number_right_spark, ["falls"])

@app.callback(Output("card-4-incidents", "children"), [Input("time_range", "value")])
def card_val_4_incident(time_range):
    return card_value(time_range, incidents.percent_without_incident_in_period, "falls", "percent_without", left_number_right_spark, ["falls"])

@app.callback(Output("card-5-incidents", "children"), [Input("time_range", "value")])
def card_val_5_incident(time_range):
    return card_value(time_range, incidents.major_harm_percent, "falls", "major_harm_percent", left_number_right_spark, ["falls"])

@app.callback(Output("card-6-incidents", "children"), [Input("time_range", "value")])
def card_val_6_incident(time_range):
    return card_value(time_range, incidents.adjusted_per_100MM, "falls", "adjusted_per100MM", left_number_right_spark, ["falls"])

@app.callback(Output("card-7-incidents", "children"), [Input("time_range", "value")])
def card_val_7_incident(time_range):
    return card_value(time_range, incidents.incident_per_100MM, "infections", "per_100MM", left_number_right_spark, ["infections"])

@app.callback(Output("card-8-incidents", "children"), [Input("time_range", "value")])
def card_val_8_incident(time_range):
    return card_value(time_range, incidents.ppts_w_incident, "infections", "unique_ppts", left_number_right_spark, ["infections"])

@app.callback(Output("card-9-incidents", "children"), [Input("time_range", "value")])
def card_val_9_incident(time_range):
    return card_value(time_range, incidents.percent_by_repeaters, "infections", "percent_by_repeaters", left_number_right_spark, ["infections"])

@app.callback(Output("card-10-incidents", "children"), [Input("time_range", "value")])
def card_val_10_incident(time_range):
    return card_value(time_range, incidents.percent_without_incident_in_period, "infections", "percent_without", left_number_right_spark, ["infections"])

@app.callback(Output("card-11-incidents", "children"), [Input("time_range", "value")])
def card_val_11_incident(time_range):
    return card_value(time_range, incidents.sepsis_per_100, "infections", "sepsis_per_100MM", left_number_right_spark)

@app.callback(Output("card-12-incidents", "children"), [Input("time_range", "value")])
def card_val_12_incident(time_range):
    return card_value(time_range, incidents.uti_per_100, "infections", "uti_per_100MM", left_number_right_spark)

@app.callback(Output("card-13-incidents", "children"), [Input("time_range", "value")])
def card_val_13_incident(time_range):
    return card_value(time_range, incidents.incident_per_100MM, "med_errors", "per_100MM", left_number_right_spark, ["med_errors"])

@app.callback(Output("card-14-incidents", "children"), [Input("time_range", "value")])
def card_val_14_incident(time_range):
    return card_value(time_range, incidents.ppts_w_incident, "med_errors", "unique_ppts", left_number_right_spark, ["med_errors"])

@app.callback(Output("card-15-incidents", "children"), [Input("time_range", "value")])
def card_val_15_incident(time_range):
    params = time_range_dict[time_range][0]()

    current_value = incidents.most_common_med_errors_responsibility(params)
    total = incidents.total_incidents(params, incident_table="med_errors")
    
    if total == 0:
        return text_val_no_sparkline(f"{current_value[0]}(0%)", "incidents-eda")
   
    percent = int(current_value[1]) /  total* 100

    return text_val_no_sparkline(f"{current_value[0]}({round(percent,2)}%)", "incidents-eda")

@app.callback(Output("card-16-incidents", "children"), [Input("time_range", "value")])
def card_val_16_incident(time_range):
    return card_value(time_range, incidents.percent_without_incident_in_period, "med_errors", "percent_without", left_number_right_spark, ["med_errors"])

@app.callback(Output("card-17-incidents", "children"), [Input("time_range", "value")])
def card_val_17_incident(time_range):
    return card_value(time_range, incidents.major_harm_percent, "med_errors", "major_harm_percent", left_number_right_spark, ["med_errors"])

@app.callback(Output("card-18-incidents", "children"), [Input("time_range", "value")])
def card_val_18_incident(time_range):
    return card_value(time_range, incidents.high_risk_med_error_count, "med_errors", "high_risk", left_number_right_spark)

@app.callback(Output("card-19-incidents", "children"), [Input("time_range", "value")])
def card_val_19_incident(time_range):
    return card_value(time_range, incidents.incident_per_100MM, "wounds", "per_100MM", left_number_right_spark, ["wounds"])

@app.callback(Output("card-20-incidents", "children"), [Input("time_range", "value")])
def card_val_20_incident(time_range):
    return card_value(time_range, incidents.ppts_w_incident, "wounds", "unique_ppts", left_number_right_spark, ["wounds"])

@app.callback(Output("card-21-incidents", "children"), [Input("time_range", "value")])
def card_val_21_incident(time_range):
    return card_value(time_range, incidents.avg_wound_healing_time, "wounds", "avg_healing_time", left_number_right_spark)

@app.callback(Output("card-22-incidents", "children"), [Input("time_range", "value")])
def card_val_22_incident(time_range):
    return card_value(time_range, incidents.percent_without_incident_in_period, "wounds", "percent_without", left_number_right_spark, ["wounds"])

@app.callback(Output("card-23-incidents", "children"), [Input("time_range", "value")])
def card_val_23_incident(time_range):
    return card_value(time_range, incidents.unstageable_wound_percent, "wounds", "percent_unstageable", left_number_right_spark)

@app.callback(Output("card-24-incidents", "children"), [Input("time_range", "value")])
def card_val_24_incident(time_range):
    return card_value(time_range, incidents.pressure_ulcer_per_100, "wounds", "pressure_ulcer_per_100", left_number_right_spark)

@app.callback(Output("card-25-incidents", "children"), [Input("time_range", "value")])
def card_val_25_incident(time_range):
    return card_value(time_range, incidents.incident_per_100MM, "burns", "per_100MM", left_number_right_spark, ["burns"])

@app.callback(Output("card-26-incidents", "children"), [Input("time_range", "value")])
def card_val_26_incident(time_range):
    return card_value(time_range, incidents.ppts_w_incident, "burns", "unique_ppts", left_number_right_spark, ["burns"])

@app.callback(Output("card-27-incidents", "children"), [Input("time_range", "value")])
def card_val_27_incident(time_range):
    return card_value(time_range, incidents.percent_by_repeaters, "burns", "percent_by_repeaters", left_number_right_spark, ["burns"])

@app.callback(Output("card-28-incidents", "children"), [Input("time_range", "value")])
def card_val_28_incident(time_range):
    return card_value(time_range, incidents.percent_without_incident_in_period, "burns", "percent_without", left_number_right_spark, ["burns"])

@app.callback(Output("card-29-incidents", "children"), [Input("time_range", "value")])
def card_val_29_incident(time_range):
    return card_value(time_range, incidents.third_degree_burn_rate, "burns", "third_degree_rate", left_number_right_spark)

@app.callback(Output("card-30-incidents", "children"), [Input("time_range", "value")])
def card_val_30_incident(time_range):
    return card_value(time_range, incidents.rn_assessment_following_burn_percent, "burns", "rn_assessment_percent", left_number_right_spark)
