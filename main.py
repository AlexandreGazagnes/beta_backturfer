#!/usr/bin/env python3
# coding: utf-8



###############################################################################

#       BETA_BACKTURFER

###############################################################################


# import 
from src.misc           import * 
from src.turfing        import BetRoom, TurfingRoom
from strats.easy        import Strats





def main() : 
    # main dataframe
    df  = pk_load("ptu_cache_18_vince_only_1_cote_added_cotepodium", "data/")
    DF  = df.copy()


    # call
    _df = BetRoom.winning(df, Strats.n_winning_cote, N=0)
    r   = TurfingRoom.once(df, BetRoom.podium, Strats.n_winning_cote, N=0)



if __name__ == '__main__':
    main()

