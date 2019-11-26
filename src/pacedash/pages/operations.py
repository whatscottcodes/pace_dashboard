import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import (
    enrollment,
    center_enrollment,
    demographics,
    agg,
    card_value,
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
        Row(indicator_header("Operations"), className="header-row"),
        Row(
            [
                card_col(
                    card_title="Census",
                    card_val_id="card-1-ops",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Providence",
                    card_val_id="card-2-ops",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Woonsocket",
                    card_val_id="card-3-ops",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Westerly",
                    card_val_id="card-4-ops",
                    color=color_palette[1],
                    size=3,
                ),
            ],
            className="first-row",
        ),
        Row(
            [
                card_col(
                    card_title="Avg. Attendance PVD",
                    card_val_id="card-5-ops",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Avg. Attendance WOO",
                    card_val_id="card-6-ops",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Avg. Attendance WES",
                    card_val_id="card-7-ops",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Cancellation Rate PVD",
                    card_val_id="card-8-ops",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Cancellation Rate WOO",
                    card_val_id="card-9-ops",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Cancellation Rate WES",
                    card_val_id="card-10-ops",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
            ],
            className="second-row",
        ),
        Row(
            [
                card_col(
                    card_title="Attending Day Center(%)",
                    card_val_id="card-11-ops",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Rides by PACE(%)",
                    card_val_id="card-12-ops",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Staffing Ratio",
                    card_val_id="card-13-ops",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Staff Hours per DC Ppt",
                    card_val_id="card-14-ops",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Level 2 Events in DC",
                    card_val_id="card-15-ops",
                    color=color_palette[1],
                    font_size="2vmax",
                ),
                card_col(
                    card_title="Avg. Risk Score",
                    card_val_id="card-16-ops",
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


def avg_agg_column(params, col, table):
    """
    Helper function for finding the average of an aggregate column 

    Args:
        params(tuple): start date and end date in format 'YYYY-MM-DD'
        col(str): name of column to find average of
        table(str): name of table column is in

    Return:
        float: average of column during period
    """
    return agg.single_value_query(
        f"SELECT ROUND(AVG({col}), 2) FROM {table} WHERE month BETWEEN ? AND ?", params
    )


@app.callback(Output("card-1-ops", "children"), [Input("time_range", "value")])
def card_val_1_operations(time_range):
    return card_value(
        time_range,
        enrollment.census_during_period,
        "enrollment",
        "census",
        top_number_bottom_spark,
    )


@app.callback(Output("card-2-ops", "children"), [Input("time_range", "value")])
def card_val_2_operations(time_range):
    return card_value(
        time_range,
        center_enrollment.census_on_end_date,
        "center_enrollment",
        "pvd_census",
        top_number_bottom_spark,
        ["Providence"],
    )


@app.callback(Output("card-3-ops", "children"), [Input("time_range", "value")])
def card_val_3_operations(time_range):
    return card_value(
        time_range,
        center_enrollment.census_on_end_date,
        "center_enrollment",
        "woon_census",
        top_number_bottom_spark,
        ["Woonsocket"],
    )


@app.callback(Output("card-4-ops", "children"), [Input("time_range", "value")])
def card_val_4_operations(time_range):
    return card_value(
        time_range,
        center_enrollment.census_on_end_date,
        "center_enrollment",
        "wes_census",
        top_number_bottom_spark,
        ["Westerly"],
    )


@app.callback(Output("card-5-ops", "children"), [Input("time_range", "value")])
def card_val_5_operations(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "pvd_actual_census",
        left_number_right_spark,
        ["pvd_actual_census", "center_enrollment"],
    )


@app.callback(Output("card-6-ops", "children"), [Input("time_range", "value")])
def card_val_6_operations(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "woon_actual_census",
        left_number_right_spark,
        ["woon_actual_census", "center_enrollment"],
    )


@app.callback(Output("card-7-ops", "children"), [Input("time_range", "value")])
def card_val_7_operations(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "wes_actual_census",
        left_number_right_spark,
        ["wes_actual_census", "center_enrollment"],
    )


@app.callback(Output("card-8-ops", "children"), [Input("time_range", "value")])
def card_val_8_operations(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "pvd_pace_cancelation_rate",
        left_number_right_spark,
        ["pvd_pace_cancelation_rate", "center_enrollment"],
    )


@app.callback(Output("card-9-ops", "children"), [Input("time_range", "value")])
def card_val_9_operations(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "woon_pace_cancelation_rate",
        left_number_right_spark,
        ["woon_pace_cancelation_rate", "center_enrollment"],
    )


@app.callback(Output("card-10-ops", "children"), [Input("time_range", "value")])
def card_val_10_operations(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "wes_pace_cancelation_rate",
        left_number_right_spark,
        ["wes_pace_cancelation_rate", "center_enrollment"],
    )


@app.callback(Output("card-11-ops", "children"), [Input("time_range", "value")])
def card_val_11_operations(time_range):
    return card_value(
        time_range,
        demographics.percent_attending_dc,
        "demographics",
        "percent_attending_dc",
        top_number_bottom_spark,
    )


@app.callback(Output("card-12-ops", "children"), [Input("time_range", "value")])
def card_val_12_operations(time_range):
    return ""


@app.callback(Output("card-13-ops", "children"), [Input("time_range", "value")])
def card_val_13_operations(time_range):
    return ""


@app.callback(Output("card-14-ops", "children"), [Input("time_range", "value")])
def card_val_14_operations(time_range):
    return ""


@app.callback(Output("card-15-ops", "children"), [Input("time_range", "value")])
def card_val_15_operations(time_range):
    return ""


@app.callback(Output("card-16-ops", "children"), [Input("time_range", "value")])
def card_val_16_operations(time_range):
    return ""

