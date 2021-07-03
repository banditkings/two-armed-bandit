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

# row = html.Div([
#         dbc.Row([html.H1(id='output-score')])
#     ], style={'padding': '25px'}
# )

def serve_layout():
    """Function to serve layout such that it refreshes on page load"""
    global g
    g = game()

    layout = html.Div([
                header,
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Pull Arm 1", id='button1', n_clicks=0),
                        dbc.Button("Pull Arm 1 x10", id='button1_10', n_clicks=0)
                        ]),
                    dbc.Col([
                        dbc.Button("Pull Arm 2", id='button2', n_clicks=0),
                        dbc.Button("Pull Arm 2 x10", id='button2_10', n_clicks=0)
                        ])
                ]),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='fig1')),
                    dbc.Col(dcc.Graph(id='fig2'))
                ]),
                html.Div([
                    dbc.Row([html.H1(id='output-score')])
                    ], style={'padding': '25px'}),
            ])
    return layout

@app.callback(
    Output("fig1", "figure"),
    [Input("button1", "n_clicks"),
    Input("button1_10", "n_clicks")]
)
def singlebet_0(n, n10):    
    """make a single bet on arm 0"""
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'button1_10' in changed_id:
        g.make_bet(0, 10)
        return g.show_fig(0)
    elif 'button1' in changed_id:
        g.make_bet(0, 1)
        return g.show_fig(0)
    else:
        return g.show_fig(0)

@app.callback(
    Output("fig2", "figure"),    
    [Input("button2", "n_clicks"),
    Input("button2_10", "n_clicks")]
)
def singlebet_1(n, n10):
    """make a single bet on arm 1"""
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'button2_10' in changed_id:
        g.make_bet(1, 10)
        return g.show_fig(1)
    elif 'button2' in changed_id:
        g.make_bet(1, 1)
        return g.show_fig(1)
    else:
        return g.show_fig(1)

@app.callback(
    Output("output-score", "children"),
    [Input("button1", "n_clicks"),
    Input("button1_10", "n_clicks"),
    Input("button2", "n_clicks"),
    Input("button2_10", "n_clicks")]
)
def return_score(n1, n2, n3, n4):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'button' in changed_id:
        result = g.score()
        return result

app.layout = serve_layout

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8080, debug=True)