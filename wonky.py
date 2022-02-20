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
        self.reset()
        
        # Guess Matrix, for storing old guesses
        self.guess_matrix = {}
        
        return
    
    def _set_corpus_to_df(self, word_series):
        """ Convert pd.Series of Words to df with 1 letter per Col """
        
        df = []
        for word in word_series:
            df.append([i for i in word])
        df = pd.DataFrame(df, columns=range(1, 6))
        
        return df
        
    def reset(self):
        """ Resets Game to Start Again """
        
        # Guess Storage
        self.exclude = []    # list of letters
        self.solved = {}     # dict of form {1:'A', 5:'X'} where No are posns 
        self.known = []      # list of letters
        
        # Guess Matrix, for storing old guesses
        self.guess_matrix = {}
        
        # dict of lists for for position or NEAR letters
        self.partial ={1:[],2:[],3:[],4:[],5:[]}
        
        return
    
    def guess_update(self, guess, result):
        """ Update Class Things Based on a Word & Result List 
        
        INPUTS:
            guess - either a string of 5-letters or list of 5-letters
            results - list with either "HIT", "MISS" or "NEAR"
        
        """
        
        # minor error handling on guess
        # we want a list of 5-letters ['F','A','R', 'T', 'S']
        # also want to limit to 5 letters & have as uppercase
        try:
            guess = [guess] if isinstance(guess, str) else guess
            guess = [char for char in guess[0]] if len(guess) == 1 else guess
            guess = [guess[i].upper() for i in range(self.n)]
        except:
            raise "Error: Guess input doesn't appear to be a 5 letter word"
            
        # error handling for teh results matrix
        # need to make sure results have exactly 5 values
        # they must each be either HIT, MISS or NEAR
        if len(result) != self.n:
            raise "Error: Results list doen't contain 5-values"
        for r in result:
            if r not in ["HIT", "MISS", "NEAR"]:
                raise "Error: Result contains value != HIT/MISS/NEAR"
        
        # iterate over each letter of a ziped list
        # means v will be of the form [("A", "MISS")]
        for i, v in enumerate(list(zip(guess, result)), 1):
            
            letter, letter_result = v    # unpack for readability
            
            # Results can either be "HIT", "MISS" or "NEAR"
            if letter_result == "HIT":
                
                self.solved[i] = letter
                
                # Need to be very careful here!
                # If a letter is solved we need to check if it was known
                # In which case we should remove it, BUT it could be a double
                # So we must only remove ONE instance from the known list
                # Note as we iterate in this loop we APPEND
                if letter in self.known:
                    self.known.remove(letter)
                
            elif letter_result == "NEAR":
                
                # important we append, even if it is already in the list
                # metters for the case where there is a double letter i.e BOOTS
                # we previously knew of O now we tried BOTLO (not a real word)
                # need to be able to solve one & maintain known for 2nd
                # we can remove excess letters later
                self.known.append(letter)
                
                # also update list of positions where we found known letters
                # these can be excluded from this position later
                self.partial[i].append(letter)
            
            elif letter_result == "MISS":
                self.exclude.append(letter)
            else:
                continue
                
        # store previous guesses to the guess matrix
        # use the current guess number as the key
        n = len(self.guess_matrix) + 1
        self.guess_matrix[n] = dict(guess=guess, result=result)
        
        # Tidy up prior info
        self.exclude = list(set(sorted(self.exclude)))
        self.known = list(set(sorted(self.known)))
        
        return guess

    def guess_list(self):
        """ Filters Corpus Based on Rules 
        
        
        """
        
        df = self.corpus.copy()    # pull in corpus from self
        
        # filter out words whre we know letters to exclude
        if len(self.exclude) > 0:
            exclude = [i.upper() for i in self.exclude]
            df = df[~df.isin(exclude).any(axis=1)]
        
        # filter for known solved letters (positions & locations)
        if not len(self.solved.keys()) == 0:
            for k, v in self.solved.items():
                df = df[df.loc[:, int(k)] == v.upper()]
                
        # filter for previous guesses where we know the position of NEAR
        # these letters could still be in the word but can't be in that position
        # partial dict is instansiated with keys 1-5 and lists as values
        # this is because unlike solved there could be multiple misses
        for k, v in self.partial.items():
            if len(v) > 0:
                for letter in v:
                    df = df[df.loc[:, int(k)] != letter.upper()]
                
        # filter where letter is know but position not so
        # we copy df but remove solved columns, then filter for known letters
        # use the index of our filtered copied cersion on original df
        # otherwise the final df will forget the solved letters
        idx = ~df.columns.isin(list(self.solved.keys()))    # index solved cols
        x = df.loc[:, idx].copy()    
        
        # filter through each known letter
        for l in self.known:
            x = x[x.isin([l.upper()]).any(axis=1)]
        
        df = df.loc[x.index, :]   # use index of filtered on original df
        
        # store the top n_store guesses to self for later use
        self.top_guess = ["".join(df.loc[i,:]) for i in df.index]
        
        return df
    
    
# %%

# wonky = Wonky()

# g = ("ABOUT", ["MISS", "NEAR", "HIT", "MISS", "NEAR"])
# wonky.guess_update(*g)
# x = wonky.guess_list()
# print(x.head())

# #wonky.guess_update("every", ["MISS", "MISS", "MISS", "MISS", "MISS"])
# #x = wonky.guess_list()
# #print(x.head())

# #wonky.guess_update("spill", ["HIT", "MISS", "HIT", "HIT", "HIT"])
# #x = wonky.guess_list()
# #print(x.head())


# # %% Build a complicated WORDLE

# # TARGET WORD: BOOTS

# # GUESSES
# #   ("ABOUT", ["MISS", "NEAR", "HIT", "MISS", "NEAR"])
# #   (")

# x = ['a', 'b', 'c', 'a']
# x.remove(0)

x = ["x", "x"]
y = "".join(x)














