#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:47:51 2020
Parallel version of chain run set up for Pennsylvania.
Some nice stuff added to DataFrame structure to add congressional district labels in order of actual increasing congressional district No.
@author: dinos
this version sums over the election "index"
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:55:12 2020
uses recom proposal
@author: dpg
"""
#from multiprocessing import Pool
from multiprocessing import set_start_method, freeze_support
#from multiprocessing import Pool
from multiprocessing import get_context

import matplotlib.pyplot as plt
import time
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain_xtended_muni,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from gerrychain.constraints import single_flip_contiguous, contiguous
from functools import partial
import geopandas
import pandas
import pandas as pd
import numpy as np
from gerrychain.metrics import mean_median, efficiency_gap, polsby_popper
from get_districtlabels import get_labels, get_labels_comp
from get_electioninfo import get_elections
import random
import os 
from total_splits import total_splits, total_muni_splits
import district_list as dl
import conditional_dump as cd
from seat_winprob import seat_winprob
from calc_fracwins_comp import calc_fracwins_comp

def multichain_run(i1, graph, chainlength, my_apportionment, poptol, my_electionproxy, composite, rs, rsw, rfw, rmm, reg, rpp, 
                   datastruct, state, splitno, munisplitno, maxsplits, maxmunisplits, win_volatility):
    hi_eg = 0.04  #spit out maps for anything with efficiency gap over this
    random.seed(os.urandom(10)*i1) 
  #  poptol = 0.03  #min population deviation
    elections, composite = get_elections(state)
    
    if "TOTPOP" in graph._node[0]:
        popkey = "TOTPOP"
    elif "PERSONS" in graph._node[0]:
        popkey = "PERSONS"
    else:
        popkey = []
        print("woops no popkey in file, look @ graph_PA._node[0] to figure out what the keyword for population is\n")
#CONFIGURE UPDATERS
#We want to set up updaters for everything we want to compute for each plan in the ensemble.


# Population updater, for computing how close to equality the district
# populations are. "TOTPOP" is the population column from our shapefile.
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}


# Election updaters, for computing election results using the vote totals
# from our shapefile.
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)


#INITIAL PARTITION
    initial_partition = GeographicPartition(graph, assignment=my_apportionment, updaters=my_updaters)
    
    #this block obtains the Congressional District Labels and converts to string labels, cds
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    cds = get_labels_comp(initial_partition, composite) #get congressional district labels

    nparts = len(initial_partition)
    #ranpart = recursive_tree_part(graph, range(nparts), ideal_population, popkey,poptol - .01,node_repeats=1)
    #randpartition = GeographicPartition(graph,assignment = ranpart, updaters = my_updaters)
    
    contiguous_parts = lambda p: contiguous(p)
    pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, poptol)
    proposal = partial(recom,
                   pop_col=popkey,
                   pop_target=ideal_population,
                   epsilon=poptol,
                   node_repeats=20
                  )

    compactness_bound = constraints.UpperBound(
    lambda p: len(p["cut_edges"]),
    2*len(initial_partition["cut_edges"])
    )
    chain = MarkovChain_xtended_muni(
    proposal=proposal,
    constraints=[contiguous_parts,
        pop_constraint,
        compactness_bound],
    accept=accept.always_accept,
    initial_state= initial_partition,  #randpartition,
    total_steps=chainlength,
    maxsplits = maxsplits, 
    maxmunisplits = maxmunisplits
    )
    for part in chain:
        if part.good == 1:
            datax = np.zeros((nparts,1))  #nparts = ndistricts
            votes_r = np.zeros((nparts,))
            votes_d = votes_r.copy()
            rmm_tmp = 0
            rs_tmp = 0
            rfw_tmp = 0
            reg_tmp = 0
            if (i1 ==0) & (part.counter % 10 == 0):
                print(part.counter)
            
            for compelection in composite:
                #rsw_tmp += part.state[compelection].wins("Democratic")   #for calculating fractional seas from INDEX
                votes_d += part.state[compelection].votes("Democratic") #create the vote index
                votes_r += part.state[compelection].votes("Republican")
                rs_tmp += part.state[compelection].wins("Democratic")
                rmm_tmp += mean_median(part.state[compelection])
                reg_tmp += efficiency_gap(part.state[compelection])
                datax += pandas.DataFrame(sorted(part.state[compelection].percents("Democratic" )), index=cds)
                
    
            rfw_tmp  = calc_fracwins_comp(part.state,composite, electionvol)
            rsw_tmp = np.greater(votes_d, votes_r).sum() #now find who won how many seats from the sum of votes
            rmm_tmp = rmm_tmp/len(composite)
            reg_tmp = reg_tmp/len(composite)
            rs_tmp = rs_tmp/len(composite)
            votes_dpc = votes_d/(votes_d + votes_r)
            #winsfrac = seat_winprob(np.array(votes_dpc), win_volatility) #for calculating frac seats from INDEX
            #fwinstot_tmp = winsfrac.sum()
            datax = datax.transpose() / len(composite)
            
            rsw.append(rsw_tmp)
            rs.append(rs_tmp)
            rmm.append(rmm_tmp)
            reg.append(reg_tmp)
            #rfw.append(fwinstot_tmp)
            rfw.append(rfw_tmp)
            rpp.append(np.mean(pd.Series(polsby_popper(part.state))))  #depends on geometry of the partition only not on vote outcomes
            datastruct = pandas.concat([datastruct, datax])
            splitno.append(total_splits(part.state))
            munisplitno.append(total_muni_splits(part.state))#splits don't depend on individual election results, only on partition so not in loop
           
            #cd.eg_gt(part.state,hi_eg, state, my_apportionment,my_electionproxy, i1, 'county')
            #cd.eg_zero(part,zero_eg, state, my_apportionment, my_electionproxy, i1)
    return i1, rs, rsw,rfw, rmm, reg, rpp, datastruct, splitno , munisplitno          

#MAIN PROGRAM HERE:
    #few key lines for making parallel pool not mess up (freeze_support() and __spec__ definition)
if __name__ == '__main__':
    freeze_support()
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    
      
        #    set_start_method("spawn")
        #    set_start_method("spawn")
   
   
    proposaltype = "recom"
    popkey=''
    #exec(open("input_templates/PA_HDIST_SEN12.py").read()) 
    #exec(open("input_templates/PA_CD_2011_SEN12.py").read()) 
    #exec(open("input_templates/MI_SENDIST_PRES16.py").read()) 
    #exec(open("input_templates/PA_CD_2011_SEN12.py").read()) 
 #   exec(open("input_templates/PA_HDIST_lrc_muni.py").read()) 
   # exec(open("input_templates/PA_HDIST_lrc_muni3_prisoners.py").read()) 
#    exec(open("input_templates/PA_CD17_sumf.py").read()) 
#    exec(open("input_templates/PA_HDIST_lrc_munisumf.py").read())
    exec(open("input_templates/PA_HDIST_lrc.py").read()) 
    
    dontfeedin = 0  #if set=0, feeds in data, otherwise skip
 #   poolsize=40
    
    corrlength=50

    countysp = ' splits ' +str(maxsplits)  #labels for graphs and output filenames
    normalize=''
    elections, composite = get_elections(state)
    #read in data file here:
    
    if 'dontfeedin' in globals():
        if dontfeedin == 0 or not( 'graph_PA' in globals()):
            if ".json" in my_electiondatafile:
                graph_PA = Graph.from_json(my_electiondatafile)
            else:
                df = geopandas.read_file( my_electiondatafile)
                if 'MUNIUNIQUE' not in df.columns:
                    df["MUNIUNIQUE"] = df.COUNTYFP20 + df.MCD_NAME + df.MCD_TYP_NM
                exec(open("./splice_assignment_fn.py").read())
                
    else:
        if ".json" in my_electiondatafile:
            graph_PA = Graph.from_json(my_electiondatafile)
        else:
            df = geopandas.read_file( my_electiondatafile)
            if 'MUNIUNIQUE' not in df.columns:
                df["MUNIUNIQUE"] = df.COUNTYFP20 + df.MCD_NAME + df.MCD_TYP_NM
            exec(open("./splice_assignment_fn.py").read())
            
    
    
    #SETUP initial_partition & get initial DataFrame here - redundant but needed to setup datastruct
    #in parallel - 0th point resu, then append to it
    # 
    if ('popkey' not in globals() ) :
            
        if "TOTPOP" in graph_PA._node[0]:
            popkey = "TOTPOP"
        elif "PERSONS" in graph_PA._node[0]:
            popkey = "PERSONS"
        else:
            popkey = ''
    if popkey == '':
        print("woops no popkey in file, look @ graph_PA._node[0] to figure out what the keyword for population is\n")
    #CONFIGURE UPDATERS
    #We want to set up updaters for everything we want to compute for each plan in the ensemble.
    
    
    # Population updater, for computing how close to equality the district
    # populations are. "TOTPOP" is the population column from our shapefile.
    elections, composite = get_elections(state)
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}
    
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)
    
    initial_partition = GeographicPartition(graph_PA, assignment=my_apportionment, updaters=my_updaters)
    num_districts = len(initial_partition)
    cds = get_labels_comp(initial_partition, composite) #get congressional district labels
    #RUNNING THE CHAIN
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    t0=time.time()
    
    # This will take about 10 minutes.
    #setup variables
    rs = [[0 for x in range(1)] for x in range(poolsize)] 
    rsw = [[0 for x in range(1)] for x in range(poolsize)] #  np.zeros([poolsize, chainlength])
    rfw = [[0 for x in range(1)] for x in range(poolsize)] #  np.zeros([poolsize, chainlength])
    
    rmm = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    reg = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    rpp = [[0 for x in range(1)] for x in range(poolsize)] # np.zeros([poolsize, chainlength])
    splitno = [[0 for x in range(1)] for x in range(poolsize)] 
    munisplitno = [[0 for x in range(1)] for x in range(poolsize)]
    data1 = np.zeros((1,num_districts))
    for compelection in composite:
        data1  += initial_partition[compelection].percents("Democratic") 

    data1 = data1/len(composite)
    data1 = pd.DataFrame(sorted(list(data1)), columns=cds)
    datastruct = []
    #setup parallel list of DataFrames
    for nn in range(poolsize):
        datastruct.append(data1)
    ctx = get_context("fork") #spawn
    p = ctx.Pool(poolsize)
    print("starting parallel runs\n")  
    updated_vals = p.starmap(multichain_run, [(i1, graph_PA, chainlength, my_apportionment, poptol, my_electionproxy, composite, rs[i1],
                                               rsw[i1],rfw[i1], rmm[i1], reg[i1], rpp[i1], datastruct[i1], state, splitno[i1], munisplitno[i1], \
                                                   maxsplits, maxmunisplits, electionvol) for i1 in range(poolsize)])
    
    for i1, rs_updated, rsw_updated,rfw_updated, rmm_updated, reg_updated, rpp_updated, datastruct_updated, splitno_updated, munisplitno_updated in updated_vals:
        rsw[i1] = rsw_updated
        rs[i1] = rs_updated
        rfw[i1] = rfw_updated
        rmm[i1] = rmm_updated
        reg[i1] = reg_updated
        rpp[i1] = rpp_updated
        datastruct[i1] = datastruct_updated
        splitno[i1] = splitno_updated
        munisplitno[i1] = munisplitno_updated
    #clean up data
    rsw_bak= rsw.copy()   #just to be on the safe side
    
    reg_bak = reg.copy()
    
    rmm_bak = rmm.copy()
    datastruct_bak = datastruct.copy()
    for nn in range(poolsize): #clean up since 1st value in each list is a junk '0'
        junk = rsw[nn].pop(0)
        junk = rs[nn].pop(0)
        junk = rfw[nn].pop(0)
        junk = reg[nn].pop(0)
        junk = rmm[nn].pop(0)
        junk = splitno[nn].pop(0)
        junk = munisplitno[nn].pop(0)
    
    iter1 = range(corrlength-1,corrlength+chainlength-1,corrlength)   #since the correlation length is 200, only collect every 200th point
    reg_clean = []
    rmm_clean = []
    rsw_clean = []
    rs_clean = []
    rfw_clean = []
    rpp_clean = []
    splitno_clean = []
    munisplitno_clean = []
    for nn in range(poolsize):
        for kk in iter1: 
            reg_clean.append(reg[nn][kk]) 
            rmm_clean.append(rmm[nn][kk]) 
            rsw_clean.append(rsw[nn][kk])
            rs_clean.append(rs[nn][kk])
            rfw_clean.append(rfw[nn][kk])
            rpp_clean.append(rpp[nn][kk])
            splitno_clean.append(splitno[nn][kk])
            munisplitno_clean.append(munisplitno[nn][kk])
                 
    #data1 = data1.transpose()
    #data1 = pandas.DataFrame((initial_partition["SEN12"].percents("Democratic") ))
    t1=time.time()
    print( (t1-t0)/60, " min runtime\n")
    exec(open("condense_datastruct6.py").read()) 
    # RUN condense_datastruct.py after this to unpack the data structure and plot it