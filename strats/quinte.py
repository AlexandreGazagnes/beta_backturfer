#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc import *
from numpy.random import randint, choice



# class
class QuinteStrats : 

    _type       = "strats"
    _subtype    = "quinte"

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
    def choix_de_la__N__meilleure_cote(results, N, n=1, cote_type="direct") : 
        """chose the horse with nth best cote"""
        
        if not isinstance(N, int) : 
            raise ValueError("N should be an int")

        if N >= len(results) : 
            info("N sup >= nb chevaux")
            return -1

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

        if n==1 : 
            return r.numero.iloc[N]
        elif n > 1 and n <7 : 
            return list(r.numero.iloc[N:n+N])


    @change_repr
    def choix_des_5_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""

        return QuinteStrats.choix_de_la__N__meilleure_cote(results, 0, 5, cote_type)



