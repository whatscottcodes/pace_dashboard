import dash_html_components as html
from ..components import Row

def page_not_found(pathname):
    """
    If pathname is not in index, returns the Div below.
    """
    return html.Div(Row([html.H1(f" Oh no, {pathname} not found!")], style={'margin-top': '5vh'}))
