import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sqlite3
from ..app import app
from ..components import Col, Row
from ..helpers_configs import db_filepath, dropdown_style, color_palette, update_dates
from ..layouts import (
    center_team_dropdown_col,
    select_date_col,
    month_quarter_radio,
    equal_graph_row,
    small_trend_graph,
    card_col
)
from ..utilization_utils import (
    filter_cols, filter_cols_snf,
    additional_filter_options, additional_filter_options_snf,
    update_visit_graph, update_los_graph,
    update_readmit_graph, card_titles,
    admits_discharges, er_to_inp, snf_days,
    los_per_100mm, readmits_30_day, all_readmits, alos,
    utilization_table_types
)

layout = (
    html.Div(
        [
            Row(
                [
                    center_team_dropdown_col(),
                    select_date_col(),
                    Col(
                        [
                            dcc.Dropdown(
                                id="utl-filter",
                                value=None,
                                searchable=True,
                                style=dropdown_style
                            ),
                            Row(
                                [
                                    Col(
                                        [
                                            dcc.Dropdown(
                                                id="data-source",
                                                options=utilization_table_types,
                                                value="inpatient",
                                                searchable=False,
                                                clearable=False,
                                                style=dropdown_style
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
                                                    {"label": "Top 5",
                                                        "value": "5"},
                                                    {"label": "10", "value": "10"},
                                                    {"label": "All",
                                                        "value": "all"},
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
                                id="filter-values",
                                style=dropdown_style
                            ),
                            dcc.Dropdown(
                                id="additional-filter",
                                style=dropdown_style
                            )
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
                            dcc.RadioItems(
                                id="date-radio",
                                options=[
                                    {"label": "Admissions",
                                        "value": "admission_date"},
                                    {"label": "Discharges",
                                        "value": "discharge_date"},
                                ],
                                value="admission_date",
                            )
                        ],
                        bp="md",
                        size=2, mobile_size=6,
                        style={
                            "padding-top": "0.5vh",
                            "display": "flex",
                            "flex-direction": "row",
                            "justify-content": "flex-end",
                        },
                    ),
                    Col(
                        [
                            month_quarter_radio()
                        ],
                        bp="md",
                        size=2, mobile_size=6,
                        style={
                            "padding-top": "0.5vh",
                            "display": "flex",
                            "flex-direction": "row",
                            "justify-content": "flex-start",
                        },
                    ),
                ],
                className='options-row'
            ),
            equal_graph_row('visit-graph', 'los-graph'),

            Row(
                [
                    small_trend_graph('readmit-graph'),
                    Col(
                        [
                            Row(
                                [
                                    card_col('', 'utl-card-1',
                                             color_palette[3], size=4,
                                             title_id='utl-card-1-title', height='100%'),
                                    card_col('', 'utl-card-2',
                                             color_palette[3], size=4,
                                             title_id='utl-card-2-title', height='100%'),
                                    card_col('', 'utl-card-3',
                                             color_palette[3], size=4,
                                             title_id='utl-card-3-title', height='100%')
                                ], style = {
                                    'display':'flex',
                                    'flex-direction': 'row',
                                    'justify-content': 'center',
                                    'align-items': 'center'
                                    }
                            ),
                            Row(
                                [
                                    card_col('30 Day Readmit', 'utl-card-4',
                                             color_palette[1], size=4, height='100%'),
                                    card_col('', 'utl-card-5',
                                             color_palette[1], size=4,
                                             title_id='utl-card-5-title', height='100%'),
                                    card_col('', 'utl-card-6',
                                             color_palette[1], size=4,
                                             title_id='utl-card-6-title', height='100%')
                                ], style = {
                                    'display':'flex',
                                    'flex-direction': 'row',
                                    'justify-content': 'center',
                                    'align-items': 'center',
                                    'margin-top': '1vh'
                                    }
                            ),
                        ], size = 6
                    ),
                ],
                className = 'bottom-row'
            ),
        ]
    )
)

@app.callback(
    Output("utl-filter", "options"),
    [Input('data-source', 'value')]
)
def return_col_filters(data_source):
    """
    Returns dropdown of columns that
    can be used to filter the table
    based on the utlization type
    """
    if data_source != 'inpatient_snf':
        return filter_cols
    return filter_cols_snf

@app.callback(
    Output("utl-filter", "value"),
    [Input('data-source', 'value')]
)
def return_col_value(arg):
    """
    Set additional filter value to none when data source is changed
    """
    return None

@app.callback(Output("filter-values", "options"), [Input("utl-filter", "value"), Input('data-source', 'value')])
def update_filter_options(selected_filter, data_source):
    """
    Returns the values in the selected column
    to be used to filter the table.
    """
    if selected_filter != None:

        if data_source == 'inpatient_psych':
            data_source = 'inpatient'

        if data_source == 'er':
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
            return [{"label": 'Yes', "value": val[0]} if val[0] == 1.0 else {"label": 'No', "value": val[0]} for val in results]

        else:
            return [
                {"label": val[0], "value": val[0]}
                for val in results if val[0] != None]

    return [{}]


@app.callback(Output("filter-values", "value"), [Input("utl-filter", "value")])
def update_filter_value(arg):
    """Sets filter default value to None"""
    return None


@app.callback(Output("additional-filter", "options"), [Input("filter-values", "options"), Input('data-source', 'value')])
def update_additional_options(selected_filter, data_source):
    """
    Sets options to further filter the data
    """
    if (selected_filter != [{}]) & (data_source != 'inpatient_snf'):
        filter_labels = [val['label'] for val in selected_filter]
        return [val for val  in additional_filter_options if val['label'] not in filter_labels]
    if (selected_filter != 'admit_reason') & (data_source == 'inpatient_snf'):
        return additional_filter_options_snf
    return [{}]


@app.callback(Output("additional-filter", "value"), [Input("utl-filter", "value")])
def update_additional_value(arg):
    """Sets additional filter default value to None"""
    return None


@app.callback(
    Output("visit-graph", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("date-radio", "value"),
        Input("utl-filter", "value"),
        Input("utl-filter-amnt", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def visit_graph(start_date, end_date, utl_type, date_type, filter_col, amnt, freq, center, *additional_filters):
    """Updates visits graph, left of the two equal graphs in the second row
    based on user selected options"""
    start_date, end_date = update_dates(start_date, end_date, freq)
    return update_visit_graph(start_date, end_date, utl_type, date_type,
                              filter_col, amnt, freq, center, *additional_filters)


@app.callback(
    Output("los-graph", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("utl-filter-amnt", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def los_graph(start_date, end_date, utl_type, filter_col, amnt, freq, center, *additional_filters):
    """Updates average los graph, right of the two equal graphs in the second row
    based on user selected options"""
    start_date, end_date = update_dates(start_date, end_date, freq)
    return update_los_graph(start_date, end_date, utl_type, filter_col, amnt, freq, center, *additional_filters)


@app.callback(
    Output("readmit-graph", "figure"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("utl-filter-amnt", "value"),
        Input("freq-radio", "value"),
        Input("center-drop", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def readmit_graph(start_date, end_date, utl_type, filter_col, amnt, freq, center, *additional_filters):
    """Updates readmit graph, located in bottom row based on user selected options"""
    start_date, end_date = update_dates(start_date, end_date, freq)
    return update_readmit_graph(start_date, end_date, utl_type, filter_col, amnt, freq, center, *additional_filters)


# cards are numbered from left to right, starting in the top row of cards
# callbacks below update the title cards based on utilization type
# card 4 title does not change, always 30-Day Readmit

@app.callback(Output("utl-card-1-title", "children"), [Input("data-source", "value")])
def update_card1_title(utl_type):
    return card_titles[1][utl_type]


@app.callback(Output("utl-card-2-title", "children"), [Input("data-source", "value")])
def update_card2_title(utl_type):
    return card_titles[2][utl_type]


@app.callback(Output("utl-card-3-title", "children"), [Input("data-source", "value")])
def update_card3_title(utl_type):
    return card_titles[3][utl_type]


@app.callback(Output("utl-card-5-title", "children"), [Input("data-source", "value")])
def update_card5_title(utl_type):
    return card_titles[5][utl_type]


@app.callback(Output("utl-card-6-title", "children"), [Input("data-source", "value")])
def update_card6_title(utl_type):
    return card_titles[6][utl_type]

# callbacks below update cards values based on utilization type


@app.callback(
    Output("utl-card-1", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("center-drop", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def update_card1(start_date, end_date, utl_type, filter_col, center, col_filter, additional_filter):
    """
    Updates left card in first card row based on utilization type and user choices
    """
    return admits_discharges(utl_type, 'admission_date', center, start_date, end_date, filter_col, col_filter, additional_filter)


@app.callback(
    Output("utl-card-2", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("center-drop", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def update_card2(start_date, end_date, utl_type, filter_col, center, col_filter, additional_filter):
    """
    Updates middle card in first card row based on utilization type and user choices
    """
    if utl_type == 'er':
        return er_to_inp(center, start_date, end_date, filter_col, col_filter, additional_filter)
    if utl_type == 'er_only':
        total_er = admits_discharges(
            'er', "admission_date", center, start_date, end_date, filter_col, col_filter, additional_filter)
        er_only = admits_discharges('er_only', "admission_date", center,
                                    start_date, end_date, filter_col, col_filter, additional_filter)
                        
        return f"{round(er_only/total_er*100, 2)}%"

    return admits_discharges(utl_type, "discharge_date", center, start_date, end_date, filter_col, col_filter, additional_filter)


@app.callback(
    Output("utl-card-3", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("center-drop", "value"),
        Input("utl-card-1", "children"),
        Input("utl-card-2", "children"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def update_card3(
    start_date, end_date, utl_type, filter_col, center, er_visits, er_inp, col_filter, additional_filter
):
    """
    Updates right card in first card row based on utilization type and user choices
    """
    if utl_type == 'er':
        if er_inp is None:
            er_inp = 0
        if (er_visits == 0) | (er_inp =='N/A'):
            return "N/A"
        return f"{round(er_inp / (er_visits)*100, 2)}%"
    if utl_type == 'er_only':
        return 'WIP'
    if utl_type == "inpatient_snf":
        return snf_days(center, start_date, end_date, filter_col, col_filter, 'Custodial')

    return los_per_100mm(utl_type, center, start_date, end_date, filter_col, col_filter, additional_filter)


@app.callback(
    Output("utl-card-4", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("center-drop", "value"),
        Input("utl-card-1", "children"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def update_card4(start_date, end_date, utl_type, filter_col, center, admits, col_filter, additional_filter):
    """
    Updates left card in second card row based on utilization type and user choices
    """
    percent, total = readmits_30_day(
        utl_type, admits, center, start_date, end_date, filter_col, col_filter, additional_filter)
    return f"{percent}% ({total})"


@app.callback(
    Output("utl-card-5", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("center-drop", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def update_card5(start_date, end_date, utl_type, filter_col, center, col_filter, additional_filter):
    """
    Updates middle card in second card row based on utilization type and user choices
    """
    if utl_type == "inpatient_snf":
        return snf_days(center, start_date, end_date, filter_col, col_filter, 'Skilled')
    return all_readmits(utl_type, center, start_date, end_date, filter_col, col_filter, additional_filter)


@app.callback(
    Output("utl-card-6", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("data-source", "value"),
        Input("utl-filter", "value"),
        Input("center-drop", "value"),
        Input("filter-values", "value"),
        Input("additional-filter", "value")
    ],
)
def update_card6(start_date, end_date, utl_type, filter_col, center, col_filter, additional_filter):
    """
    Updates right card in second card row based on utilization type and user choices
    """
    if utl_type == "inpatient_snf":
        return snf_days(center, start_date, end_date, filter_col, col_filter, 'Respite')
    return alos(utl_type, center, start_date, end_date, filter_col, col_filter, additional_filter)
