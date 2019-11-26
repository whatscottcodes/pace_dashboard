import sqlite3
import pandas as pd
import plotly.graph_objs as go
from .helper_functions import (
    sql_return_df,
    db_filepath,
    create_center_sql,
    create_join_sql,
    build_bar_layout,
    build_scatter_layout)
from .settings import color_palette

from .enrollment_eda_utils import census_count_df
import textwrap
from pandas.core.groupby.groupby import DataError
from titlecase import titlecase


#options for utilization drop down
utilization_table_types = [
                                                    {
                                                        "label": "Inpatient",
                                                        "value": "acute",
                                                    },
                                                    {
                                                        "label": "Inpatient - Psych",
                                                        "value": "psych",
                                                    },
                                                    {
                                                        "label": "ER Only",
                                                        "value": "er_only",
                                                    },
                                                    {
                                                        "label": "Custodial",
                                                        "value": "custodial",
                                                    },
                                                    {
                                                        "label": "Respite",
                                                        "value": "respite",
                                                    },
                                                    {
                                                        "label": "Skilled",
                                                        "value": "skilled",
                                                    },
                                                ]

# set columns from each dataset, this could be done automatically,

filter_cols = [
    {"label": "Hospital/Facility", "value": "facility"},
    {"label": "Admit Reason", "value": "admit_reason"},
    {"label": "Discharge Reason", "value": "discharge_disposition"},
    {"label": "Day of the Week", "value": "dow"},
    {"label": "Enrolled within 6 Months", "value": "w_six_months"},
]

binary_filters = ["w_six_months"]

filter_cols_snf = [
    {"label": "Hospital/Facility", "value": "facility"},
    {"label": "Admit_reason", "value": "admit_reason"},
    {"label": "Enrolled within 6 Months", "value": "w_six_months"},
]

additional_filter_options = [
    {"label": "Monday", "value": "Monday"},
    {"label": "Tuesday", "value": "Tuesday"},
    {"label": "Wednesday", "value": "Wednesday"},
    {"label": "Thursday", "value": "Thursday"},
    {"label": "Friday", "value": "Friday"},
    {"label": "Saturday", "value": "Saturday"},
    {"label": "Sunday", "value": "Sunday"},
    {"label": "Within 6 Months", "value": "6_mo"}
]

# set corresponding columns to the return value for the second filter drop down
additonal_filter_cols = {
    "Monday": "dow",
    "Tuesday": "dow",
    "Wednesday": "dow",
    "Thursday": "dow",
    "Friday": "dow",
    "Saturday": "dow",
    "Sunday": "dow",
    "6_mo": "w_six_months",
    "Skilled": "admit_reason",
    "Custodial": "admit_reason",
    "Respite": "admit_reason",
    None: None
}


def create_filter_sql(cols, filter_col_index, filter_val, additional_filter, params):
    """
    Creates SQL statements to filter a table based on
    filters selected by the user.

    Args:
        cols: List of column names to be included in the SQL query

        filter_col_index: col list index corresponding to the column
            to be used to filter the table

        filter_val: value in the filter column used to filter the table

        additional_filter: additional filter select by the user,
            corresponding column in table got using additional_filter_cols dict

        params: list of parameters for the parameterized query

    Returns:
        filter_value_sql: string containing SQL statements that can be added
        to a query to filter the results using the user input filters

        params: list of parameters for the parameterized query with necessary
            filter parameters added
    """
    if filter_val is not None:
        filter_value_sql = f"""AND {cols[filter_col_index]} = ?"""
        params.extend([f"{filter_val}"])
    else:
        filter_value_sql = ""

    if additional_filter is not None:
        adtl_filter_col = additonal_filter_cols[additional_filter]
        cols.extend([adtl_filter_col])
        filter_value_sql += f""" AND {adtl_filter_col} = ?"""

        if additional_filter in ["6_mo", "oc", "ss", "visit"]:
            params.extend([f"{1.0}"])
        else:
            params.extend([f"{additional_filter}"])
    return filter_value_sql, params


def build_visit_query(
    utl_type,
    date_type,
    cols,
    center,
    start_date,
    end_date,
    freq,
    col_filter,
    additional_filter,
):
    """
    Creates dataframe of specific utilization related visits.

    Args:
        utl_type: type of utilization user is looking for.
            Current values are inpatient, inpatient_psych, er,
            er_only and inpatient_snf.
            Should match up to tables in database, but inpatient psych is not
            currently it's own table. Handled using an if statement below.

        date_type: Specifies where to use Admission or Discharge
            date to count visits.

        cols: List of column names to be included in the SQL query.

        center: Name of PACE center

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        col_filter: column to be used to filter the table, can be None.
            If not None, dataframe will break out visits by the values
            in the columns.
            i.e.; by hospital dx, or other column selected

        additional_filter: additional filters selected by the user, can be None
            First filter will be a specific value from the filter column,
            second can be an additional filter corresponding to a different column.
            These value column pairs are in additonal_filter_cols

    Returns:
        df: dataframe of visit data to be used for plotting
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    filter_value_sql, params = create_filter_sql(
        cols, 1, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, utl_type)

    if utl_type == "er":
        query = f"""
            SELECT *
            FROM (SELECT {', '.join(col for col in cols if col!=None)} FROM er_only
            UNION ALL
            SELECT {', '.join(col for col in cols if col!=None)} FROM acute
            WHERE acute.er = 1) AS U
            {join_sql}
            WHERE U.{date_type} BETWEEN ? AND ?
            {filter_value_sql}
            {center_sql};
            """

    else:
        query = f"""
            SELECT {', '.join(col for col in cols if col!=None)}
            FROM {utl_type}
            {join_sql}
            WHERE {date_type} BETWEEN ? AND ?
            {filter_value_sql}
            {center_sql};
            """

    df = sql_return_df(query, params, [date_type])
    df['date_bby'] = df[date_type].copy()
    df[date_type] = df[date_type].dt.to_period(freq[0])
    df["count"] = 1
    return df


def build_los_query(
    utl_type, cols, center, start_date, end_date, freq, col_filter, additional_filter
):
    """
    Creates dataframe of specific utilization related length of stay data.

    Args:
        utl_type: type of utilization user is looking for.
            Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
            Should match up to tables in database, but inpatient psych is not currently
            it's own table. Handled using an if statement below.

        date_type: Specifies where to use Admission or Discharge date to count visits.

        cols: List of column names to be included in the SQL query.

        center: Name of PACE center

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        freq: M or Q, determines if results should be grouped by month or quarter

        col_filter: column to be used to filter the table, can be None.
            If not None, dataframe will break out visits by the values in the columns.
            i.e.; by hospital dx, or other column selected

        additional_filter: additional filters selected by the user, can be None
            First filter will be a specific value from the filter column, second can
            be an additional filter corresponding to a different column. These value
            column pairs are in additonal_filter_cols

    Returns:
        df: dataframe of length of stay data to be used for plotting
    """

    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    sql_cols = cols.copy()
    sql_cols.append("los")

    if (utl_type == "er_only"):
        utl_type = "acute"
        admission_sql = "AND er = 1"
    else:
        admission_sql = ''

    filter_value_sql, params = create_filter_sql(
        sql_cols, 1, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, utl_type)

    query = f"""
            SELECT {', '.join(col for col in sql_cols if col!=None)}
            FROM {utl_type}
            {join_sql}
            WHERE discharge_date BETWEEN ? AND ?
            {filter_value_sql}
            {center_sql};
            """
    df = sql_return_df(query, params, ["discharge_date"])
    df["discharge_date"] = df["discharge_date"].dt.to_period(freq[0])

    return df


def build_readmit_query(
    utl_type, cols, center, start_date, end_date, freq, col_filter, additional_filter
):
    """
     Creates dataframe of specific utilization related 30 day readmission data.

     Args:
         utl_type: type of utilization user is looking for.
             Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
             Should match up to tables in database, but inpatient psych is not currently
             it's own table. Handled using an if statement below.

         date_type: Specifies where to use Admission or Discharge date to count visits.

         cols: List of column names to be included in the SQL query.

         center: Name of PACE center

         start_date: First date to include in resulting dataframe

         end_date: Last date to include in resulting dataframe

         freq: M or Q, determines if results should be grouped by month or quarter

         col_filter: column to be used to filter the table, can be None.
             If not None, dataframe will break out visits by the values in the columns.
             i.e.; by hospital dx, or other column selected

         additional_filter: additional filters selected by the user, can be None
             First filter will be a specific value from the filter column, the second value
             can be None or be a value from a column different from the filter column.
             These value column pairs are found in the additonal_filter_cols dictionary

     Returns:
         df: dataframe of 30 day readmission data to be used for plotting
     """

    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    sql_cols = cols.copy()
    sql_cols.append("days_since_last_admission")

    filter_value_sql, params = create_filter_sql(
        sql_cols, 1, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, utl_type)

    query = f"""
        SELECT {', '.join(col for col in sql_cols if col!=None)}
        FROM {utl_type}
        {join_sql}
        WHERE admission_date BETWEEN ? AND ?
        AND days_since_last_admission <= 30
        {filter_value_sql}
        {center_sql};
        """
    df = sql_return_df(query, params, ["admission_date"])
    df["admission_date"] = df["admission_date"].dt.to_period(freq[0])
    df["count"] = 1

    return df


def col_order(utl_type, cols, center, start_date, end_date, freq, additional_filters=[None, None]):
    """
    Creates list with column names in the order they should be plotted. Allows colors to match from one
    graph to another.

    Args:
        *args: Should contain utl_type, cols, center, params, *additional_filters

        utl_type: type of utilization user is looking for.
            Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
            Should match up to tables in database, but inpatient psych is not currently
            it's own table. Handled using an if statement below.

        cols: List of column names that were included in the SQL query and will now be plotted

        center: Name of PACE center

        params: list of parameters for the parameterized query
        
        freq: M or Q, determines if results should be grouped by month or quarter

        additional_filter: additional filters selected by the user, can be None
            First filter will be a specific value from the filter column, second can
            be an additional filter corresponding to a different column. These value
            column pairs are in additonal_filter_cols

    Returns:
        plot_cols: list of column names in order they were plotted in the visit graph
    """

    if (utl_type == "er_only") or (utl_type == "er"):
        cols = ["admission_date"] + cols[1:]

    df = build_visit_query(
        utl_type,
        cols[0],
        cols,
        center,
        start_date,
        end_date,
        freq,
        additional_filters[0],
        additional_filters[1],
    )
    df["count"] = 1

    plot_df = df.groupby(cols).sum()["count"].unstack(0).T.reset_index()
    plot_cols = (
        plot_df.sum(numeric_only=True).sort_values(ascending=False)
    ).index.tolist()

    return plot_cols


# GRAPHS


def filter_col_df_sum(cols, filter_col, additional_filters, df, summary_col):
    """
      Creates dataframe for plotting utilization data grouped by the cols using the sum function
      and a list of columns to be included in the plot

      Args:
          cols: List of column names to be included in the SQL query.

          col_filter: column to be used to filter the table, can be None.
              If not None, dataframe will break out visits by the values in the columns.
              i.e.; by hospital dx, or other column selected

          additional_filter: additional filters selected by the user, can be None
              First filter will be a specific value from the filter column, the second value
              can be None or be a value from a column different from the filter column.
              These value column pairs are found in the additional_filter_cols dictionary

          df: dataframe to be grouped and filtered

          summary_col: column to be summed in group by

      Returns:
          plot_df: grouped dataframe for plotting
          plot_cols: column of the dataframe to be included in plot
      """
    if ((filter_col is not None) and (additional_filters[1] is not None)) or (
        filter_col is None
    ):
        plot_df = df.groupby(cols).sum()[summary_col].reset_index()

    elif filter_col is not None:
        plot_df = df.groupby(cols).sum()[summary_col].unstack(0).T.reset_index()
    return plot_df


def filter_col_df_mean(cols, filter_col, additional_filters, df, summary_col):
    """
    Creates dataframe for plotting utilization data grouped by the cols using the sum function
    and a list of columns to be included in the plot

    Args:
        cols: List of column names to be included in the SQL query.

        col_filter: column to be used to filter the table, can be None.
            If not None, dataframe will break out visits by the values in the columns.
            i.e.; by hospital dx, or other column selected

        additional_filter: additional filters selected by the user, can be None
            First filter will be a specific value from the filter column, the second value
            can be None or be a value from a column different from the filter column.
            These value column pairs are found in the additional_filter_cols dictionary

        df: dataframe to be grouped and filtered

        summary_col: column to be summed in group by

    Returns:
        plot_df: grouped dataframe for plotting
        plot_cols: column of the dataframe to be included in plot
    """
    if ((filter_col != None) and (additional_filters[1] != None)) or (
        filter_col == None
    ):
        plot_df = df.groupby(cols).mean()[summary_col].reset_index()

    elif filter_col != None:
        plot_df = df.groupby(cols).mean()[summary_col].unstack(0).T.reset_index()

    return plot_df


def filter_col_df(
    cols,
    filter_col,
    additional_filters,
    df,
    summary_col,
    amnt,
    groupby_mean=False,
    set_col_order=False,
    *args,
):
    """
      Creates dataframe for plotting utilization data grouped by the cols using the sum function
      and a list of columns to be included in the plot

      Args:
          cols: List of column names to be included in the SQL query.

          col_filter: column to be used to filter the table, can be None.
              If not None, dataframe will break out visits by the values in the columns.
              i.e.; by hospital dx, or other column selected

          additional_filter: additional filters selected by the user, can be None
              First filter will be a specific value from the filter column, the second value
              can be None or be a value from a column different from the filter column.
              These value column pairs are found in the additional_filter_cols dictionary

          df: dataframe to be grouped and filtered

          summary_col: column to be summed in group by

          amnt: Number of columns to be included in the plot, can be 5, 10, or all

          groupby_mean: Default to False, if True, groupby uses mean() instead of sum()

          set_col_order: Default to False, if True, col_order is called, so the order of
              this plot_cols matches the order of the plot_cols from the visit graph.

          *args: parameters for col_order, should be utl_type, cols, center, start_date,
            end_date, freq, and *additional_filters

    Returns:
          plot_df: grouped dataframe for plotting
          plot_cols: column of the dataframe to be included in plot
    """
    try:
        if groupby_mean:
            plot_df = filter_col_df_mean(
                cols, filter_col, additional_filters, df, summary_col
            )
        else:
            plot_df = filter_col_df_sum(
                cols, filter_col, additional_filters, df, summary_col
            )
    except DataError:
        plot_df = pd.DataFrame()
    if set_col_order:
        plot_cols = col_order(*args)
        plot_cols = [col for col in plot_cols if col in plot_df.columns]
    else:
        plot_cols = (
            plot_df.sum(numeric_only=True).sort_values(ascending=False)
        ).index.tolist()

    if amnt != "all":
        plot_cols = plot_cols[: int(amnt)]

    return plot_df, plot_cols


def add_total_to_plotdf(total_df, plot_df, date_type, freq):
    """
      Merges plot_df with a df containing the total visits for each month of quarter.
      Allows for easy plotting of the percent of visits corresponding to a filter

      Args:
          total_df: dataframe of visits during the selected date range

          plot_df: dataframe created using utilization type, data range, and user filters

          date_type: Specifies where Admission or Discharge date was used to count visits.

          freq: M or Q, determines if total_df should be grouped by month or quarter

      Returns:
          plot_df: plot_df now including a total row for the the total visits
              in the period.
    """
    total_df = total_df.groupby(date_type).sum()["count"].reset_index()
    total_df.rename(columns={'count':'total_count'}, inplace=True)
    return plot_df.merge(total_df, on=date_type, how="left")


def update_visit_graph(
    start_date,
    end_date,
    utl_type,
    date_type,
    filter_col,
    amnt,
    freq,
    center,
    graph_type,
    *additional_filters,
):
    """
     Plots a bar graph of the percent of visits related to each filter or a bar graph of the visit counts
     if no filters are selected

     Args:
         start_date: First date to include in plotting dataframe

         end_date: Last date to include in plotting dataframe

         utl_type: type of utilization user is looking for.
             Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
             Should match up to tables in database, but inpatient psych is not currently
             it's own table. Handled using an if statement in query function

         date_type: Specifies if Admission or Discharge date is being used to count visits.

         filter_col: column to be used to filter the table, can be None.

         amnt: Number of columns to be included in the plot, can be 5, 10, or all 

         freq: M or Q, determines if total_df should be grouped by month or quarter

         center: Name of PACE center

         additional_filters: additional filter value selected by the user, can be None.
             Will be a value from a column different from the filter column.
             These value column pairs are found in the additional_filter_cols dictionary

     Returns:
         dict: containing plotly figure data and layout information
    """
    filtered_flag = filter_col != None
    bar_flag = graph_type == 'bar'
    if bar_flag:
        chart_func = go.Bar
    else:
        chart_func = go.Scatter

    if (utl_type == "er_only") or (utl_type == "er"):
        date_type = "admission_date"

    cols = [date_type]

    if filtered_flag:
        cols.extend([filter_col])
    df = build_visit_query(
        utl_type,
        date_type,
        cols,
        center,
        start_date,
        end_date,
        freq,
        additional_filters[0],
        additional_filters[1],
    )

    if df.empty:
        return dict(data=[], layout=build_bar_layout("Utilization Visits"))

    plot_df, plot_cols = filter_col_df(
        cols, filter_col, additional_filters, df, "count", amnt
    )

    if filtered_flag:
        total_df = build_visit_query(
            utl_type, date_type, cols, center, start_date, end_date, freq, None, None
        )
        plot_df = add_total_to_plotdf(total_df, plot_df, date_type, freq)

        if filter_col in binary_filters:
            legend_names = [
                "Yes" if col == 1.0 else "No" if col == 0.0 else col for col in plot_cols
            ]
        else:
            legend_names = plot_cols

        fig_data = [
                chart_func(
                    x=plot_df[date_type].astype(str),
                    y=round((plot_df[col] / plot_df["total_count"]) * 100, 2),
                    name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                    text=[f"{p}%({v})" for p, v in zip(round((plot_df[col] / plot_df["total_count"]) * 100, 2), plot_df[col])],
                    hoverinfo="x+name+text",
                    marker=dict(color=color),
                )
                for col, name, color in zip(plot_cols, legend_names, color_palette)
            ]
        legend = dict(orientation="h", y=-0.15, font={"size": 9.5})
        y_title = 'Percent'
        df_min = 0
        df_max = 100
    else:
        fig_data = [
                chart_func(
                    x=plot_df[date_type].astype(str),
                    y=plot_df[col],
                    hoverinfo="x+y",
                    marker=dict(color=color),
                )
                for col, color in zip(plot_cols, color_palette)
            ]
        legend = {}
        y_title = 'Visits'
        df_min = min(plot_df[plot_cols].min().values)
        df_max = max(plot_df[plot_cols].max().values)

    if ((end_date.month - start_date.month) < 6) & ((end_date.year - start_date.year) < 1) & (freq != 'Q'):
        x_ticks = plot_df[date_type].astype(str)
    else:
        x_ticks = pd.Series([])

    if filtered_flag:
        col_filter_text = " ".join(filter_col.split("_")).title()
        if additional_filters[0] is None:
            filter_title = f" by {col_filter_text}"
        else:
            filter_title = f" for {additional_filters[0]}({col_filter_text})"
    else:
        filter_title = ''
    title_date = date_type.split("_")[0].title()
    
    if bar_flag:
        fig_layout = build_bar_layout(f"{utl_type.title()} {title_date}s{filter_title}", legend = legend, y_title=y_title, x_ticks=x_ticks)
    else:
        fig_layout = build_scatter_layout(f"{utl_type.title()} {title_date}s{filter_title}", df_min, df_max, x_ticks=x_ticks, legend=legend, y_title=y_title)
    return dict(data=fig_data, layout=fig_layout)


def update_los_graph(
    start_date, end_date, utl_type, filter_col, amnt, freq, center, graph_type, *additional_filters
):
    """
     Plots a scatter plot of the alos monthly and separated by filter if filters are provided. Plots a bar graph
     if the frequency is set to quarterly. 

     Args:
         start_date: First date to include in plotting dataframe

         end_date: Last date to include in plotting dataframe

         utl_type: type of utilization user is looking for.
             Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
             Should match up to tables in database, but inpatient psych is not currently
             it's own table. Handled using an if statement in query function

         filter_col: column to be used to filter the table, can be None.

         amnt: Number of columns to be included in the plot, can be 5, 10, or all

         freq: M or Q, determines if total_df should be grouped by month or quarter

         center: Name of PACE center

         additional_filters: additional filter value selected by the user, can be None.
             Will be a value from a column different from the filter column.
             These value column pairs are found in the additonal_filter_cols dictionary

     Returns:
         dict: containing plotly figure data and layout information
    """
    filtered_flag = filter_col != None
    bar_flag = graph_type == 'bar'
    if bar_flag:
        chart_func = go.Bar
    else:
        chart_func = go.Scatter
    cols = ["discharge_date"]

    if filtered_flag:
        cols.extend([filter_col])

    df = build_los_query(
        utl_type,
        cols,
        center,
        start_date,
        end_date,
        freq,
        additional_filters[0],
        additional_filters[1],
    )
    if df.empty:
        return dict(data=[], layout=build_bar_layout("Utilization Visits"))

    if filtered_flag:
        col_order_args = (
            utl_type,
            cols,
            center,
            start_date,
            end_date,
            freq,
            additional_filters,
        )
        set_col_order = True
    else:
        col_order_args = []
        set_col_order = False

    plot_df, plot_cols = filter_col_df(
        cols,
        filter_col,
        additional_filters,
        df,
        "los",
        amnt,
        True,
        set_col_order,
        *col_order_args,
    )


    if filter_col in binary_filters:
        legend_names = [
            "Yes" if col == 1.0 else "No" if col == 0.0 else col for col in plot_cols
        ]
    else:
        legend_names = plot_cols

    if ((end_date.month - start_date.month) < 6) & ((end_date.year - start_date.year) < 1) & (freq != 'Q'):
        x_ticks = plot_df['discharge_date'].astype(str)
    else:
        x_ticks = pd.Series([])

    if (freq == "Q") | filtered_flag:
        if additional_filters[1]:
            fig_data = [
                chart_func(
                    x=plot_df["discharge_date"].astype(str),
                    y=plot_df['los'],
                    name='<br>'.join(textwrap.wrap(titlecase(additional_filters[0]), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color_palette[0]),
                )
            ]
            legend = dict(orientation="h", y=-0.15, font={"size": 9.5})

        else:
            fig_data = [
                chart_func(
                    x=plot_df["discharge_date"].astype(str),
                    y=plot_df[col],
                    name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color),
                )
                for col, name, color in zip(plot_cols, legend_names, color_palette)
            ]
            legend = dict(orientation="h", y=-0.15, font={"size": 9.5})
    
    else:
        fig_data = [
            chart_func(
                x=plot_df["discharge_date"].astype(str),
                y=plot_df[col],
                name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                hoverinfo="x+name+y",
                marker=dict(color=color),
            )
            for col, name, color in zip(plot_cols, legend_names, color_palette)
        ]
        legend = {}
    if bar_flag:
        fig_layout = build_bar_layout("ALOS", legend = legend, x_ticks=x_ticks)

    else:
        df_min = min(plot_df[plot_cols].min().values)
        df_max = max(plot_df[plot_cols].max().values)

        fig_layout = build_scatter_layout("ALOS", df_min, df_max, legend=legend, x_ticks=x_ticks)

    return dict(data=fig_data, layout=fig_layout)


def update_readmit_graph(
    start_date, end_date, utl_type, filter_col, amnt, freq, center, graph_type, *additional_filters
):
    """
     Plots a scatter plot of the number of 30-day readmits in a month, separated by filter if filters are provided. Plots a bar graph
     if the frequency is set to quarterly.

     Args:
         start_date: First date to include in plotting dataframe

         end_date: Last date to include in plotting dataframe

         utl_type: type of utilization user is looking for.
             Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
             Should match up to tables in database, but inpatient psych is not currently
             it's own table. Handled using an if statement in query function

         filter_col: column to be used to filter the table, can be None.

         amnt: Number of columns to be included in the plot, can be 5, 10, or all

         freq: M or Q, determines if total_df should be grouped by month or quarter

         center: Name of PACE center

         additional_filters: additional filter value selected by the user, can be None.
             Will be a value from a column different from the filter column.
             These value column pairs are found in the additonal_filter_cols dictionary

     Returns:
         dict: containing plotly figure data and layout information
    """
    filtered_flag = filter_col != None
    bar_flag = graph_type == 'bar'
    if bar_flag:
        chart_func = go.Bar
    else:
        chart_func = go.Scatter
    cols = ["admission_date"]

    if filtered_flag:
        cols.extend([filter_col])

    df = build_readmit_query(
        utl_type,
        cols,
        center,
        start_date,
        end_date,
        freq,
        additional_filters[0],
        additional_filters[1],
    )
    if df.empty:
        return dict(data=[], layout=build_bar_layout("Utilization Visits"))

    if filtered_flag:
        col_order_args = (
            utl_type,
            cols,
            center,
            start_date,
            end_date,
            freq,
            additional_filters,
        )
        set_col_order = True
    else:
        col_order_args = []
        set_col_order = False

    plot_df, plot_cols = filter_col_df(
        cols,
        filter_col,
        additional_filters,
        df,
        "count",
        amnt,
        False,
        set_col_order,
        *col_order_args,
    )

    if filter_col in binary_filters:
        legend_names = [
            "Yes" if col == 1.0 else "No" if col == 0.0 else col for col in plot_cols
        ]
    else:
        legend_names = plot_cols

    if (freq == "Q") | filtered_flag:
        if additional_filters[1]:
            fig_data = [
                chart_func(
                    x=plot_df["admission_date"].astype(str),
                    y=plot_df['count'],
                    name='<br>'.join(textwrap.wrap(
                       titlecase(additional_filters[0]), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color_palette[0]),
                )
            ]
            legend = dict(orientation="h", y=-0.15, font={"size": 9.5})
        else:
            fig_data = [
                chart_func(
                    x=plot_df["admission_date"].astype(str),
                    y=plot_df[col],
                    name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color),
                )
                for col, name, color in zip(plot_cols, legend_names, color_palette)
                if col != 0
            ]  
            legend = dict(orientation="h", y=-0.15, font={"size": 9.5})
    else:
        fig_data = [
            chart_func(
                x=plot_df["admission_date"].astype(str),
                y=plot_df[col],
                name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                marker=dict(color=color),
            )
            for col, name, color in zip(plot_cols, legend_names, color_palette)
        ]
        legend = {}
    
    if bar_flag:
        fig_layout = build_bar_layout('30 Day Readmits', legend=legend)
    else:
        df_min = min(plot_df[plot_df.columns[1:]].min().values)
        df_max = max(plot_df[plot_df.columns[1:]].max().values)
        fig_layout = build_scatter_layout('30 Day Readmits', 
            df_min,
            df_max,
            legend=legend)

    return dict(data=fig_data, layout=fig_layout)
