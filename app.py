# -*- coding: utf-8 -*-
"""
App Developed on Tuesday 17th Feb to Solve these annoying Wordle things

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


def card_old_guesses(wonky, width_px=50):
    """ Set Up Matrix Ready to Store Old Guesses """
    
    def _tile(letter):
        return dbc.Input(value="{}".format(letter),
                         disabled=True,
                         style={'width':width_px, 'height':width_px,
                                'text-align':'center',
                                'font-size':20, 'font-weight':'bold',
                                'bg-color':'lightgrey'})
    
    matrix = []
    n_guess = len(wonky.guess_matrix)
    
    if n_guess > 0:
        
        for r in range(n_guess):
            
            zippy = wonky.guess_matrix[r]
            
            row = []    # setup new row list
            
            for i, c in enumerate(zippy):
                letter = zippy[0]
                row.append(_tile(letter))
              
            # append row of tiles to matrix
            matrix.append(dbc.Row(row))
            
    else:
        
        # for r in range(1, 2):
        #     row = []    # setup new row list
        #     # iterate over row adding columns of tiles
        #     for c in range(1, 6):
        #         row.append(_tile(r, c))
        #     # append row of tiles to matrix
        #     matrix.append(dbc.Row(row))
                
        return matrix






# %% LAYOUT

layout = html.Div([
        
    html.H1("Wonking Wordle"),
    
    dbc.Card([
        
        dbc.Card([card_refresh(wonky)], id='card-interface'),
        
        dbc.Row([
            dbc.Col([
                dbc.Button("Update Guess", id='button-update', n_clicks=0),
                dbc.Button("Reset", id='button-reset'),
            ], width={'offset':10, 'size':2})
        ]),
        
        
        dbc.Row([
            dbc.Col([
                html.H5("Best Guesses: "),
                html.Div(id='div-word-list', style={'margin-left':'25px'})
            ], width=2),
            
            dbc.Col([
                dbc.Row(card_old_guesses(wonky), id='old-guesses'),
            ], width=3),
            
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

    ], body=True)
    
], className='container')    # End layout

# %% CALLBACKS

# def child_guess_matrix(children, n, guess, results):
#     """ 
    
#     THIS IS REALLT FIDDLEY
    
#     The Guess Matrix is 
    
    
#     """
    
#     if n == 0:
#         #children[n-1]['props']['children'][1]['props']['value'] = "A"
        
#         #return str(children[n]['props']['children'][0]['props'])
#         return children
#     else:
        

#         zippy = list(zip(guess, results))    
        
#         # itserate over each column of guesses and update stuff
#         # n should start at 1 and it the row we are smashing
#         for i, v in enumerate(guess):
            
#             children[n-1]['props']['children'][i]['props']['value'] = v
            
#             # if results[i] == "HIT":
#             #     colour = 'seagreen'
#             # elif results[i] == "NEAR":
#             #     colour = 'orange'
#             # else:
#             #     colour = 'red'
            
            
#             #children[n-1]['props']['children'][i]['props']['style']['bg-color'] = 'blue'  
        
#         return children
    

@app.callback(output={'words':Output('div-word-list', 'children'),
                      'excluded':Output('div-excluded', 'children'),
                      'known':Output('div-known', 'children'),
                      'card-guess':Output('card-interface', 'children'),
                      'old-guesses':Output('old-guesses', 'children'),
                      },
              inputs={'n_clicks':Input('button-update', 'n_clicks'),
                      'reset':Input('button-reset', 'n_clicks'),
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

def callback_guess(n_clicks, reset,
                   guesses, results,):
    
    # iterate through each result & update wonky accordingly
    # either a HIT, MISS or NEAR
    for i, v in enumerate(results):
        
        g = str(guesses[i]).upper()
        
        if v == 'HIT':
            # solved is a dict with keys == solved number
            # so bring in the index (+1) and the letter
            wonky.solved[i+1] = g
        
        elif v == 'MISS':
            # now know to exlude this letter
            wonky.exclude.append(g)
        
        else:
            # now know letter is in the word, just wrong location
            wonky.known.append(g)
            
    if n_clicks > 0:
        
        # zip the guesses & results to a list and append to wonky class
        zippy = list(zip(guesses, results))
        wonky.guess_matrix.append(zippy)
            
        # Need to do some tidying up
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
            'old-guesses': card_old_guesses(wonky),
            }

# %% RUN DASH APP

# app.title='Wonking Wordle'
app.layout=layout

if __name__ == '__main__':
    app.run_server(debug=True)