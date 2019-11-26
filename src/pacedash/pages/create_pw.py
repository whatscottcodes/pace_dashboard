import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from ..helper_functions import color_palette
from ..app import app
from ..components import Row, Col
from ..login_utils import check_user

layout = html.Div(
    [
        Row(
            [
                Col(
                    [
                        Row(
                            [
                                Col(
                                    [
                                        html.H2(
                                            "Create Password",
                                            style={
                                                "color": color_palette[2],
                                                "font-size": "3.5vmin",
                                            },
                                        )
                                    ],
                                    style={
                                        "padding-bottom": "1vh",
                                        "padding-top": "1vh",
                                        "display": "flex",
                                        "flex-direction": "row",
                                        "justify-content": "flex-start",
                                        "align-items": "center",
                                    },
                                )
                            ]
                        ),
                        Row(
                            [
                                Col(
                                    [
                                        dcc.Input(
                                            id="uname-box",
                                            type="text",
                                            size=40,
                                            placeholder="Enter your username",
                                            style={
                                                "font-size": "1vmax",
                                                "text-align": "center",
                                                "width": "98%",
                                                "height": "98%",
                                                "border-color": "#ccc",
                                                "border-style": "solid",
                                                "border-width": "1px",
                                                "border-radius": "4px",
                                            },
                                        )
                                    ],
                                    bp="md",
                                    size=12,
                                )
                            ],
                            style={"margin-bottom": "2vh"},
                        ),
                        Row(
                            [
                                Col(
                                    [
                                        dcc.Input(
                                            id="pwd-box",
                                            type="password",
                                            size=40,
                                            n_submit_timestamp="0",
                                            placeholder="Enter your password",
                                            style={
                                                "font-size": "1vmax",
                                                "text-align": "center",
                                                "width": "98%",
                                                "height": "98%",
                                                "border-color": "#ccc",
                                                "border-style": "solid",
                                                "border-width": "1px",
                                                "border-radius": "4px",
                                            },
                                        )
                                    ],
                                    bp="md",
                                    size=12,
                                )
                            ],
                            style={"margin-bottom": "2vh"},
                        ),
                        Row(
                            [
                                Col(
                                    [
                                        html.Button(
                                            children="Submit",
                                            n_clicks=0,
                                            type="submit",
                                            id="login-button",
                                            className="login-button",
                                            n_clicks_timestamp="0",
                                        )
                                    ],
                                    bp="md",
                                    size=3,
                                )
                            ],
                            style={"margin-bottom": "2vh"},
                        ),
                        Row(
                            id="user_creation",
                            style={
                                "height": "13vh",
                                "color": color_palette[0],
                                "padding-bottom": "1vh",
                                "display": "flex",
                                "flex-direction": "row",
                                "justify-content": "flex-start",
                                "align-items": "center",
                            },
                        ),
                    ],
                    size=3,
                    mobile_size=6,
                    style={
                        "height": "40vh",
                        "background-color": "white",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "align-items": "center",
                        "border-color": "white",
                        "border-style": "solid",
                        "border-width": "1px",
                        "border-radius": "10px",
                    },
                )
            ],
            style={
                "padding-bottom": "1vh",
                "padding-top": "13vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
                "align-items": "center",
            },
        )
    ]
)


@app.callback(
    Output("user_creation", "children"),
    [Input("login-button", "n_clicks"), Input("pwd-box", "n_submit")],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def update_output(n_clicks, n_submits, username, password):
    """
    Checks username and password information after
    return is pressed or create button is clicked

    Args:
        n_clicks(int): indicates if create button is clicked

        n_submits(int): indicates if enter is pressed while in
        password box

        username(str): username

        password(str): password
    
    Returns:
        Link to login or error message. Default return before click/return is
        the password restrictions
    """
    if n_submits == None:
        n_submits = 0
    if (n_clicks == 0) and (n_submits == 0):
        return html.P(
            "Password must be 8 characters long and include one uppercase letter, two numbers, and a special character.",
            style={
                "text-align": "center",
                "font-size": "2vmin",
                "content-align": "center",
            },
        )
    if (n_clicks > 0) or (n_submits > 0):
        return check_user(username, password)
