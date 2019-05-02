import dash_html_components as html
from .users_mgt import add_user
import re
import sqlite3
from .helpers_configs import user_db
from .app import User
from flask_login import login_user
from werkzeug.security import check_password_hash
from .users_mgt import add_user



def redirect_to_login(n_clicks):
    """
    Redirects user to login page if button is pressed
    """
    if n_clicks > 0:
        return '/login'

#password/login functions
def validate(password):
    """
    Validates that the set password matches the restrictions
    Restrictions:
        Longer than 8 characters
        At least 2 numbers
        At least 1 capital letter
        No spaces
        At least 1 special charactr (cannot be * or ;)

    Args:
        password: password user has created
    
    Returns:
        Bool: True if valid, False if not
        Str: Error message is not valie, empty if valid
    """
    if len(password) < 8:
        return False, "Make sure your password is at lest 8 letters"
    elif sum(map(str.isdigit, password)) < 2:
        return False, "Make sure your password has atleast 2 numbers in it"
    elif re.search('[A-Z]',password) is None: 
        return False, "Make sure your password has atleast one capital letter in it"
    elif re.search(r"\s", password) is not None:
        return False, "Make sure your password does not contains any spaces"
    elif re.match("^[a-zA-Z0-9_]*$", password) is not None:
        return False, 'Make sure your password has a special chartacter'
    elif ('*' in password) or (';' in password) or ('=' in password):
        return False, '* or ; is not allowed'

    return True , ''

def check_user(username, password):
    """
    Checks that username and password are valid

    All users must be in the username table in the users database
    and have a 0 in the 'has_password' column

    Args:
        username: username string

        password: password string
    
    Returns:
        Link to login or error message.
    """
    if re.search(r"\s", username) is not None:
        return 'User does not exist'
    if ('*' in username) or ('=' in username) or (';' in username):
        return 'User does not exist'
    
    conn = sqlite3.connect(user_db)
    c = conn.cursor()

    q = """
        SELECT username, email, has_password FROM usernames
        WHERE username = ?;
        """
    try:
        user, email, has_password = c.execute(q, [username]).fetchone()
    except TypeError:
        conn.close()
        return 'User does not exist'
    
    if has_password == 0:
        if validate(password)[0]:
            add_user(f"{user}",password,f"{email}")
            update_usernames = """
                UPDATE usernames
                SET has_password = 1
                WHERE username = ?;
                """
            c.execute(update_usernames, [username])
            conn.commit()
            conn.close()
        else:
            return html.P(validate(password)[1], style={'text-align':'center', 'font-size':'2vmin', 'content-align':'center', "padding-top": "2.5vh"})
    else:
        return 'Password already set'
        
    
    return html.A('Password created, please login',
            href="/login",
            style={"display": "flex",
                "flex-direction": "row", 'padding':0,
                "justify-content": "flex-start", "align-items": "flex-start", 'font-size':'2vmin'})