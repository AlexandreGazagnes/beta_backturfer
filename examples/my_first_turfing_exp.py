#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc           import * 
from src.turfing        import BetRoom, TurfingRoom
from strats.easy        import Strats


# funct
def main() : 

    # main dataframe
    df  = pk_load("ptu_cache_18_vince_only_1_cote_added_cotepodium", "data/")
    DF  = df.copy()
    print("Consider all races for 2018 at Vincennes hippodrome\n\n")


    # % of winning bet
    _df = BetRoom.winning(df, Strats.n_winning_cote, N=0, verbose=False)
    r   = _df.good_bet.value_counts(normalize=True)[1]
    print(f"if you try a 'winning' bet, only on the horse with best winning cote, you will win at {round(r*100, 2)}%") 

    _df = BetRoom.winning(df, Strats.n_winning_cote, N=1, verbose=False)
    r   = _df.good_bet.value_counts(normalize=True)[1]
    print(f"if you try a 'winning' bet, only on the horse with 2nd  winning cote, you will win at {round(r*100, 2)}%") 

    _df = BetRoom.winning(df, Strats.n_winning_cote, N=2, verbose=False)
    r   = _df.good_bet.value_counts(normalize=True)[1]
    print(f"if you try a 'winning' bet, only on the horse with 3rd  winning cote, you will win at {round(r*100, 2)}%") 


    print("\n\n*********************    B U T    *********************\n\n")


    # % of financial loose
    r = TurfingRoom.once(df, BetRoom.winning, Strats.n_winning_cote, N=0, bet_value=1, verbose=False)
    print(f"if you try a 'winning' bet, only on the horse with best winning cote, you will loose only {round(r*100, 2)}%") 

    r = TurfingRoom.once(df, BetRoom.winning, Strats.n_winning_cote, N=1, bet_value=1, verbose=False)
    print(f"if you try a 'winning' bet, only on the horse with 2nd  winning cote, you will loose only {round(r*100, 2)}%") 

    r = TurfingRoom.once(df, BetRoom.winning, Strats.n_winning_cote, N=1, bet_value=1, verbose=False)
    print(f"if you try a 'winning' bet, only on the horse with 3rd winning cote, you will loose only {round(r*100, 2)}%") 


if __name__ == '__main__':
    main()


