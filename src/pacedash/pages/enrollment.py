import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import enrollment, card_value, agg
from ..settings import color_palette

from ..layouts import (
    card_col,
    indicator_header,
    left_number_right_spark,
    top_number_bottom_spark,
)

layout = html.Div(
    [
        Row(indicator_header("Enrollment"), className="header-row"),
        Row(
            [
                card_col(
                    card_title="Census",
                    card_val_id="card-1-enrollment",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Enrolled",
                    card_val_id="card-2-enrollment",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Disenrolled",
                    card_val_id="card-3-enrollment",
                    color=color_palette[1],
                    size=3,
                ),
                card_col(
                    card_title="Net Enrollment",
                    card_val_id="card-4-enrollment",
                    color=color_palette[1],
                    size=3,
                ),
            ],
            className="first-row",
        ),
        Row(
            [
                card_col(
                    card_title="Voluntary Disenrollments(%)",
                    card_val_id="card-5-enrollment",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Inquiries",
                    card_val_id="card-6-enrollment",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Avg. Days to Enrollment",
                    card_val_id="card-7-enrollment",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="180 Day Conversion Rate",
                    card_val_id="card-8-enrollment",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Growth",
                    card_val_id="card-9-enrollment",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Churn",
                    card_val_id="card-10-enrollment",
                    color=color_palette[3],
                    font_size="1.25vmax",
                ),
            ],
            className="second-row",
        ),
        Row(
            [
                card_col(
                    card_title="Avg. Attendance PVD",
                    card_val_id="card-11-enrollment",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Avg. Attendance WOO",
                    card_val_id="card-12-enrollment",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Avg. Attendance WES",
                    card_val_id="card-13-enrollment",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Cancellation Rate PVD",
                    card_val_id="card-14-enrollment",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Cancellation Rate WOO",
                    card_val_id="card-15-enrollment",
                    color=color_palette[1],
                    font_size="1.25vmax",
                ),
                card_col(
                    card_title="Cancellation Rate WES",
                    card_val_id="card-16-enrollment",
                    color=color_palette[1],
                    font_size="1.25vmax",
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

@app.callback(Output("card-1-enrollment", "children"), [Input("time_range", "value")])
def card_val_1_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.census_on_end_date,
        "enrollment",
        "census",
        top_number_bottom_spark,
    )


@app.callback(Output("card-2-enrollment", "children"), [Input("time_range", "value")])
def card_val_2_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.enrolled,
        "enrollment",
        "enrolled",
        top_number_bottom_spark,
    )


@app.callback(Output("card-3-enrollment", "children"), [Input("time_range", "value")])
def card_val_3_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.disenrolled,
        "enrollment",
        "disenrolled",
        top_number_bottom_spark,
    )


@app.callback(Output("card-4-enrollment", "children"), [Input("time_range", "value")])
def card_val_4_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.net_enrollment,
        "enrollment",
        "net_enrollment",
        top_number_bottom_spark,
    )


@app.callback(Output("card-5-enrollment", "children"), [Input("time_range", "value")])
def card_val_5_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.voluntary_disenrolled_percent,
        "enrollment",
        "voluntary_disenrolled",
        left_number_right_spark,
    )


@app.callback(Output("card-6-enrollment", "children"), [Input("time_range", "value")])
def card_val_6_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.inquiries,
        "enrollment",
        "inquiries",
        left_number_right_spark,
    )


@app.callback(Output("card-7-enrollment", "children"), [Input("time_range", "value")])
def card_val_7_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.avg_days_to_enrollment,
        "enrollment",
        "avg_days_to_enrollment",
        left_number_right_spark,
    )


@app.callback(Output("card-8-enrollment", "children"), [Input("time_range", "value")])
def card_val_8_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.conversion_rate_180_days,
        "enrollment",
        "conversion_rate_180_days",
        left_number_right_spark,
    )


@app.callback(Output("card-9-enrollment", "children"), [Input("time_range", "value")])
def card_val_9_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.growth_rate,
        "enrollment",
        "growth_rate",
        left_number_right_spark,
    )


@app.callback(Output("card-10-enrollment", "children"), [Input("time_range", "value")])
def card_val_10_enrollment(time_range):
    return card_value(
        time_range,
        enrollment.churn_rate,
        "enrollment",
        "churn_rate",
        left_number_right_spark,
    )


@app.callback(Output("card-11-enrollment", "children"), [Input("time_range", "value")])
def card_val_11_enrollment(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "pvd_actual_census",
        left_number_right_spark,
        ["pvd_actual_census", "center_enrollment"],
    )


@app.callback(Output("card-12-enrollment", "children"), [Input("time_range", "value")])
def card_val_12_enrollment(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "woon_actual_census",
        left_number_right_spark,
        ["woon_actual_census", "center_enrollment"],
    )


@app.callback(Output("card-13-enrollment", "children"), [Input("time_range", "value")])
def card_val_13_enrollment(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "wes_actual_census",
        left_number_right_spark,
        ["wes_actual_census", "center_enrollment"],
    )


@app.callback(Output("card-14-enrollment", "children"), [Input("time_range", "value")])
def card_val_14_enrollment(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "pvd_pace_cancelation_rate",
        left_number_right_spark,
        ["pvd_pace_cancelation_rate", "center_enrollment"],
    )


@app.callback(Output("card-15-enrollment", "children"), [Input("time_range", "value")])
def card_val_15_enrollment(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "woon_pace_cancelation_rate",
        left_number_right_spark,
        ["woon_pace_cancelation_rate", "center_enrollment"],
    )


@app.callback(Output("card-16-enrollment", "children"), [Input("time_range", "value")])
def card_val_16_enrollment(time_range):
    return card_value(
        time_range,
        avg_agg_column,
        "center_enrollment",
        "wes_pace_cancelation_rate",
        left_number_right_spark,
        ["wes_pace_cancelation_rate", "center_enrollment"],
    )
