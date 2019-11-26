# These parameters will be passed to the 'config' attribute of the Flask
# instance used by the Dash app. They must be in UPPER CASE in order to take
# effect. For more information see http://flask.pocoo.org/docs/config.
import os
from datetime import timedelta
from pathlib import Path

#
# Config For your app
#

# Your App's title
TITLE = "PACE of RI"

ROUTES_PATHNAME_PREFIX = "/"

# The ID of the element used to inject each page of the multi-page app into
CONTENT_CONTAINER_ID = "dash-container"

NAVBAR_CONTAINER_ID = "navbar"

# Boolean that indicates whether to insert a navigation bar into the
# header/sidebar.
NAVBAR = True

# Ordered iterable of navbar items: tuples of (route, name), where 'route' is a
# string corresponding to path of the route (will be prefixed with
# URL_BASE_PATHNAME) and 'name' is a string corresponding to the name of the nav
# item.
NAV_ITEMS = (
    ("enrollment", "Enrollment"),
    ("demographics", "Demographics"),
    ("incidents", "Incidents"),
    ("operations", "Operations"),
    ("utilization", "Utilization"),
)


###File paths for using the dashboard - used all over
###only need to be set here
###only need to be changed if you use a different name
###for your databases
path_prefix = Path().absolute()
db_filepath = "src/pacedash/data/PaceDashboard.db"
user_db = f"{path_prefix}/src/pacedash/data/users.db"
log_path = "src/pacedash/data/log.txt"
agg_filepath = "src/pacedash/data/agg.db"

SECRET_KEY = os.urandom(12)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{user_db}"

SQLALCHEMY_TRACK_MODIFICATIONS = False

PERMANENT_SESSION_LIFETIME = timedelta(minutes=90)

PREFERRED_URL_SCHEME = "http"

# color palette for graphs and cards
color_palette = [
    "#00B760",  # this should be first color of your program
    "#8DCC8F",  # this should be a lighter shade of the first color of your program
    "#442359",  # this should be the second color of your program
    "#775F86",  # this should be a lighter of the second color of your program
    "#6EA4BF",
    "#CADDE7",
    "#F06449",
    "#F6AA9B",
    "#EF934C",
    "#F6C49D",
    "#191919",
    "#6C6C6C",
    "#F2C14E",
    "#F6D78E",
    "#fff",
]

# configuration for plotly graphs
graph_config = {
    "modeBarButtonsToRemove": [
        "sendDataToCloud",
        "hoverClosestCartesian",
        "autoScale2d",
        "select2d",
        "toggleSpikelines",
        "hoverCompareCartesian",
        "pan2d",
        "lasso2d",
    ],
    "responsive": "true",
    "displaylogo": "false",
    "sendData": "false",
    "showAxisDragHandles": "false",
    "doubleClick": "reset",
    # "editable": "true",
    "showAxisRangeEntryBoxes": "false",
    "toImageButtonOptions": {"format": "svg", "filename": "PACE_chart"},
}

# style of common dropdowns
dropdown_style = {"width": "100%", "white-space": "nowrap", "text-overflow": "ellipsis"}
