from flask_login import LoginManager, UserMixin
from . import create_app, create_dash
from .layouts import main_layout_header
from .users_mgt import db, User as base
from .run_db_update import update_db, update_files

# update dashboard database upon start
# update_db()

# update dashboard files upon start
# update_files()

# The Flask instance
server = create_app()

# The Dash instance
app = create_dash(server)

app.config.suppress_callback_exceptions = True

server = app.server

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"

# Create User class with UserMixin
class User(UserMixin, base):
    pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Push an application context so we can use Flask's 'current_app'
with server.app_context():
    # load the rest of our Dash app
    from . import index

    # configure the Dash instance's layout
    app.layout = main_layout_header()

