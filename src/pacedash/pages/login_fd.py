# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from ..settings import color_palette
from ..app import app
from ..components import Row, Col
from ..login_utils import redirect_to_login
from ..settings import forgot_pw_email

# Create app layout
layout = html.Div(
    [
        dcc.Location(id="url_login_df", refresh=True),
        Row(
            id="spacer",
            style={
                "color": color_palette[0],
                "height": "2vh",
                "padding-bottom": "1vh",
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
                                        html.Button(
                                            children="Login",
                                            n_clicks=0,
                                            id="back-button",
                                            className="login-button",
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
                                            href=f"mailto:{forgot_pw_email}?Subject=Forgot%20Password",
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

# Create callbacks
@app.callback(Output("url_login_df", "pathname"), [Input("back-button", "n_clicks")])
def logout_dashboard(n_clicks):
    """
    When the login button is clicked the login page layout is loaded.
    """
    return redirect_to_login(n_clicks)
