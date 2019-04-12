#!/usr/bin/env python3
# coding: utf-8


# import 
# from backturfer.misc import *
# from numpy.random import randint, choice
from backturfer.misc import change_repr
from backturfer.strats.multi   import MultiStrats



# class
class QuinteStrats(MultiStrats)  : 

    _type       = "strats"
    _subtype    = "quinte"

    strats_str = {  
        'choix_des_5_meilleures_cotes' : 'choix des 5 meilleures_cotes', 
        'choix_des_2_a_6_meilleures_cotes' : 'choix des 2ème à 6ème meilleures_cotes',
        'choix_des_3_a_7_meilleures_cotes' : 'choix des 3ème à 7ème meilleures_cotes',
        'choix_des__N__a__Np5__meilleures_cotes' : 'choix des -N-ème à -Np5-ème meilleures_cotes',

        'choix_des_5_pires_cotes_inscrites' : 'choix_des 5 pires cotes inscrites', 
        'choix_des_5_pires_cotes_partantes' : 'choix_des 5 pires cotes partantes',
        'choix_des_2_a_6_pires_cotes_inscrites' : 'choix des 2ème à 6ème pires cotes inscrites',
        'choix_des_2_a_6_pires_cotes_partantes' : 'choix des 2ème à 6ème pires cotes partantes',
        'choix_des__N__a__Np5__pires_cotes_inscrites' : 'choix des -N-ème à -Np5-ème pires cotes inscrites',
        'choix_des__N__a__Np5__pires_cotes_partantes' : 'choix des -N-ème à -Np5-ème pires cotes partantes',

        'choix_aleatoire_5_inscrits' :'choix aléatoire 5 inscrits',
        'choix_aleatoire_5_partants' : 'choix aléatoire 5 partants',
        'choix_aleatoire_5_entre_les__N__et__M__meilleures_cotes' : 'choix aléatoire 5 entre les -N-ème et -M-ème meilleures_cotes', 
        'choix_aleatoire_5_entre_les__N__et__M__pires_cotes_inscrites' : 'choix aléatoire 5 entre les -N-ème et -M-ème pires cotes inscrites',
        'choix_aleatoire_5_entre_les__N__et__M__pires_cotes_partantes' : 'choix aléatoire 5 entre les -N-ème et -M-ème pires cotes partantes',

        'choix_aleatoire_5_parmi_les_7_meilleures_cotes' : 'choix aléatoire 5 parmi les 7 meilleures cotes',
        'choix_aleatoire_5_parmi_les_10_meilleures_cotes' : 'choix aléatoire 5 parmi les 10 meilleures cotes',
        'choix_aleatoire_5_parmi_les__N__meilleures_cotes' : 'choix aléatoire 5 parmi les -N-ème meilleures cotes',

        'choix_aleatoire_5_parmi_les_7_pires_cotes_inscrites' : 'choix aléatoire 5 parmi les 7 pires cotes inscrites',
        'choix_aleatoire_5_parmi_les_7_pires_cotes_partantes' : 'choix aléatoire 5 parmi les 7 pires cotes partantes',
        'choix_aleatoire_5_parmi_les_10_pires_cotes_inscrites' : 'choix aléatoire 5 parmi les 10 pires cotes inscrites',
        'choix_aleatoire_5_parmi_les_10_pires_cotes_partantes' : 'choix aléatoire 5 parmi les 10 pires cotes partantes',
        'choix_aleatoire_5_parmi_les__N__pires_cotes_inscrites' : 'choix aléatoire 5 parmi les -N- pires cotes inscrites',
        'choix_aleatoire_5_parmi_les__N__pires_cotes_partantes' : 'choix aléatoire 5 parmi les -N- pires cotes partantes',
                }


    # CHOIX PRECIS - MEILLEURS
    # -------------------------------------

    @change_repr
    def choix_des_5_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des_N__meilleures_cotes(results, 0, 5, cote_type)

    @change_repr
    def choix_des_2_a_6_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        return MultiStrats.choix_des_N__meilleures_cotes(results, 1, 5, cote_type)

    @change_repr
    def choix_des_3_a_7_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        return MultiStrats.choix_des_N__meilleures_cotes(results, 2, 5, cote_type)

    @change_repr
    def choix_des__N__a__Np5__meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        return MultiStrats.choix_des_N__meilleures_cotes(results, N-1, 5, cote_type)


    # CHOIX PRECIS - PIRES
    # -------------------------------------

    @change_repr
    def choix_des_5_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, 0, 5, cote_type)

    @change_repr
    def choix_des_5_pires_cotes_partantes(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_des_2_a_6_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, 1, 5, cote_type)

    @change_repr
    def choix_des_2_a_6_pires_cotes_partantes(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_des__N__a__Np5__pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, N-1, 5, cote_type)

    @change_repr
    def choix_des__N__a__Np5__pires_cotes_partantes(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")


    # CHOIX ALEATOIRE PUR
    # -------------------------------------

    @change_repr
    def choix_aleatoire_5_inscrits(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 5, cote_type)

    @change_repr
    def choix_aleatoire_5_partants(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        raise NotImplementedError("not NotImplementedError")

    @change_repr
    def choix_aleatoire_5_entre_les__N__et__M__meilleures_cotes(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("not NotImplementedError")

    @change_repr
    def choix_aleatoire_5_entre_les__N__et__M__pires_cotes_inscrites(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_5_entre_les__N__et__M__pires_cotes_partantes(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("NotImplementedError")


    # CHOIX ALEATOIRE VS COTES - MEILLEURS
    # -------------------------------------

    @change_repr
    def choix_aleatoire_5_parmi_les_7_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 7, 5, cote_type)

    @change_repr
    def choix_aleatoire_5_parmi_les_10_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 10, 5, cote_type)

    @change_repr
    def choix_aleatoire_5_parmi_les__N__meilleures_cotes(results, N, n=None, cote_type="direct") : 
        """chose the horse with best cote"""  
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, N-1, 5, cote_type)


    # CHOIX ALEATOIRE VS COTES - PIRES
    # -------------------------------------

    @change_repr
    def choix_aleatoire_5_parmi_les_7_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_5_parmi_les_7_pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_5_parmi_les_10_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_5_parmi_les_10_pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_5_parmi_les__N__pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_5_parmi_les__N__pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")



