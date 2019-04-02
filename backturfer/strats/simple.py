#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc import change_repr
from backturfer.strats.multi   import MultiStrats
# from numpy.random import randint, choice


# class
class SimpleStrats(MultiStrats) : 

    _type       = "strats"
    _subtype    = "simple"


    strats_str  = { 'choix_de_la_meilleure_cote'      : 'choix de la meilleure cote',
                    'choix_aleatoire_un_inscrit'  : 'choix aleatoire un inscrit',
                    'choix_aleatoire_un_partant'  : 'choix aleatoire un partant',  
                    'choix_aleatoire_parmi_les__N__meilleures_cotes' : 'choix alétoire parmi les N meilleures cotes', 
                    'choix_aleatoire_parmi_les_3_meilleures_cotes': 'choix_aleatoire_parmi_les_3_meilleures_cotes',
                    'choix_aleatoire_parmi_les_5_meilleures_cotes' : 'choix_aleatoire_parmi_les_5_meilleures_cotes' }


    # CHOIX PRECIS - MEILLEURS
    # -------------------------------------

    @change_repr
    def choix_de_la_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, 0, 1, cote_type)

    @change_repr
    def choix_de_la_2_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, 1, 1, cote_type)

    @change_repr
    def choix_de_la_3_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, 2, 1, cote_type)

    @change_repr
    def choix_de_la__N__meilleure_cote(results, N, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, N-1, 1, cote_type)


    # CHOIX PRECIS - PIRES
    # -------------------------------------

    @change_repr
    def choix_de_la_pire_cote_inscrite(results, N=None, n=None, cote_type="direct"):

        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_de_la_pire_cote_partante(results, N=None, n=None, cote_type="direct"):

        raise NotImplementedError("NotImplementedError")


    # CHOIX ALEATOIRE PUR
    # -------------------------------------

    @change_repr
    def choix_aleatoire_un_inscrit(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 1, cote_type)


    @change_repr
    def choix_aleatoire_un_partant(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        raise NotImplementedError("not NotImplementedError")

    @change_repr
    def choix_aleatoire_entre_les__N__et__M__meilleures_cotes(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("not NotImplementedError")


    # CHOIX ALEATOIRE VS COTES - MEILLEURS
    # -------------------------------------

    @change_repr
    def choix_aleatoire_parmi_les_3_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 3, 1, cote_type)


    @change_repr
    def choix_aleatoire_parmi_les_5_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, 5, 1, cote_type)


    @change_repr
    def choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, n=None, cote_type="direct") : 
        """chose the horse with best cote"""   
        return MultiStrats.choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, 1, cote_type)



    # CHOIX ALEATOIRE VS COTES - PIRES
    # -------------------------------------

    @change_repr
    def choix_aleatoire_parmi_les_3_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_parmi_les_3_pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_parmi_les_5_pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_parmi_les_5_pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

