# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 18:06:33 2022

@author: T333208
"""

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

from wonky import Wonky

wonky = Wonky()


layout = html.Div(
    children=[
        
        html.H1("TEST"),
        
    ],    # End container-children
)         # End page_container




# %%

app = dash.Dash(__name__, 
                external_stylesheets = [dbc.themes.BOOTSTRAP],
                )

app.title='Wonking Wordle'
app.layout=layout


if __name__ == '__main__':
    app.run_server(debug=True)