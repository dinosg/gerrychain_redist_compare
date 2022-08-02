#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:47:51 2020

@author: dinos


This does NOT perform a Markov chain simulation but instead recreates EACH instance of a simulated district partition from scratch
using recursive_tree_part to create random districts. While this is slow, 
Some nice stuff added to DataFrame structure to add congressional district labels in order of actual increasing congressional district No.

dependencies include stopit - install with pip (conda install didn't work for me)
It prevents recursive_tree_part from getting hung-up indefinitely, uses time_out to define maximum limit before timing out
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

Created on Tue Mar 24 16:55:12 2020
uses recom proposal
@author: dpg
"""

from total_splits import total_splits, total_muni_splits
import geopandas
import backup_chain as bc
from multiprocessing import set_start_method, freeze_support
#from multiprocessing import Pool
from multiprocessing import get_context
import backup_chain as bc
import matplotlib.pyplot as plt
import time
import stopit
from gerrychain import (GeographicPartition, Partition, Graph, MarkovChain,
                        proposals, updaters, constraints, accept, Election)
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from functools import partial
from strcmp_matlab import strfilter
import pandas
import pandas as pd
import numpy as np
from gerrychain.metrics import mean_median, efficiency_gap, polsby_popper
from get_districtlabels import get_labels, get_labels_comp
from norm_50 import norm_data
from get_electioninfo import get_elections
import random
import os 
import conditional_dump as cd
from calc_fracwins_comp import calc_fracwins_comp
 
def multichain_run(i1, graph, chainlength, my_apportionment, poptol, my_electionproxy, rs, rsw,rfw, rmm, reg, rpp, datastruct, state, splitno, munisplitno, win_volatility):
    hi_mm = -.01
 #   poptol = 0.06  #min % population deviation per district
    totsteps = 2
    elections, composite = get_elections(state)
    time_out = 300   #modify depending on how fast a machine usually performs recursive_tree_part
    if "TOTPOP" in graph._node[0]:
        popkey = "TOTPOP"
    elif "PERSONS" in graph._node[0]:
        popkey = "PERSONS"
    else:
            popkey = []
            print("woops no popkey in file, look @ graph._node[0] to figure out what the keyword for population is\n")
#CONFIGURE UPDATERS
#We want to set up updaters for everything we want to compute for each plan in the ensemble.


# Population updater, for computing how close to equality the district
# populations are. "TOTPOP" is the population column from our shapefile.
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}


# Election updaters, for computing election results using the vote totals
# from our shapefile.
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)


#INITIAL PARTITION (useful for CD labels)
    initial_partition = GeographicPartition(graph, assignment=my_apportionment, updaters=my_updaters)
    
    #this block obtains the Congressional District Labels and converts to string labels, cds
    
    cds = get_labels_comp(initial_partition, composite) #get congressional district labels
    nparts = len(initial_partition)
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    random.seed(os.urandom(10)*i1) 
   
    pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, poptol)
    proposal = partial(recom,
                   pop_col=popkey,
                   pop_target=ideal_population,
                   epsilon=poptol,
                   node_repeats=2
                  )
    itno = 0
    for zz in range(chainlength):
        with stopit.ThreadingTimeout(time_out) as to_ctx_mgr:
            assert to_ctx_mgr.state == to_ctx_mgr.EXECUTING
            ranpart = recursive_tree_part(graph, range(nparts), ideal_population, popkey,poptol-.003,node_repeats=1)
            randpartition = GeographicPartition(graph,assignment = ranpart, updaters = my_updaters)
        
        if to_ctx_mgr.state == to_ctx_mgr.EXECUTED:
            if i1 == 2 & zz % 2 == 0:
                print('step ',zz)
            compactness_bound = constraints.UpperBound(
            lambda p: len(p["cut_edges"]),
            2*len(initial_partition["cut_edges"])
            )
            chain = MarkovChain(
            proposal=proposal,
            constraints=[
                pop_constraint,
                compactness_bound],
            accept=accept.always_accept,
            initial_state=randpartition,
            total_steps = totsteps
            )
            
            
            #print(i1,  " got here\n")
    for part in chain:
        
        datax = np.zeros((nparts,1))  #nparts = ndistricts
        votes_r = np.zeros((nparts,))
        votes_d = votes_r.copy()
        rmm_tmp = 0
        rs_tmp = 0
        reg_tmp = 0
        rs_tmp = 0
        rfw_tmp = 0
        rsw_tmp = 0
        
        
        for compelection in composite:
            rsw_tmp += part[compelection].wins("Democratic")
            rfw_tmp  = calc_fracwins_comp(part,composite, electionvol)
            votes_d += part[compelection].votes("Democratic") #create the vote index
            votes_r += part[compelection].votes("Republican")
            rs_tmp += part[compelection].wins("Democratic")
            rmm_tmp += mean_median(part[compelection])
            reg_tmp += efficiency_gap(part[compelection])
            datax += pandas.DataFrame(sorted(part[compelection].percents("Democratic" )), index=cds)
            
            
        rfw_tmp  = calc_fracwins_comp(part,composite, electionvol)
        rsw_tmp = np.greater(votes_d, votes_r).sum() #now find who won how many seats from the sum of votes
        rmm_tmp = rmm_tmp/len(composite)
        reg_tmp = reg_tmp/len(composite)
        rs_tmp = rs_tmp/len(composite)
        votes_dpc = votes_d/(votes_d + votes_r)
        #winsfrac = seat_winprob(np.array(votes_dpc), win_volatility)
        #fwinstot_tmp = winsfrac.sum()
        datax = datax.transpose() / len(composite)
        if i1 ==0:
            print(zz)
        rsw.append(rsw_tmp)
        rs.append(rs_tmp)
        rmm.append(rmm_tmp)
        reg.append(reg_tmp)
        #rfw.append(fwinstot_tmp)
        rfw.append(rfw_tmp)
        rpp.append(np.mean(pd.Series(polsby_popper(part))))  #depends on geometry of the partition only not on vote outcomes
        datastruct = pandas.concat([datastruct, datax])
        splitno.append(total_splits(part))
        munisplitno.append(total_muni_splits(part))#splits don't depend on individual election results, only on partition so not in loop
       
        #cd.eg_gt(part.state,hi_eg, state, my_apportionment,my_electionproxy, i1, 'county')
        #cd.eg_zero(part,zero_eg, state, my_apportionment, my_electionproxy, i1)
    return i1, rs, rsw,rfw, rmm, reg, rpp, datastruct, splitno , munisplitno  
          
#MAIN PROGRAM HERE:
    #few key lines for making parallel pool not mess up (freeze_support() and __spec__ definition)
if __name__ == '__main__':
    freeze_support()
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    dontfeedin = 0  #if set=0, feeds in data, otherwise skip
    #poolsize=8
   # chainlength=250
    totsteps = 2
    normalize=''
    #postfix='composite ppart'
    countysp=''
#DEFINE CONSTANTS:
   
    
   # exec(open("input_templates/MI_SENDIST_PRES16.py").read())
  #  exec(open("input_templates/PA_HDIST_SEN12.py").read()) 
    #exec(open("input_templates/PA_HDIST_lrc_muni3.py").read()) 
    #exec(open("input_templates/WI_ASM_SEN16.py").read()) 
    #exec(open("inFput_templates/TX_HD_SEN12.py").read()) 
    #exec(open("input_templates/MD_SEND_PRES16_countyloop.py").read()) #read in input tem
   #exec(open("input_templates/MA_SEND_PRES16_countyloop.py").read()) #read in input tem
   # my_electionproxy_alternate = my_electionproxy
    #for PA data:
   # exec(open("input_templates/PA_HDIST_lrc.py").read())
    exec(open("input_templates/PA_CD17_sumf.py").read())
    
    elections, composite = get_elections(state)
    
    
    if 'dontfeedin' in globals():
        if dontfeedin == 0 or not( 'graph' in globals()):
            if ".json" in my_electiondatafile:
                graph = Graph.from_json(my_electiondatafile)
            else:
                df = geopandas.read_file( my_electiondatafile) 
                exec(open("./splice_assignment_fn.py").read())
    else:
        if ".json" in my_electiondatafile:
            graph = Graph.from_json(my_electiondatafile)
        else:
            df = geopandas.read_file( my_electiondatafile) 
            exec(open("./splice_assignment_fn.py").read())
         
    if 'poptol' not in globals():
        poptol = 0.03
    if "TOTPOP" in graph._node[0]:
        popkey = "TOTPOP"
    elif "PERSONS" in graph._node[0]:
        popkey = "PERSONS"
    else:
        popkey = []
        print("woops no popkey in file, look @ graph._node[0] to figure out what the keyword for population is\n")
    #CONFIGURE UPDATERS
    #We want to set up updaters for everything we want to compute for each plan in the ensemble.
    
    
    # Population updater, for computing how close to equality the district
    # populations are. "TOTPOP" is the population column from our shapefile.
    my_updaters = {"population": updaters.Tally(popkey, alias="population")}
    
    election_updaters = {election.name: election for election in elections}
    my_updaters.update(election_updaters)
    
    #run chain ONCE to clean up graph and use primary election assignment name...
    #INITIAL PARTITION
    initial_partition = GeographicPartition(graph, assignment=my_apportionment, updaters=my_updaters)
    # initial_partition, graph, my_updaters = norm_data(graph, my_updaters, my_apportionment, my_electionproxy, my_electionproxy_alternate)
    # cds = get_labels(initial_partition, my_electionproxy) #get congressional district labels
    #RUNNING THE CHAIN
    ideal_population = sum(list(initial_partition["population"].values())) / len(initial_partition)
    num_districts = len(initial_partition)
    # We use functools.partial to bind the extra parameters (pop_col, pop_target, epsilon, node_repeats)
    # of the recom proposal.
    
    
    t0=time.time()
    #now can do initial_partition and know my_electionproxy will be OK, won't need alternate
     
    cds= get_labels_comp(initial_partition, composite) #get congressional district labels
    # This will take about 10 minutes.
    #setup variables
    rsw = [[0 for x in range(1)] for x in range(poolsize)] #  np.zeros([poolsize, chainlength])
    rs = [[0 for x in range(1)] for x in range(poolsize)]
    rfw = [[0 for x in range(1)] for x in range(poolsize)]
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
    
    #key defs for setting up parallel pool HERE:
    ctx = get_context("fork")  #"spawn"
    p = ctx.Pool(poolsize)
    updated_vals = p.starmap(multichain_run, [(i1, graph, chainlength, my_apportionment, poptol, my_electionproxy, 
                                               rs[i1], rsw[i1], rfw[i1], rmm[i1], reg[i1], rpp[i1], datastruct[i1], 
                                               state, splitno[i1], munisplitno[i1], win_volatility) for i1 in range(poolsize)])
    
    for i1, rs_updated, rsw_updated, rfw_updated, rmm_updated, reg_updated, rpp_updated,  \
    datastruct_updated, splitno_updated, munisplitno_updated in updated_vals:
        rs[i1] = rs_updated
        rfw[i1] = rfw_updated
        rsw[i1] = rsw_updated
        rmm[i1] = rmm_updated
        reg[i1] = reg_updated
        splitno[i1] = splitno_updated
        rpp[i1] = rpp_updated
        munisplitno[i1] = munisplitno_updated
        
        
        datastruct[i1] = datastruct_updated
    #clean up data
    rsw_bak= rsw.copy()   #just to be on the safe side
    
    reg_bak = reg.copy()
    
    rmm_bak = rmm.copy()
    datastruct_bak = datastruct.copy()
    for nn in range(poolsize): #clean up since 1st value in each list is a junk '0'
        junk = rfw[nn].pop(0)
        junk = rs[nn].pop(0)
        junk = rsw[nn].pop(0)
        junk = reg[nn].pop(0)
        junk = rmm[nn].pop(0)
        junk = rpp[nn].pop(0)
        junk = splitno[nn].pop(0)
        junk = munisplitno[nn].pop(0)
    
    #iter1 = range(chainlength * totsteps)   #since the correlation length is 200, only collect every 200th point
    iter1 = range(np.shape(rsw)[1])   #should be equal to chainlength
    reg_clean = []
    rmm_clean = []
    rsw_clean = []
    rfw_clean = []
    rs_clean = []
    rpp_clean = []
    splitno_clean = []
    munisplitno_clean = []
    for nn in range(poolsize):
        for kk in iter1: 
            if rsw[nn][kk] > -1 :   #skip over workers that failed timeout, with -1 in 'won districts'
                reg_clean.append(reg[nn][kk]) 
                rmm_clean.append(rmm[nn][kk]) 
                rsw_clean.append(rsw[nn][kk]) 
                rfw_clean.append(rfw[nn][kk]) 
                rs_clean.append(rs[nn][kk]) 
                rpp_clean.append(rpp[nn][kk])
                splitno_clean.append(splitno[nn][kk])
                munisplitno_clean.append(munisplitno[nn][kk])
                #rpp_clean.append(1)
                 
    #data1 = data1.transpose()
    #data1 = pandas.DataFrame((initial_partition["SEN12"].percents("Democratic") ))
    t1=time.time()
    exec(open("condense_datastruct6.py").read()) 
    #exec(open("condense_datastruct_minimal.py").read())    #run condense_datastruct.py as a script using this namespace
    # RUN condense_datastruct.py after this to unpack the data structure and plot it
    
    """
    
    data_condensed = pandas.DataFrame([]) #null dataframe to start
    threadcount = len(datastruct) #depth of datastruct list object
    skipno = 1  # basically, don't skip b/c
    for ii in range(threadcount):
        data_x = datastruct[ii]
        data_x.columns = cds
        sx = data_x.shape
        sx0 = sx[0]  #this is the # of iterations per dataframe... loop thru these skipping every 100- 200
        data_x.index = range(sx0)
     #   indexer = range(skipno-1, sx0+ skipno-1, skipno)  #collect data from these rows
        indexer = range(sx0-1)
        for kk in indexer:
            if rsw[ii][kk] > -1:   #skip over workers that timed out
                data_condensed= pandas.concat([data_condensed,data_x[kk:kk+1]])
          
    outname = "redist_data/" + state + "_" + my_apportionment + "_" + my_electionproxy + "xppart0" + \
    str(chainlength)+ "x" + str(poolsize)  + normalize + postfix
    bc.save2(outname,data_condensed, reg_clean, rmm_clean, rsw_clean, rpp_clean,splitno_clean, reg, rmm, rsw, rpp, splitno)
    print(t1-t0, "seconds\n")       
    plt.figure()
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Draw 50% line
    #ax.axhline(0.5, color="#cccccc")
    ax.axhline(0.5, color="b")
    
    # Draw boxplot
    #data1.boxplot(ax=ax, positions=range(len(data1.columns)))
    data_condensed.boxplot(positions=range(len(data_condensed.columns)),showfliers=False)
    # Draw initial plan's Democratic vote %s (.iloc[0] gives the first row)
    plt.plot(sorted(data1.iloc[0]), "ro")
    
    # Annotate
    titlestr = state + " " + my_apportionment + "  x" + str(chainlength) + " x" + str(poolsize) + normalize + postfix
    ax.set_title(titlestr)
    ax.set_ylabel("Democratic vote % " + my_electionproxy)
    ax.set_xlabel("Sorted districts")
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    
    plt.show()
    """
