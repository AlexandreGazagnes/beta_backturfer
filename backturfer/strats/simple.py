#!/usr/bin/env python3
# coding: utf-8


# import 
# from backturfer.misc import *
from backturfer.strats.multi   import MultiStrats
# from numpy.random import randint, choice


# class
class SimpleStrats(MultiStrats) : 

    _type       = "strats"
    _subtype    = "simple"

    # strats_str =[   ('choix_de_la_meilleure_cote', 'choix de la meilleure cote'),
    #                 ('choix_de_la__N__meilleure_cote', 'choix de la - N - meilleure cote'),
    #                 ('choix_aleatoire_parmi_les_inscrits', 'choix aléatoire parmi les inscrits'),
    #                 ('choix_aleatoire_parmi_les_partants', 'choix aléatoire parmi les partants'),
    #                 ('choix_aleatoire_parmi_les__N__meilleures_cotes',
    #                             'choix aleatoire parmi les - N - meilleures cotes'),
    #                 ('choix_aleatoire_parmi_les_3_meilleures_cotes',
    #                             'choix aleatoire parmi les 3 meilleures cotes'),
    #                 ('ne_jamais_parier', 'ne jamais parier'),
    #                 ('pile_ne_pas_jouer_face_jouer_la_meilleure_cote', 'pile ne pas jouer face jouer la meilleure cote'),
    #                 ("choisir_la_pire_cote_inscrite", "choisir la pire cote inscrite"),
    #                 ('choisir_la_pire_cote_partante', 'choisir la pire cote partante')]


    @change_repr
    def choix_de_la_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return self.choix_des_N__meilleures_cotes(results, 0, 1, cote_type)


    @change_repr
    def choix_aleatoire_un_inscrit(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return self.choix_aleatoire_parmi_les_inscrits(results, 0, 1, cote_type)


    @change_repr
    def choix_aleatoire_un_partant(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        raise NotImplementedError("not NotImplementedError")


    @change_repr
    def choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return self.choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, 1, cote_type)


    @change_repr
    def choix_aleatoire_parmi_les_3_meilleures_cotes(results, N,=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return self.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 3, 1, cote_type)




    # # @change_repr
    # # def choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, n=1, cote_type="direct") : 
    # #     """chose one horse random given the N best cotes"""

    # #     if not isinstance(N, int) : 
    # #         raise ValueError("N should be an int")

    # #     if  N == 0 : 
    # #         return -1

    # #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)
    # #     best_N_cotedirect = r.numero.iloc[:N].values

    # #     r = choice(best_N_cotedirect, size=n, replace=False)
    # #     if len(r) == 1 : 
    # #         r = r[0]

    # #     return r


    # # @change_repr
    # # def choix_aleatoire_parmi_les_3_meilleures_cotes(results, N=None, n=1, cote_type="direct") : 
    # #     """chose one horse random given the 3 best cotes"""

    # #     return SimpleStrats.choix_aleatoire_parmi_les__n__meilleures_cotes(results, 3, n, cote_type)


    # # # @change_repr
    # # # def random_1_btwn_n_and_m_best_winning_cote(results, n ,m, cote_type="direct") : 
    # # #     """chose one horse random between the n+1 and the m+1 rank of best cotes"""

    # # #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)
    # # #     best_n_m_cotedirect = r.numero.iloc[n:m].values

    # # #     return choice(best_n_m_cotedirect)


    # @change_repr
    # def choix_de_la__N__meilleure_cote(results, N, n=0, cote_type="direct") : 
    #     """chose the horse with nth best cote"""
        
    #     if not isinstance(N, int) : 
    #         raise ValueError("N should be an int")

    #     if N >= len(results) : 
    #         info("N sup >= nb chevaux")
    #         return -1

    #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

    #     return r.numero.iloc[N]


    # @change_repr
    # def choix_de_la_meilleure_cote(results, N=None, n=0, cote_type="direct") : 
    #     """chose the horse with best cote"""

    #     return SimpleStrats.choix_de_la__N__meilleure_cote(results, 0, n, cote_type)


    # @change_repr
    # def ne_jamais_parier(results, N=None) : 
    #     """just go to the hippo, no bets, just enjoy races and stalk beautiful ladies"""

    #     return -1


    # @change_repr
    # def pile_ne_pas_jouer_face_jouer_la_meilleure_cote(results, N=None, cote_type="direct") : 
    #     """go to the hippo, flip a coin and 1/2 decide to bet or not, if bet, use best_cote_strategy"""

    #     n = randint(0, 2)
    #     if n : return SimpleStrats.choix_de_la__N__meilleure_cote(results, 0, cote_type)
    #     else : return -1


    # @change_repr
    # def choisir_la_pire_cote_inscrite(results, N=None, cote_type="direct") : 
    #     """chose the horse with best cote)"""

    #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

    #     return r.numero.iloc[-1]


    # @change_repr
    # def choisir_la_pire_cote_partante(results, N=None, cote_type="direct") : 
    #     """chose the horse with best cote)"""

    #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

    #     raise NotImplementedError
