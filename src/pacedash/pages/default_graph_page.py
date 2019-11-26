import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ..components import Row, Col
from ..app import app

from ..layouts import graph_row_figure, select_date_col, month_quarter_radio

from ..helper_functions import (
    agg,
    create_line_graph,
    create_team_line_graph,
    create_bar_graph,
)
import pandas as pd
import urllib


layout = html.Div(
    [
        Row(
            [
                select_date_col(),
                Col(
                    [month_quarter_radio()],
                    bp="md",
                    size=2,
                    mobile_size=6,
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-content": "center",
                    },
                ),
                Col(
                    [
                        html.A(
                            "Download Data",
                            id="download-link-graphs",
                            download="data.csv",
                            href="",
                            target="_blank",
                        )
                    ],
                    bp="md",
                    size=1,
                    mobile_size=6,
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "align-content": "center",
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
                    size=7,
                    mobile_size=12,
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "center",
                        "align-items": "flex-end",
                    },
                ),
            ],
            className="options-row",
        ),
        Row(
            id="main-graph-page",
            style={
                "padding-bottom": "1vh",
                "padding-top": "1vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
    ]
)


@app.callback(
    Output("main-graph-page", "children"),
    [
        Input("url", "pathname"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
    ],
)
def return_page_layout(pathname, start_date, end_date, freq):
    """
    Returns a graph if the pathname is of the format agg_table-col
    and returns a 404 page otherwise

    Args:
        pathname(str): url of page
        start_date(str): start date of period used to filter graph
        end_date(str): end date of period used to filter graph
        freq: frequency grouping of graph data - quarterly grouping creates
            a bar graph, line for monthly
    
    Returns:
        list: components to be passed to html Row function
    """
    try:
        table, col = pathname.split("-")

    except ValueError:
        return [html.H1(f" Oh no, {pathname} not found!")]
    if table[1:5] == "team":
        if freq == "QS":
            table = f"{table}_q"
            plot_type = "bar"
        else:
            plot_type = "scatter"

        plot_df = agg.team_plot_df(
            table[1:],
            col,
            (
                pd.to_datetime(start_date).strftime("%Y-%m-%d"),
                pd.to_datetime(end_date).strftime("%Y-%m-%d"),
            ),
        )
        figure = create_team_line_graph(
            plot_df, plot_type, title_suffix=" ".join(col.split("_")).title()
        )
    else:
        if freq == "QS":
            table = f"{table}_q"
            plot_func = create_bar_graph
        else:
            plot_func = create_line_graph

        plot_df = agg.get_plot_df(
            table[1:],
            col,
            (
                pd.to_datetime(start_date).strftime("%Y-%m-%d"),
                pd.to_datetime(end_date).strftime("%Y-%m-%d"),
            ),
        )

        figure = plot_func(
            plot_df,
            title=" ".join(col.split("_")).title(),
            x_title=plot_df.columns[0].title(),
            y_title=plot_df.columns[1].title(),
        )

    if figure is None:
        return [html.H1(f" Oh no, {pathname} not found!")]

    return graph_row_figure(figure)


@app.callback(
    Output("download-link-graphs", "href"),
    [
        Input("url", "pathname"),
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("freq-radio", "value"),
    ],
)
def update_download_link(pathname, start_date, end_date, freq):
    """
    Returns a csv string of the data used to create the chart

    Args:
        pathname(str): url of page
        start_date(str): start date of period used to filter graph
        end_date(str): end date of period used to filter graph
        freq: frequency grouping of graph data - quarterly grouping creates
            a bar graph, line for monthly
    
    Returns:
        str: string used to allow user to download csv of data
    """
    try:
        table, col = pathname.split("-")
    except ValueError:
        return ""

    if table[1:5] == "team":
        if freq == "QS":
            table = f"{table}_q"

        dff = agg.team_plot_df(
            table[1:],
            col,
            (
                pd.to_datetime(start_date).strftime("%Y-%m-%d"),
                pd.to_datetime(end_date).strftime("%Y-%m-%d"),
            ),
        )
    else:
        if freq == "QS":
            table = f"{table}_q"

        dff = agg.get_plot_df(
            table[1:],
            col,
            (
                pd.to_datetime(start_date).strftime("%Y-%m-%d"),
                pd.to_datetime(end_date).strftime("%Y-%m-%d"),
            ),
        )

    csv_string = dff.to_csv(index=False, encoding="utf-8")
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(
        csv_string
    )
    return csv_string
