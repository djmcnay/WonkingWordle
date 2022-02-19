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


COLOURS = {'green':'seafoam',
           'orange':'sienna',
           'red':'red',
           }

# %%

def card_refresh(wonky, width_px=75):
    """ MAIN GUESS INPUT CARD & RESULTS """
    
    def _input_letter(idx=1):
        
        # different options depending on if letter has been solved
        # use wonky's solved dict as input
        if idx in wonky.solved.keys():
            disabled=True
            letter_value=str(wonky.solved[idx]).upper()
            bg_colour='green',
        else:
            disabled=False
            letter_value=""
            bg_colour='white'
        
        # DBC Input Box
        letter = dbc.Input(
            id="input-{}".format(idx), 
            type='text',
            value=letter_value,
            maxlength=1,
            disabled=disabled,
            style={'text-align':'center',
                   'font-size':30, 'font-weight':'bold',
                   'width':width_px, 'height':width_px,
                   'background-color':bg_colour,}
            )
        
        return dbc.Col([letter])
    
    def _input_result(idx=1):
        
        if idx in wonky.solved.keys():
            value='HIT'
            disabled=True
        else:
            value='MISS'
            disabled=False
        
        # DCC Dropdown Menu
        opts = ['HIT', 'MISS', 'NEAR']    # options list
        result = dcc.Dropdown(
            id="dd-{}".format(idx),
            options=[{'label':i, 'value':i} for i in opts],
            value=value,
            clearable=False,
            disabled=disabled,
            style={'text-align':'left',
                   'font-size':12,
                   'width':width_px,
                   'margin-top':'10px'}
            )
        
        return dbc.Col(result)
    
    # Create dbc Rows for the Guess Letters & Results
    row_guesses = dbc.Row([_input_letter(i) for i in range(1, 6)])
    row_results = dbc.Row([_input_result(i) for i in range(1, 6)])
    
    return dbc.Col([row_guesses, row_results], id='card-interface')


# %% LAYOUT

layout = html.Div([
    
    dbc.Row([
        dbc.Col([html.H2("Wonking Wordle"),], width=11),
        dbc.Col([
            dcc.Location(id='url', refresh=True),
            dbc.Button("⟳", 
                       id='button-reload', 
                       style={'font-size':32,
                      'height':'35px','width':'35px',
                      'display': 'inline-flex',
                      'align-items': 'center', 
                      'border-radius':'50%',},
               ),
        ], width=1),
    ], className="d-flex align-items-center",),
    
    dbc.Card([
        
        #dbc.Card([card_refresh(wonky)], id='card-interface'),    # use func to build guess & results grid
        card_refresh(wonky),
        
        # Row for Model Best Guess Dropdown & Update Model
        dbc.Row([
            
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Pick-a-Punt:"),  
                    dcc.Dropdown(id='dd-top-punts', style={'width':'125px'}),
                ], className='m-3'),
            ], width=8),
            
            
            # Update Model Button
            dbc.Col([
                dbc.Button("Update Wonking Engine", 
                           id='button-update', 
                           n_clicks=0,
                           style={'width':'100%', 
                                  #'height':'80%',
                                  }),
            ], width={'offset':0, 'size':4}),
        ], className='m-2'),
        
        dbc.Row([
            dbc.Col([
                html.H5("Top Punts: "),
                html.Div(id='div-word-list', style={'margin-left':'25px'})
            ], width=4),
            
            dbc.Col([
                html.H5("Failure Reminders: "),
                #dbc.Row(card_old_guesses(wonky), id='old-guesses'),
            ], width=8),
            
        ]),
    
    ], body=True)
    

], className='container')

# %% CALLBACKS

@app.callback(Output("url", "href"),
              Input("button-reload", "n_clicks"),
              prevent_initial_call=True,)
def reload_data(_):
    """ Refresh Dash App - Almost Boilerplate 
    Source:
        https://stackoverflow.com/questions/61716381/dash-python-app-button-for-action-and-refresh-the-page
    """
    wonky.reset()    # use wonky function to remove class data
    return "/"

@app.callback(output={'words':Output('div-word-list', 'children'),
                      'top_punt':Output('dd-top-punts', 'value'),
                      'top_punts':Output('dd-top-punts', 'options'),
                      'card-guess':Output('card-interface', 'children'),
                      #'excluded':Output('div-excluded', 'children'),
                      #'known':Output('div-known', 'children'),
                      #'old-guesses':Output('old-guesses', 'children'),
                      },
              inputs={'n_clicks':Input('button-update', 'n_clicks'),
                      'guesses':(State('input-1', 'value'),
                                 State('input-2', 'value'),
                                 State('input-3', 'value'),
                                 State('input-4', 'value'),
                                 State('input-5', 'value'),),
                      'results':(State('dd-1', 'value'),
                                 State('dd-2', 'value'),
                                 State('dd-3', 'value'),
                                 State('dd-4', 'value'),
                                 State('dd-5', 'value'),),
                      })
def callback_guess(n_clicks,
                   guesses, results,):
    
    # wonky has a function to update itself when you have a word & results
    wonky.guess_update(guesses, results)
    
    # Run Guess Update
    # Produce list of best words
    df = wonky.guess_list()
    words = [html.P("".join(df.loc[i,:])) for i in df.index[0:10]]
    
    # Update Dropdown list of Top Punts
    # wonky.guess_list() creates a list of words in wonky.top_guess
    top_punts = [{'label':i, 'value':i} for i in wonky.top_guess]
    top_punt = [wonky.top_guess[0]]
    
    return {'words':words,
            'top_punts':top_punts,
            'top_punt':top_punt,
            'card-guess':card_refresh(wonky),
            }


@app.callback(output={'guess':(Output('input-1', 'value'),
                               Output('input-2', 'value'),
                               Output('input-3', 'value'),
                               Output('input-4', 'value'),
                               Output('input-5', 'value'))},
              inputs={'dd':Input('dd-top-punts', 'value'),})
def use_dd_to_update_guess(dd):
    """ Uses Top Punts Dropdown to Update Guess Options """
    
    if isinstance(dd, str):
        return {'guess':[c for c in dd]}
    elif isinstance(dd, list):
        return {'guess':[c for c in dd[0]]}


# %% RUN DASH APP

# app.title='Wonking Wordle'
app.layout=layout

if __name__ == '__main__':
    app.run_server(debug=True)