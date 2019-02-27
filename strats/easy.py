#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import *
from numpy.random import randint, choice


# class
class Strats : 

    @change_repr
    def random_choice(results, N=None, cote_type="direct") : 
        """chose one horse random"""

        if not isinstance(N, int) : 
            raise ValueError("N should be an int")

        return choice(results.numero)

    @change_repr
    def random_1_on_n_best_winning_cote(results, N, cote_type="direct") : 
        """chose one horse random given the N best cotes"""

        if not isinstance(N, int) : 
            raise ValueError("N should be an int")

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)
        best_N_cotedirect = r.numero.iloc[:N].values

        return choice(best_N_cotedirect)


    @change_repr
    def random_1_on_3_best_winning_cote(results, N=None, cote_type="direct") : 
        """chose one horse random given the 3 best cotes"""

        return Strats.random_1_on_n_best_winning_cote(results, 3, cote_type)


    @change_repr
    def random_1_btwn_n_and_m_best_winning_cote(results, n ,m, cote_type="direct") : 
        """chose one horse random between the n+1 and the m+1 rank of best cotes"""

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)
        best_n_m_cotedirect = r.numero.iloc[n:m].values

        return choice(best_n_m_cotedirect)


    @change_repr
    def n_winning_cote(results, N, cote_type="direct") : 
        """chose the horse with nth best cote"""
        
        if not isinstance(N, int) : 
            raise ValueError("N should be an int")

        if N >= len(results) : 
            info("N sup >= nb chevaux")
            return -1

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

        return r.numero.iloc[N]


    @change_repr
    def best_winning_cotes(results, N=None, cote_type="direct") : 
        """chose the horse with best cote"""

        return Strats.n_winning_cote(results, 0, cote_type)


    @change_repr
    def never_bet(results, N=None) : 
        """just go to the hippo, no bets, just enjoy races and stalk beautiful ladies"""

        return -1


    @change_repr
    def random_bet_or_not_best_winning_cote(results, N=None, cote_type="direct") : 
        """go to the hippo, flip a coin and 1/2 decide to bet or not, if bet, use best_cote_strategy"""

        n = randint(0, 2)
        if n : return Strats.best_winning_cote(results, cote_type=cote_type)
        else : return -1


    @change_repr
    def worst_cote(results, N=None, cote_type="direct") : 
        """chose the horse with best cote)"""

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

        return r.numero.iloc[-1]


