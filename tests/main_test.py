#!/usr/bin/env python3
# coding: utf-8


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from backturfer import * 
import pytest


def test_df_shape() : 

    df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")

    assert len(df) == 130571
    assert len(df.columns) == 16
    assert 'url' in df.columns
    assert 'comp' in df.columns
    assert 'results' not in df.columns


def test_RaceSelector() : 
    
    df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
    form        = { 'date_start': "2018-01-01", 'quinte' : 1, 
                    'euro_only' : True, 'typec': [  'attelé', 'monté', "plat"]}
    race_sel    = RaceSelector(form)
    df          = race_sel(df)

    assert len(df) == 362
    assert len(df.columns) == 16
    assert 'url' in df.columns
    assert 'comp' in df.columns
    assert 'results' not in df.columns


def test_GroupBy_internalize_results() : 

    from backturfer import * 
    
    df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
    form        = { 'date_start': "2018-01-01", 'quinte' : 1, 
                    'euro_only' : True, 'typec': [  'attelé', 'monté', "plat"]}
    race_sel    = RaceSelector(form)
    df          = race_sel(df)

    df = GroupBy.internalize_results(df)

    assert "results" in df.columns
    results = df.results.iloc[0]
    assert isinstance(results, pd.DataFrame)
    assert "cl" in results.columns
    assert "numero" in results.columns



