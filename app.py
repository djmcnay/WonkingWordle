# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 18:06:33 2022

@author: T333208
"""

# %% IMPORTS

import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

# wonky wordle class we build
from wonky import Wonky
wonky = Wonky()             # initialise


# %%

def card_refresh(wonky):
    
    def _input_letter(id='input-1'):
        return dbc.Input(id=id, 
                         type='text',
                         maxlength=1,
                         style={'text-align':'center',
                                'font-size':30,
                                'font-weight':'bold'})
    
    def _input_result(id='dd-1'):
        
        opts = ['HIT', 'MISS', 'NEAR']    # options list
        
        return dcc.Dropdown(id=id,
                            options=[{'label':i, 'value':i} for i in opts],
                            value='MISS',
                            clearable=False,
                            disabled=False,
                            style={'text-align':'left',
                                   'font-size':12,
                                   'margin-top':'10px'})
    
    card = dbc.Row([
    
        dbc.Col([
            _input_letter(id='input-1'),
            _input_result(id='result-1'),
        ], width=1),
        
        dbc.Col([
            _input_letter(id='input-2'),
            _input_result(id='result-2'),
        ], width=1),
        
        dbc.Col([
            _input_letter(id='input-3'),
            _input_result(id='result-3'),
        ], width=1),
        
        dbc.Col([
            _input_letter(id='input-4'),
            _input_result(id='result-4'),
        ], width=1),
        
        dbc.Col([
            _input_letter(id='input-5'),
            _input_result(id='result-5'),
        ], width=1),
        
    ])
    
    
    return card


# %% LAYOUT

layout = html.Div([
        
    html.H1("Wonking Wordle"),
    
    dbc.Card([
        dbc.Row([
            card_refresh(wonky),
        ]),
    ], body=True)
    
    
        
],)    # End layout

# %% RUN DASH APP

app = dash.Dash(__name__, 
                external_stylesheets = [dbc.themes.BOOTSTRAP],
                title='WonkingWordle',
                )

# app.title='Wonking Wordle'
app.layout=layout


if __name__ == '__main__':
    app.run_server(debug=True)