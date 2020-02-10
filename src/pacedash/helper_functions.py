import sqlite3
import calendar
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import paceutils
from .settings import color_palette, db_filepath, agg_filepath

helpers = paceutils.Helpers(db_filepath)
enrollment = paceutils.Enrollment(db_filepath)
demographics = paceutils.Demographics(db_filepath)
utilization = paceutils.Utilization(db_filepath)
incidents = paceutils.Incidents(db_filepath)
center_enrollment = paceutils.CenterEnrollment(db_filepath)
center_demographics = paceutils.CenterDemographics(db_filepath)
team = paceutils.Team(db_filepath)
quality = paceutils.Quality(db_filepath)
agg = paceutils.Agg(agg_filepath)

#dictionary for time range buttons
time_range_dict = {
    "last_month": (helpers.last_month, helpers.prev_month_dates),
    "month_td": (helpers.month_to_date, helpers.prev_month_dates),
    "last_quarter": (helpers.last_quarter, helpers.prev_quarter_dates),
    "quarter_td": (helpers.quarter_to_date, helpers.prev_quarter_dates),
}

def arrow_direction(prev_val, current_val):
    """
    Returns font icon arrow based on 
    comparison of values

    Args:
        prev_val(float/int): previous value of indicator
        current(float/int): current value of indicator

    Returns:
        str: "up-big" if current value is larger,
            "down-big" if current value is smaller,
            "minus" if they are equal
            These all correspond to FA icon names
    """
    if current_val > prev_val:
        return "up-big"
    if current_val < prev_val:
        return "down-big"
    return "minus"


def below_threshold(threshold, current_value):
    """
    Returns a color based on the values relation to the threshold.
    This function is used for values that should be BELOW their
    threshold

    Args:
        threshold(int/float): threshold value for indicator
        current_value(int/float): value of the indicator
    
    Returns:
        str: green hex is below threshold, red if above,
            black if equal
    """
    if current_value < threshold:
        return "#00B760"
    if current_value > threshold:
        return "#E3170A"
    return "#030027"


def above_threshold(threshold, current_value):
    """
    Returns a color based on the values relation to the threshold.
    This function is used for values that should be ABOVE their
    threshold

    Args:
        threshold(int/float): threshold value for indicator
        current_value(int/float): value of the indicator
    
    Returns:
        str: green hex is above threshold, red if below,
            black if equal
    """
    if current_value > threshold:
        return "#00B760"
    if current_value < threshold:
        return "#E3170A"
    return "#030027"


def indicator_color(threshold=None, current_value=0, polarity="above"):
    """
    Returns a color based on the values relation to the threshold.
 
    Args:
        threshold(int/float): threshold value for indicator
        current_value(int/float): value of the indicator
        polarity(str): above means the indicator should be above the threshold,
            below means the indicator should be below
    
    Returns:
        str: green hex is indicators is in good standing, red if not,
            black if equal or no threshold or direction is indicated
    """
    if threshold is None:
        return "#030027"
    if polarity == "above":
        return above_threshold(threshold, current_value)
    else:
        return below_threshold(threshold, current_value)
    return "#030027"
    
def card_value(time_range, value_function, agg_table, agg_col, card_layout, additional_args=None, threshold_value=None, polarity="above"):
    """
    Returns a bootstrap card with values defined in the design of the dashboard.

    Args:
        time_range(str): time range value from time radio button
        value_function(func): function to use to calculate the indicator - most come from
            the paceutils module
        agg_table: table in the agg database to use to build the dataframe for the sparkline
        agg_col: column in the table to use to build the dataframe for the sparkline
        card_layout(func): function that creates the row, col and card bootstrap elements
        additional_args(list): list of additional arguments for the value_function
        threshold_value(int/float):  threshold value for indicator
        polarity(str): above means the indicator should be above the threshold,
            below means the indicator should be below
    
    Returns:
        list: list of bootstrap components that create a card
    """
    params = time_range_dict[time_range][0]()
    prev_params = time_range_dict[time_range][1](params)

    if additional_args is None:
        prev_value = value_function(prev_params)
        current_value = value_function(params)
    else:
        prev_value = value_function(prev_params, *additional_args)
        current_value = value_function(params, *additional_args)

    arrow = arrow_direction(prev_value, current_value)
    
    plot_df = agg.get_plot_df(agg_table, agg_col, params=helpers.last_year())
    figure = sparkline(plot_df)
    if threshold_value is not None:
        color = indicator_color(threshold_value, current_value, polarity)
        return card_layout(
            current_value, arrow, f"{agg_table}-{agg_col}", figure, f"sparkline-{agg_col}", color
        )
    return card_layout(
            current_value, arrow, f"{agg_table}-{agg_col}", figure, f"sparkline-{agg_col}"
        )


def create_daterange(start_date, end_date, freq, update=True):
    """
    Create a range of dates for given start date, end date and frequency

    Args:
        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        freq: Determines if range should be by month or quarter

    Returns: daterange
    """
    if update:
        start_date, end_date = update_dates(start_date, end_date, freq)

    return pd.date_range(start_date, end_date, freq=freq)


def update_dates(start_date, end_date, freq):
    """
    Moves start date and end date to beginning of month or quarter and
    end of month for month frequency.

    Args:
        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

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
        start_date = (pd.to_datetime(start_date) + pd.tseries.offsets.DateOffset(days=1)) - pd.offsets.QuarterBegin(
            startingMonth=1
        )
        end_date = (pd.to_datetime(end_date) + pd.tseries.offsets.DateOffset(days=1)) - pd.offsets.QuarterEnd()

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
    if (min_y < 0) & (min_dp >= 0):
        return 0
    else:
        return min_y


def sql_return_df(query, params, date_cols):
    """
    Returns a pandas dataframe of the provided SQL query

    Args:
        query: Valid SQL query

        params: parameter for parameterized SQL query

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
        center_sql = f"AND centers.center = ?"
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
            Will return empty if no center filter is selected (i.e. center=all)
    """
    if center != "all":
        return f"JOIN centers ON {table}.member_id = centers.member_id"
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

    margin = {"pad": 10, "l": 55, "r": 55, "t": 35, "b": 65}
    title_y = 1.05
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

    margin = {"pad": 10, "l": 55, "r": 55, "t": 45, "b": 65}
    title_y = 1.05
    if small_margins:
        margin = {"pad": 5, "l": 35, "r": 35, "t": 45, "b": 20}
        title_y = 1.15

    scale_max = df_max * 1.10

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

def create_line_graph(plot_df, title="", x_title="", y_title=""):
    """
    Function for creating a simple plotly line graph. Useful in keeping the
    default graph page of the dashboard simple

    Args:
        plot_df(DataFrame): dataframe to plot, two column, first column for x-axis
            second for the y.
        title(str): title of the plot
        x_title: label of x-axis
        y_title: label of y-axis

    Returns:
        dict: dictionary to pass to ploty graph figure

    """
    fig_data = [
        go.Scatter(
            x=plot_df.iloc[:, 0].astype(str),
            y=plot_df.iloc[:, 1],
            text=plot_df.iloc[:, 1],
            mode="lines",
            line={"width": 7, "color": color_palette[0]},
            hoverinfo="x+y",
        )
    ]

    fig_layout = build_scatter_layout(
        title,
        plot_df.iloc[:, 1].min() * 1.05,
        plot_df.iloc[:, 1].max() * 1.05,
        x_title,
        y_title,
    )

    return dict(data=fig_data, layout=fig_layout)


def create_bar_graph(plot_df, title="", x_title="", y_title=""):
    """
    Function for creating a simple plotly bar graph. Useful in keeping the
    default graph page of the dashboard simple

    Args:
        plot_df(DataFrame): dataframe to plot, two column, first column for x-axis
            second for the y.
        title(str): title of the plot
        x_title: label of x-axis
        y_title: label of y-axis

    Returns:
        dict: dictionary to pass to ploty graph figure

    """
    plot_df["quarter"] = pd.PeriodIndex(pd.to_datetime(plot_df.iloc[:, 0]), freq="Q")
    fig_data = [
        go.Bar(
            x=plot_df["quarter"].astype(str),
            y=plot_df.iloc[:, 1],
            text=plot_df.iloc[:, 1],
            marker={"color": color_palette[0]},
            hoverinfo="x+y",
            showlegend=False,
        )
    ]

    fiq_layout = build_bar_layout(title, x_title=x_title, y_title=y_title)

    return dict(data=fig_data, layout=fiq_layout)


def create_team_line_graph(plot_df, plot_type="scatter", title_suffix=""):
    """
    Function for creating a plotly subplot of bar or line graphs.
    Useful in keeping the default graph page of the dashboard simple

    ##TO DO: generalize for any number of teams

    Args:
        plot_df(DataFrame): dataframe to plot, with a dat columns and
        a column for each team.
        plot_type(str): scatter for line graph, bar for a bar chart

    Returns:
        dict: dictionary to pass to ploty graph figure

    """
    fig = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f"Central {title_suffix}", f"South {title_suffix}", f"East {title_suffix}", f"North {title_suffix}"),
    )

    team_colors = {
        "Central": "#FE6B39",
        "East": "#FFD166",
        "North": "#439A86",
        "South": "#118AB2",
    }

    if plot_type == "bar":
        plot_df["quarter"] = pd.PeriodIndex(pd.to_datetime(plot_df["month"]), freq="Q")
        central = go.Bar(
            x=plot_df["quarter"].astype(str),
            y=plot_df["Central"],
            text=plot_df["Central"],
            marker={"color": team_colors["Central"]},
            hoverinfo="x+y",
        )
        south = go.Bar(
            x=plot_df["quarter"].astype(str),
            y=plot_df["South"],
            text=plot_df["South"],
            marker={"color": team_colors["South"]},
            hoverinfo="x+y",
        )
        east = go.Bar(
            x=plot_df["quarter"].astype(str),
            y=plot_df["East"],
            text=plot_df["East"],
            marker={"color": team_colors["East"]},
            hoverinfo="x+y",
        )
        north = go.Bar(
            x=plot_df["quarter"].astype(str),
            y=plot_df["North"],
            text=plot_df["North"],
            marker={"color": team_colors["North"]},
            hoverinfo="x+y",
        )

    if plot_type == "scatter":
        central = go.Scatter(
            x=plot_df["month"],
            y=plot_df["Central"],
            mode="lines",
            line={"width": 7, "color": team_colors["Central"]},
            hoverinfo="x+y",
        )
        south = go.Scatter(
            x=plot_df["month"],
            y=plot_df["South"],
            mode="lines",
            line={"width": 7, "color": team_colors["South"]},
            hoverinfo="x+y",
        )
        east = go.Scatter(
            x=plot_df["month"],
            y=plot_df["East"],
            mode="lines",
            line={"width": 7, "color": team_colors["East"]},
            hoverinfo="x+y",
        )
        north = go.Scatter(
            x=plot_df["month"],
            y=plot_df["North"],
            mode="lines",
            line={"width": 7, "color": team_colors["North"]},
            hoverinfo="x+y",
        )

    fig.add_trace(central, 1, 1)
    fig.add_trace(south, 2, 1)
    fig.add_trace(east, 3, 1)
    fig.add_trace(north, 4, 1)

    fig.update_yaxes(
        range=[plot_df["Central"].min() * 0.95, plot_df["Central"].max() * 1.05],
        row=1,
        col=1,
        showline=True,
        linewidth=1,
        linecolor="black",
        nticks=4,
    )
    fig.update_yaxes(
        range=[plot_df["South"].min() * 0.95, plot_df["South"].max() * 1.05],
        row=2,
        col=1,
        showline=True,
        linewidth=1,
        linecolor="black",
        nticks=4,
    )
    fig.update_yaxes(
        range=[plot_df["East"].min() * 0.95, plot_df["East"].max() * 1.05],
        row=3,
        col=1,
        showline=True,
        linewidth=1,
        linecolor="black",
        nticks=4,
    )
    fig.update_yaxes(
        range=[plot_df["North"].min() * 0.95, plot_df["North"].max() * 1.05],
        row=4,
        col=1,
        showline=True,
        linewidth=1,
        linecolor="black",
        nticks=4,
    )

    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", row=1, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", row=2, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", row=3, col=1)
    fig.update_xaxes(showline=True, linewidth=1, linecolor="black", row=4, col=1)

    fig.update_layout(
        margin={"pad": 10, "l": 55, "r": 55, "t": 35, "b": 65},
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        title="Participants",
    )

    return fig


def sparkline(plot_df):
    """
    Creates a plotly figure of a sparkline

    Args:
        plot_df(DataFrame): dataframe to plot, two column, first column for x-axis
            second for the y.

    Returns:
        dict: dictionary to pass to ploty graph figure
    """

    figure = {
        "data": [
            go.Scatter(
                x=plot_df.iloc[:, 0],
                y=plot_df.iloc[:, 1],
                mode="lines",
                text=plot_df.iloc[:, 1],
                line={"width": 3, "color": "#262626"},
                hoverinfo="none",
            )
        ],
        "layout": go.Layout(
            margin={"pad": 0, "l": 10, "r": 10, "t": 10, "b": 10},
            xaxis={
                "showgrid": False,
                "showline": False,
                "zeroline": False,
                "showticklabels": False,
            },
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            showlegend=False,
            autosize=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        ),
    }
    
    return figure
