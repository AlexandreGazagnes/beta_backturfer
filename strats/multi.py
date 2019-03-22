#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc import *
from numpy.random import randint, choice

# class
class MultiStrats : 

    __strat_types = ["choix_de_la__N__meilleure_cote", ]
    __cote_types = ["direct", "prob"]
 
    _type       = "strats"
    _subtype    = "multi"


    def __init__(self, strat_type, N=0, n=1, cote_type="direct") : 

        assert isinstance(N, int)
        assert isinstance(n, int)
        assert cote_type in self.__cote_types
        if not strat_type == "choix_de_la__N__meilleure_cote" :
            raise NotImplentedError("please be patient young padawan....")

        self.strat_type = strat_type
        self.N = N
        self.n = n
        self.Class = f"MultiStrats.{self.strat_type}"

    def __call__(self, results) : 

        if self.strat_type == "choix_de_la__N__meilleure_cote" : 
            if N >= len(results) : 
                info("N sup >= nb chevaux")
                return -1

            r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

            return r.numero.iloc[N]


    def __repr__(self) : 
        return f"MultiStrats.{self.strat_type}"




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


