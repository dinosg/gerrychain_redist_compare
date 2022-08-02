#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""

#my_apportionment = "DRA_compact"    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
#my_apportionment = "HDlrcfinal" 
#my_apportionment = "HDlrc"
my_apportionment="benning"
my_apportionment = my_apportionment[0:10]
my_electionproxy = "SEN16"           #pick the election to use as a statewide proxy for partisan voting for districted seats
my_electionproxy_alternate = "SEN16"
#my_electiondatafile = "./PA-shapefiles-master/LRC_2021/lrc2021_electdat_HD.shp"    #PATH to the election data
my_electiondatafile = "./PA-shapefiles-master/LRC_2021/lrc2021_electdat.shp"    #PATH to the election data
#my_electiondatafile ="./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
#state = "PA"
state = "PA_lrcbarber"
poptol=0.05
cutedgemax=1.2
maxsplits = 195# 186
maxmunisplits = 110 #120
electionvol = 0.05
win_volatility = electionvol
#ex_dist_name='PA_HD/DRA_most_compact_PAHD2022.txt'
#ex_dist_name='PA_HD/benninghoff_amendment.txt'
ex_dist_name=''
geotag="GEOID20"
#postfix='countyonly'
postfix='ppart'
popkey='P0010001'
chainlength=400
poolsize=40