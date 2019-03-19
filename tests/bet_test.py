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


    def test_bet_consistancy_3(self, selected_df) : 
        """bet results for one race"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1086803
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2018-08-21/reunion-deauville/resultats-rapports/prix-de-la-barberie-1086803"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 2
        assert _df.good_bet == False


    def test_bet_consistancy_4(self, selected_df) : 
        """bet results good_bet rate"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1101558
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2018-10-16/reunion-chantilly/resultats-rapports/prix-d-orry-1101558"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 16
        assert _df.win_horse == 13
        assert _df.good_bet == False


    def test_bet_consistancy_5(self, selected_df) : 
        """bet results good_bet rate"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1115896
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2019-01-18/reunion-cagnes-sur-mer/resultats-rapports/prix-charles-gastaud-1115896"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 7
        assert _df.win_horse == 17
        assert _df.good_bet == False


    def test_bet_consistancy_6(self, selected_df) : 
        """bet results good_bet rate"""

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1124061
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2019-01-24/reunion-vincennes/resultats-rapports/prix-de-la-semaine-internationale-1124061"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 15
        assert _df.win_horse == 15
        assert _df.good_bet == True

 

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


    def test_bet_consistancy_2(self, selected_df) : 
        """bet results good_bet rate"""

        # bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        # _df = bet.run(selected_df)
        # rate = round(sum(_df.good_bet)/len(_df), 2)
        # assert rate == 0.25
        pass


    def test_bet_consistancy_3(self, selected_df) : 
        """bet results for one race"""

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1086803
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2018-08-21/reunion-deauville/resultats-rapports/prix-de-la-barberie-1086803"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 2
        assert (_df.win_horses == [6, 16, 4]).all()
        assert _df.good_bet == False


    def test_bet_consistancy_4(self, selected_df) : 
        """bet results good_bet rate"""

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1101558
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2018-10-16/reunion-chantilly/resultats-rapports/prix-d-orry-1101558"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 16
        assert (_df.win_horses == [13,1,12]).all()
        assert _df.good_bet == False


    def test_bet_consistancy_5(self, selected_df) : 
        """bet results good_bet rate"""

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1115896
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2019-01-18/reunion-cagnes-sur-mer/resultats-rapports/prix-charles-gastaud-1115896"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 7
        assert (_df.win_horses == [17, 10, 7]).all()
        assert _df.good_bet == True


    def test_bet_consistancy_6(self, selected_df) : 
        """bet results good_bet rate"""

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        df = selected_df.copy()

        _comp = 1124061
        df = df.loc[df.comp == _comp, :]
        assert len(df) == 1
        assert df.url.iloc[0] == "https://www.paris-turf.com/programme-courses/2019-01-24/reunion-vincennes/resultats-rapports/prix-de-la-semaine-internationale-1124061"
        
        _df = bet.run(df)
        assert len(_df) == 1

        _df = _df.iloc[0]
        assert _df.bet_horse == 15
        assert (_df.win_horses == [15, 11, 6]).all()
        assert _df.good_bet == True



