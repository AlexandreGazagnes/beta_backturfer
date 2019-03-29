#!/usr/bin/env python3
# coding: utf-8


# import 
# from backturfer.misc import *
from backturfer.misc import change_repr
from backturfer.strats.multi   import MultiStrats
# from numpy.random import randint, choice


# class
class CoupleStrats(MultiStrats) : 

    _type       = "strats"
    _subtype    = "couple"


    @change_repr
    def choix_des_2_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des_N__meilleures_cotes(results, 0, 2, cote_type)


    @change_repr
    def choix_aleatoire_2_inscrits(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 2, cote_type)


    @change_repr
    def choix_aleatoire_2_partants(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        raise NotImplementedError("not NotImplementedError")


    @change_repr
    def choix_aleatoire_2_parmi_les__N__meilleures_cotes(results, N=5, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, 2, cote_type)


    @change_repr
    def choix_aleatoire_2_parmi_les_3_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 3, 2, cote_type)



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


    # @change_repr
    # def choix_aleatoire_parmi_les_inscrits(results, N=None, n=1, cote_type="direct") : 
    #     """chose one horse random"""

    #     r = choice(results.numero, size=numb, replace=False)
    #     if len(r) == 1 : 
    #         r = r[0]

    #     return r

    # @change_repr
    # def choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, n=1, cote_type="direct") : 
    #     """chose one horse random given the N best cotes"""

    #     if not isinstance(N, int) : 
    #         raise ValueError("N should be an int")

    #     if  N == 0 : 
    # #         return -1

    # #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)
    # #     best_N_cotedirect = r.numero.iloc[:N].values

    # #     r = choice(best_N_cotedirect, size=n, replace=False)
    # #     if len(r) == 1 : 
    # #         r = r[0]

    # #     return r

    # @change_repr
    # def choix_de_la__N__meilleure_cote(results, N, n=1, cote_type="direct") : 
    #     """chose the horse with nth best cote"""
        
    #     if not isinstance(N, int) : 
    #         raise ValueError("N should be an int")

    #     if N >= len(results) : 
    #         info("N sup >= nb chevaux")
    #         return -1

    #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

    #     if n==1 : 
    #         return r.numero.iloc[N]
    #     elif n > 1 and n <7 : 
    #         return list(r.numero.iloc[N:n+N])


    # @change_repr
    # def choix_des_2_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""

    #     return CoupleStrats.choix_de_la__N__meilleure_cote(results, 0, 2, cote_type)



