import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..app import app
from ..components import Row, Col
from ..helpers_configs import color_palette
from ..login_utils import redirect_to_login


layout = html.Div(
    [
        dcc.Location(id="url_logout_df", refresh=True),
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
                                            "You Have Been Logged Out",
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
@app.callback(Output("url_logout_df", "pathname"), [Input("back-button", "n_clicks")])
def logout_dashboard(n_clicks):
    return redirect_to_login(n_clicks)
