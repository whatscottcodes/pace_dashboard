import sqlite3
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Col, Row
from ..helper_functions import db_filepath, update_dates
from ..settings import dropdown_style
from ..layouts import (
    center_dropdown_col,
    select_date_col,
    month_quarter_radio,
    equal_graph_row,
)
from ..utilization_eda_utils import (
    filter_cols,
    filter_cols_snf,
    additional_filter_options,
    update_visit_graph,
    update_los_graph,
    update_readmit_graph,
    utilization_table_types,
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
                            id="utl-filter",
                            value=None,
                            searchable=True,
                            style=dropdown_style,
                        ),
                        Row(
                            [
                                Col(
                                    [
                                        dcc.Dropdown(
                                            id="data-source",
                                            options=utilization_table_types,
                                            value="acute",
                                            searchable=False,
                                            clearable=False,
                                            style=dropdown_style,
                                        )
                                    ],
                                    bp="md",
                                    size=5,
                                    style={
                                        "padding-top": "0.5vh",
                                        "display": "flex",
                                        "flex-direction": "column",
                                        "justify-content": "center",
                                        "align-content": "center",
                                    },
                                ),
                                Col(
                                    [
                                        dcc.RadioItems(
                                            id="utl-filter-amnt",
                                            options=[
                                                {"label": "Top 5", "value": "5"},
                                                {"label": "10", "value": "10"},
                                                {"label": "All", "value": "all"},
                                            ],
                                            value="5",
                                        )
                                    ],
                                    bp="md",
                                    size=7,
                                    style={
                                        "padding-top": "0.5vh",
                                        "display": "flex",
                                        "flex-direction": "column",
                                        "justify-content": "center",
                                        "align-content": "center",
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
                Col(
                    [
                        dcc.Dropdown(
                            id="filter-values", style=dropdown_style, value=None
                        ),
                        dcc.Dropdown(
                            id="additional-filter", style=dropdown_style, value=None
                        ),
                    ],
                    bp="md",
                    size=2,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                    },
                ),
                Col(
                    [
                        dcc.Dropdown(
                            id="graph-one-stat",
                            options=[
                                {"label": "Admissions", "value": "admission_date"},
                                {"label": "Discharges", "value": "discharge_date"},
                                {"label": "ALOS", "value": "alos"},
                                {"label": "30-Day Readmits", "value": "30-day"},
                            ],
                            value="admission_date",
                            style=dropdown_style,
                        ),
                        dcc.Dropdown(
                            id="graph-two-stat",
                            options=[
                                {"label": "Admissions", "value": "admission_date"},
                                {"label": "Discharges", "value": "discharge_date"},
                                {"label": "ALOS", "value": "alos"},
                                {"label": "30-Day Readmits", "value": "30-day"},
                            ],
                            value="alos",
                            style=dropdown_style,
                        ),
                    ],
                    bp="md",
                    size=2,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                    },
                ),
                Col(
                    [month_quarter_radio()],
                    bp="md",
                    size=2,
                    mobile_size=6,
                    style={
                        "padding-top": "0.5vh",
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "flex-end",
                    },
                ),
            ],
            className="options-row",
        ),
        equal_graph_row("utl-graph-one", "utl-graph-two"),
        Row(
            [
                Col(
                    [
                        dcc.RadioItems(
                            id="graph_type",
                            options=[
                                {"label": "Bar", "value": "bar"},
                                {"label": "Line", "value": "line"},
                            ],
                            value="bar",
                        )
                    ],
                    bp="md",
                    size=6,
                    mobile_size=12,
                    style={
                        "padding-top": "0.5vh",
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "flex-start",
                    },
                ),
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
                                    html.H6("Enroll. EDA", style={"font-size": "1vmax"}),
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
                                    html.H6("Incidents EDA", style={"font-size": "1vmax"}),
                                    href="/incidents-eda"
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
                                    href="/utilization-eda"                                    
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
                        )
                    ],
                    size=6, mobile_size = 12,
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "center",
                        "align-items": "flex-end",
                    },
                )
            ],
            className="bottom-row",
        ),
    ]
)


@app.callback(Output("utl-filter", "options"), [Input("data-source", "value")])
def return_col_filters(data_source):
    """
    Returns dropdown of columns that
    can be used to filter the table
    based on the utilization type
    """
    if data_source not in ["custodial", "respite", "skilled"]:
        return filter_cols
    return filter_cols_snf


@app.callback(Output("utl-filter", "value"), [Input("data-source", "value")])
def return_col_value(arg):
    """
    Set additional filter value to none when data source is changed
    """
    return None


@app.callback(
    Output("filter-values", "options"),
    [Input("utl-filter", "value"), Input("data-source", "value")],
)
def update_filter_options(selected_filter, data_source):
    """
    Returns the values in the selected column
    to be used to filter the table.
    """
    if selected_filter != None:

        if data_source == "er":
            data_source = f"""(SELECT {selected_filter} FROM er_only
                UNION ALL
                SELECT {selected_filter} FROM inpatient
                WHERE inpatient.er = 1)"""

        conn = sqlite3.connect(db_filepath)
        c = conn.cursor()
        q = f"""SELECT DISTINCT({selected_filter})
        FROM {data_source}"""
        results = c.execute(q).fetchall()
        conn.close()

        if len(results) <= 3:
            results = [val for val in results if val[0] != None]
            return [
                {"label": "Yes", "value": val[0]}
                if val[0] == 1.0
                else {"label": "No", "value": val[0]}
                for val in results
            ]

        else:
            return [
                {"label": val[0], "value": val[0]} for val in results if val[0] != None
            ]

    return [{}]


@app.callback(Output("filter-values", "value"), [Input("utl-filter", "value")])
def update_filter_value(arg):
    """Sets filter default value to None"""
    return None


@app.callback(
    Output("additional-filter", "options"),
    [Input("filter-values", "options"), Input("data-source", "value")],
)
def update_additional_options(selected_filter, data_source):
    """
    Sets options to further filter the data
    """
    if (selected_filter != [{}]) & (data_source != "inpatient_snf"):
        filter_labels = [val["label"] for val in selected_filter]
        return [
            val
            for val in additional_filter_options
            if val["label"] not in filter_labels
        ]
    return [{}]


@app.callback(Output("additional-filter", "value"), [Input("utl-filter", "value")])
def update_additional_value(arg):
    """Sets additional filter default value to None"""
    return None


@app.callback(
    Output("utl-graph-one", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("graph-one-stat", "value"),
        Input("utl-filter", "value"),
        Input("utl-filter-amnt", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
        Input("graph_type", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value"),
    ],
)
def utl_graph_one(
    start_date,
    end_date,
    utl_type,
    graph_stat,
    filter_col,
    amnt,
    freq,
    center,
    graph_type,
    *additional_filters,
):
    """Updates visits graph, left of the two equal graphs in the second row
    based on user selected options"""
    start_date, end_date = update_dates(start_date, end_date, freq)
    if graph_stat == "admission_date":
        return update_visit_graph(
            start_date,
            end_date,
            utl_type,
            "admission_date",
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )
    if graph_stat == "discharge_date":
        return update_visit_graph(
            start_date,
            end_date,
            utl_type,
            "discharge_date",
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )
    if graph_stat == "alos":
        return update_los_graph(
            start_date,
            end_date,
            utl_type,
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )
    if graph_stat == "30-day":
        return update_readmit_graph(
            start_date,
            end_date,
            utl_type,
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )


@app.callback(
    Output("utl-graph-two", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("graph-two-stat", "value"),
        Input("utl-filter", "value"),
        Input("utl-filter-amnt", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
        Input("graph_type", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value"),
    ],
)
def utl_graph_two(
    start_date,
    end_date,
    utl_type,
    graph_stat,
    filter_col,
    amnt,
    freq,
    center,
    graph_type,
    *additional_filters,
):
    """Updates visits graph, left of the two equal graphs in the second row
    based on user selected options"""
    start_date, end_date = update_dates(start_date, end_date, freq)

    if graph_stat == "admission_date":
        return update_visit_graph(
            start_date,
            end_date,
            utl_type,
            "admission_date",
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )
    if graph_stat == "discharge_date":
        return update_visit_graph(
            start_date,
            end_date,
            utl_type,
            "discharge_date",
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )
    if graph_stat == "alos":
        return update_los_graph(
            start_date,
            end_date,
            utl_type,
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )
    if graph_stat == "30-day":
        return update_readmit_graph(
            start_date,
            end_date,
            utl_type,
            filter_col,
            amnt,
            freq,
            center,
            graph_type,
            *additional_filters,
        )

