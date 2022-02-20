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

COLOURS = {'green':'teal',
           'amber':'purple',
           'red':'#ed1153',    # some pinky colour I found
           'theme':'#ed1153',
           'tile':'lightgrey',
           }

# %%

def card_refresh(wonky, width_px=70):
    """ MAIN GUESS INPUT CARD & RESULTS """
    
    def _input_letter(idx=1):
        
        # different options depending on if letter has been solved
        # use wonky's solved dict as input
        if idx in wonky.solved.keys():
            disabled=True
            letter_value=str(wonky.solved[idx]).upper()
            bg_colour=COLOURS['green'],
        else:
            disabled=False
            letter_value=""
            bg_colour=COLOURS['tile']
        
        # DBC Input Box
        letter = dbc.Input(
            id="input-{}".format(idx), 
            type='text',
            value=letter_value,
            maxlength=1,
            disabled=disabled,
            style={'text-align':'center',
                   'font-size':35, 'font-weight':'bold',
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
                   'margin-top':'10px',
                   'background-color':COLOURS['tile']}
            )
        
        return dbc.Col(result)
    
    # Create dbc Rows for the Guess Letters & Results
    row_guesses = dbc.Row([_input_letter(i) for i in range(1, 6)])
    row_results = dbc.Row([_input_result(i) for i in range(1, 6)])
    
    return dbc.Col([row_guesses, row_results], id='card-interface')


def card_of_failure(wonky, width_px=50):
    """ """
    
    #text = str(wonky.guess_matrix)
    children = []
    
    # template for a scrabble tile thing for the each letter
    def _tile(letter, colour):
        return dbc.Input(value="{}".format(letter),
                         type='text',
                         disabled=True,
                         style={'width':width_px, 'height':width_px,
                                'text-align':'center',
                                'font-size':18, 
                                'font-weight':'bold',
                                'color':'lightgrey',
                                'background-color':colour,
                                },)
    
    # guess matrix is a dictionary, which starts empty
    # every time there is a guess we add a key, which is also a dict
    # which in turn stores lists of the guess letters & the results
    # only proceed if there is at least one stored guess
    if len(wonky.guess_matrix.keys()) > 0:
        
        # now iterate over historical guess words 
        for k, v in wonky.guess_matrix.items():
             
            # unpack dictionary into lists of guess letters & results
            guess, result = v['guess'], v['result']
            
            # set up a blank list to append tiles too for this row (guess)
            # then iterate over letters in the word appending tiles to the row
            row = []
            for i, letter in enumerate(guess):
                
                # determine tile colour based on the result
                if result[i] == "HIT":
                    colour = COLOURS['green']
                elif result[i] == "MISS":
                    colour = COLOURS['red']
                elif result[i] == "NEAR":
                    colour = COLOURS['amber']
                
                # build tile and append to this row
                row.append(_tile(letter, colour))
            
            # now append whole row (so one 5 letter word guess with 5 tiles)
            # to the childrens list
            children.append(dbc.Row(row))
    
    return dbc.Col(children)

# %% MARKDOWN

md_question = """ This is version 1 of my attempt to optimise Wordle.

### Source Dictionaries
This a proving a pain in the backside. Our primary source is from  
[WordFrequency.info](https://www.wordfrequency.info/) who have a great data set
which takes the billion word, Corpus of Contemporary American English (COCA) 
and looks for word frequency, standardising by source. Unfortunately, they
only let you have the first, 5,000 words for free (~430 5-letter words); if 
anyone wants to [contribute](https://www.buymeacoffee.com/panda) 
towards the $95 for the full data set that would be appreciated.

Google searches for American English dictionaries in CSV format tend to yield 
[bragitoff.com](https://www.bragitoff.com/2016/03/english-dictionary-in-csv-format/) 
which seems impresive, but practically turns out to be about as much use  as a 
chocolate teapot. Instead we're using the 77,000 word American dictionary and the 
194,000 mixed UK and American word lists from [here](http://www.gwicks.net/dictionaries.htm).

Filtering for 5-letter words, that means we have about 11,000 unique words 
although some will be proper English rather than American.

### Method
Our method for v1 is very simple and does leave some holes - notably we aren't 
(yet) excluding the positions of known "nears" so the model may suggest, for 
example, "ABOUT" has an A but not in position 1 but we may still get words that 
start with A; for the moment just pay attention.

I also have a plan to create a scoring system to optimise for the best seed 
words, but that is only if I can still be bothered (and if v1 fails to beat Ann's brain).

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/default-red.png#center)](https://www.buymeacoffee.com/panda)
"""

md_terminate = """ Afraid we've run out of road...

Which means either you've been 💩 entering your guesses/results, or, 
more likely, today's solution isn't yet in our dictionary.

We leverage the *free* data from [WordFrequency.info](https://www.wordfrequency.info/) 
which only gives us the 5,000 most commonly used words in American English 
*(about 430 5-letter words)* and supplement with some 
[open source word lists](http://www.gwicks.net/dictionaries.htm).

More details in the questions section.

If you'd like to contribute to the $95 required to buy the full word list, 
you can [buy me a brew ☕](https://www.buymeacoffee.com/panda)

"""

md_disclaimer = """ Disclaimer: Some people aren't good with words, they choose 
simple, pleasing words, like *"boobs"*. However, sometimes these people  find 
themselves around word enthusiasts, the type who love nonsense like Scrabble. 
This is the app for those who choose action, and optimisation, over words.

On the off chance you've stumbled on this page and don't know what Wordle is, 
avoid clicking [here](https://www.nytimes.com/games/wordle/index.html); 
if you do, I especially suggest avoiding letting your partner or friends know 
about Wordle lest they get excessively competitive. Should you find yourself 
in such a predicament, you could place a friendly wager about your level of 
skill and avoid telling them about this app.

If it isn't obvious, I have nothing to do Wordle or the New York Times. This 
is a toy so if anyone from a big corporation would like to sue me, 
just let me know and I'll delete the app. """

# %%

tooltips = html.Div([
    
    # Refresh Button
    dbc.Tooltip(
        ["Reload & clear current guesses"],
        target="button-reload",
        style={'font-size':'18px',}),
    
])

modals = html.Div([
    
    # Model Details
    dbc.Modal(
        [dbc.ModalHeader(html.H4("BOOBS")),
         dbc.ModalBody([
             dcc.Markdown([md_question], 
                          style={'text-align':'justify',
                                 'font-color':COLOURS['theme']})]
        ),],
        id="modal-question",
        keyboard=True,
        centered=True,
        autofocus =True,
        size="lg",
        is_open=False,
        style={}),
    
    
        # Model Details
    dbc.Modal(
        [dbc.ModalHeader(html.H4("No More Valid Combinations 😔")),
         dbc.ModalBody([
             dcc.Markdown([md_terminate], 
                          style={'text-align':'justify',
                                 'font-color':COLOURS['theme']})]
        ),],
        id="modal-terminate",
        keyboard=True,
        centered=True,
        autofocus =True,
        size="sm",
        is_open=False,
        style={}),
    
])

# %% LAYOUT

layout = html.Div([
    
    # Hidden useful stuff like Modals, Tooltips & Toasts
    tooltips,
    modals,

    dbc.Card([
        
        # Title & Refresh Button
        dbc.Row([
            dbc.Col([html.H2("Wonking Wordle"),], width=8),
            dbc.Col([
                
                # Question, Modal 
                dbc.Button("?", 
                           id='button-question', 
                           style={'font-size':30,
                                  'text-align':'center',
                                  'height':'40px','width':'40px',
                                  'border-radius':'50%',
                                  'background-color':COLOURS['theme']}),
                
                # refresh button
                # the dcc.Location is part of the boilerplate needed to reload
                dcc.Location(id='url', refresh=True),
                dbc.Button("⟳", 
                           id='button-reload', 
                           style={'font-size':38,
                                  'height':'40px','width':'40px',
                                  'display': 'inline-flex',
                                  'align-items': 'center', 
                                  'border-radius':'50%',
                                  'margin':'5px',
                                  'background-color':COLOURS['theme']},
                   ),
            ], width=4, style={'text-align':'right'}),
        ], className="d-flex align-items-center",),
        
        #dbc.Card([card_refresh(wonky)], id='card-interface'),    # use func to build guess & results grid
        card_refresh(wonky),
        
        # Row for Model Best Guess Dropdown & Update Model
        dbc.Row([
            
            dbc.Col([
                dbc.InputGroup([
                    dbc.InputGroupText("Pick-a-Punt:", 
                                       style={'margin-right':'5px',
                                              'font-size':'18px',
                                              'color':COLOURS['theme']}),  
                    dcc.Dropdown(id='dd-top-punts', 
                                 style={'width':'125px',
                                        'background-color':COLOURS['tile']}),
                ], className='m-3'),
            ], width=7),
            
            # Update Model Button
            dbc.Col([
                dbc.Button("Update Wonking Engine", 
                           id='button-update', 
                           n_clicks=0,
                           style={'width':'100%', 
                                  #'margin-top':'8px',
                                  'background-color':COLOURS['theme'],
                                  }),
            ], width={'offset':0, 'size':5}),
        ], className='m-2 d-flex align-items-center'),
        
        dbc.Row([
            dbc.Col([
                html.H5("Top Punts: "),
                dbc.Card(id='div-word-list', 
                         body=True,
                         style={'text-align':'center',
                                'opacity':0.8})
            ], width=3),
            
            dbc.Col([
                html.H5("Failure Reminders: "),
                dbc.Card([card_of_failure(wonky)], 
                         id='card-failure', 
                         style={'display': 'inline-flex',
                                'align-items': 'right', 
                                'border': 'none',
                                }),
            ], width={'offset':2, 'size':7}, ),
            
        ]),
        
        dbc.Row([], id='test', style={'font-color':COLOURS['theme']}),
        
        dbc.CardFooter([
            dcc.Markdown(md_disclaimer, style={'color':COLOURS['theme']}),
        ]),
    
    ], body=True, style={'background-color':'rgba(0,0,0,0.84)',
                         'border':'none'})
    

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

@app.callback(output={"is_open":Output("modal-question", "is_open")},
              inputs={"n":Input("button-question", "n_clicks"),
                      "is_open":State("modal-question", "is_open")})
def modal_details_tempport(n, is_open):
    """ """
    if n:
        return {"is_open":not is_open}
    return {"is_open":is_open}

@app.callback(output={'words':Output('div-word-list', 'children'),
                      'top_punt':Output('dd-top-punts', 'value'),
                      'top_punts':Output('dd-top-punts', 'options'),
                      'card-guess':Output('card-interface', 'children'),
                      'failure':Output('card-failure', 'children'),
                      'test':Output('test', 'children'),
                      "modal_terminate":Output("modal-terminate", "is_open")
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
                      "is_open":State("modal-terminate", "is_open"),
                      })
def callback_guess(n_clicks,
                   guesses, results,
                   is_open,
                   ):
    
    # wonky has a function to update itself when you have a word & results
    if n_clicks >0:
        wonky.guess_update(guesses, results)
    
    # Run Guess Update
    # Produce list of best words
    df = wonky.guess_list()
    words = [html.P("".join(df.loc[i,:])) for i in df.index[0:8]]
    
    # Update Dropdown list of Top Punts
    # wonky.guess_list() creates a list of words in wonky.top_guess
    top_punts = [{'label':i, 'value':i} for i in wonky.top_guess]
    
    # causes errors if we have run out of viable words
    
    if len(wonky.top_guess) > 0:
        top_punt = [wonky.top_guess[0]]
    else:
        top_punt = [char for char in str("*****")]
        if len(wonky.solved.keys()) > 0:
            for k, v in wonky.solved.items():
                top_punt[k-1] = v
        top_punt = "".join(top_punt)
            
        # launch modal
        is_open = not is_open
            
    return {'words':words,
            'top_punts':top_punts,
            'top_punt':top_punt,
            'card-guess':card_refresh(wonky),
            'failure':card_of_failure(wonky),
            'test':len(wonky.top_guess),
            'modal_terminate':is_open,
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
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)