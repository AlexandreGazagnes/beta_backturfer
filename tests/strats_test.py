#!/usr/bin/env python3
# coding: utf-8


import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from tests.generic import *






class TestSimpleStratsGagnant(TestGeneric) : 
    """test class for simple gagnants bets"""

    bet_type  = "simple_gagnant"

    def test_choix_de_la_meilleure_cote(self, selected_df) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_de_la_meilleure_cote)

    def test_choix_aleatoire_un_inscrit(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_un_inscrit)

    # def test_choix_aleatoire_un_partant(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_un_partant)

    def test_choix_aleatoire_parmi_les_3_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_parmi_les_3_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)


class TestSimpleStratsPlace(TestGeneric) : 
    """test class for simple gagnants bets"""

    bet_type  = "simple_place"

    def test_choix_de_la_meilleure_cote(self, selected_df) : 
        """just Bet.run() and various features"""
        
        _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_de_la_meilleure_cote)

    def test_choix_aleatoire_un_inscrit(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_un_inscrit)

    # def test_choix_aleatoire_un_partant(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_un_partant)

    def test_choix_aleatoire_parmi_les_3_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_parmi_les_3_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)





class TestCoupleStratsOrdre(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "couple_ordre"

    def test_choix_des_2_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_des_2_meilleures_cotes)

    def test_choix_aleatoire_2_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_inscrits)

    # def test_choix_aleatoire_2_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_un_partant)

    def test_choix_aleatoire_2_parmi_les_3_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_parmi_les_3_meilleures_cotes)

    # def test_choix_aleatoire_2_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_parmi_les__N__meilleures_cotes)



class TestCoupleStratsGagnant(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "couple_gagnant"

    def test_choix_des_2_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_des_2_meilleures_cotes)

    def test_choix_aleatoire_2_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_inscrits)

    # def test_choix_aleatoire_2_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_un_partant)

    def test_choix_aleatoire_2_parmi_les_3_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_parmi_les_3_meilleures_cotes)

    # def test_choix_aleatoire_2_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_parmi_les__N__meilleures_cotes)



class TestCoupleStratsPlace(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "couple_place"

    def test_choix_des_2_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_des_2_meilleures_cotes)

    def test_choix_aleatoire_2_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_inscrits)

    # def test_choix_aleatoire_2_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_un_partant)

    def test_choix_aleatoire_2_parmi_les_3_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_parmi_les_3_meilleures_cotes)

    # def test_choix_aleatoire_2_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, CoupleStrats.choix_aleatoire_2_parmi_les__N__meilleures_cotes)



class TestTrioStratsOrdre(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "trio_ordre"

    def test_choix_des_3_meilleures_cotes(self, selected_df) : 
        """just Bet.run() and various features"""
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_des_3_meilleures_cotes)

    def test_choix_aleatoire_3_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_inscrits)

    # def test_choix_aleatoire_3_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_partants)

    def test_choix_aleatoire_3_parmi_les_5_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_parmi_les_5_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)


class TestTrioStratsDesordre(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "trio_desordre"

    def test_choix_des_3_meilleures_cotes(self, selected_df) : 
        """just Bet.run() and various features"""
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_des_3_meilleures_cotes)

    def test_choix_aleatoire_3_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_inscrits)

    # def test_choix_aleatoire_3_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_partants)

    def test_choix_aleatoire_3_parmi_les_5_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_parmi_les_5_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)


class TestTierceStratsOrdre(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "tierce_ordre"

    def test_choix_des_3_meilleures_cotes(self, selected_df) : 
        """just Bet.run() and various features"""
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_des_3_meilleures_cotes)

    def test_choix_aleatoire_3_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_inscrits)

    # def test_choix_aleatoire_3_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_partants)

    def test_choix_aleatoire_3_parmi_les_5_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_parmi_les_5_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)


class TestTierceStratsDesordre(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "tierce_desordre"

    def test_choix_des_3_meilleures_cotes(self, selected_df) : 
        """just Bet.run() and various features"""
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_des_3_meilleures_cotes)

    def test_choix_aleatoire_3_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_inscrits)

    # def test_choix_aleatoire_3_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_partants)

    def test_choix_aleatoire_3_parmi_les_5_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_3_parmi_les_5_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, TrioStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)


class TestQuinteStratsOrdre(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "quinte_ordre"

    def test_choix_des_5_meilleures_cotes(self, selected_df) : 
        """just Bet.run() and various features"""
        _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_des_5_meilleures_cotes)

    def test_choix_aleatoire_5_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_5_inscrits)

    # def test_choix_aleatoire_5_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_5_partants)

    def test_choix_aleatoire_5_parmi_les_7_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_5_parmi_les_7_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)


class TestQuinteStratsDesordre(TestGeneric) : 
    """test class for simple gagnants bets"""
    
    bet_type = "quinte_desordre"

    def test_choix_des_5_meilleures_cotes(self, selected_df) : 
        """just Bet.run() and various features"""
        _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_des_5_meilleures_cotes)

    def test_choix_aleatoire_5_inscrits(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_5_inscrits)

    # def test_choix_aleatoire_5_partants(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_5_partants)

    def test_choix_aleatoire_5_parmi_les_7_meilleures_cotes(self, selected_df) : 
        _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_5_parmi_les_7_meilleures_cotes)

    # def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
    #     _df = self.run(selected_df, self.bet_type, QuinteStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)









# class TestQuinteStrats(TestGeneric) : 
#     """test class for simple gagnants bets"""
    
#     bet_type = "simple_gagnant"

#     def test_choix_de_la_meilleure_cote(self, selected_df) : 
#         """just Bet.run() and various features"""
        
#         _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_de_la_meilleure_cote)

#     def test_choix_aleatoire_un_inscrit(self, selected_df) : 
#         _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_un_inscrit)

#     def test_choix_aleatoire_un_partant(self, selected_df) : 
#        # _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_un_partant)
#        pass

#     def test_choix_aleatoire_parmi_les_3_meilleures_cotes(self, selected_df) : 
#         _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_parmi_les_3_meilleures_cotes)

#     def test_choix_aleatoire_parmi_les__N__meilleures_cotes(self, selected_df) : 
#         _df = self.run(selected_df, self.bet_type, SimpleStrats.choix_aleatoire_parmi_les__N__meilleures_cotes)





