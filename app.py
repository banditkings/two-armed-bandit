import dash  # (version 1.19.0) pip install dash

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
from dash.dependencies import Input, Output

from src.model import game

fontawesome_stylesheet = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, fontawesome_stylesheet])


header = html.Div([
    dbc.Row(dbc.Col(html.H1("Two Armed Bandits"))),
])

row = html.Div([
        dbc.Row([html.H1("Placeholder"), html.P(id='example-output')])
    ], style={'padding': '25px'}
)

def serve_layout():
    """Function to serve layout such that it refreshes on page load"""
    global g
    g = game()

    layout = html.Div([
                header,
                dbc.Row([
                    dbc.Col(dbc.Button("Pull 1", id='button1', n_clicks=0)),
                    dbc.Col(dbc.Button("Pull 2", id='button2', n_clicks=0))
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='fig1')),
                    dbc.Col(dcc.Graph(figure=g.show_fig(1)))
                ]),
                row
            ])
    return layout

@app.callback(
    Output("fig1", "figure"), [Input("button1", "n_clicks")]
)
def on_button_click(n):
    if n is None:
        return "Not clicked."
    else:
        global g
        g.make_bet(0)
        return g.show_fig(0) 

app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)