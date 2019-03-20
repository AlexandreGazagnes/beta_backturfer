#!/usr/bin/env python3
# coding: utf-8


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from backturfer import *
from strats     import * 
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

@pytest.fixture
def simple_strat():
    return SimpleStrats.choix_de_la_meilleure_cote

@pytest.fixture
def couple_strat():
    return CoupleStrats.choix_des_2_meilleures_cotes



class Test_SimpleGagnant() : 
    """test class for simple gagnants bets"""

    def test_bet_run(self, selected_df, simple_strat) : 
        """just Bet.run()"""

        bet = Bet("simple_gagnant", simple_strat)
        # info(bet)
        # info(bet.__dict__)
        _df = bet.run(selected_df.copy())
        

    def test_bet_consistancy_0(self, selected_df, simple_strat) : 
        """bet results columns"""

        bet = Bet("simple_gagnant", simple_strat)
        _df = bet.run(selected_df.copy())

        for i in ['bet_horse', 'win_horse', 'bet_or_not', 'horse_cote', 'good_bet']  : 
            assert i in _df.columns


    def test_bet_consistancy_1(self, selected_df, simple_strat) : 
        """bet results 'bet horses' """

        bet = Bet("simple_gagnant", simple_strat)
        _df = bet.run(selected_df.copy())

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


    def test_bet_consistancy_2(self, selected_df, simple_strat) : 
        """bet results good_bet rate"""

        bet = Bet("simple_gagnant", simple_strat)
        _df = bet.run(selected_df.copy())
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


    def test_bet_consistancy_7(self, selected_df) : 
        """bet winnings"""

        comps = [   1071233, 1075658, 1123874, 1072071, 1107118, 1068713, 1104842,
                    1096257, 1048673, 1069402, 1048673, 1104733, 1106948, 1048545,
                    1082366, 1086335, 1064636, 1123874, 1106671, 1085399, 1084597,
                    1064570, 1124061, 1111058, 1084683, 1096257, 1085414, 1104965,
                    1048673, 1086567 ]

        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]   
        # assert len(_df) == len(comps)
        _df = bet.run(_df)
        assert _df.good_bet.all()


    def test_bet_consistancy_8(self, selected_df) : 
        """bet loosing"""

        comps = [   1053493, 1071754, 1104696, 1072040, 1099183, 1077608, 1064617,
                    1084724, 1116020, 1072897, 1099339, 1071622, 1069459, 1104801,
                    1086901, 1065454, 1070386, 1071415, 1048698, 1111115, 1064547,
                    1104679, 1106908, 1072040, 1086093, 1074598, 1104931, 1070386,
                    1086093, 1116020 ]
     
        bet = Bet("simple_gagnant", Strats.choix_de_la_meilleure_cote)
        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]   
        
        # for i in comps : 
        #     if i not in _df.comp : 
        #         raise ValueError(i)

        # assert len(_df) == len(comps)

        _df = bet.run(_df)
        assert not _df.good_bet.any()

        
class Test_SimplePlace() : 
    """test class for simple places bets"""

    def test_bet_run(self, selected_df, simple_strat) : 

        """just Bet.run()"""
        bet = Bet("simple_place", simple_strat)
        _df = bet.run(selected_df.copy())


    def test_bet_consistancy_0(self, selected_df, simple_strat) : 
        """bet results columns"""

        bet = Bet("simple_place", simple_strat)
        _df = bet.run(selected_df.copy())

        for i in ['bet_horse', 'win_horses', 'bet_or_not', 'horse_cote', 'good_bet']  : 
            assert i in _df.columns


    def test_bet_consistancy_1(self, selected_df, simple_strat) : 
        """bet results 'bet horses' """

        bet = Bet("simple_place", simple_strat)
        _df = bet.run(selected_df.copy())

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


    def test_bet_consistancy_7(self, selected_df) : 
        """bet winnings"""

        comps = [   1086541, 1077608, 1072071, 1085443, 1048614, 1084714, 1069172,
                    1086645, 1064461, 1104559, 1084714, 1095149, 1048470, 1073055,
                    1101268, 1086645, 1107118, 1101268, 1124432, 1124400, 1048470,
                    1104867, 1069172, 1068713, 1124149, 1107118, 1086567, 1064538,
                    1099401, 1074598 ]

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)

        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]   
        # assert len(_df) == len(comps)
        _df = bet.run(_df)
        assert _df.good_bet.all()

    def test_bet_consistancy_8(self, selected_df) : 
        """bet loosing"""

        comps = [   1088486, 1048658, 1113348, 1059769, 1076989, 1086486, 1123937,
                    1101678, 1058997, 1058974, 1104801, 1084848, 1074502, 1072949,
                    1071797, 1072040, 1124606, 1099313, 1071389, 1048453, 1104896,
                    1074660, 1084724, 1073103, 1104679, 1124410, 1071813, 1085999,
                    1113356, 1113356    ]

        bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]   

        # for i in comps : 
        #     if i not in _df.comp : 
        #         raise ValueError(i)

        # assert len(_df) == len(comps)

        _df = bet.run(_df)
        assert not _df.good_bet.any()
       


class Test_CoupleGagnant() : 
    """test class for simple places bets"""

    def test_bet_run(self, selected_df, couple_strat) : 
        """just Bet.run()"""

        bet = Bet("couple_gagnant", couple_strat)
        _df = bet.run(selected_df.copy())


    def test_bet_consistancy_0(self, selected_df, couple_strat) : 
        """bet results columns"""

        bet = Bet("couple_gagnant", couple_strat)
        _df = bet.run(selected_df.copy())

        for i in ['bet_horses', 'win_horses', 'bet_or_not', 'couple_cote', 'good_bet']  : 
            assert i in _df.columns


    def test_bet_consistancy_1(self, selected_df, couple_strat) : 
        """test wining bets """

        comps = [   1048427, 1048524, 1048568, 1048579, 1053457, 1064524, 1064538,
                    1067714, 1068191, 1068449, 1069402, 1071233, 1071295, 1073132,
                    1074464, 1077608, 1084396, 1084597, 1095242, 1095842, 1104124,
                    1104631, 1104733, 1104867, 1104947, 1106948, 1107726, 1109088,
                    1123999, 1124088, 1124619, 1124647 ]
        
        bet = Bet("couple_gagnant", couple_strat)

        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]   
        assert len(_df) == len(comps)
        _df = bet.run(_df)
        assert _df.good_bet.all()


    def test_bet_consistancy_2(self, selected_df, couple_strat) : 
        """test loosing bets """

        comps = [  1104565, 1048720, 1084724, 1105039, 1069210, 1086567, 1068571,
                   1071389, 1085487, 1073002, 1069230, 1099313, 1071780, 1073032,
                   1074502, 1083092, 1071389, 1124181, 1071797, 1101732, 1104737,
                   1104559, 1048573, 1068093, 1113348, 1101558, 1068713, 1068093,
                   1074502, 1048680 ]

        bet = Bet("couple_gagnant", couple_strat)

        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]   
        
        # for i in comps : 
        #     if i not in _df.comp : 
        #         raise ValueError(i)

        # assert len(_df) == len(comps)

        _df = bet.run(_df)
        assert not _df.good_bet.any()


class Test_CoupleOrdre() : 
    """test class for simple places bets"""

    def test_bet_run(self, selected_df, couple_strat) : 
        """just Bet.run()"""

        bet = Bet("couple_ordre", couple_strat)
        _df = bet.run(selected_df.copy())


    def test_bet_consistancy_0(self, selected_df, couple_strat) : 
        """bet results columns"""

        bet = Bet("couple_ordre", couple_strat)
        _df = bet.run(selected_df.copy())

        for i in ['bet_horses', 'win_horses', 'bet_or_not', 'couple_cote', 'good_bet']  : 
            assert i in _df.columns


    def test_bet_consistancy_1(self, selected_df, couple_strat) : 
        """test wining bets """

        comps = [  1042867, 1068191, 1104631, 1071295, 1104867, 1003334, 1107726,
                   1107726, 1003149, 1048579, 1003300, 1003300, 1048579, 1003091,
                   1095242, 1071233, 1048579, 1124647, 1003149, 1032444, 1029599,
                   1003334, 1023485, 1124619, 1003149, 1095242, 1124088, 1104733,
                   1003091, 1069402  ]

        bet = Bet("couple_ordre", couple_strat)

        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]   
        assert len(_df) == len(comps)
        _df = bet.run(_df)
        assert _df.good_bet.all()

    def test_bet_consistancy_2(self, selected_df, couple_strat) : 
        """test loosing bets """

        comps = [   1003100, 1099183, 1048353, 1069230, 1084419, 1053499, 1085584,
                    1088213, 1048587, 1116165, 1029744, 1069275, 1124149, 1048012,
                    1030176, 1075620, 1084404, 1104938, 1017959, 1023075, 1003225,
                    1019381, 1064461, 1022597, 1023852, 1018481, 1083102, 1087008,
                    1048614, 1106602    ]

        bet = Bet("couple_ordre", couple_strat)

        _df = selected_df.copy()
        _df = _df.loc[_df.comp.apply(lambda i : i in comps), :]     
        # for i in comps : 
        #     if i not in _df.comp : 
        #         raise ValueError(i)

        # assert len(_df) == len(comps)

        _df = bet.run(_df)
        assert not _df.good_bet.any()
        

class Test_CouplePlace() : 
    """test class for simple places bets"""

    def test_bet_run(self, selected_df, couple_strat) : 
        """just Bet.run()"""

        bet = Bet("couple_place", couple_strat)
        _df = bet.run(selected_df.copy())


    def test_bet_consistancy_0(self, selected_df, couple_strat) : 
        """bet results columns"""

        bet = Bet("couple_place", couple_strat)
        _df = bet.run(selected_df.copy())

        for i in ['bet_horses', 'win_horses', 'bet_or_not', 'couple_cote', 'good_bet']  : 
            assert i in _df.columns
