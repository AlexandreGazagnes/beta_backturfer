#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc import *
from numpy.random import randint, choice



# class
class CoupleStrats : 

    _type       = "strats"
    _subtype    = "couple"

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
    def choix_aleatoire_parmi_les_inscrits(results, N=None, numb=1, cote_type="direct") : 
        """chose one horse random"""

        r = choice(results.numero, size=numb, replace=False)
        if len(r) == 1 : 
            r = r[0]

        return r