import dash_table
from .helper_functions import team
from .settings import color_palette

###hold all team function used to create team comparison table
all_team_funcs = [
    (team.admissions_by_team, ["acute"]),
    (team.er_only_visits_by_team, None),
    (team.admissions_by_team, ["psych"]),
    (team.days_by_team, ["custodial"]),
    (team.days_by_team, ["respite"]),
    (team.days_by_team, ["skilled"]),
    (team.discharges_by_team, ["acute"]),
    (team.alos_for_discharges_by_team, ["acute"]),
    (team.readmits_by_team, ["acute", 30]),
    (team.avg_age_by_team, None),
    (team.percent_primary_non_english_by_team, None),
    (team.avg_years_enrolled_by_team, None),
    (team.ppts_in_custodial_by_team, None),
    (team.mortality_by_team, None),
    (team.percent_of_discharges_with_mortality_in_30_by_team, None),
    (team.mortality_within_30days_of_discharge_rate_by_team, None),
    (team.no_hosp_admission_since_enrollment_by_team, None),
    (team.pressure_ulcer_rate_by_team, None),
    (team.total_incidents_by_team, ["falls"]),
    (team.incidents_per_member_by_team, ["falls"]),
    (team.ppts_w_incident_by_team, ["falls"]),
    (team.total_incidents_by_team, ["med_errors"]),
    (team.incidents_per_member_by_team, ["med_errors"]),
    (team.ppts_w_incident_by_team, ["med_errors"]),
    (team.total_incidents_by_team, ["infections"]),
    (team.incidents_per_member_by_team, ["infections"]),
    (team.ppts_w_incident_by_team, ["infections"]),
]


def create_comparison_table(params, return_df=False):
    """
    Creates dash table with rows of indicators
    and column of team names for the indicated time period.

    params (tuple): start date and end date in format 'YYYY-MM-DD'
    return_df(bool): indicates if the pandas dataframe should be returned
    instead of the dash table

    Returns:
        dash table: dash table object
        or
        DataFrame: pandas dataframe
    """

    df = team.ppts_on_team(params)
    for func in all_team_funcs:
        team_summary_func = func[0]
        args = func[1]
        if args is None:
            df = df.merge(team_summary_func(params), on="team", how="left")
        else:
            df = df.merge(team_summary_func(params, *args), on="team", how="left")

    df.columns = [col.title() for col in df.columns]
    df = df.sort_values("Participants", ascending=False).T
    df.columns = df.loc["Team"]
    df.drop("Team", inplace=True)
    df.fillna(0, inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Indicator", None: "None"}, inplace=True)

    if return_df:
        return df

    return dash_table.DataTable(
        id="table",
        columns=[
            {"name": col, "id": i}
            for col, i in zip(df.columns, list(df.to_dict("rows")[0].keys()))
        ],
        data=df.to_dict("rows"),
        style_as_list_view=False,
        style_table={"width": "80vw", "maxHeight": "90vh", "overflowY": "scroll"},
        style_cell={"textAlign": "center"},
        style_header={
            "backgroundColor": color_palette[1],
            "fontColor": "white",
            "fontWeight": "bold",
        },
    )
