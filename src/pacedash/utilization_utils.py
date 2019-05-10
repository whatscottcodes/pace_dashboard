import sqlite3
import pandas as pd
import plotly.graph_objs as go
from .helpers_configs import (
    sql_return_df,
    db_filepath,
    color_palette,
    create_center_sql,
    create_join_sql,
    build_bar_layout,
    build_scatter_layout)
from .census_utils import census_count_df
import textwrap
from pandas.core.groupby.groupby import DataError
from titlecase import titlecase
# utilization card titles change based on the type of utlization selected
# some summary statistics would not make sense for certain utilizations

utilization_table_types = [
                                                    {
                                                        "label": "Inpatient",
                                                        "value": "inpatient",
                                                    },
                                                    {
                                                        "label": "Inpatient - Psych",
                                                        "value": "inpatient_psych",
                                                    },
                                                    {
                                                        "label": "ER",
                                                        "value": "er",
                                                    },
                                                    {
                                                        "label": "ER Only",
                                                        "value": "er_only",
                                                    },
                                                    {
                                                        "label": "SNF",
                                                        "value": "inpatient_snf",
                                                    },
                                                ]
card_one_titles = {
    "inpatient": "Admissions",
    "inpatient_psych": "Admissions",
    "er_only": "Visits",
    "er": "Visits",
    "inpatient_snf": "Admissions",
}

card_two_titles = {
    "inpatient": "Discharges",
    "inpatient_psych": "Discharges",
    "er_only": "% of ER Visits",
    "er": "ER to Inpatient",
    "inpatient_snf": "Discharges",
}

card_three_titles = {
    "inpatient": "LOS per 100MM",
    "inpatient_psych": "LOS per 100MM",
    "er_only": "Observation",
    "er": "Admission Rate",
    "inpatient_snf": "Cust. Days 100MM",
}

# card four title does not change based on utilization type,
# always 30-day Readmit

card_five_titles = {
    "inpatient": "Total Readmits",
    "inpatient_psych": "Total Readmits",
    "er_only": "Total Readmits",
    "er": "Total Readmits",
    "inpatient_snf": "Skilled Days 100MM",
}

card_six_titles = {
    "inpatient": "ALOS",
    "inpatient_psych": "ALOS",
    "er_only": "ALOS for Inpatient",
    "er": "ALOS for Inpatient",
    "inpatient_snf": "Respite Days 100MM",
}

# dictionary of card title dictionaries to avoid importing
# all individual dicts into utlization page
# key: card number, value: dictionary containing
# utlization type:card title pairs

card_titles = {
    1: card_one_titles,
    2: card_two_titles,
    3: card_three_titles,
    5: card_five_titles,
    6: card_six_titles,
}

# set columns from each dataset, this could be done automatically,
# as it is in incidents, if this dataset had better column names

filter_cols = [
    {"label": "Hospital/Facility", "value": "facility"},
    {"label": "Discharge Dx", "value": "discharge_dx"},
    {"label": "PACE Reason", "value": "reason"},
    {"label": "Admit Reason", "value": "admit_reason"},
    {"label": "Discharge Reason", "value": "discharge_reason"},
    {"label": "Preventable", "value": "preventable"},
    {"label": "Day of the Week", "value": "dow"},
    {"label": "Time of Day", "value": "time"},
    {"label": "Admitted From", "value": "admitted_from"},
    {"label": "Admitted From (details)", "value": "admitting_facility"},
    {"label": "Days Since MD", "value": "days_MD"},
    {"label": "Related To", "value": "related"},
    {"label": "Living Situation", "value": "living_situation"},
    {"label": "Enrolled within 6 Months", "value": "w_six_months"},
    {"label": "PACE Aware of S/S", "value": "aware_ss"},
    {"label": "PACE Aware of Visit Prior", "value": "aware_visit"},
]

binary_filters = ["preventable", "w_six_months", "aware_ss", "aware_visit"]

filter_cols_snf = [
    {"label": "Hospital/Facility", "value": "facility"},
    {"label": "Admit_reason", "value": "admit_reason"},
    {"label": "Enrolled within 6 Months", "value": "w_six_months"},
]

additional_filter_options = [
    {"label": "11P-8A", "value": "11P-8A"},
    {"label": "8A-5P", "value": "8A-5P"},
    {"label": "5P-11P", "value": "5P-11P"},
    {"label": "Monday", "value": "Monday"},
    {"label": "Tuesday", "value": "Tuesday"},
    {"label": "Wednesday", "value": "Wednesday"},
    {"label": "Thursday", "value": "Thursday"},
    {"label": "Friday", "value": "Friday"},
    {"label": "Saturday", "value": "Saturday"},
    {"label": "Sunday", "value": "Sunday"},
    {"label": "Alone", "value": "Alone"},
    {"label": "Family", "value": "Family"},
    {"label": "Staff", "value": "Staff"},
    {"label": "Within 6 Months", "value": "6_mo"},
    {"label": "Sent By OC", "value": "oc"},
    {"label": "Aware of S/S", "value": "ss"},
    {"label": "Aware of Visit", "value": "visit"},
    {"label": "Preventable", "value": 1},
]

additional_filter_options_snf = [
    {"label": "Skilled", "value": "skilled"},
    {"label": "Custodial", "value": "custodial"},
    {"label": "Respite", "value": "respite"},
]

# set corresponding columns to the return value for the second filter drop down
additonal_filter_cols = {
    "11P-8A": "time",
    "8A-5P": "time",
    "5P-11P": "time",
    "Unknown": "time",
    "Monday": "dow",
    "Tuesday": "dow",
    "Wednesday": "dow",
    "Thursday": "dow",
    "Friday": "dow",
    "Saturday": "dow",
    "Sunday": "dow",
    "Alone": "living_situation",
    "Family": "living_situation",
    "Staff": "living_situation",
    "6_mo": "w_six_months",
    "oc": "sent_by_oc",
    "ss": "aware_ss",
    "visit": "aware_visit",
    "Preventable/Avoidable": "preventable",
    "Skilled": "admit_reason",
    "Custodial": "admit_reason",
    "Respite": "admit_reason",
    None: None
}

# admission sql line based on utlization type
# created to cut down on if/then statements
admission_sql_dict = {
    "inpatient_er": "AND er = 1",
    "inpatient": "AND admission_type = 'Acute Hospital'",
    "inpatient_psych": "AND admission_type = 'Psych Unit / Facility'",
    "inpatient_snf": "",
    "er": "",
    "er_only": "",
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
            corresponding column in table got using additonal_filter_cols dict

        params: list of paremeters for the parameterized query

    Returns:
        filter_value_sql: string containing SQL statements that can be added
        to a query to filter the results using the user input filters

        params: list of paremeters for the parameterized query with necessary
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
    Creates dataframe of specific utlization related visits.

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

        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        col_filter: column to be used to filter the table, can be None.
            If not None, dateframe will break out visits by the values
            in the columns.
            ie; by hospital dx, or other column selected

        additional_filter: additional filters selected by the user, can be None
            First filter will be a specific value from the filter column,
            second can be an additional filter corresponding to a different column.
            These value column pairs are in additonal_filter_cols

    Returns:
        df: dataframe of visit data to be used for plotting
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

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
            SELECT {', '.join(col for col in cols if col!=None)} FROM inpatient
            WHERE inpatient.er = 1) AS U
            {join_sql}
            WHERE U.{date_type} BETWEEN ? AND ?
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    else:
        query = f"""
            SELECT {', '.join(col for col in cols if col!=None)}
            FROM {utl_type}
            {join_sql}
            WHERE {date_type} BETWEEN ? AND ?
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    df = sql_return_df(query, params, [date_type])
    df['date_bby'] = df[date_type].copy()
    df[date_type] = df[date_type].dt.to_period(freq)
    df["count"] = 1
    return df


def build_los_query(
    utl_type, cols, center, start_date, end_date, freq, col_filter, additional_filter
):
    """
    Creates dataframe of specific utlization related length of stay data.

    Args:
        utl_type: type of utilization user is looking for.
            Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
            Should match up to tables in database, but inpatient psych is not currently
            it's own table. Handled using an if statement below.

        date_type: Specifies where to use Admission or Discharge date to count visits.

        cols: List of column names to be included in the SQL query.

        center: Name of PACE center

        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        freq: M or Q, determines if results should be grouped by month or quarter

        col_filter: column to be used to filter the table, can be None.
            If not None, dateframe will break out visits by the values in the columns.
            ie; by hospital dx, or other column selected

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

    if (utl_type == "er_only") or (utl_type == "er"):
        utl_type = "inpatient"
        admission_sql = admission_sql_dict["inpatient_er"]
    else:
        admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

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
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """
    df = sql_return_df(query, params, ["discharge_date"])
    df["discharge_date"] = df["discharge_date"].dt.to_period(freq)

    return df


def build_readmit_query(
    utl_type, cols, center, start_date, end_date, freq, col_filter, additional_filter
):
    """
     Creates dataframe of specific utlization related 30 day readmission data.

     Args:
         utl_type: type of utilization user is looking for.
             Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
             Should match up to tables in database, but inpatient psych is not currently
             it's own table. Handled using an if statement below.

         date_type: Specifies where to use Admission or Discharge date to count visits.

         cols: List of column names to be included in the SQL query.

         center: Name of PACE center

         start_date: First date to include in resulting dateframe

         end_date: Last date to include in resulting dateframe

         freq: M or Q, determines if results should be grouped by month or quarter

         col_filter: column to be used to filter the table, can be None.
             If not None, dateframe will break out visits by the values in the columns.
             ie; by hospital dx, or other column selected

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

    if (utl_type == "er_only") or (utl_type == "er"):
        utl_type = "inpatient"
        admission_sql = admission_sql_dict["inpatient_er"]
    else:
        admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

    query = f"""
        SELECT {', '.join(col for col in sql_cols if col!=None)}
        FROM {utl_type}
        {join_sql}
        WHERE admission_date BETWEEN ? AND ?
        AND days_since_last_admission <= 30
        {admission_sql}
        {filter_value_sql}
        {center_sql};
        """
    df = sql_return_df(query, params, ["admission_date"])
    df["admission_date"] = df["admission_date"].dt.to_period(freq)
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

        params: list of paremeters for the parameterized query
        
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


# CARDS


def admits_discharges(
    utl_type,
    date_type,
    center,
    start_date,
    end_date,
    filter_col,
    col_filter,
    additional_filter,
):
    """
    Calculates number of admissions or discharges of a utlization type in a given date range and filtered by selected
    user filters

    Args:
        utl_type: type of utilization user is looking for.
            Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
            Should match up to tables in database, but inpatient psych is not currently
            it's own table. Handled using an if statement below

        date_type: Specifies if Admission or Discharge date is being used to count visits.

        center: Name of PACE center

        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        filter_col: column to be used to filter the table, can be None.

        col_filter: value in the filter column to filter the table by.

        additional_filter: additional filter value selected by the user, can be None.
            Will be a value from a column different from the filter column.
            These value column pairs are found in the additonal_filter_cols dictionary

    Returns:
        int: number of admissions or discharges
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

    filter_value_sql, params = create_filter_sql(
        [filter_col], 0, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)
    
    sql_cols =  ''.join([f", {col}" for col in [filter_col]+[additonal_filter_cols[additional_filter]] if col!=None])

    if utl_type == "er":
        join_sql = create_join_sql(center, "U")
        query = f"""
            SELECT COUNT(*){sql_cols}
            FROM (SELECT admission_date{sql_cols} FROM er_only
            UNION ALL
            SELECT admission_date{sql_cols} FROM inpatient
            WHERE inpatient.er = 1) AS U
            {join_sql}
            WHERE U.{date_type} BETWEEN ? AND ?
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    else:
        join_sql = create_join_sql(center, utl_type)
        query = f"""
            SELECT COUNT(*){sql_cols}
            FROM {utl_type}
            {join_sql}
            WHERE {date_type} BETWEEN ? AND ?
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()
    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return result


def er_to_inp(center, start_date, end_date, filter_col, col_filter, additional_filter):
    """
    Calculates number of er visits than result in inpatient admission in a given date range and filtered by selected
    user filters

    Args:
        center: Name of PACE center

        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        filter_col: column to be used to filter the table, can be None.

        col_filter: value in the filter column to filter the table by.

        additional_filter: additional filter value selected by the user, can be None.
            Will be a value from a column different from the filter column.
            These value column pairs are found in the additonal_filter_cols dictionary

    Returns:
        int: number of er visits than result in inpatient admission
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    filter_value_sql, params = create_filter_sql(
        [filter_col], 0, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, "inpatient")

    sql_cols = "SUM(er)" + ''.join([f", {col}" for col in [filter_col]+[additonal_filter_cols[additional_filter]] if col!=None])

    query = f"""
            SELECT {sql_cols}
            FROM inpatient
            {join_sql}
            WHERE admission_date BETWEEN ? AND ?
            AND admission_type = 'Acute Hospital'
            {filter_value_sql}
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]
    
    conn.close()
    if result is None:
        return 'N/A'
    return result


def los_per_100mm(
    utl_type, center, start_date, end_date, filter_col, col_filter, additional_filter
):
    """
    Calculates the length of stay (in days) per 100 member months of a utlization type in a given date range and filtered by selected
    user filters

    Args:
        utl_type: type of utilization user is looking for.
            Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
            Should match up to tables in database, but inpatient psych is not currently
            it's own table. Handled using an if statement below

        center: Name of PACE center

        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        filter_col: column to be used to filter the table, can be None.

        col_filter: value in the filter column to filter the table by.

        additional_filter: additional filter value selected by the user, can be None.
            Will be a value from a column different from the filter column.
            These value column pairs are found in the additonal_filter_cols dictionary

    Returns:
        float: length of stay (in days) per 100 member months
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    if (utl_type == "er_only") or (utl_type == "er"):
        utl_type = "inpatient"
        admission_sql = admission_sql_dict["inpatient_er"]
    else:
        admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

    filter_value_sql, params = create_filter_sql(
        [filter_col], 0, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, utl_type)

    sql_cols = "SUM(los)" + ''.join([f", {col}" for col in [filter_col]+[additonal_filter_cols[additional_filter]] if col!=None])

    los_query = f"""
            SELECT {sql_cols}
            FROM {utl_type}
            {join_sql}
            WHERE discharge_date BETWEEN ? AND ?
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    discharges = c.execute(los_query, params).fetchone()[0]

    conn.close()

    if discharges == None:
        return "N/A"

    pmpm_df = census_count_df(center, params[0], params[1], "M")

    los_days_per_100 = (discharges / pmpm_df["Census"].sum()) * 100

    return round(los_days_per_100, 2)


def alos(
    utl_type, center, start_date, end_date, filter_col, col_filter, additional_filter
):
    """
    Calculates the average length of stay (in days) of a utlization type in a given date range and filtered by selected
    user filters

    Args:
        utl_type: type of utilization user is looking for.
            Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
            Should match up to tables in database, but inpatient psych is not currently
            it's own table. Handled using an if statement below

        center: Name of PACE center

        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        filter_col: column to be used to filter the table, can be None.

        col_filter: value in the filter column to filter the table by.

        additional_filter: additional filter value selected by the user, can be None.
            Will be a value from a column different from the filter column.
            These value column pairs are found in the additonal_filter_cols dictionary

    Returns:
        float: average length of stay (in days)
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    if (utl_type == "er_only") or (utl_type == "er"):
        utl_type = "inpatient"
        admission_sql = admission_sql_dict["inpatient_er"]
    else:
        admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

    filter_value_sql, params = create_filter_sql(
        [filter_col], 0, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, utl_type)

    sql_cols = "AVG(los)" + ''.join([f", {col}" for col in [filter_col]+[additonal_filter_cols[additional_filter]] if col!=None])

    query = f"""
            SELECT {sql_cols}
            FROM {utl_type}
            {join_sql}
            WHERE discharge_date BETWEEN ? AND ?
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    try:
        result = round(result, 2)
    except TypeError:
        result = "N/A"

    return result


def snf_days(center, start_date, end_date, filter_col, col_filter, stay_type):
    """
     Calculates the length of stay (in days) for inpatient SNF admission of a specified type
     in a given date range and filtered by selected user filters

     Args:
         center: Name of PACE center

         start_date: First date to include in resulting dateframe

         end_date: Last date to include in resulting dateframe

         filter_col: column to be used to filter the table, can be None.

         col_filter: value in the filter column to filter the table by.

         stay_type: type of SNF stay, can be custodial, skilled, or respite

     Returns:
         int: length of stay (in days)

     To Do:
         Possible add the additional filter option, but it doesn't seem like we need to know
         (or have robust enough data) if being admitted to a certain SNF AND
         being admitted at a given time result in longer daya of a SPECIFIC
         stay type
     """
    params = [
        pd.to_datetime(start_date).date(),
        pd.to_datetime(end_date).date(),
        stay_type,
    ]

    filter_value_sql, params = create_filter_sql(
        [filter_col], 0, col_filter, None, params
    )

    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, "inpatient_snf")

    sql_cols = "SUM(los)" + ''.join([f", {col}" for col in [filter_col] if col!=None])

    query = f"""
            SELECT {sql_cols}
            FROM inpatient_snf
            {join_sql}
            WHERE discharge_date BETWEEN ? AND ?
            AND admit_reason = ?
            {filter_value_sql}
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    snf_days = c.execute(query, params).fetchone()[0]

    conn.close()

    if snf_days == None:
        return "N/A"

    pmpm_df = census_count_df(center, params[0], params[1], "M")

    snf_days_per_100 = (snf_days / pmpm_df["Census"].sum()) * 100

    return round(snf_days_per_100, 2)


def all_readmits(
    utl_type, center, start_date, end_date, filter_col, col_filter, additional_filter
):
    """
     Calculates the number of readmits of a utlization type in a given date range
     and filtered by selected user filters

     Args:
         utl_type: type of utilization user is looking for.
             Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
             Should match up to tables in database, but inpatient psych is not currently
             it's own table. Handled using an if statement below.

         center: Name of PACE center

         start_date: First date to include in resulting dateframe

         end_date: Last date to include in resulting dateframe

         filter_col: column to be used to filter the table, can be None.

         col_filter: value in the filter column to filter the table by.

         additional_filter: additional filter value selected by the user, can be None.
             Will be a value from a column different from the filter column.
             These value column pairs are found in the additonal_filter_cols dictionary

     Returns:
         int: number of readmits
     """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

    filter_value_sql, params = create_filter_sql(
        [filter_col], 0, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)

    sql_cols = ''.join([f", {col}" for col in [filter_col]+[additonal_filter_cols[additional_filter]] if col!=None])

    if utl_type == "er":
        join_sql = create_join_sql(center, "U")
        query = f"""
            SELECT COUNT(*){sql_cols}
            FROM (SELECT admission_date, days_since_last_admission{sql_cols} FROM er_only
            UNION ALL
            SELECT admission_date, days_since_last_admission{sql_cols} FROM inpatient
            WHERE inpatient.er = 1) AS U
            {join_sql}
            WHERE U.admission_date BETWEEN ? AND ?
            AND U.days_since_last_admission > 0
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    else:
        join_sql = create_join_sql(center, utl_type)
        query = f"""
            SELECT COUNT(*){sql_cols}
            FROM {utl_type}
            {join_sql}
            WHERE admission_date BETWEEN ? AND ?
            AND days_since_last_admission > 0
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return result


def readmits_30_day(
    utl_type,
    admits,
    center,
    start_date,
    end_date,
    filter_col,
    col_filter,
    additional_filter,
):
    """
     Calculates the number of 30-day readmits(readmitted within 30 days) of a utlization type in a given date range
     and filtered by selected user filters

     Args:
         utl_type: type of utilization user is looking for.
             Current values are inpatient, inpatient_psych, er, er_only and inpatient_snf.
             Should match up to tables in database, but inpatient psych is not currently
             it's own table. Handled using an if statement below.

         center: Name of PACE center

         start_date: First date to include in resulting dateframe

         end_date: Last date to include in resulting dateframe

         filter_col: column to be used to filter the table, can be None.

         col_filter: value in the filter column to filter the table by.

         additional_filter: additional filter value selected by the user, can be None.
             Will be a value from a column different from the filter column.
             These value column pairs are found in the additonal_filter_cols dictionary

     Returns:
         int: number of 30-day readmits
     """
    if admits == 0:
        return "N/A", "N/A"

    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    if (utl_type == "er_only") or (utl_type == "er"):
        utl_type = "inpatient"
        admission_sql = admission_sql_dict["inpatient_er"]
    else:
        admission_sql = admission_sql_dict[utl_type]

    if utl_type == "inpatient_psych":
        utl_type = "inpatient"

    filter_value_sql, params = create_filter_sql(
        [filter_col], 0, col_filter, additional_filter, params
    )

    center_sql, params = create_center_sql(center, params)

    sql_cols =  ''.join([f", {col}" for col in [filter_col]+[additonal_filter_cols[additional_filter]] if col!=None])

    if utl_type == "er":
        join_sql = create_join_sql(center, "U")
        query = f"""
            SELECT COUNT(*){sql_cols}
            FROM (SELECT admission_date, days_since_last_admission{sql_cols} FROM er_only
            UNION ALL
            SELECT admission_date, days_since_last_admission{sql_cols} FROM inpatient
            WHERE inpatient.er = 1) AS U
            {join_sql}
            WHERE U.admission_date BETWEEN ? AND ?
            AND U.days_since_last_admission <= 30
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    else:
        join_sql = create_join_sql(center, utl_type)
        query = f"""
            SELECT COUNT(*){sql_cols}
            FROM {utl_type}
            {join_sql}
            WHERE admission_date BETWEEN ? AND ?
            AND days_since_last_admission <= 30
            {admission_sql}
            {filter_value_sql}
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    rate = (result / admits) * 100

    return (round(rate, 2), result)


# GRAPHS


def filter_col_df_sum(cols, filter_col, additional_filters, df, summary_col):
    """
      Creates dataframe for plotting utlization data grouped by the cols using the sum function
      and a list of columns to be included in the plot

      Args:
          cols: List of column names to be included in the SQL query.

          col_filter: column to be used to filter the table, can be None.
              If not None, dateframe will break out visits by the values in the columns.
              ie; by hospital dx, or other column selected

          additional_filter: additional filters selected by the user, can be None
              First filter will be a specific value from the filter column, the second value
              can be None or be a value from a column different from the filter column.
              These value column pairs are found in the additonal_filter_cols dictionary  

          df: dataframe to be grouped and filtered

          summary_col: column to be summed in groupby

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
    Creates dataframe for plotting utlization data grouped by the cols using the sum function
    and a list of columns to be included in the plot

    Args:
        cols: List of column names to be included in the SQL query.

        col_filter: column to be used to filter the table, can be None.
            If not None, dateframe will break out visits by the values in the columns.
            ie; by hospital dx, or other column selected

        additional_filter: additional filters selected by the user, can be None
            First filter will be a specific value from the filter column, the second value
            can be None or be a value from a column different from the filter column.
            These value column pairs are found in the additonal_filter_cols dictionary  

        df: dataframe to be grouped and filtered

        summary_col: column to be summed in groupby

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
      Creates dataframe for plotting utlization data grouped by the cols using the sum function
      and a list of columns to be included in the plot

      Args:
          cols: List of column names to be included in the SQL query.

          col_filter: column to be used to filter the table, can be None.
              If not None, dateframe will break out visits by the values in the columns.
              ie; by hospital dx, or other column selected

          additional_filter: additional filters selected by the user, can be None
              First filter will be a specific value from the filter column, the second value
              can be None or be a value from a column different from the filter column.
              These value column pairs are found in the additonal_filter_cols dictionary  

          df: dataframe to be grouped and filtered

          summary_col: column to be summed in groupby

          amnt: Number of columns to be included in the plot, can be 5, 10, or all

          groupby_mean: Defualt to False, if True, groupby uses mean() instead of sum()

          set_col_order: Default to False, if True, col_order is called, so the order of
              this plot_cols matches the order of the plot_cols from the visit graph.

          *args: paremters for col_order, should be utl_type, cols, center, start_date,
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
      Allows for easy plotting of the percent of vists corresponding to a filter

      Args:
          total_df: dataframe of visits during the selected date range

          plot_df: dataframe created using utlization type, data range, and user filters

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
    *additional_filters,
):
    """
     Plots a bar graph of the percent of visits related to each filter or a bar graph of the visit counts
     if no filters are selected

     Args:
         start_date: First date to include in plotting dateframe

         end_date: Last date to include in plotting dateframe

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
             These value column pairs are found in the additonal_filter_cols dictionary

     Returns:
         dict: contianging plotly figure data and layout information
    """
    filtered_flag = filter_col != None

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
            go.Bar(
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
    else:
        fig_data = [
            go.Bar(
                x=plot_df[date_type].astype(str),
                y=plot_df[col],
                hoverinfo="x+y",
                marker=dict(color=color),
            )
            for col, color in zip(plot_cols, color_palette)
        ]
        legend = {}
        y_title = 'Visits'

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
    fig_layout = build_bar_layout(f"{utl_type.title()} {title_date}s{filter_title}", legend = legend, y_title=y_title, x_ticks=x_ticks)

    return dict(data=fig_data, layout=fig_layout)


def update_los_graph(
    start_date, end_date, utl_type, filter_col, amnt, freq, center, *additional_filters
):
    """
     Plots a scatter plot of the alos monthly and serperated by filter if filters are provided. Plots a bar graph
     if the frequency is set to quarterly. 

     Args:
         start_date: First date to include in plotting dateframe

         end_date: Last date to include in plotting dateframe

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
         dict: contianging plotly figure data and layout information
    """
    filtered_flag = filter_col != None
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
                go.Bar(
                    x=plot_df["discharge_date"].astype(str),
                    y=plot_df['los'],
                    name='<br>'.join(textwrap.wrap(titlecase(additional_filters[0]), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color_palette[0]),
                )
            ]
            

        else:
            fig_data = [
                go.Bar(
                    x=plot_df["discharge_date"].astype(str),
                    y=plot_df[col],
                    name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color),
                )
                for col, name, color in zip(plot_cols, legend_names, color_palette)
            ]
        fig_layout = build_bar_layout("ALOS", legend = dict(orientation="h", y=-0.15, font={"size": 9.5}), x_ticks=x_ticks)
    
    else:
        fig_data = [
            go.Scatter(
                x=plot_df["discharge_date"].astype(str),
                y=plot_df[col],
                name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                hoverinfo="x+name+y",
                marker=dict(color=color),
            )
            for col, name, color in zip(plot_cols, legend_names, color_palette)
        ]

        df_min = min(plot_df[plot_cols].min().values)
        df_max = max(plot_df[plot_cols].max().values)

        fig_layout = build_scatter_layout("ALOS", df_min, 
        df_max, x_ticks=x_ticks)

    return dict(data=fig_data, layout=fig_layout)


def update_readmit_graph(
    start_date, end_date, utl_type, filter_col, amnt, freq, center, *additional_filters
):
    """
     Plots a scatter plot of the number of 30-day readmits in a month, serperated by filter if filters are provided. Plots a bar graph
     if the frequency is set to quarterly. 

     Args:
         start_date: First date to include in plotting dateframe

         end_date: Last date to include in plotting dateframe

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
         dict: contianging plotly figure data and layout information
    """
    filtered_flag = filter_col != None

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
                go.Bar(
                    x=plot_df["admission_date"].astype(str),
                    y=plot_df['count'],
                    name='<br>'.join(textwrap.wrap(
                       titlecase(additional_filters[0]), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color_palette[0]),
                )
            ]
        else:
            fig_data = [
                go.Bar(
                    x=plot_df["admission_date"].astype(str),
                    y=plot_df[col],
                    name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                    hoverinfo="x+name+y",
                    marker=dict(color=color),
                )
                for col, name, color in zip(plot_cols, legend_names, color_palette)
                if col != 0
            ]
        fig_layout = build_bar_layout('30 Day Readmits', legend = dict(font={"size": 9.5}),
        small_margins=True)
    
    else:
        fig_data = [
            go.Scatter(
                x=plot_df["admission_date"].astype(str),
                y=plot_df[col],
                name='<br>'.join(textwrap.wrap(titlecase(str(name)), width=15)),
                marker=dict(color=color),
            )
            for col, name, color in zip(plot_cols, legend_names, color_palette)
        ]
        df_min = min(plot_df[plot_df.columns[1:]].min().values)
        df_max = max(plot_df[plot_df.columns[1:]].max().values)
        fig_layout = build_scatter_layout('30 Day Readmits', 
            df_min,
            df_max,
            small_margins=True)
    
    return dict(data=fig_data, layout=fig_layout)
