#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc import *
from numpy.random import randint, choice

# class
class MultiStrats : 

    _type       = "strats"
    _subtype    = "multi"


    @change_repr
    def choix_de_la__N__meilleure_cote(results, N, n, cote_type="direct") : 
        """chose the horse with nth best cote"""
        
        if not isinstance(N, int) : 
            raise ValueError("N should be an int")

        if not isinstance(n, int) : 
            raise ValueError("N should be an int")
  
        if N >= len(results) : 
            warning(f"N sup >= nb chevaux : {N} >= {len(results)}")
            input()
            return -1

        if (n >5) or(n<1) : 
            warning(f"invalid n : {n}")
            input()
            return -1


        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

        if n==1             : return r.numero.iloc[N]
        elif n > 1 and n <6 : return list(r.numero.iloc[N:n+N])
        else                : raise ValueError("choix_de_la__N__meilleure_cote")



    @change_repr
    def choix_de_la_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_de_la__N__meilleure_cote(results, 0, 1, cote_type)


    @change_repr
    def choix_des_2_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_de_la__N__meilleure_cote(results, 0, 2, cote_type)

    @change_repr
    def choix_des_3_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""
        return MultiStrats.choix_de_la__N__meilleure_cote(results, 0, 3, cote_type)


    @change_repr
    def choix_des_5_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
        """chose the horse with best cote"""

        return MultiStrats.choix_de_la__N__meilleure_cote(results, 0, 5, cote_type)



    # __strat_types = ["choix_de_la__N__meilleure_cote", ]
    # __cote_types = ["direct", "prob"]
 

    # def __init__(self, strat_type, N=0, n=1, cote_type="direct") : 

    #     assert isinstance(N, int)
    #     assert isinstance(n, int)
    #     assert cote_type in self.__cote_types
    #     if not strat_type == "choix_de_la__N__meilleure_cote" :
    #         raise NotImplentedError("please be patient young padawan....")

    #     self.strat_type = strat_type
    #     self.N = N
    #     self.n = n
    #     self.Class = f"MultiStrats.{self.strat_type}"

    # def __call__(self, results, N, n) : 

    #     if self.strat_type == "choix_de_la__N__meilleure_cote" : 
    #         if N >= len(results) : 
    #             info("N sup >= nb chevaux")
    #             return -1

    #         r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

    #         return r.numero.iloc[N]


    # def __repr__(self) : 
    #     return f"MultiStrats.{self.strat_type}"


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

