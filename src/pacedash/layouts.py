from flask import current_app as server
import dash_core_components as dcc
import dash_html_components as html
from .components import Col, Row, Header, Card, Fa
from .helper_functions import helpers
from .settings import graph_config, dropdown_style, color_palette

#headers
def main_layout_header():
    """
    Creates dash app layout with header
    Used as a default for this dash app
    """
    return html.Div(
        [
            html.Div(
                id="header",
                children=[Header(), html.Div(
                    id=server.config["NAVBAR_CONTAINER_ID"]), html.Div(id='logout')], style={'height': '6vh'}),
            html.Div(
                className="container-fluid",
                children=Row(Col(id=server.config["CONTENT_CONTAINER_ID"], size=12, style={'margin-top': '3vmin', 'margin-bottom': 0}))),
            dcc.Location(id="url", refresh=False),
        ]
    )

def indicator_header(title):
    """
    Bootstrap columns with a page title and time radio buttons
    for each indicator page

    Args:
        title(str): Page title
    
    Returns:
        list: list to be passed to a bootstrap row component
    """
    return [Col([
             html.H1(title, id='page-title')
            ], size = 8, style = {"text-align": "left",
                                "justify-content": "center",
                                "flex-direction": "column",
                                "display": "flex"}),
            Col([
            dcc.RadioItems(
                                id='time_range',
                                options=[
                                    {"label": "Month to Date", "value":"month_td"},
                                    {"label": "Last Month",
                                     "value": "last_month"},
                                    {"label": "Last Quarter", "value": "last_quarter"},
                                    {"label": "Quarter to Date", "value": "quarter_td"}
                                ],
                                value="month_td",
                            )
            ], size = 4, style = {"display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "align-items": 'flex-end'})]

def utilization_header(title):
    """
    Bootstrap columns with a page title and time radio buttons
    for utilization indicator page - adds links to other
    utilization pages not on nav bag

    Args:
        title(str): Page title
    
    Returns:
        list: list to be passed to a bootstrap row component
    """
    return [Col([
             html.H1(title, id='page-title')
            ], size = 5, style = {"text-align": "left",
                                "justify-content": "center",
                                "flex-direction": "column",
                                "display": "flex"}),
            Col(
                            [
                                dcc.Link(
                                    html.H6("Inpatient/ER", style={
                                            "font-size": "1vmax"}),
                                    href="/inpatient",
                                )
                            ],
                            size=1,
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
                                        "Nursing Facility", style={"font-size": "1vmax"}
                                    ),
                                    href="/nursing-facility",
                                )
                            ],
                            size=1,
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "center",
                            },
                        ),
            Col([
            dcc.RadioItems(
                                id='time_range',
                                options=[
                                    {"label": "Month to Date", "value":"month_td"},
                                    {"label": "Last Month",
                                     "value": "last_month"},
                                    {"label": "Last Quarter", "value": "last_quarter"},
                                    {"label": "Quarter to Date", "value": "quarter_td"}
                                ],
                                value="month_td",
                            )
            ], size = 5, style = {"display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "align-items": 'flex-end'})]

                     
#card column wrappers
def card_col(card_title='', card_val_id='', color=color_palette[1], size=2, title_id='', width='95%', height='90%', font_size="2.5vmax"):
    """
    Creates a column contains one bootstrap card

    Args:
        card_title: title of card
        card_val_id: id for card value body
        card_color: color of card header
        size: width of column
        title_id: if title needs to be updated with a callback
            this is set to the id and card_title is set to ''

    Returns:
        Column containing one card
    """
    return Col(
        [
            Card(
                [
                    html.H6(
                        card_title,
                        id=title_id,
                        className="card-header",
                        style={
                            "background-color": color
                                },
                    ),
                    html.H3(id=card_val_id, className="card-value", style={
    "font-size": font_size}),
                ],
                style={"width": width, "height": height},
            )
        ],
        bp="md",
        size=size, mobile_size = 6,
        style={
            "display": "flex",
            "flex-direction": "row",
            "justify-content": "center",
            "align-items": "center",
        },
    )

def small_clear_card(card_title, card_val):
    """
    Creates a column with a card that is clear with a gray border

    Args:
        card_title: title of card
        card_val: value for body of card


    Returns:
        column with card
    """
    return Col(
        [
            Card(
                [
                    html.H3(
                        card_title,
                        style={
                            "font-size": "1.25vw"},
                    ),
                    html.H2(
                        [card_val],
                        style={
                            "font-size": "1.75vw"},
                    ),
                ],
                style={
                    "background-color": "transparent",
                    "border-style": "solid",
                    "border-width": "2px",
                },
            )
        ],
        bp="md",
        size=3, mobile_size=3
    )

#card number/sparkline layouts

def left_number_right_spark(value, arrow, viz_page, figure, graph_id, indicator_color="#030027"):
    """
    Bootstrap row and columns to be used in a bootstrap card;
    Formatted to have an indicator number next to an arrow symbol, next to a sparkline
    
    Args:
        value(int/float): value of the indicator
        arrow(str): name of FA icon to use as arrow symbol
        viz_page(str): end of url to link to for related visualization
        figure(dict): sparkline plotly figure
        graph_id(str): id of plotly graph - all need to be different for dash
        indicator_cold(str): hex string indicating value color based on thresholds
    
    Returns:
        list: list to be passed to a bootstrap card body component
    """
    return [
        Row(
            [
                Col(
                    [
                  html.P([html.A(
                            [str(value)],
                            href=f"/{viz_page}",
                            target="_blank",
                            style={"color": indicator_color},
                        ), html.Span(Fa(arrow), style={"color":"black"})])
                    ],
                    size=5,
                    mobile_size=12,
                    style={
                        "padding-right": 0,
                        "align-content": "center",
                        "justify-content": "center",
                        "flex-direction": "column",
                        "display": "flex",
                        
                    },
                ),
            Col(
                [
            dcc.Graph(
                id=graph_id,
                figure = figure, 
                style={
                    "width": "100%",
                    "min-height": "8vh",
                    "padding-top": '0vh',
                    "padding-bottom": '0vh',
                    "display": "flex",
                    "flex-direction": "column",
                    "justify-content": "flex-start",
                    "align-items": "flex-start",
                },
                config= {'displayModeBar': False}
            )
        ],
        size=7, mobile_size = 12,
        style={"color": "#2E2C2F",
               "background-color": "transparent",
               "min-height":"8vh",
               "align-content": "center",
               "justify-content": "center",
               "flex-direction": "row",
               "display": "flex",
               "padding-left":0},
    )
            ],
            style={"width": "100%", "margin-top": "1vmin"},
        )
    ]

def top_number_bottom_spark(value, arrow, viz_page, figure, graph_id, indicator_color="#030027"):
    """
    Bootstrap row and columns to be used in a bootstrap card;
    Formatted to have an indicator number next to an arrow symbol
    with a sparkline below
    
    Args:
        value(int/float): value of the indicator
        arrow(str): name of FA icon to use as arrow symbol
        viz_page(str): end of url to link to for related visualization
        figure(dict): sparkline plotly figure
        graph_id(str): id of plotly graph - all need to be different for dash
        indicator_cold(str): hex string indicating value color based on thresholds
    
    Returns:
        list: list to be passed to a bootstrap card body component
    """
    return [
        Row(
            [
                Col(
                    [
                    html.P([html.A(
                            [str(value)],
                            href=f"/{viz_page}",
                            target="_blank",
                            style={"color": indicator_color},
                        ), html.Span(Fa(arrow), style={"color":"black"})])
                    ],
                    size=12,
                    mobile_size=12,
                    style={
                        "padding-right": 0,
                        "align-content": "center",
                        "justify-content": "center",
                        "flex-direction": "row",
                        "display": "flex",
                        
                    },
                )], style={"width": "100%", "margin-top": "1vmin"}),
                Row([
            Col(
                [
            dcc.Graph(
                id=graph_id,
                figure = figure, 
                style={
                    "width": "100%",
                    "min-height": "8vh",
                    "padding-top": '0vh',
                    "padding-bottom": '0vh',
                    "display": "flex",
                    "flex-direction": "column",
                    "justify-content": "flex-start",
                    "align-items": "flex-start",
                },
                config= {'displayModeBar': False}
            )
        ],
        size=12, mobile_size = 12,
        style={"color": "#2E2C2F",
               "background-color": "transparent",
               "min-height":"8vh",
               "align-content": "center",
               "justify-content": "center",
               "flex-direction": "row",
               "display": "flex",
               "padding-left":0},
    ),
            ],
            style={"width": "100%"},
        )
    ]

def text_val_no_sparkline(value, viz_page, indicator_color="#030027"):
    """
    Bootstrap row and columns to be used in a bootstrap card;
    Formatted to have a just an indicator string
    
    Args:
        value(int/float): value of the indicator
        viz_page(str): end of url to link to for related visualization
        indicator_cold(str): hex string indicating value color based on thresholds
    
    Returns:
        list: list to be passed to a bootstrap card body component
    """
    return [
        Row(
            [
                Col(
                    [
                  html.P([html.A(
                            [str(value)],
                            href=f"/{viz_page}",
                            target="_blank",
                            style={"color": indicator_color},
                        )])
                    ],
                    size=12,
                    mobile_size=12,
                    style={
                        "padding-right": 0,
                        "align-content": "center",
                        "justify-content": "center",
                        "flex-direction": "column",
                        "display": "flex",
                        
                    },
                )
            ],
            style={"width": "100%", "margin-top": "1vmin"},
        )
    ]

#graph layouts

def equal_graph_row(graph1_id, graph2_id):
    """
    Creates a row with two equally sized graphs

    Args:
        graph1_id: id for left graph
        graph2_id: id for right graph

    Returns:
        Row containing column and graph objects
    """
    return Row(
        [
            Col(
                dcc.Graph(
                    id=graph1_id,
                    style={
                        "width": "100%",
                        "height": "70vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "center"
                    },
                    config=graph_config,
                ),
                size=6, mobile_size=12, 
                style={"color": "#2E2C2F",
                       "background-color": "transparent"},
            ),
            Col(
                [
                    dcc.Graph(
                        id=graph2_id,
                        style={
                            "width": "100%",
                            "height": "70vh",
                            "display": "flex",
                            "flex-direction": "column",
                            "justify-content": "center",
                            "align-items": "center"
                        },
                        config=graph_config,
                    )
                ],
                size=6, mobile_size=12, 
                style={"color": "#2E2C2F",
                       "background-color": "transparent"},
            ),
        ],
        style={
            "padding-bottom": "1vh",
            "padding-top": "1vh",
            "display": "flex",
            "flex-direction": "row",
            "justify-content": "center",
            "align-items": "center",
        },
    )

def graph_row(graph1_id):
    """
    Creates a row with one graphs

    Args:
        graph1_id: id for left graph

    Returns:
        Row containing column and graph objects
    """
    return Row(
        [
            Col(
                dcc.Graph(
                    id=graph1_id,
                    style={
                        "width": "100%",
                        "height": "80vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "center"
                    },
                    config=graph_config,
                ),
                size=10, mobile_size=10, 
                style={"color": "#2E2C2F",
                       "background-color": "transparent"},
            ),
        ],
        style={
            "padding-bottom": "1vh",
            "padding-top": "1vh",
            "display": "flex",
            "flex-direction": "row",
            "justify-content": "center",
            "align-items": "center",
        },
    )

def graph_row_figure(figure):
    """
    Takes a figure returns the row child for one graph

    Args:
        graph1_id: id for left graph
        graph2_id: id for right graph

    Returns:
        Row containing column and graph objects
    """
    return [
            Col(
                dcc.Graph(
                    id='main-page-graph',
                    figure=figure,
                    style={
                        "width": "100%",
                        "height": "80vh",
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "center",
                        "align-items": "center"
                    },
                    config=graph_config,
                ),
                size=10, mobile_size=10, 
                style={"color": "#2E2C2F",
                       "background-color": "transparent"},
            ),
        ]

#various dropdown and radio groupings
def data_drop_with_graph_radios(drop_id, drop_options, drop_value, radio_id, radio_value):
    """
    Creates a column with a dropdown that is created dynamically by a callback
    with a radio that is also updated by a callback 

    Args:
        drop_id: id for the dropdown
        drop_options: options for the dropdown
        drop_value: default value for the dropdown
        radio_id: id for the radio button
        radio_value: default value for the radio

    Returns:
        column with dropdown and radio filter
    """
    return Col(
        [
            dcc.Dropdown(
                id=drop_id,
                options=drop_options,
                value=drop_value,
                clearable=False
            ),
            Row(
                [
                    Col(
                        [
                            dcc.RadioItems(
                                id=radio_id,
                                value=radio_value,
                                labelStyle={"padding": "0.5vh"},
                            )
                        ],
                        bp="md",
                        size=12,
                        style={
                            "padding-right": 0,
                            "display": "flex",
                            "flex-direction": "column",
                            "justify-content": "center",
                        },
                    )
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
    )

def graph_drop_with_filter_amnt(drop_id, drop_value, radio_id, filter_id):
    """
    Creates a column with a dropdown that is created dynamically by a callback
    with a radio below to limit the amount of results and a dropdown that
    can further filter the data

    Args:
        drop_id: id for the first dropdown
        drop_value: default value for the first dropdown
        radio_id: id for the radio button
        filter_id: id for the second dropdown

    Returns:
        column with dropdown, radio filter, and additional filter dropdown
    """
    return Col(
        [
            dcc.Dropdown(id=drop_id,
                         value=drop_value,
                         style=dropdown_style),
            Row(
                [
                    Col(
                        [
                            dcc.RadioItems(
                                id=radio_id,
                                options=[
                                    {"label": "Top 5",
                                     "value": "5"},
                                    {"label": "10", "value": "10"},
                                ],
                                value="5",
                            )
                        ],
                        bp="md",
                        size=5, mobile_size=5,
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
                                id=filter_id, multi=True, style=dropdown_style
                            )
                        ],
                        bp="md",
                        size=7, mobile_size=7,
                        style={
                            "padding-top": "0.5vh",
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
        size=3, mobile_size=6,
        style={
            "padding-top": "0.5vh",
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
        },
    )

def center_dropdown_col():
    """
    Create column contains a drop down with PACE centers and a drop down with
    PACE teams

    #To Do:
        Add teams to database and get working
    """
    return Col(
        [
            Row([
            Col([
            dcc.Dropdown(
                id="center-drop",
                options=[
                    {"label": "All Centers", "value": "all"},
                    {"label": "Providence", "value": "Providence"},
                    {"label": "Westerly", "value": "Westerly"},
                    {"label": "Woonsocket", "value": "Woonsocket"},
                ],
                value="all",
                searchable=False,
            )], bp="md",
        size=12, mobile_size=12,
        style={
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
        }
        )]),
            Row([])
        ],
        bp="md",
        size=2, mobile_size=6,
        style={
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
        },
    )


def select_date_col():
    """
    Creates column contains two input cells (stacked)
    Top is the start date, bottom is the end date
    Included an Input component to allow updating of
    date every 12 hours.
    """
    return Col(
        [
            dcc.Input(
                id="start_date",
                type="text",
                size=13,
                style={
                    "text-align": "center",
                    "width": "100%",
                    "height": "100%",
                    "border-color": "#ccc",
                                    "border-style": "solid",
                                    "border-width": "1px",
                                    "border-radius": "4px",
                                    "border-bottom-style": "none",
                },
            ),
            dcc.Input(
                id="end_date",
                type="text",
                size=13,
                style={
                    "text-align": "center",
                    "width": "100%",
                    "height": "100%",
                    "border-color": "#ccc",
                                    "border-style": "solid",
                                    "border-width": "1px",
                                    "border-radius": "4px",
                },
            ),
            dcc.Interval(
                id='interval-component',
                interval=12*60*60*1000,  # 12 hours in milliseconds
                n_intervals=0
            )
        ],
        bp="md",
        size=1, mobile_size=6,
        style={
            "margin-top": "-1vh",
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "center",
            "align-items": "flex-start",
        },
    )

def month_quarter_radio():
    """
    Allows for one line creation of radio button
    with Month and Quarter options
    Used on almost every page
    """
    return dcc.RadioItems(
        id="freq-radio",
        options=[
            {"label": "Month",
             "value": "MS"},
            {"label": "Quarter",
             "value": "QS"},
        ],
        value="MS",
    )

def pop_up_options_row():
    return Row(
        [
            center_team_dropdown_col(),
            select_date_col(),
            month_quarter_radio()
        ],
        className="options-row",
    )
