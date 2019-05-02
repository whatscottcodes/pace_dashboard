# These parameters will be passed to the 'config' attribute of the Flask
# instance used by the Dash app. They must be in UPPER CASE in order to take
# effect. For more information see http://flask.pocoo.org/docs/config.
import os
from datetime import timedelta
from .helpers_configs import user_db

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
    ("census", "Census"),
    ("demographics", "Demographics"),
    ("incidents", "Incidents"),
    ("utilization", "Utilization"),
    ("grievances", "Grievances"),
)

SECRET_KEY = os.urandom(12)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{user_db}"

SQLALCHEMY_TRACK_MODIFICATIONS = False

PERMANENT_SESSION_LIFETIME = timedelta(minutes=90)

PREFERRED_URL_SCHEME = "http"

