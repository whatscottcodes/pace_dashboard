import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from ..app import app, User
from ..components import Row, Col
from ..helpers_configs import log_path, color_palette
from flask_login import login_user
from werkzeug.security import check_password_hash
import datetime

layout = html.Div(
    [
        dcc.Location(id="url_login", refresh=True),
        Row(
            id="output-state",
            style={
                "color": color_palette[0],
                "height": "2vh",
                "padding-bottom": "5vh",
                "padding-top": "5vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
        Row(
            [
                Col(
                    [
                        Row(
                            [
                                Col(
                                    [
                                        html.H2(
                                            "Please Login",
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
                                            children="Login",
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
                            [
                                Col(
                                    [
                                        html.A(
                                            "Create Password",
                                            href="/create_password",
                                            style={
                                                "display": "flex",
                                                "flex-direction": "row",
                                                "padding": 0,
                                                "justify-content": "flex-start",
                                                "align-items": "flex-start",
                                                "font-size": "2vmin",
                                            },
                                        )
                                    ],
                                    bp="md",
                                    size=12,
                                )
                            ],
                            style={"margin-bottom": "1vh"},
                        ),
                        Row(
                            [
                                Col(
                                    [
                                        html.A(
                                            "Forgot Password",
                                            href="mailto:snelson@pace-ri.org?Subject=Forgot%20Password",
                                            style={
                                                "display": "flex",
                                                "flex-direction": "row",
                                                "padding": 0,
                                                "justify-content": "flex-start",
                                                "align-items": "flex-start",
                                                "font-size": "2vmin",
                                            },
                                        )
                                    ],
                                    bp="md",
                                    size=12,
                                )
                            ],
                            style={"margin-bottom": "1vh"},
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
                "padding-top": "1vh",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "center",
                "align-items": "center",
            },
        ),
    ]
)


@app.callback(
    Output("url_login", "pathname"),
    [Input("login-button", "n_clicks"), Input("pwd-box", "n_submit")],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def success(n_clicks, n_submits, input1, input2):
    user = User.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):

            log_file = open(log_path, "a")
            log_file.write(f"{user.username}, {datetime.datetime.now()}, 1\n")
            log_file.close()

            login_user(user)
            return "/census"
        else:
            pass
    else:
        pass


@app.callback(
    Output("output-state", "children"),
    [Input("login-button", "n_clicks"), Input("pwd-box", "n_submit")],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def update_output(n_clicks, n_submits, input1, input2):
    if n_submits == None:
        n_submits = 0

    if (n_clicks > 0) or (n_submits > 0):
        user = User.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ""
            else:
                return "Incorrect Username or Password"
        else:
            return "Incorrect Username or Password"
    else:
        return ""

