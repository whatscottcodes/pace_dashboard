import urllib
import dash_html_components as html
from dash.dependencies import Input, Output
from ..app import app
from ..components import Row, Col
from ..team_utils import create_comparison_table
from ..layouts import indicator_header
from ..helper_functions import time_range_dict
from ..settings import color_palette

layout = html.Div(
    [
        Row(indicator_header(title="Team Comparison"), className="header-row"),
        Row(
            [
                Col(
                    [
                        html.A(
                            "Download Data",
                            id="download-link",
                            download="team_comparison.csv",
                            href="",
                            target="_blank",
                        )
                    ],
                    size=1,
                    mobile_size=12,
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "justify-content": "flex-start",
                        "align-items": "flex-start",
                    },
                ),
                Col(
                    id="team-table",
                    size=11,
                    mobile_size=12,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "flex-start",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
            },
        ),
    ]
)

indictors_to_url = {
    "Participants": "team_info-ppts",
    "Acute Admissions": "team_utl-acute_admissions",
    "Er_Only": "team_utl-acute_admissions",
    "Psych Admissions": "team_utl-er_only_visits",
    "Custodial Days": "team_utl-custodial_days",
    "Respite Days": "team_utl-respite_days",
    "Skilled Days": "team_utl-skilled_days",
    "Acute Discharges": "team_utl-acute_discharges",
    "Acute Alos": "team_utl-acute_alos",
    "Acute 30 Day Readmits": "team_utl-readmits",
    "Age": "team_info-avg_age",
    "Percent Non English": "team_info-percent_primary_non_english",
    "Avg_Years_Enrolled": "team_info-avg_years_enrolled",
    "Ppts In Custodial": "team_utl-custodial_ppts",
    "Mortality Rate": "team_info-mortality",
    "% Of Discharges With Death Within 30 Days": "team_utl-percent_of_discharges_with_mortality_in_30",
    "Death Within 30 Days Of Discharge Date": "team_utl-mortality_within_30_days_of_discharge",
    "Percent With No Admissions Since Enrollment": "team_utl-no_hosp_admission_since_enrollment",
    "Wound Rate": "team_incidents-wounds_per_100MM",
    "Falls": "team_incidents-falls",
    "Falls Per 100 Ppts": "team_incidents-falls_per_100MM",
    "Individuals W/ Falls": "team_incidents-falls_unique_ppts",
    "Med_Errors": "team_incidents-med_errors",
    "Med_Errors Per 100 Ppts": "team_incidents-med_errors_per_100MM",
    "Individuals W/ Med_Errors": "team_incidents-med_errors_unique_ppts",
    "Infections": "team_incidents-infections",
    "Infections Per 100 Ppts": "team_incidents-infections_per_100MM",
    "Individuals W/ Infections": "team_incidents-infections_unique_ppts",
}


@app.callback(Output("team-table", "children"), [Input("time_range", "value")])
def update_team_table(time_range):
    """
    Updates table of the count of participants
    from each city/town based on user choices
    """
    params = time_range_dict[time_range][0]()
    dff = create_comparison_table(params, return_df=True)

    return html.Table(
        # Header
        [
            html.Tr(
                [html.Th(col) for col in dff.columns],
                style={
                    "background-color": color_palette[0],
                    "color": "white",
                    "text-align": "center",
                },
            )
        ]
        +
        # Body
        [
            html.Tr(
                [
                    html.Td(
                        html.A(
                            dff.iloc[i][col],
                            href=f"{indictors_to_url[dff.iloc[i][col]]}",
                            target="_blank",
                        ),
                        style={"text-align": "center"},
                    )
                    if col == "Indicator"
                    else html.Td(dff.iloc[i][col], style={"text-align": "center"})
                    for col in dff.columns
                ]
            )
            for i in range(dff.shape[0])
        ],
        className="table table-striped",
    )


@app.callback(Output("download-link", "href"), [Input("time_range", "value")])
def update_download_link(time_range):
    """
    Returns a csv string of the data used to create the chart

    Args:
        time_range(str): time period of the table values
        
    Returns:
        str: string used to allow user to download csv of data
    """
    params = time_range_dict[time_range][0]()
    dff = create_comparison_table(params, return_df=True)
    csv_string = dff.to_csv(index=False, encoding="utf-8")
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(
        csv_string
    )
    return csv_string
