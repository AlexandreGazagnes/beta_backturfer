#!/usr/bin/env python3
# coding: utf-8


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

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

class Test_SimpleGagnant() : 
    """test class for simple gagnants bets"""

    def test_bet_init(self) : 
        """just Bet.__init__()"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        # info(bet)
        # info(bet.__dict__)


    def test_bet_run(self, selected_df) : 
        """just Bet.run()"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        # info(bet)
        # info(bet.__dict__)
        _df = bet.run(selected_df)
        

    def test_bet_consistancy_0(self, selected_df) : 
        """bet results columns"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        _df = bet.run(selected_df)

        for i in ['bet_horse', 'win_horse', 'bet_or_not', 'horse_cote', 'good_bet']  : 
            assert i in _df.columns


    def test_bet_consistancy_1(self, selected_df) : 
        """bet results 'bet horses' """

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        _df = bet.run(selected_df)

        for _ in range(10) : # run 10 times 
            while True : 
                race_0   = _df.iloc[np.random.choice(_df.index), :] # pick a random race
                result_0 = race_0.results.sort_values("cotedirect", ascending=True, axis=0)
                try : 
                    if (result_0.cotedirect.iloc[0] > 0.0 ) and (result_0.cotedirect.iloc[0] < 10.0 ) : # be sure prob !=0
                        break
                except : # if error just pass it 
                    pass

            assert race_0.bet_horse == result_0.numero.iloc[0] 


    def test_bet_consistancy_2(self, selected_df) : 
        """bet results good_bet rate"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        _df = bet.run(selected_df)
        rate = round(sum(_df.good_bet)/len(_df), 2)
        assert rate == 0.25


class Test_SimplePlace() : 
    """test class for simple places bets"""

    def test_bet_init(self) : 

        """just Bet.__init__()"""
        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        info(bet)
        info(bet.__dict__)


    def test_bet_run(self, selected_df) : 

        """just Bet.run()"""
        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        _df = bet.run(selected_df)


    def test_bet_consistancy_0(self, selected_df) : 
        """bet results columns"""

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        _df = bet.run(selected_df)

        for i in ['bet_horse', 'win_horses', 'bet_or_not', 'horse_cote', 'good_bet']  : 
            assert i in _df.columns


    def test_bet_consistancy_1(self, selected_df) : 
        """bet results 'bet horses' """

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        _df = bet.run(selected_df)

        for _ in range(10) : # run 10 times 
            while True : 
                race_0   = _df.iloc[np.random.choice(_df.index), :] # pick a random race
                result_0 = race_0.results.sort_values("cotedirect", ascending=True, axis=0)
                try : 
                    if (result_0.cotedirect.iloc[0] > 0.0 ) and (result_0.cotedirect.iloc[0] < 10.0 ) : # be sure prob !=0
                        break
                except : # if error just pass it 
                    pass

            assert race_0.bet_horse == result_0.numero.iloc[0] 



class Test_CoupleGagnant() : 
    """test class for simple places bets"""

    def test_bet_init(self) : 
        """just Bet.__init__()"""

        bet = Bet("couple_gagnant", Strats.choix_de_la_meilleure_cote)
        info(bet)
        info(bet.__dict__)


    def test_bet_run(self, selected_df) : 
        """just Bet.run()"""

        bet = Bet("couple_gagnant", Strats.choix_de_la_meilleure_cote)

        with pytest.raises(NotImplementedError):
            _df = bet.run(selected_df)


    def test_bet_consistancy_0(self, selected_df) : 
        """bet results columns"""

        bet = Bet("couple_gagnant", Strats.choix_de_la_meilleure_cote)
    
        with pytest.raises(NotImplementedError):
            _df = bet.run(selected_df)
            for i in ['bet_horses', 'win_horses', 'bet_or_not', 'horse_cote', 'good_bet']  : 
                assert i in _df.columns




