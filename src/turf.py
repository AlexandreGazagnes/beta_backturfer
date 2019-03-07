#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc       import *
from src.groupby    import GroupBy
from strats.easy    import Strats





class TurfingRoom : 
    """ """
    
    def __compute_delta(df) : 
        
        bank_init           = df.bet_init.sum()
        bank_final          = df.bet_final.sum()
        delta               = round((bank_final-bank_init) /(bank_init+0.0000001),4)

        return delta


    def __gains_and_loss(df, bet_value=1, verbose=True) : 

        df["bet_init"]      = bet_value * df.bet_or_not
        df["bet_results"]   = (df.bet_init * df.gains) - df.bet_init
        df["bet_final"]     = df.bet_init + df.bet_results
        # df["%_real_gains"]  = round( df.bet_results /df.bet_value, 4)

        # compute delta
        bank_init           = df.bet_init.sum()
        bank_final          = df.bet_final.sum()
        delta               = round((bank_final-bank_init) /(bank_init+0.0000001),4)

        if verbose : 
            warning(df["bet_results"].describe())
            warning(df["bet_results"].tail())
            warning(f"bank_init {bank_init}, final_bank {bank_final}, delta {delta*100}%")

        return df


    def once(df, bet_familly, strategy, N=None, bet_value=1, verbose=True) : 

        assert isinstance(df, pd.DataFrame)
        assert callable(bet_familly)
        assert bet_familly.Class == "Bet"
        assert callable(strategy)
        assert strategy.Class == "Strats"

        _df         = bet_familly(df, strategy, N, verbose)
        _df         = TurfingRoom.__gains_and_loss(df, bet_value, verbose)

        delta       = TurfingRoom.__compute_delta(df)

        bet_ratio   = round(100 * sum(df.good_bet)/len(df), 2) 

        if verbose :
            info(f"delta is {delta} %")
            info(f"bet_ratio is {bet_ratio}%")

        return delta, bet_ratio, _df


    def randomized(df, bet_familly, strategy, nb=30, N=None, bet_value=1, verbose=True) : 
        
        assert isinstance(df, pd.DataFrame)
        assert callable(bet_familly)
        assert bet_familly.Class == "Bet"
        assert callable(strategy)
        assert strategy.Class == "Strats"
        
        assert isinstance(nb, int)
        assert (nb>5 and nb<=100)

        deltas, bet_ratios = list(), list()
        for _ in range(nb) : 
            delta, bet_ratio, _ = TurfingRoom.once(df, bet_familly, strategy, N, bet_value, verbose)
            deltas.append(delta)
            bet_ratios.append(bet_ratio)

        deltas, bet_ratios = pd.Series(deltas), pd.Series(bet_ratios)

        if verbose : 
            info(deltas.describe())
            info(deltas.tail())
            info(deltasbet_ratios.describe())
            info(bet_ratios.tail())

        return deltas.describe(), bet_ratios.describe(), None 


