#!/usr/bin/env python3
# coding: utf-8


from backturfer import *
import pytest


@pytest.fixture
def raw_df() : 
    return  pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")


@pytest.fixture
def selected_df() : 
        df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
        form        = { 'date_start': "2018-01-01", 'quinte' : 1, 
                        'euro_only' : True, 'typec': [  'attelé', 'monté', "plat"]}
        race_sel    = RaceSelector(form)
        df          = race_sel(df)

        return df


class TestGeneric() : 

    def run(self, _selected_df, _bet_type, _strat) : 
        """ perform a Bet().run()"""
        return Bet(_bet_type, _strat).run(_selected_df.copy())


    def columns(self,_df, cols ) : 
        assert pd.Series([i in _df.columns for i in cols]).all()


    def rate(self,_selected_df, _bet_type, _strat, rate) : 
        _df = Bet(_bet_type, _strat).run(_selected_df.copy())
        assert round(sum(_df.good_bet)/len(_df), 2) == round(rate, 2)


    def individuals(self, _selected_df, _bet_type, _strat, params) : 

        if _bet_type == "simple_gagnant" : _bet_horse_label, _win_horse_label = "bet_horses", "win_horses"
        elif _bet_type == "simple_place" : _bet_horse_label, _win_horse_label = "bet_horses", "win_horses"
        else                             : _bet_horse_label, _win_horse_label = "bet_horses", "win_horses"

        # force to have list items for bet_horse and win_horse
        if not isinstance(params[0][2], Iterable) : 
            params = [[i[0], i[1], [i[2],], i[3], i[4] ] for i in params]
        if not isinstance(params[0][1], Iterable) : 
            params = [[i[0], [i[1],], i[2], i[3], i[4] ] for i in params]

        _df = Bet(_bet_type, _strat).run(_selected_df.copy())
        _df = _df.loc[list(_df.comp.apply(lambda i : i in [i[0] for i in params])), :]
        assert len(_df) == len(params)

        for _comp, _bet_horse, _win_horse, _good_bet, _url in params : 
            sub_df = _df.loc[_df.comp == _comp, :]
            assert len(sub_df)          == 1
            assert sub_df.url.iloc[0]   == _url
            
            if not isinstance(sub_df[_bet_horse_label].iloc[0], Iterable) : 
                sub_df[_bet_horse_label]  = sub_df[_bet_horse_label].apply(lambda i : [i,])
            if not isinstance(sub_df[_win_horse_label].iloc[0], Iterable) : 
                sub_df[_win_horse_label]  = sub_df[_win_horse_label].apply(lambda i : [i,])
            
            sub_df = sub_df.iloc[0]
            try :    r = (sub_df[_bet_horse_label]     == _bet_horse).all()
            except : r = (sub_df[_bet_horse_label]     == _bet_horse)
            assert r 
            
            try :    r = (sub_df[_win_horse_label]     == _win_horse).all()
            except : r = (sub_df[_win_horse_label]     == _win_horse)
            assert r 

            assert (sub_df.good_bet              == _good_bet)


    def good(self,_selected_df, _bet_type, _strat, comps) : 
        comps=pd.Series(comps).unique()
        _df = _selected_df.copy()
        _df = _df.loc[list(_df.comp.apply(lambda i : i in comps)), :]   
        # assert len(_df) == len(comps)
        assert Bet(_bet_type, _strat).run(_df).good_bet.all()


    def wrong(self,_selected_df, _bet_type, _strat, comps) : 
        comps=pd.Series(comps).unique()
        _df = _selected_df.copy()
        _df = _df.loc[list(_df.comp.apply(lambda i : i in comps)), :]   
        # assert len(_df) == len(comps)
        assert not Bet(_bet_type, _strat).run(_df).good_bet.any()