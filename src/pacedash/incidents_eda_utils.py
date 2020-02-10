import textwrap
from titlecase import titlecase
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from .helper_functions import (
    create_center_sql,
    create_join_sql,
    sql_return_df,
    build_bar_layout,
    build_scatter_layout,
    helpers
)
from .settings import color_palette
from .enrollment_eda_utils import census_count_df


#label and values for incident dropdowns
incident_types_dropdown = [
    {"label": "Falls", "value": "falls"},
    {"label": "Med Errors", "value": "med_errors"},
    {"label": "Burns", "value": "burns"},
    {"label": "Infections", "value": "infections"},
    {"label": "Wounds", "value": "wounds"}
]

#grouping options for med_errors
med_error_dropdown_options = [
    "location",
    "severity",
    "responsibility",
    "error_type",
    "contributing_factors",
    "actions_taken",
]

#grouping options for burns
burns_dropdown_options = [
    "location",
    "burn_location",
    "burn_degree",
    "contributing_factors",
    "actions_taken",
]

#grouping options for falls
falls_dropdown_options = [
    "location",
    "location_details",
    "activity_at_time_of_fall",
    "assistance_at_time_of_fall",
    "footwear",
    "severity",
    "environmental_factors",
    "symptoms",
    "following_treatment",
    "contributing_factors",
    "actions_taken",
]

#grouping options for infections
infections_dropdown_options = [
    "infection_type",
    "medication_prescribed",
    "where_infection_was_acquired",
    "infection_treated_by",
]

#grouping options for wounds
wounds_dropdown_options = [
    "living_situation",
    "living_details",
    "day_center",
    "pressure_ulcer",
    "burn",
    "wound_type"
]

#secondary dropdown values for each incident type
drop_downs = {
    "med_errors": med_error_dropdown_options,
    "burns": burns_dropdown_options,
    "falls": falls_dropdown_options,
    "infections": infections_dropdown_options,
    "wounds": wounds_dropdown_options,
}

# falls columns grouped by option
environmental_factors = [
    "clutter",
    "disrepair",
    "dme_not_in_use",
    "found_on_floor",
    "furniture",
    "gait_device_non_compliance",
    "needed_to_use_restroom",
    "oxygentubing",
    "poor_lighting",
    "rugs",
    "seatbelt_unbuckled",
    "seatbelt_unbuckled_by_participant",
    "transfer_without_assistance",
    "uneven_pavement",
    "wet_floor",
]

symptoms = [
    "body_pain",
    "chest_pain",
    "dizziness",
    "fainted",
    "headache",
    "incontinence",
    "increased_confusion",
    "loss_of_balance",
    "poor_vision",
    "shortness_of_breath",
    "weakness",
    "dementia_factors",
]


following_treatment = [
    "treatment_administered",
    "hypoglycemia",
    "hypotension",
    "syncope",
    "follow_up_xray",
    "follow_up_labs",
    "follow_up_er",
    "follow_up_hospital",
    "follow_up_paramedics",
]

contributing_factors_falls = [
    "improper_footwear",
    "improper_transfer_caregiver",
    "improper_transfer_family_member",
    "improper_transfer_pace_contractor",
    "improper_transfer_pace_staff",
    "lost_balance_items_not_properly_stored",
    "lost_balance_legs_buckled",
    "lost_balance_location_in_disrepair",
]

actions_taken_falls = [
    "intervention_medication_eval_change",
    "intervention_clinic_medical",
    "intervention_nutrition_services",
    "intervention_pt",
    "intervention_ot",
    "intervention_day_center",
    "intervention_dme",
    "intervention_other",
    "action_family_education",
    "action_home_care_assessment",
    "action_implemented_falls_prevention_program",
    "action_implemented_new_policy",
    "action_increased_ot_pt",
    "action_initiated_contractor_oversight",
    "action_initiated_quality_improvement_activities",
    "action_medication_evaluation_change",
    "action_modified_alf_environment",
    "action_modified_hospital_environment",
    "action_modified_nf_environment",
    "action_modified_pace_center_environment",
    "action_modified_ppt_home_environment",
    "action_ot_assessment",
    "action_pcp_assessment",
    "action_ppt_education",
    "action_pt_assessment",
    "action_revised_existing_policy",
    "action_rn_assessment",
    "action_staff_education",
]
#maps falls dropdown grouping to their columns
falls_dict = {
    "location": ["location"],
    "location_details": ["location_details"],
    "activity_at_time_of_fall": ["activity_at_time_of_fall"],
    "assistance_at_time_of_fall": ["assistance_at_time_of_fall"],
    "footwear": ["footwear"],
    "severity": ["severity"],
    "environmental_factors": environmental_factors,
    "symptoms": symptoms,
    "following_treatment": following_treatment,
    "contributing_factors": contributing_factors_falls,
    "actions_taken": actions_taken_falls,
}

# med_errors columns grouped by option
responsibility = [
    "responsibility_pharmacy",
    "responsibility_clinic",
    "responsibility_home_care",
    "responsibility_facility",
    "responsible_facility_name",
    "other_responsible_party",
]

error_type = [
    "wrong_dose",
    "wrong_dose_not_administered",
    "wrong_med_tx",
    "wrong_med_tx_not_administered",
    "wrong_ppt",
    "wrong_ppt_not_administered",
    "wrong_route",
    "wrong_label_not_administered",
    "wrong_time_day",
    "dose_omitted_not_administered",
    "expired_order",
    "transcription",
    "not_ordered",
    "med_given_despite_hold_order_vs",
    "med_tx_given_with_known_allergy",
    "med_tx_given_beyond_stop_date",
    "other_error_code",
]

contributing_factors_med_errors = [
    "change_in_delivery_method",
    "change_in_pharmacy",
    "communication_with_inpatient_hospice",
    "communication_with_acs",
    "communication_with_alf",
    "communication_with_hospital",
    "communication_with_nursing_facility",
    "communication_with_pharmacy",
    "administered_by_unauthorized_staff",
    "new_staff_member",
    "order_transcription_error",
    "participant_id_error",
    "pharmacy_error",
    "physician_prescription_error",
    "similar_name",
    "staff_error",
    "other_contributing_factor",
]

actions_taken_med_errors = [
    "family_education",
    "home_care_assessment",
    "implemented_falls_prevention_program",
    "implemented_new_policy",
    "increased_ot_pt",
    "initiated_contractor_oversight",
    "initiated_quality_improvement_activities",
    "medication_evaluation_change",
    "modified_alf_environment",
    "modified_hospital_environment",
    "modified_nf_environment",
    "modified_pace_center_environment",
    "modified_ppt_home_environment",
    "ot_assessment",
    "pcp_assessment",
    "ppt_education",
    "pt_assessment",
    "revised_existing_policy",
    "rn_assessment",
    "staff_education",
    "increase_home_care",
    "increased_center_attendance",
    "change_in_contracted_provider",
    "change_to_medication_administration_process",
    "change_to_participant_identification_process",
    "changes_to_medication_prescription_process",
    "changes_to_medication_transcription_process",
    "implemented_a_new_medication_delivery_system",
    "requested_a_corrective_action_plan_from_contracted_provider",
]
#maps med_errors dropdown grouping to their columns
med_errors_dict = {
    "location": ["location"],
    "location_details": ["location_details"],
    "severity": ["severity"],
    "responsibility": responsibility,
    "error_type": error_type,
    "contributing_factors": contributing_factors_med_errors,
    "actions_taken": actions_taken_med_errors,
}

# burns columns grouped by options
contributing_factors_burns = [
    "adaptive_equipment_not_used",
    "decrease_in_center_attendance",
    "decrease_in_home_care",
    "delay_of_scheduled_home_care",
    "diagnosis_of_dementia",
    "equipment_malfunction",
    "hot_food",
    "hot_water",
    "improper_food_handling",
    "improper_use_of_chemicals",
    "improperly_sored_chemicals",
    "lack_of_education_caregiver",
    "lack_of_education_contractor",
    "lack_of_education_participant",
    "lack_of_education_staff",
    "non_compliance_with_medications",
    "non_compliance_with_care_plan_caregiver",
    "non_compliance_with_care_plan_contractor",
    "non_compliance_with_care_plan_participant",
    "non_compliance_with_care_plan_staff",
    "non_compliance_with_pace_policies",
    "participant_cognitive_impairment",
    "participant_cooking",
    "participant_cooking_instructed_not_to_cook",
    "participant_did_not_wait_for_assistance",
    "participant_smoking",
    "participant_curling_iron",
    "participant_iron",
    "participant_lighter",
    "participant_left_unsupervised",
    "no_applicable_policies",
    "sun_exposure",
    "unknown_conributing_factor",
]

actions_taken_burns = [
    "assessment_activities",
    "assessment_dietary",
    "assessment_home_care",
    "assessment_ot",
    "assessment_pcp",
    "assessment_pt",
    "assessment_rn",
    "assessment_sw",
    "education_contracted_provider",
    "education_family_caregiver",
    "education_participant",
    "education_staff",
    "implemented_file_burn_prevention_program",
    "increased_center_attendance",
    "increased_home_care",
    "increased_pt_ot",
    "increased_staff_at_contracted_provider_facility",
    "increased_staff_at_pace_center",
    "initiated_contractor_oversight",
    "initiated_quality_improvement_activities",
    "installed_fire_extinguisher",
    "installed_smoke_detectors",
    "medication_change",
    "medication_evaluation",
    "modified_environment_participants_home",
    "modified_environment_assisted_living_facility",
    "modified_environment_hospital"
]

#maps burns dropdown grouping to their columns
burns_dict = {
    "location": ["location"],
    "location_details": ["location_details"],
    "burn_location": ["burn_location"],
    "burn_degree": ["burn_degree"],
    "contributing_factors": contributing_factors_burns,
    "actions_taken": actions_taken_burns,
}

#maps infections dropdown grouping to their columns
infections_dict = {
    "infection_type": ["infection_type"],
    "medication_prescribed": ["medication_prescribed"],
    "where_infection_was_acquired": ["where_infection_was_acquired"],
    "infection_treated_by": ["infection_treated_by"],
}

#maps wounds dropdown grouping to their columns
wounds_dict = {
    "living_situation": ["living_situation"],
    "living_details": ["living_details"],
    "day_center": ["day_center"],
    "pressure_ulcer": ["pressure_ulcer"],
    "burn": ["burn"],
    "wound_type": ["wound_type"]
}

#dictionary for getting dropdown option mapping
#for each incident
incident_dict = {
    "falls": falls_dict,
    "med_errors": med_errors_dict,
    "burns": burns_dict,
    "infections": infections_dict,
    "wounds": wounds_dict
}

def get_total_incidents(incident, start_date, end_date, freq, center):
    """
    Gets a list of total incidents in each frequency grouping ordered from
    earliest to latest

    Args:
        incident(str): table to use as incident
        start_date: start of the period in YYYY-MM-DD format
        start_date: end of the period in YYYY-MM-DD format
        freq(str): QS or MS, indicates if values should be aggregated 
            monthly or quarterly
        center(str): indicates what center to filter for
    
    Returns:
        list: total incidents for each month or quarter
    """
    params = [str(pd.to_datetime(start_date)), str(pd.to_datetime(end_date))]
    center_sql, params = create_center_sql(center, params)
    join_sql = create_join_sql(center, incident)
    
    query_dict = {'QS':f"""
    SELECT COUNT({incident}.member_id) as total,
    (cast(strftime('%m', date_time_occurred) as integer) + 2) / 3 as quarter,
    strftime('%Y', date_time_occurred) as year
    FROM {incident}
    {join_sql}
    WHERE date_time_occurred BETWEEN ? AND ?
    {center_sql}
    GROUP BY year, quarter;
    """,
                  'MS':f"""
    SELECT COUNT({incident}.member_id) as total,
    strftime('%m', date_time_occurred) as month,
    strftime('%Y', date_time_occurred) as year
    FROM {incident}
    {join_sql}
    WHERE date_time_occurred BETWEEN ? AND ?
    {center_sql}
    GROUP BY year, month;
    """}
    

    totals = [val[0] for val in helpers.fetchall_query(query_dict[freq], params)]
    
    return totals

def incidents_df(start_date, end_date, incident, center, freq):
    """
    Creates pandas dataframe from SQL table of selected incident

    Args:
        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        incident: incident table to run query on

        center: Name of PACE center

        freq: M or Q, determines if results should be grouped by
            month or quarter

    Returns:
        df: pandas dataframe with all columns of SQL table
            of selected incident with a date column for
            grouping the df by month or quarter
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]
    center_sql, params = create_center_sql(center, params)
 
    query = f"""
    SELECT DISTINCT i.* FROM {incident} i
    JOIN centers on i.member_id=centers.member_id
    WHERE i.date_time_occurred BETWEEN ? AND ?
    {center_sql};
    """
    df = sql_return_df(query, params, ["date_time_occurred"])
    df["date"] = df["date_time_occurred"].dt.to_period(freq[0])

    return df

def repeat_ppts(incident, start_date, end_date, center):
    """
    Calculates number of participants with multiple incidents,
        the percent of incidents attributed to these participants,
        the number of participants with a number of incidents
        above the outlier limit,
        and the outlier limit(mean+1SD)

    Args:
        incident: incident type user selected

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        center: Name of PACE center
        
        get_ppts: Default False, 
            if True only return a list of ppts with multiple incidents
        
        total_num_from_outlier_ppts: Default False,
            if True only return the total number of incidents
            attributed to participants with a number of
            incidents above the outlier limit

    Returns:
        ppts_w_multiple: list of ppts with multiple incidents
    """
    params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

    center_sql, params = create_center_sql(center, params)

    join_sql = create_join_sql(center, incident)

    repeat_incidents_query = f"""
        SELECT {incident}.member_id, COUNT(*) FROM {incident}
        {join_sql}
        WHERE date_time_occurred BETWEEN ? AND ?
        {center_sql}
        GROUP BY {incident}.member_id
        HAVING COUNT(*) > 1;
        """
    ppts_w_multiple = helpers.fetchall_query(repeat_incidents_query, params)
    
    return ppts_w_multiple   

def df_no_outliers(df, incident, start_date, end_date, center):
    """
    Removes any participant with a number of incidents in the
    daterange greater than the determined outlier number

    Args:
        df: incident dataframe to remove outliers from

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        incident: incident table to run query on

        center: Name of PACE center

    Returns:
        df: pandas dataframe with any participant with a number of
        incidents in the daterange greater than the
        determined outlier number removed
    """
    ppts_w_multiple = repeat_ppts(incident, start_date, end_date, center)

    incident_mean = np.mean([val[1] for val in ppts_w_multiple])
    incident_sd = np.std([val[1] for val in ppts_w_multiple])
    
    outlier_num = incident_mean + incident_sd

    outlier_ppts = [val[0] for val in ppts_w_multiple if val[1] >= int(outlier_num)]

    df = df[-df.member_id.isin(outlier_ppts)]

    return df

def update_graph(
    incident, start_date, end_date, freq, cols, incident_details, amount, center, remove_outliers
):
    """
    Creates bar graph  of incidents in time frame grouped by user selected filter

    Args:
        incident: incident type user selected

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        cols: selected column grouping to group plot by

        incident_details: value from cols to filter plot by

        amount: number of column groups to plot, can be 5 or 10

        center: Name of PACE center

        remove_outliers: if true participants with more
            incidents than the outlier number are not
            included

    Returns:
         dict: containing plotly figure data and layout information
    """
    df = incidents_df(start_date, end_date, incident, center, freq)

    if remove_outliers:
        df = df_no_outliers(df, incident, start_date, end_date, center)

    plot_cols = incident_dict[incident][cols]

    plot_df = df[["date_time_occurred", "date"] + plot_cols].copy()

    if len(plot_cols) == 1:
        plot_df = pd.concat([plot_df, pd.get_dummies(plot_df[plot_cols], prefix='', prefix_sep='')], axis=1)
    plot_df = plot_df.groupby(["date"]).sum().reset_index()
    
    totals = get_total_incidents(incident, start_date, end_date, freq, center)
    if (incident_details is None) or (len(incident_details) == 0):
        included_cols = (
            plot_df[[col for col in plot_df.columns if col != 'date']].sum().sort_values(ascending=False)[: int(amount)].index.tolist()
        )
        plot_df = plot_df[["date"] + included_cols]
    else:
        plot_df = plot_df[["date"] + incident_details]

    fig_data = [
            go.Bar(
                x=plot_df["date"].astype(str),
                y=(plot_df[col] / totals) * 100,
                text=[
                    f"{val} ({str(round((val/tot*100),2))})% {titlecase(col.replace('_', ' '))}"
                    if val != 0
                    else None
                    for val, tot in zip(plot_df[col], totals)
                ],
                hoverinfo="x+text",
                name='<br>'.join(textwrap.wrap(titlecase(" ".join(col.split("_"))), width=15)),
                marker=dict(color=color),
            )
            for col, color in zip(plot_df.columns[1:], color_palette)
            if (plot_df[col].sum()) != 0
        ]

    if ((end_date.month - start_date.month) < 6) & ((end_date.year - start_date.year) < 1) & (freq != 'Q'):
        x_ticks = plot_df['date'].astype(str)
    else:
        x_ticks = pd.Series([])
    filter_title =" ".join(cols.split("_"))
    fig_layout = build_bar_layout(
                f"Percent of {titlecase(incident)} by {titlecase(filter_title)}",
        legend = dict(orientation="h", y=-0.15, font={'size':9.5}), y_title='Percent',
        x_ticks=x_ticks
    )

    return dict(data=fig_data, layout=fig_layout)

def update_trending_graph(incident, start_date, end_date, freq, measure, center, remove_outliers):
    """
    Creates line graph of incidents, can be total or per member per month

    Args:
        incident: incident type user selected

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        freq: M or Q, determines if results should be grouped by
            month or quarter

        measure: indicates if chart should be total incidents
            or pmpm

        center: Name of PACE center

        remove_outliers: if true participants with more
            incidents than the outlier number are not
            included

    Returns:
         dict: containing plotly figure data and layout information
    """
    df = incidents_df(start_date, end_date, incident, center, freq)
    
    if remove_outliers:
        df = df_no_outliers(df, incident, start_date, end_date, center)

    plot_df = df.groupby(["date"]).count().reset_index()[["date", "date_time_occurred"]]
    plot_df.rename(columns={"date_time_occurred": "count"}, inplace=True)

    if measure == "pmpm":
        if freq == 'QS':
            pmpm_df = census_count_df(center, start_date, end_date, freq, quarter_pmpm=True)
        else:
            pmpm_df = census_count_df(center, start_date, end_date, freq)
        plot_df["count"] = (plot_df["count"] / pmpm_df["Census"]) * 100
        
        plot_title = f"{titlecase(incident)} Per 100 Participants"
    else:
        plot_title = f"{titlecase(incident)} Total"

    if freq == 'Q':
        fig_data = [
            go.Bar(
                x=plot_df["date"].astype(str),
                y=plot_df["count"],
                marker={"color": color_palette[0]},
                showlegend=False,
            )
        ]
    else:        
        fig_data = [
            go.Scatter(
                x=plot_df["date"].astype(str),
                y=plot_df["count"],
                mode="lines",
                line={"width": 7, "color": color_palette[0]},
            )
        ]

    if ((end_date.month - start_date.month) < 6) & ((end_date.year - start_date.year) < 1) & (freq != 'Q'):
        x_ticks = plot_df['date'].astype(str)
    else:
        x_ticks = pd.Series([])

    fig_layout = build_scatter_layout(
        f"{plot_title}", plot_df["count"].min(),
        plot_df["count"].max(),
        x_ticks=x_ticks
        )

    return dict(data=fig_data, layout=fig_layout)

def incident_details_options(start_date, end_date, selected_incident, selected_cols, amount, center):
    """
    Creates dictionary for incident detail drop down. If the number of column values is less than
    the amount shown, the dictionary is empty.

    Args:

        start_date: First date to include in resulting dataframe

        end_date: Last date to include in resulting dataframe

        selected_incident: incident type user selected

        selected_cols: select column to group plot by

        amount: number of groups to be show on graph

        center: Name of PACE center

    Returns:
        dict: for incident detail drop down
    """
    incident_options = incident_dict[selected_incident][selected_cols]
    
    if len(incident_options) == 1:
        params = [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]

        center_sql, params = create_center_sql(center, params)
        join_sql = create_join_sql(center, selected_incident)

        query = f"""
        SELECT DISTINCT({selected_cols})
        FROM {selected_incident}
        {join_sql}
        WHERE date_time_occurred BETWEEN ? AND ?
        {center_sql};
        """

        incident_options = [val[0] for val in helpers.fetchall_query(query, params)]
        
    if len(incident_options) > int(amount):
        return [
            {"label": titlecase(i.replace("_", " ")), "value": i}
            for i in incident_options
            if i != None
        ]
        
    return [{}]
