import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import pandas as pd
from ..app import app
from ..components import Row, Col
from ..helper_functions import center_enrollment, enrollment
from ..settings import color_palette


layout = html.Div(
    [
        Row(
            [
                Col(
                    [
                        dcc.Dropdown(
                            id="center-drop",
                            options=[
                                {"label": "All Centers", "value": "all"},
                                {"label": "Providence", "value": "Providence"},
                                {"label": "Westerly", "value": "Westerly"},
                                {"label": "Woonsocket", "value": "Woonsocket"},
                            ],
                            value="all",
                            searchable=False,
                        ),
                        dcc.Input(
                            id="start_date",
                            type="text",
                            size=13,
                            value=(
                                pd.to_datetime("today") - pd.DateOffset(years=1)
                            ).strftime("%m/%d/%Y"),
                            style={
                                "text-align": "center",
                                "width": "100%",
                                "min-height": "3vh",
                                "border-color": "#ccc",
                                "border-style": "solid",
                                "border-width": "1px",
                                "border-radius": "4px",
                            },
                        ),
                        dcc.Input(
                            id="end_date",
                            type="text",
                            size=13,
                            value=pd.to_datetime("today").strftime("%m/%d/%Y"),
                            style={
                                "text-align": "center",
                                "width": "100%",
                                "min-height": "3vh",
                                "border-color": "#ccc",
                                "border-style": "solid",
                                "border-width": "1px",
                                "border-radius": "4px",
                            },
                        ),
                        dcc.Interval(
                            id="interval-component",
                            interval=12 * 60 * 60 * 1000,  # in milliseconds
                            n_intervals=0,
                        ),
                        dcc.Link(
                            html.H6("Ppts Map"),
                            href="/map",
                            style={"font-size": "1vmin"},
                        ),
                        dcc.Link(
                            html.H6("Demo. EDA"),
                            href="/demographics-eda",
                            style={"font-size": "1vmin"},
                        ),
                        dcc.Link(
                            html.H6("Enroll. EDA"),
                            href="/enrollment-eda",
                            style={"font-size": "1vmin"},
                        ),
                        dcc.Link(
                            html.H6("Incidents EDA"),
                            href="/incidents-eda",
                            style={"font-size": "1vmin"},
                        ),
                        dcc.Link(
                            html.H6("Utl. EDA"),
                            href="/utilization-eda",
                            style={"font-size": "1vmin"},
                        ),
                    ],
                    bp="md",
                    size=2,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "flex-start",
                        "margin-bottom": "2vh",
                    },
                ),
                Col(
                    id="town-table",
                    size=10,
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "flex-start",
                    },
                ),
            ],
            style={
                "margin-top": "4vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
            },
        )
    ]
)


@app.callback(
    Output("town-table", "children"),
    [
        Input("start_date", "value"),
        Input("end_date", "value"),
        Input("center-drop", "value"),
    ],
)
def update_town_table(start_date, end_date, center):
    """
    Updates table of the count of participants
    from each city/town based on user choices
    """
    start_date = start_date.split("/")
    start_date = f"{start_date[2]}-{start_date[0]}-{start_date[1]}"

    end_date = end_date.split("/")
    end_date = f"{end_date[2]}-{end_date[0]}-{end_date[1]}"
    if center == "all":
        df = enrollment.enrollment_by_town_table((start_date, end_date))
    else:
        df = center_enrollment.enrollment_by_town_table((start_date, end_date), center)
    col_names = list(df.to_dict("rows")[0].keys())
    return dash_table.DataTable(
        id="table",
        columns=[{"name": col, "id": i} for col, i in zip(df.columns, col_names)],
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
