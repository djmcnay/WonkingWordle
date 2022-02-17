# -*- coding: utf-8 -*-
""" Funcs related to Building and Tidying up a Corpus for Wordle Solver

@author: David J McNay
"""

import pandas as pd
import numpy as np

def dict_manipulation(x, n=5):
    """ Function for Cleaning Dictionary Series 
    
    Assumes pd.Series input which is just a list of words, then:
        1. Check for non-strings 
        2. Convert to UPPER CASE ad remove duplicates
        3. then non-alphaphabetical and hyphonated words
        4. Filter by word length
        5. Reset index numbers and rename Series to 'corpus'
        
    """
    
    # check vector for non-strings then lower case words and drop duplicates
    x = x[x.apply(type) == str]
    x = x.apply(lambda i: i.upper()).drop_duplicates(keep='first')
    
    # alphabetical only - no numbers or hyphens
    x = x.apply(lambda x: x if x.isalpha() else np.nan).dropna()
    
    # filter for 5-letter words
    x = x[x.apply(len) == n]
    
    # when we return, reset the index and rename the series
    return x.reset_index().iloc[:, -1].rename('corpus')


def from_coca(fn="data/lemmas_60k.xlsx", n=5):
    """ Ranked Words from Word Frequency Corpus
    
    Source data comes from: https://www.wordfrequency.info/samples.asp
    
    This dataset uses the Corpus of Contemporary American English (COCA)
    and ranks words category to find a standardised work ranking. 
    
    Only top 5,000 words are free and I'm not paying $95 """
    
    # import 5,000 word dataseet - use rank column as index
    # we aren't filtering by category so we just keep the lemma col
    x = pd.read_excel(fn).set_index('rank').loc[:, 'lemma']
    
    return dict_manipulation(x, n=n)


def from_text(fn="data/usa2.txt", n=5):
    """ List of Words in .txt format
    
    Assumes a .txt file with a \n new line used between words, as per:
        http://www.gwicks.net/dictionaries.htm
        
    """
    
    # read in a .txt file & split by new line thing
    x = open(fn, "r").read().split('\n')
    x = pd.Series(x)
    
    return dict_manipulation(x, n=n)


def master_corpus(n=5, store=True):
    """ Build our Master Corpus from Multiple Dictionaries
    
    First off we use the COCA which is the 5,000 most frequently used words
    Then we add two lists of words:
        1. 77,000 US English Words
        2. 194,000 "English" words in both English and American spelling
        
    We were originally using a CSV Dictionary from here:
        https://www.bragitoff.com/2016/03/english-dictionary-in-csv-format/
        
    It was BOLLOCKS, 1st word we tried to solve was "Shape" which was missing.
    Instead we found this site which seems better:
        http://www.gwicks.net/dictionaries.htm
    
    """
    
    # Pull dictionaries from our sources
    freq = from_coca(fn="data/lemmas_60k.xlsx", n=n)
    usa = from_text(fn="data/usa2.txt", n=n)
    eng = from_text(fn="data/english3.txt", n=n)
    
    # concat all dicts in order (high freq, us english, english)
    # drop duplicates - there should be rather a lot
    full = pd.concat([freq, usa, eng])   
    full = full.drop_duplicates(keep='first')
    full = full.reset_index().iloc[:,-1]
        
    if store:
        # high frequency words
        freq.to_csv("data/model_high_frequency.csv",  
                    header=False, 
                    index=False, 
                    encoding='utf-8')
        
        # complete list of words
        full.to_csv("data/model_master.csv",  
                    header=False, 
                    index=False, 
                    encoding='utf-8')
    
    return {'freq':freq, 'breakpoint':len(freq), 'full':full}

master_corpus()