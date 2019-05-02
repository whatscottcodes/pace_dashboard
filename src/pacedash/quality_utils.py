import dash_table
import pandas as pd
from .census_utils import census_count_df
from .incidents_utils import total_incidents, incidents_per100mm
from .utilization_utils import admits_discharges, los_per_100mm, alos, snf_days, readmits_30_day
from collections import defaultdict
import calendar
from .helpers_configs import (
    create_daterange,
    color_palette
)

def quality_table(center):
    """
    Create table of various quality measures from other parts of the dashboard
    Can be filtered by center
    
    Args:
        center: A PACE center

    Returns:
        table: containing various quality measures

    To Do:
        Color code measures by threshold
        Create alerts based on thresholds
        Allow for dat filtering
    """
    quality_df_dict = defaultdict(list)

    today = pd.to_datetime('today')

    start_date = today - pd.offsets.MonthBegin(4)
    end_date = today - pd.offsets.MonthEnd(1)

    incidents = ['falls', 'med_errors', 'infections', 'burns', 'wounds']
    utl_types = ['inpatient', 'inpatient_psych', 'er_only', 'inpatient_snf']

    census_counts = census_count_df(center, start_date, end_date, 'M')
    quality_df_dict['Census'] = [int(month_census[1]) for month_census in census_counts.values[1:]]
    
    cols = []
    for month_end in create_daterange(start_date, end_date, 'M'):
        cols.append(calendar.month_abbr[month_end.month])
        month_start = month_end - pd.offsets.MonthEnd(1)
       
        for incident in incidents:
            quality_df_dict[f"Total {incident.title()}"].append(total_incidents(incident,  month_start, month_end, center))
            quality_df_dict[f"{incident.title()} per 100MM"].append(incidents_per100mm(incident,  month_start, month_end, center))
        
        for utl_type in utl_types:
            utl_key = ' '.join(utl_type.split("_")).title()
            quality_df_dict[f"{utl_key} Admissions"].append(admits_discharges(utl_type, 'admission_date', center,  month_start, month_end, None, None, None))

            if utl_type != 'er_only':
                quality_df_dict[f"{utl_key} Discharges"].append(admits_discharges(utl_type, 'discharge_date', center,  month_start, month_end, None, None, None))
        
            quality_df_dict[f"{utl_key} LOS per 100MM"].append(los_per_100mm(utl_type, center,  month_start, month_end, None, None, None))
            quality_df_dict[f"{utl_key} ALOS"].append(alos(utl_type, center,  month_start, month_end, None, None, None))

            admits = admits_discharges(utl_type, 'admission_date', center,  month_start, month_end, None, None, None)
            quality_df_dict[f"{utl_key} 30 Day Readmit Rate"].append(readmits_30_day(utl_type, admits, center,  month_start, month_end, None, None, None))

            if utl_type == 'inpatient_snf':
                for stay_type in ['Custodial', 'Skilled', 'Respite']:
                    quality_df_dict[f"{stay_type} Days per 100MM"].append(snf_days(center, month_start, month_end, None, None, stay_type))

    df = pd.DataFrame.from_dict(quality_df_dict, orient='index', columns = cols)
    df.reset_index(inplace=True)
    df.rename(columns={'index':'Measure'}, inplace=True)

    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_as_list_view=False,
        style_table={"width": "65vw", "maxHeight": "70vh", "overflowY": "scroll"},
        style_cell={"textAlign": "center", 'fontFamily':'Sans-serif'},
        style_cell_conditional=[
            {
            'if': {'column_id': 'Measure'},
            'textAlign': 'left'
            }
        ],
        style_header={
            "backgroundColor": color_palette[1],
            "fontColor": "white",
            "fontWeight": "bold",
        },
        is_focused = False
    )

def qapi_table(center):
    """
    Create table of PACE QAPI measures for the year
    Will need to be mostly manually built each year
    Args:
        center: A PACE center

    Returns:
        table: containing various quality measures

    To Do:
        WIP
    """
    df = pd.DataFrame.from_dict({'UTIs':'TBD'}, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index':'Measure', 0:'Value'}, inplace=True)

    return dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_as_list_view=False,
        style_table={"width": "65vw", "maxHeight": "90vh", "overflowY": "scroll"},
        style_cell={"textAlign": "left"},
        style_header={
            "backgroundColor": color_palette[1],
            "fontColor": "white",
            "fontWeight": "bold",
        },
    )