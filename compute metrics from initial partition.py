#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 13:48:25 2022

@author: dpg
"""

#plain version
rsw_tmp = 0
rmm_tmp = 0
reg_tmp = 0
for compelection in composite:
    rsw_tmp += initial_partition[compelection].wins("Democratic")
    rmm_tmp += mean_median(initial_partition[compelection])
    reg_tmp += efficiency_gap(initial_partition[compelection])
    
rsw = rsw_tmp/len(composite) #now get average per election instead of sum over all elections
rmm = rmm_tmp/len(composite)
reg = reg_tmp/len(composite)
rpp = np.mean(pd.Series(polsby_popper(initial_partition)))



#sumf version::
nparts = len(initial_partition)
votes_r = np.zeros((nparts,))
votes_d = votes_r.copy()

rmm_tmp = 0
reg_tmp = 0
rsw_tmp = 0
rs_tmp = 0
rfw_tmp = 0

for compelection in composite:
    #rsw_tmp += initial_partition[compelection].wins("Democratic")   #for calculating fractional seas from INDEX
    votes_d += initial_partition[compelection].votes("Democratic") #create the vote index
    votes_r += initial_partition[compelection].votes("Republican")
    rs_tmp += initial_partition[compelection].wins("Democratic")
    rmm_tmp += mean_median(initial_partition[compelection])
    reg_tmp += efficiency_gap(initial_partition[compelection])
 #   datax += pandas.DataFrame(sorted(initial_partition[compelection].percents("Democratic" )), index=cds)
    

rfw_tmp  = calc_fracwins_comp(initial_partition,composite, electionvol)
rsw_tmp = np.greater(votes_d, votes_r).sum() #now find who won how many seats from the sum of votes
rmm_tmp = rmm_tmp/len(composite)
reg_tmp = reg_tmp/len(composite)
rs_tmp = rs_tmp/len(composite)
rpp = np.mean(pd.Series(polsby_popper(initial_partition)))
