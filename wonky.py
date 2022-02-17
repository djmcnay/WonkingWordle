# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 17:35:18 2022

@author: T333208
"""

import pandas as pd
import numpy as np


def read_corpus(fn="data/model_high_frequency.csv"):
    """ Helper to Read a CSV List of Words to pd.Series"""
    return (pd.read_csv(fn, header=None)
              .squeeze()
              .rename('corpus'))

class Wonky(object):
    
    def __init__(self):
        
        # read in our two word lists to self
        self.freq = read_corpus("data/model_high_frequency.csv")
        self.full = read_corpus("data/model_master.csv")      
                
        # store length of high freq list to self as it's useful
        # basically want to know when we have info or are guessing from beast
        self.n_freq = len(self.freq)
        self.n = 5    # assumed size of Wordle puzzle
        
        # convert full model to df with 1 col per letter
        self.corpus = self._set_corpus_to_df(self.full)

        # Guess Storage
        self.exclude = []    # list of letters
        self.solved = {}     # dict of form {1:'A', 5:'X'} where No are posns 
        self.known = []      # list of letters
        
        return
    
    def _set_corpus_to_df(self, word_series):
        """ Convert pd.Series of Words to df with 1 letter per Col """
        
        df = []
        for word in word_series:
            df.append([i for i in word])
        df = pd.DataFrame(df, columns=range(1, 6))
        
        return df
    
    def update_exclude(self):
        """ """
        return
    
    def update_solved(self):
        """ """
        return
    
    def update_known(self):
        """ """
        return

    def guess_list(self):
        """ Filters Corpus Based on Rules """
        
        # convert corpus to df where each letter is a col
        # by iterating over each entry and split to chars
        # df now becomes our primary dataframe
        df = []
        for word in self.corpus:
            df.append([i for i in word])
        df = pd.DataFrame(df, columns=range(1, 6))
        
        # filter out words whre we know letters to exclude
        if len(self.exclude) > 0:
            exclude = [i.upper() for i in self.exclude]
            df = df[~df.isin(exclude).any(axis=1)]
        
        # filter for known letters with positions
        if not len(self.solved.keys()) == 0:
            for k, v in self.solved.items():
                df = df[df.loc[:, k] == v.upper()]
                
        # filter where letter is know but position not so
        ignore = list(self.solved.keys())
        x = df.loc[:, ~df.columns.isin(ignore)].copy()
        for l in self.known:
            x = x[x.isin([l.upper()]).any(axis=1)]
        df = df.loc[x.index, :]
        
        return df
    
    
    
w = wonky()