import pandas as pd
import sqlite3
import plotly.graph_objs as go
import textwrap
from .helper_functions import (
    create_daterange,
    sql_return_df,
    build_scatter_layout,
    build_bar_layout,
    db_filepath,
    create_center_sql,
)
from .settings import color_palette


# helpers/utils


def get_census(center_sql=""):
    """
    Returns census as of the time called

    Args:
        center_sql: string to use to filter the query
            by center. Defaults to empty, returning
            census of all locations

    Returns:
        int: number of participants at this time,
            filtered by center if center_sql is provided
    """
    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    census_query = f"""SELECT COUNT(enrollment.member_id)
    FROM enrollment
    JOIN centers on enrollment.member_id=centers.member_id
    WHERE enrollment_date <= date('now')
    AND disenrollment_date IS NULL
    {center_sql};    
    """
    census = c.execute(census_query).fetchone()[0]
    conn.close()
    return census


def enrollment_df(center, cols):
    """
    Creates a pandas dataframe of enrollment table 
    with provided columns.

    Args:        
        center: Name of PACE center

        cols: List of column names to be included in the SQL query

    Returns:
        df: dataframe of enrollment table
            with specified columns
    """

    if center != "all":
        center_sql = f"WHERE center = ?"
        params = [f"{center}"]
    else:
        center_sql = ""
        params = None

    query = f"""
    SELECT {', '.join(col for col in cols)}
    FROM enrollment
    JOIN centers on enrollment.member_id=centers.member_id
    {center_sql};
    """

    return sql_return_df(query, params, ["enrollment_date", "disenrollment_date"])


def disenroll_reasons_df(center):
    """
    Creates pandas dataframe of enrollment table 
    with columns related to disenrollment, filtered by center

    Args:        
        center: Name of PACE center

    Returns:
        df: dataframe of enrollment table
            with columns related to disenrollment
    """
    center_sql, params = create_center_sql(center, [])

    query = f"""
    SELECT disenrollment_date, disenroll_type, disenroll_reason 
    FROM enrollment
    JOIN centers on enrollment.member_id=centers.member_id
    WHERE disenroll_type = 'Voluntary'
    {center_sql};
    """

    return sql_return_df(query, params, ["disenrollment_date"])


def monthly_census_count(df, month_date, *quarter_pmpm):
    """
    Returns the census as of the given month_date
   
    Args:
        df: pandas dataframe containing enrollment details

        month_date: Date to calculate the census on, will be either
            the start or end of a month

        *quarter_pmpm: Used in quarter census function

    Return:
        int: census count
    """
    enroll_mask = df.enrollment_date <= month_date
    disenroll_mask = (df.disenrollment_date >= month_date) | (
        df.disenrollment_date.isnull()
    )
    return df[enroll_mask & disenroll_mask].shape[0]


def quarterly_census_count(df, quarter_start, quarter_pmpm=False):
    """
    Returns the census as of the given month_date
   
    Args:
        df: pandas dataframe containing enrollment details

        quarter_start: start of the quarter

        quarter_pmpm: Default to False, if True
            the quarter census is the total of the census
            from the first of each month in the quarter

    Return:
        int: census count
    """
    quarter_end = quarter_start + pd.offsets.MonthEnd(3)
    if quarter_pmpm:
        total_quarter_count = 0
        for month_start in create_daterange(quarter_start, quarter_end, "MS"):
            total_quarter_count += monthly_census_count(df, month_start)

        return total_quarter_count

    enroll_mask = df.enrollment_date <= quarter_end
    disneroll_during = df.disenrollment_date >= quarter_start
    currently_enrolled = df.disenrollment_date.isnull()
    return df[(disneroll_during | currently_enrolled) & enroll_mask].shape[0]


# PACE RI counts census as of the first of the month and
# this dict changes the monthly/quarterly radio
# dict allows keeping the m/q radio simple

# plotly quarters are oddly indicated, this is used
# to create cleaner names
quarter_dict = {
    1: "Q1",
    3: "Q1",
    4: "Q2",
    6: "Q2",
    7: "Q3",
    9: "Q3",
    10: "Q4",
    12: "Q4",
}


def quarter_dict_key(freq_start):
    """
    Creates label for quarter data points

    Args:
        freq_start: start of the quarter

    Returns:
        str: label of format year + Q + quarter number
            ie: 2018Q2
    """
    return str(freq_start.year) + quarter_dict[freq_start.month]


def month_dict_key(freq_start):
    """
    Creates label for month data points

    Args:
        freq_start: start of the month

    Returns:
        str: string of month start
    """
    return str(freq_start)


def census_count_df(
    center, start_date, end_date, freq, quarter_pmpm=False, as_of_first=False
):
    """
    Creates pandas dataframe of census count for each month
    or quarter in a given date range, filtered by center

    Args:      
        center: Name of PACE center

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        quarter_pmpm: Default to False, if True
            the quarter census is the total of the census
            from the first of each month in the quarter
    
    Returns:
        count_df: census count dataframe
    """

    counter_func_dict = {
        "MS": (monthly_census_count, month_dict_key),
        "QS": (quarterly_census_count, quarter_dict_key),
    }

    df = enrollment_df(center, cols=["enrollment_date", "disenrollment_date"])
    census_dict = {}

    count_func, dict_key = counter_func_dict[freq]

    update = True
    if as_of_first:
        start_date = pd.to_datetime(start_date) - pd.offsets.MonthBegin(1)
        end_date = pd.to_datetime(end_date) + pd.offsets.MonthEnd(1)
        update = False

    for freq_start in create_daterange(start_date, end_date, freq, update=update):
        census_dict[dict_key(freq_start)] = count_func(df, freq_start, quarter_pmpm)

    count_df = pd.DataFrame.from_dict(census_dict, orient="index").reset_index()
    count_df.rename(columns={"index": "Freq", 0: "Census"}, inplace=True)
    count_df["Freq"] = pd.to_datetime(count_df["Freq"])
    return count_df


# GRAPHS
def census_trend(start_date, end_date, freq, center):
    """
    Plots a line graph of census monthly or quarterly for a given
    date range, filtered by center

    Args:
        start_date: First date included in plotting dataframe

        end_date: Last date included in plotting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        center: Name of PACE center

     Returns:
         dict: containing plotly figure data and layout information
    """

    plot_df = census_count_df(center, start_date, end_date, freq, as_of_first=True)
    plot_df["Freq"] = plot_df["Freq"].dt.to_period(freq[0])
    if freq == "QS":
        eot = "Quarter"  # end of title
        fig_data = [
            go.Bar(
                x=plot_df["Freq"].astype(str),
                y=plot_df["Census"],
                marker={"color": color_palette[0]},
            )
        ]
        fig_layout = build_bar_layout(f"Census by {eot}")
    else:
        eot = "Month"  # end of title
        fig_data = [
            go.Scatter(
                x=plot_df["Freq"].astype(str),
                y=plot_df["Census"],
                mode="lines",
                line={"width": 7, "color": color_palette[0]},
            )
        ]

        if int(end_date.split("/")[2]) - int(start_date.split("/")[2]) <= 1:
            x_ticks = plot_df["Freq"]
        else:
            x_ticks = pd.Series([])

        fig_layout = build_scatter_layout(
            f"Census by {eot}",
            plot_df["Census"].min(),
            plot_df["Census"].max(),
            x_ticks=x_ticks,
        )

    return dict(data=fig_data, layout=fig_layout)


def enrollment_changes(start_date, end_date, freq, center):
    """
    Plots a bar graph showing enrollment changes monthly or quarterly for a given
    date range, filtered by center and a line graph showing the net enrollment

    Args:
        start_date: First date included in plotting dataframe

        end_date: Last date included in plotting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        center: Name of PACE center

     Returns:
         dict: containing plotly figure data and layout information
    """
    freq = freq[0]
    df = enrollment_df(
        center, ["enrollment_date", "disenrollment_date", "disenroll_type"]
    )

    df["enrollment_date"] = df["enrollment_date"].dt.to_period(freq[0])
    df["disenrollment_date"] = df["disenrollment_date"].dt.to_period(freq[0])

    enrollment_dict = {}
    start_date = pd.to_datetime(start_date) - pd.offsets.MonthBegin(1)
    end_date = pd.to_datetime(end_date) + pd.offsets.MonthEnd(1)

    for single_date in create_daterange(start_date, end_date, freq, update=False):
        prev_month = (single_date-pd.DateOffset(months=1)).to_period(freq)
        single_date = single_date.to_period(freq)
        
        if freq == "QS":
            dict_key = str(single_date.year) + quarter_dict[single_date.month]
        else:
            dict_key = single_date

        enrollments = df[df.enrollment_date == single_date].shape[0]
        disnerollments = df[df.disenrollment_date == single_date].shape[0]
        deaths = df[
            ((df.disenrollment_date == single_date) & (df.disenroll_type == "Deceased"))
        ].shape[0]
        net = enrollments - df[df.disenrollment_date == prev_month].shape[0]
        enrollment_dict[dict_key] = [enrollments, disnerollments, deaths, net]

    plot_df = pd.DataFrame.from_dict(
        enrollment_dict,
        orient="index",
        columns=["enrollments", "disenrollments", "deaths", "net"],
    ).reset_index()
    plot_df.rename(columns={"index": "Freq"}, inplace=True)
    plot_df["Freq"] = plot_df["Freq"].astype(str)

    #plot_df["net"] = plot_df["enrollments"][1:] - plot_df["disenrollments"][:-1]

    if freq == "QS":
        legend = dict(orientation="h", y=-0.15)
    else:
        legend = dict(orientation="h", y=-0.15)

    return {
        "data": [
            go.Bar(
                x=plot_df["Freq"],
                y=plot_df["enrollments"],
                text=plot_df["enrollments"],
                hoverinfo="text+name+x",
                name="Enrollments",
                marker={"color": color_palette[0]},
            ),
            go.Bar(
                x=plot_df["Freq"],
                y=plot_df["disenrollments"],
                base=[-y for y in plot_df["disenrollments"]],
                text=plot_df["disenrollments"],
                hoverinfo="text+name",
                name="Disenrollments",
                marker={"color": color_palette[2]},
            ),
            go.Bar(
                x=plot_df["Freq"],
                y=plot_df["deaths"],
                base=[-y for y in plot_df["deaths"]],
                text=plot_df["deaths"],
                hoverinfo="text+name",
                name="Deaths",
                marker={"color": color_palette[3]},
            ),
            go.Scatter(
                x=plot_df["Freq"],
                y=plot_df["net"],
                text=plot_df["net"],
                hoverinfo="text+name+x",
                name="Net Enrollment",
                mode="lines",
                line={"width": 3, "dash": "dash", "color": color_palette[7]},
            ),
        ],
        "layout": build_bar_layout("Enrollment Changes", "overlay", legend=legend),
    }


def time_to_disenroll(start_date, end_date, freq, center):
    """
    Plots a line graph of the average time to disenroll
    monthly or quarterly grouped by reason for a given
    date range, filtered by center

    Args:
        start_date: First date included in plotting dataframe

        end_date: Last date included in plotting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        center: Name of PACE center

     Returns:
         dict: containing plotly figure data and layout information
    """
    df = enrollment_df(
        center, ["enrollment_date", "disenrollment_date", "disenroll_type"]
    )

    df["time_to_disenroll"] = (
        df["disenrollment_date"] - df["enrollment_date"]
    ).dt.days / 365

    avg_disenroll_dict = {}

    for single_date in create_daterange(start_date, end_date, freq):
        if freq == "QS":
            dict_key = str(single_date.year) + quarter_dict[single_date.month]
        else:
            dict_key = single_date

        mask = (df.enrollment_date <= single_date) & (
            df.disenrollment_date <= single_date
        )

        all_disenroll = df[mask]["time_to_disenroll"].mean()
        vol_disenroll = df[(mask) & (df.disenroll_type == "Voluntary")][
            "time_to_disenroll"
        ].mean()
        die_disenroll = df[(mask) & (df.disenroll_type == "Deceased")][
            "time_to_disenroll"
        ].mean()
        avg_disenroll_dict[dict_key] = [all_disenroll, vol_disenroll, die_disenroll]

    plot_df = pd.DataFrame.from_dict(
        avg_disenroll_dict, orient="index", columns=["all", "voluntary", "deceased"]
    ).reset_index()
    plot_df.rename(columns={"index": "Freq"}, inplace=True)
    plot_df["Freq"] = plot_df["Freq"].astype(str)

    if freq == "QS":
        eot = "Quarter"  # end of title
    else:
        eot = "Month"  # end of title

    fig_data = [
        go.Scatter(
            x=plot_df["Freq"],
            y=plot_df["all"],
            mode="lines",
            name="All",
            line={"width": 7, "color": color_palette[0]},
        ),
        go.Scatter(
            x=plot_df["Freq"],
            y=plot_df["voluntary"],
            mode="lines",
            name="Voluntary",
            line={"width": 7, "color": color_palette[2]},
        ),
        go.Scatter(
            x=plot_df["Freq"],
            y=plot_df["deceased"],
            mode="lines",
            name="Death",
            line={"width": 7, "color": color_palette[3]},
        ),
    ]

    fig_layout = build_scatter_layout(
        f"Avg Time to Disenrollment (in Years) by {eot}",
        plot_df["voluntary"].min(),
        plot_df["deceased"].max(),
        legend=dict(orientation="h", y=-0.15),
    )

    return dict(data=fig_data, layout=fig_layout)


def disenroll_reasons(start_date, end_date, freq, center):
    """
    Plots a bar graph of the voluntary disenroll reasons
    monthly or quarterly for a given
    date range, filtered by center

    Args:
        start_date: First date included in plotting dataframe

        end_date: Last date included in plotting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        center: Name of PACE center

     Returns:
         dict: containing plotly figure data and layout information
    """
    df = disenroll_reasons_df(center)
    df["disenrollment_date"] = df["disenrollment_date"].dt.to_period(freq[0])
    disenroll_dict = {}

    for single_date in create_daterange(start_date, end_date, freq):
        single_date = single_date.to_period(freq[0])
        disenroll_counts = {}
        date_mask = df.disenrollment_date == single_date

        for reason in df.disenroll_reason.unique():
            reason_mask = df.disenroll_reason == reason
            disenroll_counts[reason.title()] = df[date_mask & reason_mask].shape[0]

        if freq == "QS":
            dict_key = str(single_date.year)[2:] + quarter_dict[single_date.month]
        else:
            dict_key = single_date

        disenroll_dict[dict_key] = disenroll_counts

    plot_df = pd.DataFrame.from_dict(disenroll_dict, orient="index").reset_index()
    plot_df.rename(columns={"index": "Quarter"}, inplace=True)

    if freq == "QS":
        eot = "Quarter"  # end of title
        legend = dict(orientation="h", y=-0.15)

    else:
        eot = "Month"  # end of title
        legend = dict(orientation="h", y=-0.15)

    fig_data = [
        go.Bar(
            x=plot_df["Quarter"].astype(str),
            y=plot_df[col],
            text=[f"{val} {col}" if val != 0 else None for val in plot_df[col]],
            hoverinfo="x+text",
            name="<br>".join(textwrap.wrap(col.title(), width=15)),
            marker=dict(color=color),
        )
        for col, color in zip(plot_df.columns[1:], color_palette)
    ]

    fig_layout = build_bar_layout(
        f"Voluntary Disenrollment Reason by {eot}", "stack", legend=legend
    )

    return dict(data=fig_data, layout=fig_layout)

### used to assign a drop down value to the correct graph
graph_choice = {
    "enroll": census_trend,
    "changes": enrollment_changes,
    "conv": None,
    "disenroll": disenroll_reasons,
    "avg_time": time_to_disenroll,
}
