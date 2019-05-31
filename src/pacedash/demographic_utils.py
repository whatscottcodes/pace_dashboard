import plotly.graph_objs as go
import squarify
import pandas as pd
import numpy as np
import sqlite3
from .helpers_configs import (
    color_palette,
    calc_min_y,
    create_daterange,
    sql_return_df,
    db_filepath,
    create_center_sql,
    build_scatter_layout,
    build_bar_layout
)

from .census_utils import census_count_df
import textwrap

demographic_attribute_options = [
    {"label": "Age", "value": "age"},
    {"label": "Gender", "value": "gender"},
    {"label": "Race/Ethnicity", "value": "race"},
    {"label": "Language Spoken", "value": "lang"},
    {"label": "Dementia Dx", "value": "dementia"},
    {"label": "Behavioral Health Dx", "value": "bh"},
]
#each demographic attribute option has a different set of graphs
#that we believe will best represent the data
#there are passed to the radio buttons under the dropdown
graph_types = {
    "age": [
        {"label": "Distribution", "value": "age_dist"},
        {"label": "Square", "value": "age_square"},
        {"label": "Avg. Trend", "value": "age_trend"},
    ],
    "gender": [
        {"label": "Distribution", "value": "gen_dist"},
        {"label": "Pie", "value": "gen_pie"},
        {"label": "Percent Trend", "value": "gen_trend"},
    ],
    "race": [
        {"label": "Line", "value": "race_bar"},
        {"label": "Square", "value": "race_sqaure"},
        {"label": "Percent Trend", "value": "race_trend"},
    ],
    "lang": [
        {"label": "Line", "value": "lang_bar"},
        {"label": "Square", "value": "lang_square"},
        {"label": "Percent Trend", "value": "lang_trend"},
    ],
    "dementia": [{"label": "Percent Trend", "value": "dementia_trend"}],
    "bh": [{"label": "Percent Trend", "value": "bh_trend"}],
    "chronic": [{"label": "Trend", "value": "chronic_trend"}],
}

def demographic_df(start_date, end_date, center, cols, date_cols=None):
    """
    Creates pandas dataframe of demographic table during given
    date range and with specified columns

    Args:
        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe
        
        center: Name of PACE center
        
        cols: List of column names to be included in the SQL query

        date_cols: names of columns to be parased using pandas datetime

    Returns:
        df: dataframe of demographic table during given
            date range and with specified columns
    """
    params = [pd.to_datetime(start_date).date(),
            pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    query = f"""
    SELECT {', '.join(col for col in cols)}
    FROM demographics d
    JOIN enrollment e ON d.member_id = e.member_id
    WHERE (disenrollment_date >= ?
    OR disenrollment_date IS NULL)
    AND e.enrollment_date <= ?
    {center_sql};
    """

    return sql_return_df(query, params, date_cols)

#GRAPHS
def create_square_graph(value_dict, df_shape, plot_title):
    """
    Plots a square area graph of demographic groups with label,
    value, and percent annotations

    Args:
        value_dict: dictionary with label of a demographic group
            with the number of participants in the group as the value

        df_shape: total number of participants in the dataset
            used to calculate the percent in each box

        plot_title: title of plot


    Returns:
         dict: contianging plotly figure data and layout information
    """
    values = [*value_dict.keys()]
    values.sort(reverse=True)  #redefine label order

    labels = [value_dict[value] for value in values]
    percents = [(value / df_shape) * 100 for value in values]

    x = 0.0
    y = 0.0
    width = 100.0
    height = 100.0

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.padded_squarify(normed, x, y, width, height)

    shapes = []
    annotations = [
        dict(
            yref="paper",
            xref="paper",
            y=1.10,
            x=0,
            text=f"<b>{plot_title}</b>",
            showarrow=False,
            font=dict(color="#323031"),
        )
    ]

    for counter, r in enumerate(rects):
        if r['dy'] <= 10:
            text = f"<b>{labels[counter]}</b> {round(percents[counter],2)}%"
            if len(text)*1.5 >= r['dx']:
                text = ''
        else:
            text = f"<b>{labels[counter]}</b><br>{round(percents[counter],2)}%"
            if len(labels[counter])*1.5 >= r['dx']:
                text = ''
        shapes.append(
            dict(
                type="rect",
                x0=r["x"],
                y0=r["y"],
                x1=r["x"] + r["dx"],
                y1=r["y"] + r["dy"],
                line=dict(width=2),
                fillcolor=color_palette[counter],
            )
        )

        annotations.append(
            dict(
                x=r["x"] + (r["dx"] / 2),
                y=r["y"] + (r["dy"] / 2),
                text=text,
                showarrow=False,
                font=dict(color="white"),
            )
        )

    fig_data = [
        go.Scatter(
            x=[r["x"] + (r["dx"] / 2) for r in rects],
            y=[r["y"] + (r["dy"] / 2) for r in rects],
            text=[
                f"{str(l)}<br>{str(v)} ppts.<br>{round(p, 2)}%"
                for l, v, p in zip(labels, values, percents)
            ],
            hoverinfo="x+text",
        )
    ]

    fig_layout = dict(
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            range=[0, 110],
            ticks="",
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            range=[0, 110],
            ticks="",
            showticklabels=False,
        ),
        shapes=shapes,
        showlegend=False,
        annotations=annotations,
        margin={"pad": 5, "l": 65, "r": 50, "t": 55, "b": 65},
        hovermode="closest",
        hoverdistance=-1,
        hoverlabel={"bgcolor": "white", "font": {"color": "black"}},
        title="",
    )

    return dict(data=fig_data, layout=fig_layout)
    
def percent_trend_graph(df, mask, plot_title, color, start_date,
                    end_date, center=None, use_raw_count=False):
    """
    Plots a line graph of the percent of participants in selected
    demographic group

    Args:
        df: pandas dataframe containing related demographic information
        start_date: First date to include in plotting dateframe

        plot_title: title of plot

        color: line color

        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

        use_raw_count: Default to False, set to True when the df has
            already been filter for the selected demographic group.
            A different counting function will be used and the PMPM
            census_count_df will be created.

     Returns:
         dict: contianging plotly figure data and layout information
    """
    #two helper functions
    def percent_count(df, *masks):
        """
        When the dataframe contains all participants and needs to be
        filtered for demographic group and enrollment this
        count fucntion is used
        """
        enroll_mask, disenroll_mask, mask = masks
        return round((
            df[enroll_mask & disenroll_mask & mask].shape[0]
            / df[enroll_mask & disenroll_mask].shape[0]
        ) * 100, 2)
    
    def raw_count(df, *masks):
        """
        When the dataframe has already been filter for the
        selected demographic group this count fucntion is used
        """
        enroll_mask, disenroll_mask, _ = masks
        return len(df[enroll_mask & disenroll_mask]["member_id"].unique())
    
    #start of percent graph creation
    if use_raw_count:
        count_func = raw_count
    else:
        count_func = percent_count

    count_dict = {}

    for single_date in create_daterange(start_date, end_date, "M"):
        enroll_mask = df.enrollment_date <= single_date
        disenroll_mask = (df.disenrollment_date >= single_date) | (
            df.disenrollment_date.isnull()
        )
        count_dict[single_date] = count_func(df, enroll_mask, disenroll_mask, mask)

    plot_df = pd.DataFrame.from_dict(count_dict, orient="index", columns=["Percent"]).reset_index()
    plot_df.rename(columns = {'index':'Freq'}, inplace=True)

    if use_raw_count:
        pmpm_df = census_count_df(center, start_date, end_date, "M")
        plot_df["Percent"] = round((plot_df["Percent"] / pmpm_df["Census"]) * 100, 2)

    fig_data = [
        go.Scatter(
            x=plot_df["Freq"],
            y=plot_df["Percent"],
            mode="lines",
            line={"width": 7, "color": color},
        )
    ]

    fig_layout = build_scatter_layout(plot_title, plot_df["Percent"].min(), plot_df["Percent"].max(), y_title='Percent')
    
    return dict(data=fig_data, layout=fig_layout)

def demographic_line_plot(demographic, plot_title, center, start_date, end_date):
    """
    Plots a line graph of the percent of participants in each
    demographic group

    Args:
        demographic: column in the dataframe corresponding to
        the selected demographic attribute

        plot_title: title of plot
        
        center: Name of PACE center

        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

     Returns:
         dict: contianging plotly figure data and layout information
    """
    #helper function
    def monthly_count(df, demographic, enroll_mask, disenroll_mask):
        """
        Create a dictionary for each month containing the percent
        of each demographic group in the month
        """
        month_count = {}

        for demo in df[demographic].unique():
            mask = df[demographic] == demo
            month_count[demo] = round((
                df[enroll_mask & disenroll_mask & mask].shape[0] /
                df[enroll_mask & disenroll_mask].shape[0]
            ) * 100,2)

        return month_count
    
    #start of line plot creation
    df = demographic_df(
        start_date,
        end_date,
        center,
        [f"d.{demographic}", "e.enrollment_date", "e.disenrollment_date"],
        ["enrollment_date", "disenrollment_date"])

    count_dict = {}

    for single_date in create_daterange(start_date, end_date, "MS"):
        
        enroll_mask = df.enrollment_date <= single_date
        disenroll_mask = (df.disenrollment_date >= single_date) | (
            df.disenrollment_date.isnull()
        )

        count_dict[single_date] = monthly_count(df, demographic, enroll_mask, disenroll_mask)
    
    plot_df = pd.DataFrame.from_dict(count_dict, orient="index").reset_index()
    plot_df.rename(columns={"index": "Quarter"}, inplace=True)
    
    fig_data = [
        go.Scatter(
            x=plot_df["Quarter"],
            y=plot_df[col],
            text=[str(round(val, 2)) + "%" for val in plot_df[col]],
            hoverinfo="x+text+name",
            name=col,
            mode="lines",
            line={"width": 4, "color": color},
        )
        for col, color in zip(plot_df.columns[1:], color_palette)
        if (isinstance(col, str)) & (plot_df[col].min() >= 0.5)
    ]
    df_max = plot_df[plot_df.columns[1:]].max().sort_values(ascending=False)
    df_min = plot_df[plot_df.columns[1:]].min().sort_values()
    
    scale_max = df_max.values[0] * 1.05

    scale_min = calc_min_y(scale_max, df_min.values[0])

    if scale_max - scale_min < 4.5:
        scale_min = scale_max - 4.5

    annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=1.10,
                x=0,
                text=f"<b>{plot_title}</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ]


    annotations.extend([
            dict(
                yref="y",
                xref="paper",
                y=plot_df[col][0] + 4.25,
                x=0,
                text=f"<b>{col}</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
         for col in df_max[:3].index
    ])

    fig_layout = go.Layout(
        margin={"pad": 5, "l": 35, "r": 50, "t": 55, "b": 65},
        xaxis= {"title": '', "showgrid": False, "showline": False},
        yaxis={
            "title": 'Percent',
            "showgrid": True,
            "zeroline": False,
            "range": [scale_min, scale_max],
        },
        autosize=True,
        annotations=annotations,
        showlegend=False,
    )
    
    return dict(data=fig_data, layout=fig_layout)
    
def age_hist(start_date, end_date, center):
    """
    Plots a histogram of participants' age in a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(start_date, end_date, center, ["d.dob"], ["dob"])

    df["age"] = (pd.to_datetime(end_date).to_period("M") - df["dob"].dt.to_period("M")).apply(lambda x: int(x.freqstr[:-1]) // 12)

    fig_data = [go.Histogram(x=df["age"], marker=dict(color=color_palette[0]), opacity=0.75)]

    fig_layout = build_bar_layout("Participant Age", x_title='Age (Years)', y_title='Number of Ppts')

    return dict(data=fig_data, layout=fig_layout)

def age_square(start_date, end_date, center):
    """
    Plots a square area graph of age groups with label,
    value, and percent annotations

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(
        start_date,
        end_date,
        center,
        ["e.member_id, e.enrollment_date, e.disenrollment_date, d.dob"],
        ["dob"],
    )

    df["age"] = (pd.to_datetime(end_date).to_period("M") - df["dob"].dt.to_period("M")).apply(lambda x: int(x.freqstr[:-1]) // 12)

    groups = [(55, 64), (65, 74), (75, 84), (85, 94), (95, 120)]
    labels = ["55 to 64", "65 to 74", "75 to 84", "85 to 94", "95+"]

    vals = [
        df[(df["age"] >= group[0]) & (df["age"] <= group[1])].shape[0]
        for group in groups
    ]
    value_dict = {val: label for label, val in zip(labels, vals)}

    return create_square_graph(value_dict, df.shape[0], 'Age Group')

def avg_age_line(start_date, end_date, center):
    """
    Plots a line graph of participants' average age
    for each month in a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(
        start_date,
        end_date,
        center,
        ["d.dob", "e.enrollment_date", "e.disenrollment_date"],
        ["dob", "enrollment_date", "disenrollment_date"],
    )

    avg_age_dict = {}

    for single_date in create_daterange(start_date, end_date, "MS"):
        df["age"] = (pd.to_datetime(single_date).to_period("M") - df["dob"].dt.to_period("M")).apply(lambda x: int(x.freqstr[:-1]) // 12)
        enroll_mask = df.enrollment_date <= single_date
        disenroll_mask = (df.disenrollment_date > single_date) | (
            df.disenrollment_date.isnull()
        )
        avg_age_dict[single_date] = df[enroll_mask & disenroll_mask]["age"].mean()

    plot_df = pd.DataFrame.from_dict(
        avg_age_dict, orient="index", columns=["Mean"]
    ).reset_index()
    plot_df.rename(columns={"index": "Freq"}, inplace=True)

    fig_data = [
        go.Scatter(
            x=plot_df["Freq"],
            y=plot_df["Mean"],
            mode="lines",
            line={"width": 7, "color": color_palette[0]},
        )
    ]

    fig_layout = build_scatter_layout("Average Age by Month", plot_df["Mean"].min(), plot_df["Mean"].max(), y_title='Age (Years)')

    return dict(data=fig_data, layout=fig_layout)

def gender_hist(start_date, end_date, center):
    """
    Plots a population pyramid of participants age groups
    filtered by gender for a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """

    df = demographic_df(start_date, end_date, center, ["d.dob", "d.gender"], ["dob"])

    df["age"] = (pd.to_datetime(end_date).to_period("M") - df["dob"].dt.to_period("M")).apply(lambda x: int(x.freqstr[:-1]) // 12)

    def bins(df, groups):
        return [
            df[(df["age"] >= group[0]) & (df["age"] <= group[1])].shape[0]
            for group in groups
        ]

    age_groups = [(55, 64), (65, 74), (75, 84), (85, 94), (95, 104), (105, 114)]

    women_bins = bins(df[df.gender == 1], age_groups)
    men_bins = bins(df[df.gender == 0], age_groups)

    y = [np.mean(age_group) for age_group in age_groups]

    men_text = [
        f"{age_group} {men_bin}" for age_group, men_bin in zip(age_groups, men_bins)
    ]
    women_text = [
        f"{age_group} {women_bin}"
        for age_group, women_bin in zip(age_groups, women_bins)
    ]

    fig_data = [
        go.Bar(
            y=y,
            x=women_bins,
            orientation="h",
            name="Women",
            text=women_text,
            hoverinfo="x+text+name",
            marker=dict(color="#F6AA9B"),
        ),
        go.Bar(
            y=y,
            x=[-1 * val for val in men_bins],
            orientation="h",
            name="Men",
            text=men_text,
            hoverinfo="x+text+name",
            marker=dict(color="#6EA4BF"),
        ),
    ]
    fig_layout = go.Layout(
        margin={"pad": 5, "l": 35, "r": 50, "t": 55, "b": 65},
        title="",
        yaxis=go.layout.YAxis(title="Age", range=[50, 105]),
        xaxis=go.layout.XAxis(
            range=[-100, 100],
            tickvals=[-100, -75, -25, 0, 25, 75, 100],
            ticktext=[100, 75, 25, 0, 25, 75, 100],
            title="Number of Ppts",
        ),
        barmode="overlay",
        bargap=0.1,
        annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=1.10,
                x=0,
                text="<b>Participant Age Group by Gender</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ],
    )

    return dict(data=fig_data, layout=fig_layout)

def gender_pie(start_date, end_date, center):
    """
    Plots a pie graph of the gender split
    in percent of ppts for a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(start_date, end_date, center, ["d.gender"])

    labels = ["Men", "Women"]
    values = [df[df.gender == 0].shape[0], df[df.gender == 1].shape[0]]
    pie_colors = ["#5789BA", "#DA5870"]

    fig_data = [
        go.Pie(
            labels=labels,
            values=values,
            hoverinfo="none",
            textinfo="label+value+percent",
            textfont=dict(size=20, color="white"),
            marker=dict(colors=pie_colors, line=dict(color="white", width=2)),
        )
    ]

    fig_layout = go.Layout(
        showlegend=False,
        title="",
        annotations=[
            dict(
                yref="paper",
                xref="paper",
                y=1.21,
                x=0,
                text="<b>Gender Split</b>",
                showarrow=False,
                font=dict(color="#323031"),
            )
        ],
    )

    return dict(data=fig_data, layout=fig_layout)

def gender_trend(start_date, end_date, center):
    """
    Plots a line graph of the percent of women
    ppts for each month in a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(
        start_date,
        end_date,
        center,
        ["d.gender", "e.enrollment_date", "e.disenrollment_date"],
        ["enrollment_date", "disenrollment_date"],
    )
    return percent_trend_graph(df, (df.gender == 1),
                            "Percent Female",
                            "#DA5870",
                            start_date,
                            end_date)
   
def race_line(start_date, end_date, center):
    """
    Plots a line graph of the percent of participants in each
    race/ethnicity group for a given date range

    Args:
        center: Name of PACE center

        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    return demographic_line_plot('race',
                            "Race/Ethnicity by Quarter</b>",
                            center,
                            start_date,
                            end_date)

def race_square(start_date, end_date, center):
    """
    Plots a square area graph of race/ethnicity groups with label,
    value, and percent annotations

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(start_date, end_date, center, ["d.race"])

    df["race"] = df.race.str.replace(
        "African American/Black", "African<br>American/<br>Black"
    )
    df["race"] = df.race.str.replace(
        "American Indian or Alaska Native", "American Indian or<br>Alaska Native"
    )

    value_dict = {df[df.race == race].shape[0]: race for race in df.race.unique()}

    return create_square_graph(value_dict, df.shape[0], 'Race/Ethnicity')

def race_trend(start_date, end_date, center):
    """
    Plots a line graph of the percent of non-white
    ppts for each month in a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(
        start_date,
        end_date,
        center,
        ["d.race", "e.enrollment_date", "e.disenrollment_date"],
        ["enrollment_date", "disenrollment_date"],
    )
    
    return percent_trend_graph(df, 
                            (df.race != "Caucasian/White"),
                            "Percent Non-White",
                            color_palette[0],
                            start_date,
                            end_date)

def lang_line(start_date, end_date, center):
    """
    Plots a line graph of the percent of participants in each
    language spoken group for a given date range

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    return demographic_line_plot('language',
                            "Primary Language by Quarter",
                            center,
                            start_date,
                            end_date)

def lang_square(start_date, end_date, center):
    """
    Plots a square area graph of primary language groups with label,
    value, and percent annotations

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(start_date, end_date, center, ["d.language"])

    value_dict = {
        df[df.language == language].shape[0]: language
        for language in df.language.unique()
    }

    return create_square_graph(value_dict, df.shape[0], 'Primary Language')

def lang_trend(start_date, end_date, center):
    """
    Plots a line graph of the percent of non-english
    speaking ppts for each month in a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    df = demographic_df(
        start_date,
        end_date,
        center,
        ["d.language", "e.enrollment_date", "e.disenrollment_date"],
        ["enrollment_date", "disenrollment_date"],
    )
    return percent_trend_graph(df,
                            (df.language != "English"),
                            "Percent Non-English as Primary Language", 
                            color_palette[0],
                            start_date,
                            end_date)

def dementia_trend(start_date, end_date, center):
    """
    Plots a line graph of the percent of ppts
    with dementia for each month in a given date range and
    possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    params = [
        pd.to_datetime(start_date).date(),
        pd.to_datetime(end_date).date(),
    ]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT dx.member_id, e.enrollment_date, e.disenrollment_date
        FROM dx
        JOIN enrollment e ON dx.member_id=e.member_id
        WHERE (instr(icd10, 'F00') > 0
        OR instr(icd10, 'F01') > 0
        OR instr(icd10, 'F02') > 0
        OR instr(icd10, 'F03') > 0
        OR instr(icd10, 'G3') > 0)
        AND (disenrollment_date >= ?
        OR disenrollment_date IS NULL)
        AND (enrollment_date <= ?)
        {center_sql};
        """
    df = sql_return_df(query, params, ['enrollment_date', 'disenrollment_date'])

    return percent_trend_graph(df, None,
                            "Percent with Dementia Related Dx",
                            color_palette[0],
                            start_date,
                            end_date,
                            center,
                            use_raw_count=True)

def bh_trend(start_date, end_date, center):
    """
    Plots a line graph of the percent of ppts
    with behavioral health dx for each month
    in a given date range and possibly filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         dict: contianging plotly figure data and layout information
    """
    params = [
        pd.to_datetime(start_date).date(),
        pd.to_datetime(end_date).date(),
        pd.to_datetime(end_date).date(),
    ]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT dx.member_id, e.enrollment_date, e.disenrollment_date
        FROM dx
        JOIN enrollment e ON dx.member_id=e.member_id
        WHERE (instr(icd10, 'F2') > 0
        OR instr(icd10, 'F31') > 0
        OR instr(icd10, 'F32') > 0
        OR instr(icd10, 'F33') > 0
        OR instr(icd10, 'F4') > 0
        OR instr(icd10, 'F6') > 0)
        AND (disenrollment_date BETWEEN ? AND ?
        OR disenrollment_date IS NULL)
        AND (enrollment_date <= ?)
        {center_sql};
        """
    df = sql_return_df(query, params, ['enrollment_date', 'disenrollment_date'])
 
    return percent_trend_graph(df, None,
                            "Percent with Behavioral Health Dx",
                            color_palette[0],
                            start_date,
                            end_date,
                            center,
                            use_raw_count=True)

#dictionary of chart building functions
#based on the selected radio button
chart_functions = {
    "age_dist": age_hist,
    "age_square": age_square,
    "age_trend": avg_age_line,
    "gen_dist": gender_hist,
    "gen_pie": gender_pie,
    "gen_trend": gender_trend,
    "race_bar": race_line,
    "race_sqaure": race_square,
    "race_trend": race_trend,
    "lang_bar": lang_line,
    "lang_square": lang_square,
    "lang_trend": lang_trend,
    "dementia_trend": dementia_trend,
    "bh_trend": bh_trend,
    "chronic_trend": None,
}

#CARDS
def dx_rate(dx, start_date, end_date, center):
    """
    Calculates percent of pariticpants with either a behvioral health dx
    (if dx=bh) or dementia(dx=dementia)

    Args:

        dx: can be "bh" or "dementia", will provide percent of participants
        over date range with a related dx

        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: percent with related dx, rounded to 2 decimal places
    """
    params = [
        pd.to_datetime(start_date).date(),
        pd.to_datetime(end_date).date(),
    ]

    center_sql, params = create_center_sql(center, params)

    if dx == "bh":
        dx_str = """(instr(icd10, 'F2') > 0
            OR instr(icd10, 'F31') > 0
            OR instr(icd10, 'F32') > 0
            OR instr(icd10, 'F33') > 0
            OR instr(icd10, 'F4') > 0
            OR instr(icd10, 'F6') > 0)
                """
    elif dx == "dementia":
        dx_str = """(instr(icd10, 'F00') > 0
            OR instr(icd10, 'F01') > 0
            OR instr(icd10, 'F02') > 0
            OR instr(icd10, 'F03') > 0
            OR instr(icd10, 'G3') > 0)
            """

    bh_dx_query = f"""
        SELECT COUNT(DISTINCT(dx.member_id)) FROM dx
        JOIN enrollment e ON dx.member_id=e.member_id
        WHERE {dx_str}
        AND (disenrollment_date >= ?
        OR disenrollment_date IS NULL)
        AND (enrollment_date <= ?)
        {center_sql};
        """

    enrolled_query = f"""
            SELECT COUNT(*)
            FROM enrollment e
            WHERE e.disenrollment_date >= ?
            OR e.disenrollment_date IS NULL
            AND e.enrollment_date <= ?
            {center_sql};
            """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()
    
    result = (
        c.execute(bh_dx_query, params).fetchone()[0]
        / c.execute(enrolled_query, params).fetchone()[0]
    ) * 100

    conn.close()
    return round(result, 2)

def avg_age(start_date, end_date, center):
    """
    Calculates average age of pariticpants for a given date range 
    and possibly filtered by center

    Args:

        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: avg participant age
    """
    params = [
        pd.to_datetime(end_date).date(),
        pd.to_datetime(start_date).date(),
        pd.to_datetime(end_date).date(),
    ]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ROUND(AVG((ifnull(julianday(e.disenrollment_date), julianday(?)) - julianday(d.dob)) / 365.25), 2)
        FROM demographics d
        JOIN enrollment e ON d.member_id = e.member_id
        WHERE (e.disenrollment_date >= ? OR e.disenrollment_date IS NULL)
        AND e.enrollment_date <= ?
        {center_sql};
        """
    
    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()
    return str(result)

def avg_years_enrolled(start_date, end_date, center):
    """
    Calculates average number of years pariticpants are enrolled
     for a given date range and filtered by center

    Args:

        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: average number of years pariticpants are enrolled
    """
    params = [
        pd.to_datetime(end_date).date(),
        pd.to_datetime(start_date).date(),
        pd.to_datetime(end_date).date(),
    ]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ROUND(AVG((ifnull(julianday(disenrollment_date), julianday(?)) - julianday(enrollment_date)) / 365.25), 2)
        FROM enrollment
        WHERE (disenrollment_date >= ? OR disenrollment_date IS NULL)
        AND enrollment_date <= ?
        {center_sql};
        """
    
    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()
    return str(result)

def attnd_day_center(start_date, end_date, center):
    """
    Calculates the number of pariticpants attending the day center
    for a given date range and filtered by center

    Args:

        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         int: number of pariticpants attending the day center
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT COUNT(DISTINCT(cd.member_id))
        FROM center_days cd
        JOIN enrollment e ON cd.member_id = e.member_id
        WHERE (e.disenrollment_date >= ? OR e.disenrollment_date IS NULL)
        AND e.enrollment_date <= ?
        AND cd.days != 'PRN'
        {center_sql};
        """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return str(result)

def non_english_percent(start_date, end_date, center):
    """
    Calculates the percent of pariticpants who do not speak
    english as their primary language for a given date
    range and filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: percent of pariticpants who do not speak
            english as their primary language
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ROUND(SUM(CASE when d.language != 'English' then 1 else 0 end) * 100.00 / count(*), 2)
        FROM demographics d
        JOIN enrollment e ON d.member_id = e.member_id
        WHERE (e.disenrollment_date >= ? OR e.disenrollment_date IS NULL)
        AND e.enrollment_date <= ?
        {center_sql};
        """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return str(result)

def non_white_percent(start_date, end_date, center):
    """
    Calculates the percent of pariticpants who are not
    white/Caucasian for a given date range and filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: percent of pariticpants who are not white/Caucasian
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ROUND(SUM(CASE when d.race != 'Caucasian/White' then 1 else 0 end) * 100.00 / count(*), 2)
        FROM demographics d
        JOIN enrollment e ON d.member_id = e.member_id
        WHERE (e.disenrollment_date >= ? OR e.disenrollment_date IS NULL)
        AND e.enrollment_date <= ?
        {center_sql};
        """

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return result

def dual_enrolled_percent(start_date, end_date, center):
    """
    Calculates the percent of pariticpants who are enrolled with
    both Medicaid and Medicare for a given date
    range and filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: percent of pariticpants who are enrolled with
            both Medicaid and Medicare
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ROUND(SUM(medicare) * 100.0 / count(*), 2)
        FROM enrollment
        WHERE (disenrollment_date >= ? OR disenrollment_date IS NULL)
        AND enrollment_date <= ?
        AND medicaid NOT NULL
        {center_sql};"""

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return result

def pneumo_vacc_rate(start_date, end_date, center):
    """
    Calculates the pneumococcal vaccination rate
    for a given date range and filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: pneumococcal vaccination rate
    """
    params = [
        pd.to_datetime(end_date).date(),
        pd.to_datetime(start_date).date(),
        pd.to_datetime(end_date).date(),
    ]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ROUND(SUM(CASE when pneumo.immunization_status NOT NULL then 1 else 0 end) * 100.00 / count(*), 2),
        ROUND((ifnull(julianday(e.disenrollment_date), julianday(?)) - julianday(d.dob)) / 365.25) as age
        FROM enrollment e
        LEFT JOIN demographics d ON e.member_id = d.member_id
        LEFT JOIN pneumo ON d.member_id = pneumo.member_id
        WHERE (e.disenrollment_date >= ? OR e.disenrollment_date IS NULL)
        AND e.enrollment_date <= ?
        AND age > 64
        {center_sql};"""

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return result

def influ_vacc_rate(start_date, end_date, center):
    """
    Calculates the influenza vaccination rate
    for a given date range and filtered by center

    Args:
        start_date: First date included in plotting dateframe

        end_date: Last date included in plotting dateframe

        center: Name of PACE center

     Returns:
         float: influenza vaccination rate
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ROUND(SUM(CASE when influ.immunization_status NOT NULL then 1 else 0 end) * 100.00 / count(*), 2)
        FROM enrollment e
        LEFT JOIN influ
        ON e.member_id = influ.member_id
        WHERE (e.disenrollment_date >= ? OR e.disenrollment_date IS NULL)
        AND e.enrollment_date <= ?
        {center_sql};"""

    conn = sqlite3.connect(db_filepath)
    c = conn.cursor()

    result = c.execute(query, params).fetchone()[0]

    conn.close()

    return result
