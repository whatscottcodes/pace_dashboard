import datetime
from flask import current_app as server
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_html_components as html
from flask_login import logout_user, current_user
import pandas as pd
from .app import app
from .pages import (
    create_pw,
    default_graph_page,
    demographics,
    demographics_eda,
    enrollment,
    enrollment_eda,
    incidents,
    incidents_eda,
    inpatient,
    login,
    login_fd,
    logout,
    nursing_facilities,
    operations,
    ppt_map,
    teams,
    town_table,
    utilization_eda,
)
from .components import Navbar
from .settings import log_path
from .utils import get_url

# The router
# Ordered iterable of routes: tuples of (route, layout), where 'route' is a
# string corresponding to path of the route (will be prefixed with Dash's
# 'routes_pathname_prefix' and 'layout' is a Dash Component.

urls = (
    ("", enrollment.layout),
    ("login", login.layout),
    ("logout", logout.layout),
    ("create_password", create_pw.layout),
    ("enrollment", enrollment.layout),
    ("demographics", demographics.layout),
    ("incidents", incidents.layout),
    ("utilization", inpatient.layout),
    ("inpatient", inpatient.layout),
    ("nursing-facility", nursing_facilities.layout),
    ("operations", operations.layout),
    ("teams", teams.layout),
    ("enrollment-eda", enrollment_eda.layout),
    ("demographics-eda", demographics_eda.layout),
    ("incidents-eda", incidents_eda.layout),
    ("utilization-eda", utilization_eda.layout),
    ("map", ppt_map.layout),
    ("town_count", town_table.layout),
)

routes = {get_url(route): layout for route, layout in urls}

# creates list of paths that need to be password protected
protected_paths = [
    f"/{page_info[0]}"
    for page_info in urls
    if page_info[0] not in ["login", "logout", "create_password"]
]

# router


@app.callback(
    Output(server.config["CONTENT_CONTAINER_ID"], "children"),
    [Input("url", "pathname")],
)
def router(pathname):
    """routes pathname to correct layout"""
    if current_user.is_authenticated:
        default_layout = default_graph_page.layout
    else:
        default_layout = login_fd.layout
    if pathname in protected_paths:
        if current_user.is_authenticated:
            return routes.get(pathname, default_layout)

        return login_fd.layout
    if pathname == "/logout":
        if current_user.is_authenticated:

            log_file = open(log_path, "a")
            log_file.write(f"{current_user.username}, {datetime.datetime.now()}, 0\n")
            log_file.close()

            logout_user()
            return routes.get(pathname, default_layout)

        return routes.get(pathname, default_layout)

    return routes.get(pathname, default_layout)


# logout button


@app.callback(Output("logout", "children"), [Input("url", "pathname")])
def user_logout(input1):
    """
    If the user is logged in, creates a logout button
    """
    if current_user.is_authenticated:
        return html.A(
            "Logout",
            href="/logout",
            style={
                "padding-top": "1.5vmin",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "flex-end",
                "align-content": "flex-end",
                "font-size": "1vmax",
                "position": "relative",
                "text-align": "center",
                "width": "48vw",
            },
        )
    else:
        return ""


@app.callback(
    Output("start_date", "value"), [Input("interval-component", "n_intervals")]
)
def update_start_date(n):
    """
    Used to update the start date value to a 
    year before today's date every 12 hours
    """
    return (pd.to_datetime("today") - pd.DateOffset(years=1)).strftime("%m/%d/%Y")


@app.callback(Output("end_date", "value"), [Input("interval-component", "n_intervals")])
def update_end_date(n):
    """
    Used to update the end date value to today's date
    every 12 hours
    """
    return pd.to_datetime("today").strftime("%m/%d/%Y")


# The Navbar
if server.config["NAVBAR"]:

    @app.callback(
        Output(server.config["NAVBAR_CONTAINER_ID"], "children"),
        [Input("url", "pathname")],
    )
    def update_nav(pathname):
        """Create the navbar with the current page set to active"""
        if pathname is None:
            # pathname is None on the first load of the app; ignore this
            raise PreventUpdate("Ignoring first url.pathname callback")
        return Navbar(items=server.config["NAV_ITEMS"], current_path=pathname)
