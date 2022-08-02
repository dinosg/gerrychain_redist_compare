#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 15:44:56 2021


@author: dpg
"""
import numpy as np
from seat_winprob import seat_winprob
def calc_fracwins_comp(thepartition, composite, win_volatility):
    
    aawinstot=0
    for the_election in composite:
        aa = thepartition[the_election]
        aapc = aa.percents("Democratic")
        aawinsfrac = seat_winprob(np.array(aapc), win_volatility)
        aawinstot += sum(aawinsfrac)
    
    aawinstot = aawinstot/len(composite)
    return aawinstot