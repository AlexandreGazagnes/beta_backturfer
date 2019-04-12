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


    strats_str  = { 
    'choix_de_la_meilleure_cote' : 'choix de la meilleure cote',
    'choix_de_la_2_meilleure_cote' : 'choix de la 2ème meilleure cote',
    'choix_de_la_3_meilleure_cote' : 'choix de la 3ème meilleure cote',
    'choix_de_la__N__meilleure_cote' : 'choix de la -N-ème meilleure_cote',

    'choix_de_la_pire_cote_inscrite' : 'choix de la pire cote inscrite',
    'choix_de_la_pire_cote_partante' : 'choix de la pire cote partante',
    'choix_de_la_2_pire_cote_inscrite' : 'choix de la 2ème pire cote inscrite',
    'choix_de_la_2_pire_cote_partante' : 'choix de la 2ème pire cote partante',
    'choix_de_la_3_pire_cote_inscrite' : 'choix de la 3ème pire cote inscrite',
    'choix_de_la_3_pire_cote_partante' : 'choix de la 3ème pire cote partante',
    'choix_de_la__N__pire_cote_inscrite' : 'choix de la -N-ème pire cote inscrite',
    'choix_de_la__N__pire_cote_partante' : 'choix de la -N-ème pire cote partante',
    
    'choix_aleatoire_un_inscrit' : 'choix aléatoire parmi les inscrits',
    'choix_aleatoire_un_partant' : 'choix aléatoire parmi les partants',
    'choix_aleatoire_entre_les__N__et__M__meilleures_cotes' : 'choix aléatoire entre les -N-ème et -M-ème meilleures cotes',
    'choix_aleatoire_entre_les__N__et__M__pires_cotes_inscrites' : 'choix aléatoire entre les -N-ème et -M-ème pires cotes inscrites',
    'choix_aleatoire_entre_les__N__et__M__pires_cotes_partantes' : 'choix aléatoire entre les -N-ème et -M-ème pires cotes partantes',
    
    'choix_aleatoire_parmi_les_3_meilleures_cotes' : 'choix aléatoire parmi les 3 meilleures cotes',
    'choix_aleatoire_parmi_les_5_meilleures_cotes' : 'choix aléatoire parmi les 5 meilleures cotes',
    'choix_aleatoire_parmi_les__N__meilleures_cotes' : 'choix aléatoire parmi les -N- meilleures cotes',

    'choix_aleatoire_parmi_les_3_pires_cotes_inscrites' : 'choix aléatoire parmi les 3 pires cotes inscrites',
    'choix_aleatoire_parmi_les_3_pires_cotes_partantes' : 'choix aléatoire parmi les 3 pires cotes partantes',
    'choix_aleatoire_parmi_les_5_pires_cotes_inscrites' : 'choix aléatoire parmi les 5 pires cotes inscrites',
    'choix_aleatoire_parmi_les_5_pires_cotes_partantes' : 'choix aléatoire parmi les 5 pires cotes partantes',
    'choix_aleatoire_parmi_les__N__pires_cotes_inscrites' : 'choix aléatoire parmi les -N- pires cotes inscrites',
    'choix_aleatoire_parmi_les__N__pires_cotes_partantes' : 'choix aléatoire parmi les -N- pires cotes partantes',
                }


    # CHOIX PRECIS - MEILLEURS
    # -------------------------------------

    @change_repr
    def choix_de_la_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, 0, 1, cote_type)

    @change_repr
    def choix_de_la_2_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with 2nd best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, 1, 1, cote_type)

    @change_repr
    def choix_de_la_3_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with 3rd best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, 2, 1, cote_type)

    @change_repr
    def choix_de_la__N__meilleure_cote(results, N, n=None, cote_type="direct") : 
        """chose the horse with N best cote"""
        return MultiStrats.choix_des__N__meilleures_cotes(results, N-1, 1, cote_type)


    # CHOIX PRECIS - PIRES
    # -------------------------------------

    @change_repr
    def choix_de_la_pire_cote_inscrite(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, 0, 1, cote_type)

    @change_repr
    def choix_de_la_pire_cote_partante(results, N=None, n=None, cote_type="direct"):
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_de_la_2_pire_cote_inscrite(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 2st worst cote / 2nd last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, 1, 1, cote_type)

    @change_repr
    def choix_de_la_2_pire_cote_partante(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_de_la_3_pire_cote_inscrite(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, 2, 1, cote_type)

    @change_repr
    def choix_de_la_3_pire_cote_partante(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_de_la__N__pire_cote_inscrite(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
        return MultiStrats.choix_des__N__pires_cotes_inscrites(results, N-1, 1, cote_type)

    @change_repr
    def choix_de_la__N__pire_cote_partante(results, N=None, n=None, cote_type="direct") :
        """chose the horse with 1st worst cote / last best cote"""
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

    @change_repr
    def choix_aleatoire_entre_les__N__et__M__pires_cotes_inscrites(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_entre_les__N__et__M__pires_cotes_partantes(results, N, M, n=None, cote_type="direct") : 
        raise NotImplementedError("NotImplementedError")


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

    @change_repr
    def choix_aleatoire_parmi_les__N__pires_cotes_inscrites(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")

    @change_repr
    def choix_aleatoire_parmi_les__N__pires_cotes_partantes(results, N=None, n=None, cote_type="direct") : 
        return NotImplementedError("NotImplementedError")




