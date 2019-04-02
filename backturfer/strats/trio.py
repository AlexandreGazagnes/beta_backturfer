#!/usr/bin/env python3
# coding: utf-8


# import 
# from backturfer.misc import *
from backturfer.misc import change_repr
from backturfer.strats.multi   import MultiStrats
# from numpy.random import randint, choice


# class
class TrioStrats(MultiStrats) : 

    _type       = "strats"
    _subtype    = "trio"

    strats_str = {  
        'choix_des_3_meilleures_cotes' : 'choix des 3 meilleures_cotes', 
        'choix_des_2_et_3_et_4_meilleures_cotes' : 'choix des 2ème 3ème et 4ème meilleures_cotes',
        'choix_des_3_et_4_et_5_meilleures_cotes' : 'choix des 3ème 4ème et 5ème meilleures_cotes',
        'choix_des__N__et__Np1__et__Np2__meilleures_cotes' : 'choix des -N-ème -Np1-ème et -Np2-ème meilleures_cotes',

        'choix_des_3_pires_cotes_inscrites' : 'choix_des 3 pires cotes inscrites', 
        'choix_des_3_pires_cotes_partantes' : 'choix_des 3 pires cotes partantes',
        'choix_des_2_et_3_et_4_pires_cotes_inscrites' : 'choix des 2ème 3ème et 4ème pires cotes inscrites',
        'choix_des_2_et_3_et_4_pires_cotes_partantes' : 'choix des 2ème 3ème et 4ème pires cotes partantes',
        'choix_des__N__et__Np1__et__Np2__pires_cotes_inscrites' : 'choix des -N-ème -Np1-ème et -Np2-ème pires cotes inscrites',
        'choix_des__N__et__Np1__et__Np2__pires_cotes_inscrites' : 'choix des -N-ème -Np1-ème et -Np2-ème pires cotes partantes',

        'choix_aleatoire_3_inscrits' :'choix_aleatoire_3_inscrits',
        'choix_aleatoire_3_inscrits' : 'choix_aleatoire_3_partants',
        'choix_aleatoire_3_entre_les__N__et__M__meilleures_cotes' : 'choix aleatoire 3 entre les -N-ème et -M-ème meilleures_cotes', 
        'choix_aleatoire_3_entre_les__N__et__M__pires_cotes_inscrites' : 'choix aleatoire 3 entre les -N-ème et -M-ème pires cotes inscrites',
        'choix_aleatoire_3_entre_les__N__et__M__pires_cotes_partantes' : 'choix aleatoire 3 entre les -N-ème et -M-ème pires cotes partantes',

        'choix_aleatoire_3_parmi_les_5_meilleures_cotes' : 'choix aléatoire 3 parmi les 5 meilleures cotes',
        'choix_aleatoire_3_parmi_les_7_meilleures_cotes' : 'choix aléatoire 3 parmi les 7 meilleures cotes',
        'choix_aleatoire_3_parmi_les__N__meilleures_cotes' : 'choix aléatoire 3 parmi les -N-ème meilleures cotes',

        'choix_aleatoire_3_parmi_les_5_pires_cotes_inscrites' : 'choix aléatoire 3 parmi les 5 pires cotes inscrites',
        'choix_aleatoire_3_parmi_les_5_pires_cotes_partantes' : 'choix aléatoire 3 parmi les 5 pires cotes partantes',
        'choix_aleatoire_3_parmi_les_7_pires_cotes_inscrites' : 'choix aléatoire 3 parmi les 7 pires cotes inscrites',
        'choix_aleatoire_3_parmi_les_7_pires_cotes_partantes' : 'choix aléatoire 3 parmi les 7 pires cotes partantes',
        'choix_aleatoire_3_parmi_les__N__pires_cotes_inscrites' : 'choix aléatoire 3 parmi les -N- pires cotes inscrites',
        'choix_aleatoire_3_parmi_les__N__pires_cotes_partantes' : 'choix aléatoire 3 parmi les -N- pires cotes partantes',
                }


    # CHOIX PRECIS - MEILLEURS
    # -------------------------------------

    @change_repr
    def choix_des_3_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des_N__meilleures_cotes(results, 0, 3, cote_type)

    @change_repr
    def choix_des_2_et_3_et_4_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        return MultiStrats.choix_des_N__meilleures_cotes(results, 1, 3, cote_type)

    @change_repr
    def choix_des_3_et_4_et_5_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        return MultiStrats.choix_des_N__meilleures_cotes(results, 2, 3, cote_type)

    @change_repr
    def choix_des__N__et__Np1__et__Np2__meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        return MultiStrats.choix_des_N__meilleures_cotes(results, N-1, 3, cote_type)


    # CHOIX PRECIS - PIRES
    # -------------------------------------

    @change_repr
    def choix_des_3_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, 0, 3, cote_type)

    @change_repr
    def choix_des_3_pires_cotes_partantes(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_des_2_et_3_et_4_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, 1, 3, cote_type)

    @change_repr
    def choix_des_2_et_3_et_4_pires_cotes_partantes(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_des__N__et__Np1__et__Np2__pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, N-1, 3, cote_type)

    @change_repr
    def choix_des__N__et__Np1__pires_cotes_partantes(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")


    # CHOIX ALEATOIRE PUR
    # -------------------------------------

    @change_repr
    def choix_aleatoire_3_inscrits(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 3, cote_type)

    @change_repr
    def choix_aleatoire_3_partants(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        raise NotImplementedError("not NotImplementedError")

    @change_repr
    def choix_aleatoire_3_entre_les__N__et__M__meilleures_cotes(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("not NotImplementedError")

    @change_repr
    def choix_aleatoire_3_entre_les__N__et__M__pires_cotes_inscrites(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_3_entre_les__N__et__M__pires_cotes_partantes(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("NotImplementedError")


    # CHOIX ALEATOIRE VS COTES - MEILLEURS
    # -------------------------------------

    @change_repr
    def choix_aleatoire_3_parmi_les_5_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 5, 3, cote_type)

    @change_repr
    def choix_aleatoire_3_parmi_les_7_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 7, 3, cote_type)

    @change_repr
    def choix_aleatoire_3_parmi_les__N__meilleures_cotes(results, N, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, 3, cote_type)


    # CHOIX ALEATOIRE VS COTES - PIRES
    # -------------------------------------

    @change_repr
    def choix_aleatoire_3_parmi_les_5_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_3_parmi_les_5_pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_3_parmi_les_7_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_3_parmi_les_7_pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_3_parmi_les__N__pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_3_parmi_les__N__pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")



