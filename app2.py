#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Developed on Tuesday 17th Feb to Solve these annoying Wordle things

This is a rebuild for v2 after a bit of an overhaul of the method

@author: David J McNay
"""

# %% IMPORTS

import dash
from dash import html, dcc, Input, State, Output
import dash_bootstrap_components as dbc

# wonky wordle class we build
from wonky import Wonky
wonky = Wonky()             # initialise

# %% Setup Dash App

app = dash.Dash(__name__, 
                external_stylesheets = [dbc.themes.SKETCHY],
                title='WonkingWordle',
                )

# %% LAYOUT

layout = html.Div([
    
    html.H1("Wonking Wordle"),
    
    
    

], className='container')

# %% RUN DASH APP

# app.title='Wonking Wordle'
app.layout=layout

if __name__ == '__main__':
    app.run_server(debug=True)