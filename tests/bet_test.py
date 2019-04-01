#!/usr/bin/env python3
# coding: utf-8


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from tests.generic import *





@pytest.fixture
def simple_strat():
    return SimpleStrats.choix_de_la_meilleure_cote


@pytest.fixture
def new_simple_strat():
    return MultiStrats("choix_de_la__N__meilleure_cote", N=0, n=1)


@pytest.fixture
def couple_strat():
    return CoupleStrats.choix_des_2_meilleures_cotes


@pytest.fixture
def trio_strat():
    return TrioStrats.choix_des_3_meilleures_cotes

@pytest.fixture
def quinte_strat():
    return QuinteStrats.choix_des_5_meilleures_cotes


class TestSimpleGagnant(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "simple_gagnant"

    def test_basics(self, selected_df, simple_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, simple_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


    # def test_bet_consistancy_1(self, selected_df, simple_strat) : 
    #     """bet results 'bet horses' """

    #     bet = Bet("simple_gagnant", simple_strat)
    #     _df = bet.run(selected_df.copy())

    #     for _ in range(10) : # run 10 times 
    #         while True : 
    #             race_0   = _df.iloc[np.random.choice(_df.index), :] # pick a random race
    #             result_0 = race_0.results.sort_values("cotedirect", ascending=True, axis=0)
    #             try : 
    #                 if (result_0.cotedirect.iloc[0] > 0.0 ) and (result_0.cotedirect.iloc[0] < 10.0 ) : # be sure prob !=0
    #                     break
    #             except : # if error just pass it 
    #                 pass

    #         assert race_0.bet_horse == result_0.numero.iloc[0] 


    def test_bet_results(self, selected_df, simple_strat) :
        """test if global good_bet rate is consistant"""

        self.rate(selected_df, self.bet_type, simple_strat, 0.25)

        params = [
        #   comp        bet_horses  win_horses     good_bet    url
        [   1086803,    2,          6,              False,      "https://www.paris-turf.com/programme-courses/2018-08-21/reunion-deauville/resultats-rapports/prix-de-la-barberie-1086803"],
        [   1101558,    16,         13,             False,      "https://www.paris-turf.com/programme-courses/2018-10-16/reunion-chantilly/resultats-rapports/prix-d-orry-1101558"],    
        [   1115896,    7,          17,             False,      "https://www.paris-turf.com/programme-courses/2019-01-18/reunion-cagnes-sur-mer/resultats-rapports/prix-charles-gastaud-1115896"], 
        [   1124061,    15,         15,             True,       "https://www.paris-turf.com/programme-courses/2019-01-24/reunion-vincennes/resultats-rapports/prix-de-la-semaine-internationale-1124061"],    
                ]
        self.individuals(selected_df, self.bet_type, simple_strat, params)

        goods = [   1071233, 1075658, 1123874, 1072071, 1107118, 1068713, 1104842,
                    1096257, 1048673, 1069402, 1048673, 1104733, 1106948, 1048545,
                    1082366, 1086335, 1064636, 1123874, 1106671, 1085399, 1084597,
                    1064570, 1124061, 1111058, 1084683, 1096257, 1085414, 1104965,
                    1048673, 1086567 ]
        self.good(selected_df, self.bet_type, simple_strat, goods)

        wrongs = [  1053493, 1071754, 1104696, 1072040, 1099183, 1077608, 1064617,
                    1084724, 1116020, 1072897, 1099339, 1071622, 1069459, 1104801,
                    1086901, 1065454, 1070386, 1071415, 1048698, 1111115, 1064547,
                    1104679, 1106908, 1072040, 1086093, 1074598, 1104931, 1070386,
                    1086093, 1116020 ]
        self.wrong(selected_df, self.bet_type, simple_strat, wrongs)

        
class TestSimplePlace(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "simple_place"

    def test_basics(self, selected_df, simple_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, simple_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


    # def test_bet_consistancy_1(self, selected_df, simple_strat) : 
    #     """bet results 'bet horses' """

    #     bet = Bet(self.bet_type, simple_strat)
    #     _df = bet.run(selected_df.copy())

    #     for _ in range(10) : # run 10 times 
    #         while True : 
    #             race_0   = _df.iloc[np.random.choice(_df.index), :] # pick a random race
    #             result_0 = race_0.results.sort_values("cotedirect", ascending=True, axis=0)
    #             try : 
    #                 if (result_0.cotedirect.iloc[0] > 0.0 ) and (result_0.cotedirect.iloc[0] < 10.0 ) : # be sure prob !=0
    #                     break
    #             except : # if error just pass it 
    #                 pass

    #         assert race_0.bet_horse == result_0.numero.iloc[0] 


    def test_bet_results(self, selected_df, simple_strat) :
        """test if global good_bet rate is consistant"""

        # self.rate(selected_df, self.bet_type, simple_strat, 0.25)

        params = [
        #   comp        bet_horse   win_horses      good_bet    url
        [   1086803,    2,          [6, 16, 4],     False,      "https://www.paris-turf.com/programme-courses/2018-08-21/reunion-deauville/resultats-rapports/prix-de-la-barberie-1086803"],
        [   1101558,    16,         [13,1,12],      False,      "https://www.paris-turf.com/programme-courses/2018-10-16/reunion-chantilly/resultats-rapports/prix-d-orry-1101558"],    
        [   1115896,    7,          [17, 10, 7],    True,       "https://www.paris-turf.com/programme-courses/2019-01-18/reunion-cagnes-sur-mer/resultats-rapports/prix-charles-gastaud-1115896"], 
        [   1124061,    15,         [15, 11, 6],    True,       "https://www.paris-turf.com/programme-courses/2019-01-24/reunion-vincennes/resultats-rapports/prix-de-la-semaine-internationale-1124061"],    
                ]
        self.individuals(selected_df, self.bet_type, simple_strat, params)

        goods = [   1086541, 1077608, 1072071, 1085443, 1048614, 1084714, 1069172,
                    1086645, 1064461, 1104559, 1084714, 1095149, 1048470, 1073055,
                    1101268, 1086645, 1107118, 1101268, 1124432, 1124400, 1048470,
                    1104867, 1069172, 1068713, 1124149, 1107118, 1086567, 1064538,
                    1099401, 1074598 ]
        self.good(selected_df, self.bet_type, simple_strat, goods)

        wrongs = [  1088486, 1048658, 1113348, 1059769, 1076989, 1086486, 1123937,
                    1101678, 1058997, 1058974, 1104801, 1084848, 1074502, 1072949,
                    1071797, 1072040, 1124606, 1099313, 1071389, 1048453, 1104896,
                    1074660, 1084724, 1073103, 1104679, 1124410, 1071813, 1085999,
                    1113356, 1113356    ]
        self.wrong(selected_df, self.bet_type, simple_strat, wrongs)


    # def test_bet_individual(self, selected_df, simple_strat) : 

    #     bet = Bet("simple_place", simple_strat)
    #     _df = bet.run(selected_df.copy())


    #     for _comp, _bet_horse, _win_horses, _good_bet, _url in params : 
    #         sub_df = _df.loc[_df.comp == _comp, :]
    #         assert len(sub_df)          == 1
    #         assert sub_df.url.iloc[0]   == _url
            
    #         sub_df = sub_df.iloc[0]
    #         assert sub_df.bet_horse     == _bet_horse
    #         assert (sub_df.win_horses   == _win_horses).all()
    #         assert sub_df.good_bet      == _good_bet


class TestCoupleGagnant(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "couple_gagnant"
    
    def test_basics(self, selected_df, couple_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, couple_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)

    def test_bet_results(self, selected_df, couple_strat) :
        """test if global good_bet rate is consistant"""

        # self.rate(selected_df, "simple_place", couple_strat, 0.25)

        goods = [   1048427, 1048524, 1048568, 1048579, 1053457, 1064524, 1064538,
                    1067714, 1068191, 1068449, 1069402, 1071233, 1071295, 1073132,
                    1074464, 1077608, 1084396, 1084597, 1095242, 1095842, 1104124,
                    1104631, 1104733, 1104867, 1104947, 1106948, 1107726, 1109088,
                    1123999, 1124088, 1124619, 1124647 ]
        self.good(selected_df, self.bet_type, couple_strat, goods)

        wrongs = [  1104565, 1048720, 1084724, 1105039, 1069210, 1086567, 1068571,
                    1071389, 1085487, 1073002, 1069230, 1099313, 1071780, 1073032,
                    1074502, 1083092, 1071389, 1124181, 1071797, 1101732, 1104737,
                    1104559, 1048573, 1068093, 1113348, 1101558, 1068713, 1068093,
                    1074502, 1048680 ]
        self.wrong(selected_df, self.bet_type, couple_strat, wrongs)


class TestCoupleOrdre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "couple_ordre"

    def test_basics(self, selected_df, couple_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, couple_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


    def test_bet_results(self, selected_df, couple_strat) :
        """test if global good_bet rate is consistant"""

        # self.rate(selected_df, "simple_place", couple_strat, 0.25)

        goods = [  1042867, 1068191, 1104631, 1071295, 1104867, 1003334, 1107726,
                   1107726, 1003149, 1048579, 1003300, 1003300, 1048579, 1003091,
                   1095242, 1071233, 1048579, 1124647, 1003149, 1032444, 1029599,
                   1003334, 1023485, 1124619, 1003149, 1095242, 1124088, 1104733,
                   1003091, 1069402  ]
        self.good(selected_df, self.bet_type, couple_strat, goods)

        wrongs = [  1003100, 1099183, 1048353, 1069230, 1084419, 1053499, 1085584,
                    1088213, 1048587, 1116165, 1029744, 1069275, 1124149, 1048012,
                    1030176, 1075620, 1084404, 1104938, 1017959, 1023075, 1003225,
                    1019381, 1064461, 1022597, 1023852, 1018481, 1083102, 1087008,
                    1048614, 1106602    ]
        self.wrong(selected_df, self.bet_type, couple_strat, wrongs)

       

class TestCouplePlace(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "couple_place"
    
    def test_basics(self, selected_df, couple_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, couple_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)



class TestDeuxSurQuatre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "deux_sur_quatre"

    def test_basics(self, selected_df, couple_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, couple_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


class TestTrioOrdre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "trio_ordre"

    def test_basics(self, selected_df, trio_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, trio_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


class TestTrioDesordre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "trio_desordre"

    def test_basics(self, selected_df, trio_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, trio_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


class TestTierceOrdre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "tierce_ordre"

    def test_basics(self, selected_df, trio_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, trio_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


class TestTierceDesordre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "tierce_desordre"

    def test_basics(self, selected_df, trio_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, trio_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


class TestQuinteOrdre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "quinte_ordre"

    def test_basics(self, selected_df, quinte_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, quinte_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


class TestQuinteDesordre(TestGeneric) : 
    """test class for simple places bets"""

    bet_type = "quinte_desordre"

    def test_basics(self, selected_df, quinte_strat) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, quinte_strat)
        cols = ['bet_horses', 'win_horses', 'bet_or_not', 'cote', 'good_bet']
        self.columns(_df, cols)


    def test_bet_results(self, selected_df, quinte_strat) :

        goods = [   1003385, 1016312, 1017959, 1020195, 1032311, 1064461, 1071483,
                    1085414, 1104605]
        self.good(selected_df, self.bet_type, quinte_strat, goods)

        wrongs = [  1070469, 1003362, 1040226, 1071797, 1019434, 1048045, 1048513,
                    1047986, 1033716, 1115942, 1032246, 1065454, 1009550, 1048643,
                    1124400, 1064502, 1029992, 1041779, 1047837, 1064547, 1059111,
                    1032342, 1101558, 1003124, 1077286, 1023195, 1104905, 1023730,
                    1048579, 1064570]
        self.wrong(selected_df, self.bet_type, quinte_strat, wrongs)





