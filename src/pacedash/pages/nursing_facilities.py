import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import utilization, card_value
from ..settings import color_palette

from ..layouts import (
    card_col,
    utilization_header,
    left_number_right_spark,
    top_number_bottom_spark,
)

layout = html.Div(
    [
        Row(utilization_header("Nursing Facilities"), className="header-row"),
        Row(
            [
                card_col(
                    card_title="Custodial per 100MM",
                    card_val_id="card-1-nfs",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Respite per 100MM",
                    card_val_id="card-2-nfs",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Skilled per 100MM",
                    card_val_id="card-3-nfs",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="ALF per 100MM",
                    card_val_id="card-4-nfs",
                    color=color_palette[1],
                    size=3,
                ),
            ],
            className="first-row",
        ),
        Row(
            [
                card_col(
                    card_title="Custodial Admissions",
                    card_val_id="card-5-nfs",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Respite Admissions",
                    card_val_id="card-6-nfs",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Skilled Admissions",
                    card_val_id="card-7-nfs",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Custodial ALOS",
                    card_val_id="card-8-nfs",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Respite ALOS",
                    card_val_id="card-9-nfs",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Skilled ALOS",
                    card_val_id="card-10-nfs",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
            ],
            className="second-row",
        ),
        Row(
            [
                card_col(
                    card_title="Custodial Days",
                    card_val_id="card-11-nfs",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Respite Days",
                    card_val_id="card-12-nfs",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Skilled Days",
                    card_val_id="card-13-nfs",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Custodial(%)",
                    card_val_id="card-14-nfs",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="ALF(%)",
                    card_val_id="card-15-nfs",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Discharged to Higher LOC(%)",
                    card_val_id="card-16-nfs",
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


@app.callback(Output("card-1-nfs", "children"), [Input("time_range", "value")])
def card_val_1_nursing_facilities(time_range):
    return card_value(time_range, utilization.ppts_in_utl_per_100MM, "utilization", "custodial_per_100MM", top_number_bottom_spark, ["custodial"])

@app.callback(Output("card-2-nfs", "children"), [Input("time_range", "value")])
def card_val_2_nursing_facilities(time_range):
    return card_value(time_range, utilization.ppts_in_utl_per_100MM, "utilization", "respite_per_100MM", top_number_bottom_spark, ["respite"])

@app.callback(Output("card-3-nfs", "children"), [Input("time_range", "value")])
def card_val_3_nursing_facilities(time_range):
    return card_value(time_range, utilization.ppts_in_utl_per_100MM, "utilization", "skilled_per_100MM", top_number_bottom_spark, ["skilled"])

@app.callback(Output("card-4-nfs", "children"), [Input("time_range", "value")])
def card_val_4_nursing_facilities(time_range):
    return card_value(time_range, utilization.ppts_in_utl_per_100MM, "utilization", "alfs_per_100MM", top_number_bottom_spark, ["alfs"])

@app.callback(Output("card-5-nfs", "children"), [Input("time_range", "value")])
def card_val_5_nursing_facilities(time_range):
    return card_value(time_range, utilization.admissions_count, "utilization", "custodial_admissions", left_number_right_spark, ["custodial"])

@app.callback(Output("card-6-nfs", "children"), [Input("time_range", "value")])
def card_val_6_nursing_facilities(time_range):
    return card_value(time_range, utilization.admissions_count, "utilization", "respite_admissions", left_number_right_spark, ["respite"])

@app.callback(Output("card-7-nfs", "children"), [Input("time_range", "value")])
def card_val_7_nursing_facilities(time_range):
    return card_value(time_range, utilization.admissions_count, "utilization", "skilled_admissions", left_number_right_spark, ["skilled"])

@app.callback(Output("card-8-nfs", "children"), [Input("time_range", "value")])
def card_val_8_nursing_facilities(time_range):
    return card_value(time_range, utilization.alos, "utilization", "custodial_alos", left_number_right_spark, ["custodial"])

@app.callback(Output("card-9-nfs", "children"), [Input("time_range", "value")])
def card_val_9_nursing_facilities(time_range):
    return card_value(time_range, utilization.alos, "utilization", "respite_alos", left_number_right_spark, ["respite"])

@app.callback(Output("card-10-nfs", "children"), [Input("time_range", "value")])
def card_val_10_nursing_facilities(time_range):
    return card_value(time_range, utilization.alos, "utilization", "skilled_alos", left_number_right_spark, ["skilled"])

@app.callback(Output("card-11-nfs", "children"), [Input("time_range", "value")])
def card_val_11_nursing_facilities(time_range):
    return card_value(time_range, utilization.utilization_days, "utilization", "custodial_days", top_number_bottom_spark, ["custodial"])

@app.callback(Output("card-12-nfs", "children"), [Input("time_range", "value")])
def card_val_12_nursing_facilities(time_range):
    return card_value(time_range, utilization.utilization_days, "utilization", "respite_days", top_number_bottom_spark, ["respite"])

@app.callback(Output("card-13-nfs", "children"), [Input("time_range", "value")])
def card_val_13_nursing_facilities(time_range):
    return card_value(time_range, utilization.utilization_days, "utilization", "skilled_days", top_number_bottom_spark, ["skilled"])

@app.callback(Output("card-14-nfs", "children"), [Input("time_range", "value")])
def card_val_14_nursing_facilities(time_range):
    return card_value(time_range, utilization.ppts_in_utl_percent, "utilization", "custodial_percent", top_number_bottom_spark, ["custodial"])

@app.callback(Output("card-15-nfs", "children"), [Input("time_range", "value")])
def card_val_15_nursing_facilities(time_range):
    return card_value(time_range, utilization.ppts_in_utl_percent, "utilization", "alfs_percent", top_number_bottom_spark, ["alfs"])

@app.callback(Output("card-16-nfs", "children"), [Input("time_range", "value")])
def card_val_16_nursing_facilities(time_range):
    return card_value(time_range, utilization.percent_nf_discharged_to_higher_loc, "utilization", "nf_higher_loc_discharge_percent", top_number_bottom_spark)