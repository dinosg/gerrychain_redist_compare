#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 11:07:44 2020
script to define constants for file read-in and computation as below
@author: dinos
"""


my_electionproxy = "SEN16"           #pick the election to use as a statewide proxy for partisan voting for districted seats
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs/PA_VTD_PLANS.shp"   #PATH to the election data
my_electiondatafile = "./PA-shapefiles-master/DRA_data/adjusted2021_electdat.shp"    #PATH to the election data LRC, NO prisoner reallocation
#my_electiondatafile = "./PA-shapefiles-master/PA_VTDs.json"   #PATH to the election data
#my_electiondatafile ="./shapefiles_multistate/WI-shapefiles-master/WI_wards_12_16/WI_ltsb_corrected_final.json"
#state = "PA_lrcbarber"
state = "PA"
my_electionproxy_alternate="USS12"
#maxsplitlist=[ 70, 50, 30, 20, 17]
#cutedgemaxlist  = [2,2,2,1.2,1.2]
poptol=0.01
electionvol = 0.05
win_volatility= electionvol
ex_dist_name='PA_CD/CARTER_PA_assignments_nosplitpcts.txt'
#ex_dist_name='PA_CD/HB2146precinct-assignments_nosplits.txt'
#ex_dist_name='PA_CD/max_competitive_PA_CD-assignments.txt'
#my_apportionment = 'CDcomp'    #type of district boundaries to calculate - eg US congressional, state senate, house etc.
my_apportionment = 'Carter'
#my_apportionment = 'hb2146'

geotag="GEOID20"
numdists = 17
postfix='ppart'
popkey='TOTPOP'
cutedgemax=1.2
maxsplits = 22
maxsplits = 85# 186



maxmunisplits =100
chainlength=400
poolsize=40
