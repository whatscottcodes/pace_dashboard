import sqlite3
import plotly.graph_objs as go
import pandas as pd
import calendar
from filepaths import db_filepath, user_db, log_path

color_palette = [
    "#00B760",  # this should be first color of your program
    "#8DCC8F",  # this should be a lighter shade of the first color of your program
    "#442359",  # this should be the second color of your program
    "#775F86",  # this should be a lighter of the seocnd color of your program
    "#6EA4BF",
    "#CADDE7",
    "#F06449",
    "#F6AA9B",
    "#EF934C",
    "#F6C49D",
    "#191919",
    "#6C6C6C",
    "#F2C14E",
    "#F6D78E",
]

# configuration for plotly graphs
graph_config = {
    "modeBarButtonsToRemove": [
        "sendDataToCloud",
        "hoverClosestCartesian",
        "autoScale2d",
        "select2d",
        "toggleSpikelines",
        "hoverCompareCartesian",
        "pan2d",
        "lasso2d",
    ],
    "responsive": "true",
    "displaylogo": "false",
    "sendData": "false",
    "showAxisDragHandles": "false",
    "doubleClick": "reset",
    # "editable": "true",
    "showAxisRangeEntryBoxes": "false",
    "toImageButtonOptions": {"format": "svg", "filename": "PACE_chart"},
}

# style of card values
card_num_style = {
    "font-size": "3vmin",
    "padding-top": "1vh",
    "word-wrap": "break-word",
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "center",
    "align-items": "center",
}

# style of dropdowns
dropdown_style = {"width": "100%", "white-space": "nowrap", "text-overflow": "ellipsis"}


def create_daterange(start_date, end_date, freq, update=True):
    """
    Create a range of dates for given start date, end date and frequency

    Args:
        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        freq: Determines if range should be by month or quarter

    Returns: daterange
    """
    if update:
        start_date, end_date = update_dates(start_date, end_date, freq)

    return pd.date_range(start_date, end_date, freq=freq)


def update_dates(start_date, end_date, freq):
    """
    Moves start date and end date to begining of month or quarter and
    end of month for month frequency.

    Args:
        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        freq: Determines if range should be by month or quarter

    Returns: start_date, end_date
    """

    if (freq == "MS") or (freq == "M"):
        try:
            start_date = start_date.split("/")
            end_date = end_date.split("/")
        except AttributeError:
            start_date = [start_date.month, start_date.day, start_date.year]
            end_date = [end_date.month, end_date.day, end_date.year]
        if int(end_date[1]) < 22:
            if int(end_date[0]) == 1:
                end_month = 12
                end_year = int(end_date[2]) - 1
            else:
                end_month = int(end_date[0]) - 1
                end_year = end_date[2]

            end_date[0] = end_month
            end_date[2] = end_year

        start_date = pd.to_datetime(f"{start_date[0]}/01/{start_date[2]}")

        end_date = pd.to_datetime(
            f"{end_date[0]}/{calendar.monthrange(int(end_date[2]),int(end_date[0]))[1]}/{end_date[2]}"
        )

    if (freq == "QS") or (freq == "Q"):
        start_date = pd.to_datetime(start_date) - pd.offsets.QuarterBegin(
            startingMonth=1
        )

        end_date = pd.to_datetime(end_date) - pd.offsets.QuarterEnd()

    return (start_date, end_date)


def calc_min_y(scale_max, min_dp):
    """
    Calculates the minimum y value for a plot so there is about
    33% white space below the plotted line

    Args:
        scale_max: Calculated maximum y-axis value (not maximum dataset data point)

        min_dp: Minimum data point

    Returns:
        float: minimum value of the y-axis
    """
    min_y = ((3 * min_dp) - (scale_max)) / 2
    if min_y < 0:
        return 0
    else:
        return min_y


def sql_return_df(query, params, date_cols):
    """
    Returns a pandas dataframe of the proivded SQL query

    Args:
        query: Valid SQL query

        params: paremeter for parameterized SQL quaery

        date_cols: columns to parse the dates in

    Returns:
        df: dataframe
    """
    conn = sqlite3.connect(db_filepath)
    df = pd.read_sql(query, conn, params=params, parse_dates=date_cols)
    conn.close()
    return df


def create_center_sql(center, params):
    """
    Create SQL need to filter query by center
    Will return empty string if filtering is
    not needed

    Args:
        center: Name of PACE center

        params: current parameters for
            related parameterized query

    Returns:
        center_sql: string that can be used to
            filter sql query by PACE center
        params: current parameters for related
        parameterized query
    """
    if center != "all":
        center_sql = f"AND center = ?"
        params += [f"{center}"]
    else:
        center_sql = ""
    return center_sql, params


def create_join_sql(center, table):
    """
    Creates SQL statements to join a table with the enrollment table to
    enable filtering by PACE center

    Args:
        center: Name of PACE center

        table: table to be joined to enrollment

    Returns:
        string: string containing a SQL statement that can be used join a table
            with the enrollment table to enable filtering by PACE center
            Will return empty if no center filter is selected (ie center=all)
    """
    if center != "all":
        return f"JOIN enrollment e ON {table}.member_id = e.member_id"
    return ""


def build_bar_layout(
    title,
    bar_mode="group",
    x_title=" ",
    y_title=" ",
    legend={},
    x_ticks=pd.Series([]),
    small_margins=False,
):
    """
    Creates plotly layout object for bar graphs

    Args:
        title: title of plot

        bar_mode: default is group, set mode of plotly bars

        x_title: x-axis title

        y_title: y-axis title

        legend: plotly legend object if needed

        small_margins: sets the margins to a narrow setting

    Returns plotly layout object
    """
    show_legend = bool(legend)

    margin = {"pad": 15, "l": 50, "r": 35, "t": 55, "b": 65}
    title_y = 1.10
    if small_margins:
        margin = {"pad": 5, "l": 35, "r": 35, "t": 35, "b": 20}
        title_y = 1.15
    if not x_ticks.empty:
        x_axis = {
            "title": x_title,
            "showgrid": False,
            "showline": False,
            "tickmode": "array",
            "tickvals": list(range(0, len(x_ticks))),
            "ticktext": [
                f"{calendar.month_abbr[int(str(date)[5:7])]} {str(date)[:4]}"
                for date in x_ticks.values
            ],
            "type": "category",
        }
    else:
        x_axis = {"title": x_title, "showgrid": False, "showline": False}

    return go.Layout(
        margin=margin,
        barmode=bar_mode,
        xaxis=x_axis,
        yaxis={"title": y_title, "showgrid": False},
        showlegend=show_legend,
        legend=legend,
        hoverdistance=5,
        annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=title_y,
                x=0,
                text=f"<b>{title}</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ],
    )


def build_scatter_layout(
    title,
    df_min,
    df_max,
    x_title=" ",
    y_title=" ",
    legend={},
    x_ticks=pd.Series([]),
    small_margins=False,
):
    """
    Creates plotly layout object for scatter plots

    Args:
        title: title of plot

        df_min: minimum value in the dataset

        df_max: maximum value in the dataset


        x_title: x-axis title

        y_title: y-axis title

        legend: plotly legend object if needed

        x_ticks: sets x_ticks to specific values, default allows plotly to choose

        small_margins: sets the margins to a narrow setting

    Returns plotly layout object
    """
    show_legend = bool(legend)

    margin = {"pad": 15, "l": 50, "r": 35, "t": 55, "b": 65}
    title_y = 1.10
    if small_margins:
        margin = {"pad": 5, "l": 35, "r": 35, "t": 35, "b": 20}
        title_y = 1.15

    scale_max = df_max * 1.05

    scale_min = calc_min_y(scale_max, df_min)

    if scale_max - scale_min < 4.5:
        scale_min = scale_max - 4.5

    if not x_ticks.empty:
        x_axis = {
            "title": x_title,
            "showgrid": False,
            "showline": False,
            "tickmode": "array",
            "tickvals": list(range(0, len(x_ticks))),
            "ticktext": [
                f"{calendar.month_abbr[int(str(date)[5:7])]} {str(date)[:4]}"
                for date in x_ticks.values
            ],
            "type": "category",
        }
    else:
        x_axis = {"title": x_title, "showgrid": False, "showline": False}

    return go.Layout(
        margin=margin,
        xaxis=x_axis,
        yaxis={
            "title": y_title,
            "showgrid": True,
            "zeroline": False,
            "range": [scale_min, scale_max],
        },
        autosize=True,
        hoverdistance=10,
        annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=title_y,
                x=0,
                text=f"<b>{title}</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ],
        showlegend=show_legend,
        legend=legend,
    )
