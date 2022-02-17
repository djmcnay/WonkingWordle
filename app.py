# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 18:06:33 2022

@author: T333208
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
                external_stylesheets = [dbc.themes.BOOTSTRAP],
                title='WonkingWordle',
                )

# %%

def card_refresh(wonky, width_px=70):
    """ """
    
    def _input_col(idx=1):
        
        if idx in wonky.solved.keys():
            disabled=True
            res_value='HIT'
            letter_value=str(wonky.solved[idx]).upper()
            bg_colour='seagreen'
        else:
            disabled=False
            res_value='MISS'
            letter_value=""
            bg_colour='white'
        
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
        
        opts = ['HIT', 'MISS', 'NEAR']    # options list
        result = dcc.Dropdown(
            id="dd-{}".format(idx),
            options=[{'label':i, 'value':i} for i in opts],
            value=res_value,
            clearable=False,
            disabled=disabled,
            style={'text-align':'left',
                   'font-size':12,
                   'width':width_px,
                   'margin-top':'10px'}
            )
        
        return dbc.Col([letter, result], width=1)
    
    card = dbc.Row([   
        _input_col(idx=1),
        _input_col(idx=2),
        _input_col(idx=3),
        _input_col(idx=4),
        _input_col(idx=5),
     
    ])
    
    return card


# %% LAYOUT

layout = html.Div([
        
    html.H1("Wonking Wordle"),
    
    dbc.Card([
        
        dbc.Card([card_refresh(wonky)], id='card-interface'),
        
        dbc.Row([
            dbc.Col([
                dbc.Button("Update Guess", id='button-update'),
                dbc.Button("Reset", id='button-reset'),
            ], width={'offset':10, 'size':2})
        ]),
        
        # Row showing the known letters & the excluded letters
        dbc.Row([
            dbc.Col([
                html.H5("Excluded Letters:"),
                html.Div(id='div-excluded', style={'font-size':20}),
            ], width=6),
            
            dbc.Col([
                html.H5("Known Letters:"),
                html.Div(id='div-known', style={'font-size':20}),    
            ], width=6)
        ]),
        
        # Best Guesses from Corpus
        dbc.Row([
            html.H5("Best Guesses: "),
            html.Div(id='div-word-list', style={'margin-left':'25px'})
        ]),
        
        dbc.Card(id='old-guesses'),

    ], body=True)
    
], className='container')    # End layout

# %% CALLBACKS

def card_guess_matrix(wonky, width_px=75):
    """ """
    
    def _tile(letter, colour):
        return dbc.Input(value=letter,        
                         type='text',        
                         disabled=True,
                         style={'text-align':'center',
                                'font-size':30, 'font-weight':'bold',
                                'width':width_px, 'height':width_px,
                                'background-color':colour,})
    
    rows = []
    
    if len(wonky.guess_matrix) == 0:
        return dbc.Row(rows)
    else:
        # each g is a guess (with 5 sub-bits)
        for g in wonky.guess_matrix:
            row = []
            for tile in g:
                row.append(_tile(g[1], g[2]))
            rows.append(dbc.Row(row))
                    
    return dbc.Col(rows)


@app.callback(output={'words':Output('div-word-list', 'children'),
                      'excluded':Output('div-excluded', 'children'),
                      'known':Output('div-known', 'children'),
                      'card-guess':Output('card-interface', 'children'),
                      'old-guesses':Output('old-guesses', 'children')},
              inputs={'n_clicks':Input('button-update', 'n_clicks'),
                      'reset':Input('button-reset', 'n_clicks'),
                      'guess1':State('input-1', 'value'),
                      'guess2':State('input-2', 'value'),
                      'guess3':State('input-3', 'value'),
                      'guess4':State('input-4', 'value'),
                      'guess5':State('input-5', 'value'),
                      'result_1':State('dd-1', 'value'),
                      'result_2':State('dd-2', 'value'),
                      'result_3':State('dd-3', 'value'),
                      'result_4':State('dd-4', 'value'),
                      'result_5':State('dd-5', 'value'),
                      })
def callback_guess(n_clicks, reset,
                   guess1, guess2, guess3, guess4, guess5,
                   result_1, result_2, result_3, result_4, result_5):
    
    # each guess & result is an input box or dropdown
    # compile them to lists to make life easier when iterating
    guesses = [guess1, guess2, guess3, guess4, guess5]
    results = [result_1, result_2, result_3, result_4, result_5]
 
    # iterate through each result & update wonky accordingly
    # either a HIT, MISS or NEAR
    guess_store = []
    for i, v in enumerate(results):
        
        g = str(guesses[i]).upper()
        
        if v == 'HIT':
            # solved is a dict with keys == solved number
            # so bring in the index (+1) and the letter
            wonky.solved[i+1] = g
            guess_store.append((i+1, g, 'seagreen'))
        
        elif v == 'MISS':
            # now know to exlude this letter
            wonky.exclude.append(g)
            guess_store.append((i+1, g, 'sienna'))
        
        else:
            # now know letter is in the word, just wrong location
            wonky.known.append(g)
            guess_store.append((i+1, g, 'seashell'))
    
    # append this result to guess matrix in wonky
    # means we can build the guess card
    wonky.guess_matrix.append(guess_store)
        
    # Need to do some tidying up
    # Guess engine will get upset if a solved letter is still in known
    # we also want to remove duplicates
    wonky.update_known()
    wonky.exclude = list(set(wonky.exclude))
    
    # Run Guess Update
    # Produce list of best words
    df = wonky.guess_list()
    words = [html.H6("".join(df.loc[i,:])) for i in df.index[0:15]]
    
    return {'card-guess':card_refresh(wonky),
            'words':words, 
            'excluded':wonky.exclude,
            'known':wonky.known,
            'old-guesses':card_guess_matrix(wonky),
            }

# %% RUN DASH APP

# app.title='Wonking Wordle'
app.layout=layout


if __name__ == '__main__':
    app.run_server(debug=True)