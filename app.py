import dash
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output 
import dash_bootstrap_components as dbc

app = Dash(__name__,use_pages=True, external_stylesheets=[dbc.themes.FLATLY])

server = app.server

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            #className="bg-light",
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Difussion of Machine Learning",
                         style={'fontSize':45, 'textAlign':'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


# Build the layout to define what will be displayed on the page


if __name__ == '__main__':
    app.run_server(debug=True)