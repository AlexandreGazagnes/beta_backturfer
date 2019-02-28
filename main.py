#!/usr/bin/env python3
# coding: utf-8



###############################################################################

#       BETA_BACKTURFER

###############################################################################


# import 
from src.misc           import * 
from src.build          import Build
from src.groupby        import GroupBy
from src.addcote        import CotePlaced, CoteDuo, CoteTierce
from src.turfing        import BetRoom, TurfingRoom
from strats.easy        import Strats

df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")


def main() : 

    # # build dataframe    
    # cachedate = Build.create_dataframe("cachedate_2016-2019_OK.csv", "data/")   
    # caractrap = Build.create_dataframe("caractrap_2016-2019_OK.csv", "data/")                              

    # # group and merge in One df
    # df = GroupBy.create_merged_dataframe(cachedate, caractrap)
    # del caractrap, cachedate

    # main dataframe
    df  = pk_load("pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
    DF  = df.copy()


    # call
    _df = BetRoom.winning(df, Strats.n_winning_cote, N=0)
    r   = TurfingRoom.once(df, BetRoom.podium, Strats.n_winning_cote, N=0)



# if __name__ == '__main__':
#     main()

