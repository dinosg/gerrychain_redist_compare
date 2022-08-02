#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 10:57:56 2020
save key variables calculated in run
@author: dinos


Templates:
    Save - 
outname = a filename
outname = "redist_data/" + state + "_" + my_apportionment + "_" + my_electionproxy + "x" + str(chainlength)+ "x" + str(poolsize) + normalize

bc.save(outname,data_condensed,  reg, rmm, rsw)
bc.save1(outname,data_condensed, reg_clean, rmm_clean, rsw_clean, reg, rmm, rsw)

    Load -
the_data, data_frame, reg, rmm, rsw = bc.load(filename)

the_data, data_frame, reg_cln, rmm_cln, rsw_cln,reg, rmm, rsw  = bc.load1(filename)
"""

import pickle as pk

def save(filename, data_frame, reg, rmm, rsw):
    the_data = {"data": data_frame, "reg": reg, "rmm": rmm, "rsw": rsw}
    pk.dump(the_data, open(filename, "wb"))
    

def load(filename):
    
    the_data = pk.load(open(filename, "rb"))
    data_frame = the_data["data"]
    reg = the_data["reg"]
    rmm = the_data["rmm"]
    rsw = the_data["rsw"]
    
    return the_data, data_frame, reg, rmm, rsw

def save1(filename, data_frame, regcln, rmmcln, rswcln, rppcln, reg, rmm, rsw, rpp):
    the_data = {"data": data_frame, "reg_cln": regcln, "rmm_cln": rmmcln, "rsw_cln": rswcln, "rpp_cln": rppcln,  "reg": reg, "rmm": rmm, "rsw": rsw , "rpp" :rpp}
    pk.dump(the_data, open(filename, "wb"))
    
def save2(filename, data_frame, regcln, rmmcln, rswcln, rppcln, splitno_cln, reg, rmm, rsw, rpp,splitno):
    the_data = {"data": data_frame, "reg_cln": regcln, "rmm_cln": rmmcln, "rsw_cln": rswcln, "rpp_cln": rppcln, "splitno_cln": splitno_cln,  "reg": reg, "rmm": rmm, \
                "rsw": rsw , "rpp" :rpp, "splitno": splitno}
    pk.dump(the_data, open(filename, "wb"))

def save3(filename, data_frame, regcln, rmmcln, rswcln, rfwcln, rppcln, splitno_cln, reg, rmm, rsw, rfw, rpp,splitno):
    the_data = {"data": data_frame, "reg_cln": regcln, "rmm_cln": rmmcln, "rsw_cln": rswcln, "rfw_cln": rfwcln, \
                "rpp_cln": rppcln, "splitno_cln": splitno_cln,  "reg": reg, "rmm": rmm, \
                "rsw": rsw , "rfw": rfw,  "rpp" :rpp, "splitno": splitno}
    pk.dump(the_data, open(filename, "wb")) 
    
def save4(filename, data_frame, regcln, rmmcln, rswcln, rfwcln, rppcln, splitno_cln, munisplitno_cln, reg, rmm, rsw, rfw,  rpp,splitno, munisplitno):
    the_data = {"data": data_frame, "reg_cln": regcln, "rmm_cln": rmmcln, "rsw_cln": rswcln, "rfw_cln": rfwcln, \
                "rpp_cln": rppcln, "splitno_cln": splitno_cln, "munisplitno_cln": munisplitno_cln, "reg": reg, "rmm": rmm, \
                "rsw": rsw , "rfw": rfw ,  "rpp" :rpp, "splitno": splitno, "munisplitno": munisplitno}
    pk.dump(the_data, open(filename, "wb")) 

def save5(filename, data_frame, regcln, rmmcln, rswcln,  rppcln, splitno_cln, munisplitno_cln, reg, rmm, rsw,  rpp,splitno, munisplitno):
    the_data = {"data": data_frame, "reg_cln": regcln, "rmm_cln": rmmcln, "rsw_cln": rswcln,  \
                "rpp_cln": rppcln, "splitno_cln": splitno_cln, "munisplitno_cln": munisplitno_cln, "reg": reg, "rmm": rmm, \
                "rsw": rsw ,   "rpp" :rpp, "splitno": splitno, "munisplitno": munisplitno}
    pk.dump(the_data, open(filename, "wb")) 
 
def save6(filename, data_frame, regcln, rmmcln, rswcln, rfwcln, rscln, rppcln, splitno_cln, munisplitno_cln, reg, rmm, rsw, rfw, rs, rpp,splitno, munisplitno):
    the_data = {"data": data_frame, "reg_cln": regcln, "rmm_cln": rmmcln, "rsw_cln": rswcln, "rfw_cln": rfwcln, "rs_cln": rscln , \
                "rpp_cln": rppcln, "splitno_cln": splitno_cln, "munisplitno_cln": munisplitno_cln, "reg": reg, "rmm": rmm, \
                "rsw": rsw , "rfw": rfw , "rs": rs,  "rpp" :rpp, "splitno": splitno, "munisplitno": munisplitno}
    pk.dump(the_data, open(filename, "wb")) 
    
def load1(filename):
    
    the_data = pk.load(open(filename, "rb"))
    data_frame = the_data["data"]
    reg = the_data["reg"]
    rmm = the_data["rmm"]
    rsw = the_data["rsw"]
    rpp = the_data["rpp"]
    reg_cln = the_data["reg_cln"]
    rmm_cln = the_data["rmm_cln"]
    rsw_cln= the_data["rsw_cln"]
    rpp_cln= the_data["rpp_cln"]
    
    
    return the_data, data_frame, reg_cln, rmm_cln, rpp_cln, rsw_cln, reg, rmm, rsw, rpp

def load2(filename):
    
    the_data = pk.load(open(filename, "rb"))
    data_frame = the_data["data"]
    reg = the_data["reg"]
    rmm = the_data["rmm"]
    rsw = the_data["rsw"]
    rpp = the_data["rpp"]
    splitno = the_data["splitno"]
    reg_cln = the_data["reg_cln"]
    rmm_cln = the_data["rmm_cln"]
    rsw_cln= the_data["rsw_cln"]
    rpp_cln= the_data["rpp_cln"]
    splitno_cln = the_data["splitno_cln"]
    return the_data, data_frame, reg_cln, rmm_cln, rpp_cln, rsw_cln, splitno_cln, reg, rmm, rsw, rpp, splitno

def load3(filename):
    #has FRACTIONAL WINS as well as dem seats won
    the_data = pk.load(open(filename, "rb"))
    data_frame = the_data["data"]
    reg = the_data["reg"]
    rmm = the_data["rmm"]
    rsw = the_data["rsw"]
    rfw = the_data["rfw"]
    rpp = the_data["rpp"]
    splitno = the_data["splitno"]
    reg_cln = the_data["reg_cln"]
    rmm_cln = the_data["rmm_cln"]
    rsw_cln= the_data["rsw_cln"]
    rfw_cln= the_data["rfw_cln"]
    rpp_cln= the_data["rpp_cln"]
    splitno_cln = the_data["splitno_cln"]
    return the_data, data_frame, reg_cln, rmm_cln, rpp_cln, rsw_cln, rfw_cln, splitno_cln, reg, rmm, rsw, rfw, rpp, splitno

def load4(filename):
    #has FRACTIONAL WINS as well as dem seats won
    the_data = pk.load(open(filename, "rb"))
    data_frame = the_data["data"]
    reg = the_data["reg"]
    rmm = the_data["rmm"]
    rsw = the_data["rsw"]
    rfw = the_data["rfw"]
    rpp = the_data["rpp"]
    splitno = the_data["splitno"]
    munisplitno = the_data["munisplitno"]
    reg_cln = the_data["reg_cln"]
    rmm_cln = the_data["rmm_cln"]
    rsw_cln= the_data["rsw_cln"]
    rfw_cln= the_data["rfw_cln"]
    rpp_cln= the_data["rpp_cln"]
    splitno_cln = the_data["splitno_cln"]
    munisplitno_cln = the_data["munisplitno_cln"]
    return the_data, data_frame, reg_cln, rmm_cln, rpp_cln, rsw_cln,rfw_cln,  splitno_cln, munisplitno_cln, reg, rmm, rsw,rfw, rpp, splitno, munisplitno

def load5(filename):
    #has FRACTIONAL WINS as well as dem seats won
    the_data = pk.load(open(filename, "rb"))
    data_frame = the_data["data"]
    reg = the_data["reg"]
    rmm = the_data["rmm"]
    rsw = the_data["rsw"]
    #rfw = the_data["rfw"]
    rpp = the_data["rpp"]
    splitno = the_data["splitno"]
    munisplitno = the_data["munisplitno"]
    reg_cln = the_data["reg_cln"]
    rmm_cln = the_data["rmm_cln"]
    rsw_cln= the_data["rsw_cln"]
    #rfw_cln= the_data["rfw_cln"]
    rpp_cln= the_data["rpp_cln"]
    splitno_cln = the_data["splitno_cln"]
    munisplitno_cln = the_data["munisplitno_cln"]
    return the_data, data_frame, reg_cln, rmm_cln, rpp_cln, rsw_cln,  splitno_cln, munisplitno_cln, reg, rmm, rsw, rpp, splitno, munisplitno

def load6(filename):
    #has FRACTIONAL WINS as well as dem seats won
    the_data = pk.load(open(filename, "rb"))
    data_frame = the_data["data"]
    reg = the_data["reg"]
    rmm = the_data["rmm"]
    rsw = the_data["rsw"]
    rs = the_data["rs"]
    rfw = the_data["rfw"]
    rpp = the_data["rpp"]
    splitno = the_data["splitno"]
    munisplitno = the_data["munisplitno"]
    reg_cln = the_data["reg_cln"]
    rmm_cln = the_data["rmm_cln"]
    rsw_cln= the_data["rsw_cln"]
    rs_cln= the_data["rs_cln"]
    rfw_cln= the_data["rfw_cln"]
    rpp_cln= the_data["rpp_cln"]
    splitno_cln = the_data["splitno_cln"]
    munisplitno_cln = the_data["munisplitno_cln"]
    return the_data, data_frame, reg_cln, rmm_cln, rpp_cln, rsw_cln,rfw_cln, rs_cln, splitno_cln, munisplitno_cln, reg, rmm, rsw,rfw,rs, rpp, splitno, munisplitno

