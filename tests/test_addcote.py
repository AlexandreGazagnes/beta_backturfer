#!/usr/bin/env python3
# coding: utf-8

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')



from src import * 
import pytest



def test_addcote_quinte_0() : 

    # url = "https://www.paris-turf.com/programme-courses/2017-02-02/reunion-vincennes/resultats-rapports/prix-de-langeais-1003300"
    df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
    url = df.loc[df.comp == 1003300, "url"].values
    assert len(url) == 1

    url = url[0]
    assert isinstance(url, str)
    
    info(url)
    cotes =   AddCote.scrap(url, cotes="all")

    assert round(cotes.loc[cotes.type == "simple_gagnant", "pmu"].values[0], 2)     == 1.7 
    assert round(cotes.loc[cotes.type == "couple_gagnant", "pmu"].values[0], 2)     == 6.8
 
    assert round(cotes.loc[cotes.type == "couple_ordre", "pmu"].values[0], 2)       == 8.3
    assert round(cotes.loc[cotes.type == "deux_sur_quatre","pmu"].values[0], 2)     == 4.40 
 
    assert round(cotes.loc[cotes.type == "trio_desordre", "pmu"].values[0], 2)      == 40.5
    assert round(cotes.loc[cotes.type == "trio_ordre", "leturf.fr"].values[0], 2)   == 61.4

    assert round(cotes.loc[cotes.type == "tierce_desordre", "pmu"].values[0], 2)    == 13.9
    assert round(cotes.loc[cotes.type == "tierce_ordre", "pmu"].values[0], 2)       == 69.5 
 
    assert round(cotes.loc[cotes.type == "quinte_desordre", "pmu"].values[0], 2)    == 56.9
    assert round(cotes.loc[cotes.type == "quinte_ordre", "pmu"].values[0], 2)       == 2845




