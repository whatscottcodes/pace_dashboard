import dash_table
from .helpers_configs import color_palette, sql_return_df, create_center_sql
import pandas as pd

def enrollment_by_town_table(start_date, end_date, center):
    """
    Creates dash_table of the number of participants who have been
    enrolled in PACE from various cities/towns in a given date range
    and filtered by center.

    Args:
        start_date: First date to include in resulting dateframe

        end_date: Last date to include in resulting dateframe

        center: Name of PACE center

    Returns:
        dash_table: table of the number of participants who have been
            enrolled in PACE from various cities/towns
    To Do:
        Possible add a way to download the table or allow
        the user to see changes in enrollment local
    """
    params = [pd.to_datetime(start_date).date(),
    pd.to_datetime(end_date).date(),
    pd.to_datetime(end_date).date(),
        ]

    center_sql, params = create_center_sql(center, params)

    query = f"""
        SELECT ad.city as 'City/Town', COUNT(*) as 'Number of Ppts' FROM addresses ad
        JOIN enrollment e ON ad.member_id=e.member_id
        WHERE (disenrollment_date BETWEEN ? AND ?
        OR disenrollment_date IS NULL)
        AND (enrollment_date <= ?)
        {center_sql}
        GROUP BY city
        ORDER BY 'Number of Ppts' DESC;
        """
    df = sql_return_df(query, params, None).sort_values("Number of Ppts", ascending=False)

    return dash_table.DataTable(
        id="table",
        columns=[{"name": col, "id": i} for col, i  in zip(df.columns, ['_0', '_1'])],
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