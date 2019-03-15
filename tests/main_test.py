#!/usr/bin/env python3
# coding: utf-8

from src import * 
import pytest

# main dataframe
info("loading dataframe")
df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")

def test_df_shape(df) : 

	assert len(df) == 130571
	assert len(df.columns) == 16
	assert 'url' in df.columns
	assert 'comp' in df.columns
	assert 'results' not in df.columns
