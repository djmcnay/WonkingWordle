#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 20:26:34 2022

@author: djmcnay
"""

import pandas as pd
import numpy as np
from wonky import Wonky
from tqdm import tqdm

wonky = Wonky()
wonky._set_corpus_to_df(wonky.freq)

def test(guess, target):
    
    _f = lambda x: [c for c in str(x)]
    
    guess = _f(guess)
    target = _f(target)

    result = []    # dummy result
    for i, v in enumerate(guess):
        if v == target[i]:
            result.append("HIT")
        elif v in target:
            result.append("NEAR")
        else:
            result.append("MISS")
    
    return result

def solve(wonky=wonky, seed="ABOUT", target="ABOUT"):
    
    for n in range(1, 9):
        
        if n == 1:
            guess = seed
        else:
            guess = wonky.top_guess[0]
            
        result = test(guess, target)             # test guess vs. target  
        wonky.guess_update(guess, result)        # update wonky guess updater
        wonky.guess_list()                       # update guess list
    
        if len(wonky.top_guess) == 1:
            break
        elif len(wonky.top_guess) == 0:
            n = 100
            break
        
    wonky.reset()
    return n ** 2

def model(wonky):
    
    wordlist = ["".join(wonky.corpus.loc[i, :]) for i in wonky.corpus.index]
    
    beast = pd.DataFrame(data=0, index=wordlist, columns=wordlist)
    
    pbar1 = tqdm(total=len(wordlist)**2)
    
    for i, target in enumerate(beast.index, 1):
        
        for seed in beast.columns:
            n = solve(wonky, seed, target)
            beast.loc[seed, target] = n
            
            pbar1.update(1)
            
    return beast.sum().sort_values()

#x = pd.Series(model(wonky).index)

def kingkong(wonky, n=100):
    
    #pbar0 = tqdm(total=n)
    
    for i in range(n):
        
        x = model(wonky)
        x = pd.Series(model(wonky).index)
        wonky._set_corpus_to_df(x)
            
        # high frequency words
        x.to_csv("data/model_opt_hf.csv",  
                 header=False, 
                 index=False, 
                 encoding='utf-8')
        
        print(x.head(15))
        print("Starting {}th iteration".format(i))
        
    
    return

x = kingkong(wonky)