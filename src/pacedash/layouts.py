from flask import current_app as server
import dash_core_components as dcc
import dash_html_components as html
from .components import Col, Row, Header, Card

from .helpers_configs import graph_config, card_num_style, dropdown_style


def main_layout_header():
    """
    Creates dash app layout with header
    Used a default for this dash app
    """
    return html.Div(
        [
            html.Div(
                id="header",
                children=[Header(), html.Div(
                    id=server.config["NAVBAR_CONTAINER_ID"]), html.Div(id='logout')], style={'height': '6vmin'}),
            html.Div(
                className="container-fluid",
                children=Row(Col(id=server.config["CONTENT_CONTAINER_ID"], size=12, style={'margin-top': '3vmin', 'margin-bottom': 0}))),
            dcc.Location(id="url", refresh=False),
        ]
    )


def sixty_forty_graph_row(graph1_id, graph2_id):
    """
    Creates a row contains a graph (on the left) that fills 60% of
    the width and a graph (on the right) that fills 40%

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
                        "height": "55vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "center"
                    },
                    config=graph_config,
                ),
                size=8, mobile_size=12,
                style={"color": "#2E2C2F",
                       "background-color": "transparent"},
            ),
            Col(
                [
                    dcc.Graph(
                        id=graph2_id,
                        style={
                            "width": "100%",
                            "height": "55vh",
                            "display": "flex",
                            "flex-direction": "column",
                            "justify-content": "center",
                            "align-items": "center"
                        },
                        config=graph_config,
                    )
                ],
                size=4, mobile_size=12,
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


def three_graph_row(graph1_id, graph2_id, graph3_id):
    """
    Creates a row with three equally sized graphs

    Args:
        graph1_id: id for left graph
        graph2_id: id for middle graph
        graph3_id: id for right graph

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
                        "height": "55vh",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                    config=graph_config,
                ),
                size=4, mobile_size=12, 
                style={"color": "#2E2C2F",
                       "background-color": "transparent"},
            ),
            Col(
                [
                    dcc.Graph(
                        id=graph2_id,
                        style={
                            "width": "100%",
                            "height": "55vh",
                            "display": "flex",
                            "flex-direction": "column",
                            "justify-content": "center",
                            "align-items": "center",
                        },
                        config=graph_config,
                    )
                ],
                size=4, mobile_size=12, 
                style={"color": "#2E2C2F",
                       "background-color": "transparent"},
            ),
            Col(
                [
                    dcc.Graph(
                        id=graph3_id,
                        style={
                            "width": "100%",
                            "height": "55vh",
                            "display": "flex",
                            "flex-direction": "column",
                            "justify-content": "center",
                            "align-items": "center",
                        },
                        config=graph_config,
                    )
                ],
                size=4, mobile_size=12, 
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
                        "height": "55vh",
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
                            "height": "55vh",
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


def center_team_dropdown_col():
    """
    Create column contains a drop down with PACE centers and a drop down with
    PACE teams

    #To Do:
        Add teams to database and get working
    """
    return Col(
        [
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
            ),
            dcc.Dropdown(
                id="team-drop",
                options=[
                    {"label": "All Teams", "value": "all"},
                    {"label": "North", "value": "north"},
                    {"label": "South", "value": "south"},
                    {"label": "East", "value": "east"},
                    {"label": "West", "value": "west"},
                ],
                value="all",
                placeholder="Select a team",
                searchable=False,
            ),
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


def card_col(card_title, card_val_id, card_color, size=2, title_id='', height='90%'):
    """
    Creates a column contains one boostrap card

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
                    html.H5(
                        card_title,
                        id=title_id,
                        className="card-header",
                        style={
                            "color": "#FFFF",
                            "background-color": card_color,
                        },
                    ),
                    html.H3(id=card_val_id, style=card_num_style),
                ],
                style={"width": "100%", "height": height},
            )
        ],
        bp="md",
        size=size, mobile_size = 4,
        style={
            "display": "flex",
            "flex-direction": "row",
            "justify-content": "center",
            "align-items": "center",
        },
    )


def small_trend_graph(graph_id):
    """
    Creates a column containing one graph object of height 23vh

    Args:
        graph_id: id for graph

    Returns:
        Column containing graph object
    """
    return Col(
        [
            dcc.Graph(
                id=graph_id,
                style={
                    "width": "100%",
                    "height": "23vh",
                    "padding-top": '0vh',
                    "padding-bottom": '0vh',
                    "display": "flex",
                    "flex-direction": "column",
                    "justify-content": "flex-start",
                    "align-items": "flex-start",
                },
                config=graph_config,
            )
        ],
        size=6, mobile_size = 12,
        style={"color": "#2E2C2F",
               "background-color": "transparent"},
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
             "value": "M"},
            {"label": "Quarter",
             "value": "Q"},
        ],
        value="M",
    )
