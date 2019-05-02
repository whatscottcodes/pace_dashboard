import sqlite3
import plotly.graph_objs as go
import numpy as np
from .census_utils import census_count_df
import pandas as pd
from .helpers_configs import (
    build_scatter_layout,
    color_palette,
    sql_return_df,
    create_center_sql,
    create_join_sql,
    build_bar_layout,
    db_filepath,
    update_dates,
)
import textwrap
from titlecase import titlecase

grievance_dropdown_options = [
    {"label": "Grievances by Category (per 100MM)", "value": "category"},
    {"label": "Grievances by Provider (per 100MM)", "value": "providers"},
    {"label": "Grievances by Type (per 100MM)", "value": "types"},
    {"label": "Time to be Resolved", "value": "time_to_resolved"},
    {"label": "Written/Oral Notification Percent", "value": "written_oral_recieved"},
    {"label": "Grievances by Category (%)", "value": "category__percent"},
    {"label": "Grievances by Provider (%)", "value": "providers_percent"},
    {"label": "Grievances by Type (%)", "value": "types__percent"},
    {"label": "Avg. Time to be Resolved", "value": "avg_time_to_resolved"},
]

col_groups = {
    "providers": ["providers"],
    "types": ["types"],
    "category": ["category_of_the_grievance"],
    "providers_percent": ["providers"],
    "types__percent": ["types"],
    "category__percent": ["category_of_the_grievance"],
    "time_to_resolved": ["date_of_resolution"],
    "avg_time_to_resolved": ["date_of_resolution"],
    "written_oral_recieved": [
        "date_of_oral_notification",
        "date_of_written_notification",
    ],
    "total": ["date_of_resolution"],
}


def grievance_query(col_group, start_date, end_date, center, freq):
    """
    Creates pandas dataframe from grievance table using
    user selected filters

    Args:
        col_group: Column selection to group grievances by

        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        center: Name of PACE center

        freq: M or Q, determines if results should be grouped by
            month or quarter

    Returns:
        df: pandas dataframe with selected columns of grievance
        SQL table
    """
    start_date, end_date = update_dates(start_date, end_date, freq)

    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    cols = ["date_grievance_received"] + col_groups[col_group]

    center_sql, params = create_center_sql(center, params)

    if center != "all":
        join_sql = f"JOIN enrollment e ON grievances.member_id = e.member_id"
    else:
        join_sql = ""

    query = f"""
            SELECT {', '.join(col for col in cols if col!=None)} 
            FROM grievances
            {join_sql}
            WHERE date_grievance_received BETWEEN ? AND ?
            {center_sql};
            """
    date_cols = [
        col
        for col in cols
        if col
        in [
            "date_grievance_received",
            "date_of_resolution",
            "date_of_oral_notification",
            "date_of_written_notification",
        ]
    ]
    df = sql_return_df(query, params, date_cols)
    df["Freq"] = df["date_grievance_received"].dt.to_period(freq)

    return df


def update_griev_graph_pmpm(df, freq, pmpm_df, x_ticks):
    """
    Creates bar graph, grouping grievances by user selected
    columns

    Args:
        df: pandas dataframe with selected columns of grievance
        SQL table

        freq: M or Q, determines if results should be grouped by
            month or quarter

        pmpm_df: pandas dataframe containing census count
        by month or quarter based on freq

    Returns:
         dict: contianging plotly figure data and layout information
    """

    df = pd.concat(
        [df, pd.get_dummies(df[df.columns[1]], prefix="", prefix_sep="")], axis=1
    )

    plot_df = df.groupby("Freq").sum()

    census = pmpm_df[pmpm_df["Freq"].isin(df["Freq"].values.tolist())][
        "Census"
    ].values.tolist()

    if freq == "Q":  # census_count_df returns one quarter too many
        plot_df = plot_df.apply(lambda x: (x / census) * 100)  # per100members
    else:
        plot_df = plot_df.apply(lambda x: (x / census) * 100)  # per100members

    plot_df.reset_index(inplace=True)

    fig_data = [
        go.Bar(
            x=plot_df["Freq"].astype(str),
            y=plot_df[col],
            name="<br>".join(textwrap.wrap(titlecase(" ".join(col.split("_"))), width=15)),
            marker=dict(color=color),
            text=[
                f"{round(val,2)} {titlecase(col.replace('_', ' '))}" if val != 0 else None
                for val in plot_df[col]
            ],
            hoverinfo="x+text",
        )
        for col, color in zip(plot_df.columns[1:], color_palette)
        if (plot_df[col].sum()) != 0
    ]

    fig_layout = build_bar_layout(
        "Grievances per 100MM",
        legend=dict(orientation="h", y=-0.15, font={"size": 9.5}),
        y_title="Per 100MM Rate",
        x_ticks=x_ticks,
    )

    return dict(data=fig_data, layout=fig_layout)


def update_griev_pie(df, x_ticks):
    """
    Creates pie graph, of grievance grouped
    by user selected columns

    Args:
        df: pandas dataframe with selected columns of grievance
        SQL table

    Returns:
         dict: contianging plotly figure data and layout information
    """

    df = pd.concat(
        [df, pd.get_dummies(df[df.columns[1:]], prefix="", prefix_sep="")], axis=1
    )

    plot_df = df.sum().reset_index()
    plot_df.rename(columns={0: "count"}, inplace=True)
    plot_df = plot_df[plot_df["count"] > 0]
    labels = [titlecase(" ".join(label.split("_"))) for label in plot_df["index"].tolist()]
    values = plot_df["count"].values.tolist()
    fig_data = [
        go.Pie(
            labels=labels,
            values=values,
            hoverinfo="label+percent+value",
            textinfo="label",
            textfont=dict(size=10, color="white"),
            marker=dict(colors=color_palette, line=dict(color="white", width=2)),
        )
    ]

    fig_layout = go.Layout(
        showlegend=False,
        title="",
        annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=1.25,
                x=0,
                text="<b>Grievances</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ],
    )

    return dict(data=fig_data, layout=fig_layout)


def notifcation_graph(df, x_ticks):
    """
    Creates bar graph with percent of oral notifications and written
    notifications for all grievances

    Args:
        df: pandas dataframe with selected columns of grievance
        SQL table

    Returns:
         dict: contianging plotly figure data and layout information
    """

    df["date_of_oral_notification"] = np.where(
        df["date_of_oral_notification"].notnull(), 1, 0
    )
    df["date_of_written_notification"] = np.where(
        df["date_of_written_notification"].notnull(), 1, 0
    )

    plot_df = df.groupby("Freq").sum().reset_index()
    # need total grievances for each frequency to calc percents
    total_df = df.groupby("Freq").count().reset_index()
    total_df.rename(
        columns={"date_grievance_received": "count"}, inplace=True
    )  # renamed for clarity
    plot_df["Oral Notification"] = (
        plot_df["date_of_oral_notification"] / total_df["count"]
    ) * 100
    plot_df["Written Notification"] = (
        plot_df["date_of_written_notification"] / total_df["count"]
    ) * 100

    fig_data = [
        go.Bar(
            x=plot_df["Freq"].astype(str),
            y=plot_df[col],
            name="<br>".join(textwrap.wrap(titlecase(" ".join(col.split("_"))), width=15)),
            marker=dict(color=color),
            text=[f"{round(val,2)}%" for val in plot_df[col].values],
            hoverinfo="x+text+name",
        )
        for col, color in zip(
            ["Oral Notification", "Written Notification"], color_palette
        )
    ]

    fig_layout = build_bar_layout(
        "Percent of Grievances with Oral or Written Notification",
        legend=dict(orientation="h", y=-0.15),
        y_title="Percent",
        x_ticks=x_ticks,
    )

    return dict(data=fig_data, layout=fig_layout)


def add_days_to_resolve_col(df):
    """
    Adds days to resolve the grievance column to given df

    Args:
        df: pandas dataframe with selected columns of grievance
        SQL table including date_of_resolution and
        date_grievance_received

    Returns:
         dict: contianging plotly figure data and layout information
    """
    df["days_to_resolve"] = (
        df["date_of_resolution"] - df["date_grievance_received"]
    ).dt.days
    df = df[df["days_to_resolve"] >= 0]

    return df


def time_to_resolve_hist(df, x_ticks):
    """
    Creates histogram graph of the time to resolve grievances

    Args:
        df: pandas dataframe with selected columns of grievance
        SQL table including date_of_resolution and
        date_grievance_received

    Returns:
         dict: contianging plotly figure data and layout information
    """

    df = add_days_to_resolve_col(df)

    y_max = np.histogram(df["days_to_resolve"], 9)[0][0]  # used to plot avg line
    avg_days = df["days_to_resolve"].mean()

    fig_data = [
        go.Histogram(
            x=df["days_to_resolve"],
            marker=dict(color=color_palette[0]),
            opacity=0.75,
            showlegend=False,
            nbinsx=10,
        ),
        go.Scatter(
            x=[avg_days, avg_days],
            y=[0, y_max],
            hoverinfo="none",
            name=f"Average Number of Days to Resolve ({round(avg_days,2)})",
            mode="lines",
            line={"color": color_palette[2], "width": 3, "dash": "dash"},
        ),
    ]

    fig_layout = build_scatter_layout(
        "Time to Resolve Grievance",
        0,
        y_max,
        legend=dict(orientation="h", y=-0.15),
        x_title="Number of Days",
        y_title="Number of Grievances",
        x_ticks=x_ticks,
    )

    return dict(data=fig_data, layout=fig_layout)


def time_to_resolve_avg(df, x__ticks):
    """
    Creates line graph graph of the time to resolve grievances

    Args:
        df: pandas dataframe with selected columns of grievance
        SQL table including date_of_resolution and
        date_grievance_received

    Returns:
         dict: contianging plotly figure data and layout information
    """

    df = add_days_to_resolve_col(df)

    plot_df = df.groupby("Freq").mean().reset_index()

    fig_data = [
        go.Scatter(
            x=plot_df["Freq"].astype(str),
            y=plot_df["days_to_resolve"],
            name="Average Number of Days to Resolve",
            mode="lines",
            line={"color": color_palette[1], "width": 3},
        )
    ]

    fig_layout = build_scatter_layout(
        "Avg. Time To Resolve Grievance",
        plot_df["days_to_resolve"].min(),
        plot_df["days_to_resolve"].max(),
        y_title="Number of Days",
        x_ticks=x__ticks,
    )

    return dict(data=fig_data, layout=fig_layout)


# dictionary of function used to create various
# graphs for the grievance data
griev_graphs = {
    "providers": update_griev_graph_pmpm,
    "types": update_griev_graph_pmpm,
    "category": update_griev_graph_pmpm,
    "providers_percent": update_griev_pie,
    "types__percent": update_griev_pie,
    "category__percent": update_griev_pie,
    "time_to_resolved": time_to_resolve_hist,
    "avg_time_to_resolved": time_to_resolve_avg,
    "written_oral_recieved": notifcation_graph,
}


def build_grievance_graphs(start_date, end_date, freq, col_group, center):
    """
    Uses griev_graphs dictionary to return the appropriate graph
    based on the user's selections

    Args:
        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        col_group: Column selection to group grievances by

        center: Name of PACE center


    Returns:
         dict: contianging plotly figure data and layout information
    """
    df = grievance_query(col_group, start_date, end_date, center, freq)

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if ((end_date.month - start_date.month) < 6) & (
        (end_date.year - start_date.year) < 1
    ):
        x_ticks = pd.Series(df["Freq"].astype(str).unique())
    else:
        x_ticks = pd.Series([])

    if col_group in ["providers", "types", "category"]:
        # start_date = df["date_grievance_received"].min()
        # end_date = df["date_grievance_received"].max() + pd.offsets.MonthEnd()

        if freq == "Q":
            pmpm_df = census_count_df(
                center, start_date, end_date, freq, quarter_pmpm=True
            )
        else:
            pmpm_df = census_count_df(center, start_date, end_date, freq)

        pmpm_df["Freq"] = pmpm_df["Freq"].dt.to_period(freq)

        return griev_graphs[col_group](df, freq, pmpm_df, x_ticks)
    return griev_graphs[col_group](df, x_ticks)


def trend_graph(start_date, end_date, freq, center):
    """
    Creates line graph of grievances pmpm for date range, filtered by center,
    and grouped by freq. Includes dash line at threshhold.

    Args:
        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        center: Name of PACE center

    Returns:
         dict: contianging plotly figure data and layout information
    """
    df = grievance_query("total", start_date, end_date, center, freq)

    plot_df = df.groupby("Freq").count().reset_index()
    plot_df.rename(columns={"date_grievance_received": "count"}, inplace=True)

    if freq == "Q":
        pmpm_df = census_count_df(center, start_date, end_date, freq, quarter_pmpm=True)
        plot_df["count"] = (plot_df["count"] / pmpm_df["Census"]) * 100
        fig_data = [
            go.Bar(
                x=plot_df["Freq"].astype(str),
                y=plot_df["count"],
                marker={"color": color_palette[0]},
                name="Grievances",
                showlegend=False,
            )
        ]
    else:
        pmpm_df = census_count_df(center, start_date, end_date, freq)

        plot_df["count"] = (plot_df["count"] / pmpm_df["Census"]) * 100
        fig_data = [
            go.Scatter(
                x=plot_df["Freq"].astype(str),
                y=plot_df["count"],
                mode="lines",
                line={"width": 7, "color": color_palette[0]},
                name="Grievances",
                showlegend=False,
            )
        ]

    fig_data.append(
        go.Scatter(
            x=plot_df["Freq"].astype(str),
            y=[7] * plot_df["Freq"].shape[0],
            mode="lines",
            line={"width": 3, "color": color_palette[6], "dash": "dash"},
            name="Threshold",
            hoverinfo="none",
        )
    )

    if plot_df["count"].max() <= 7:
        plot_max = 8
    else:
        plot_max = plot_df["count"].max()

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if ((end_date.month - start_date.month) < 6) & (
        (end_date.year - start_date.year) < 1
    ):
        x_ticks = plot_df["Freq"].astype(str)
    else:
        x_ticks = pd.Series([])

    fig_layout = build_scatter_layout(
        "Grievances Per 100MM",
        plot_df["count"].min(),
        plot_max,
        legend=dict(orientation="h", y=-0.15, font={"size": 9.5}),
        small_margins=True, x_ticks=x_ticks
    )

    return dict(data=fig_data, layout=fig_layout)


def total_grievances(start_date, end_date, center):
    """
    Calculates number of grievances in data range,
    filtered by center

    Args:
        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        center: Name of PACE center

    Returns:
        int: number of grievances 
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    join_sql = create_join_sql(center, "grievances")

    query = f"""
            SELECT COUNT(*) 
            FROM grievances
            {join_sql}
            WHERE date_grievance_received BETWEEN ? AND ?
            {center_sql};
            """
    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()
    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return result


def grievances_pmpm(start_date, end_date, center):
    num_grievances = total_grievances(start_date, end_date, center)
    pmpm_df = census_count_df(center, start_date, end_date, "M")

    griev_per_100 = (num_grievances / pmpm_df["Census"].sum()) * 100

    return round(griev_per_100, 2)


def most_common_griev_cat(start_date, end_date, center):
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    join_sql = create_join_sql(center, "grievances")

    query = f"""
            SELECT category_of_the_grievance, 
            COUNT(category_of_the_grievance) as value_count 
            FROM grievances
            {join_sql}
            WHERE date_grievance_received BETWEEN ? AND ?
            {center_sql}
            GROUP BY category_of_the_grievance
            ORDER BY value_count DESC
            LIMIT 1;
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()
    result = c.execute(query, params).fetchone()[0]
    conn.close()
    return result
