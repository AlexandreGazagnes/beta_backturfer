#!/usr/bin/env python3
# coding: utf-8



###############################################################################

#       BETA_BACKTURFER

###############################################################################


# import 
from src.misc           import * 
from src.build          import Build
from src.select         import Selector
from src.groupby        import GroupBy
from src.addcote        import CotePlaced, CoteDuo, CoteTierce
from src.turfing        import BetRoom, TurfingRoom
from strats.easy        import Strats


# main dataframe
info("loading dataframe")
df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")


# selection
info("selecting good dataframe")

selector = Selector({   'date_start': "2018-01-01",
                        'quinte'    : 1,
                        'euro_only' : True,
                        'typec'     : [  'attelé', 'monté',]}) 



df = selector.perform(df)


# load results
info("loading results")
df = GroupBy.internalize_results(df)


# bets and turf
info("just BetRoom")
_df = BetRoom.simple_gagnant(   df, 
                                Strats.choix_de_la_meilleure_cote, 
                                N=0)

info("Trurfing Room Once")
delta, bet_ratio, __df  = TurfingRoom.once( df, 
                                            BetRoom.simple_gagnant, 
                                            Strats.choix_de_la_meilleure_cote, 
                                            N=0)





DF  = df.copy()

def main() : 

    # # build dataframe    
    # cachedate = Build.create_dataframe("cachedate_2016-2019_OK.csv", "data/")   
    # caractrap = Build.create_dataframe("caractrap_2016-2019_OK.csv", "data/")                              

    # # group and merge in One df
    # df = GroupBy.create_merged_dataframe(cachedate, caractrap)
    # del caractrap, cachedate

    # main dataframe
    # df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
    # df  = df.loc[df.quinte == 1, :]
    # df  = df.loc[df.jour >= timestamp_to_int(pd.Timestamp("2018-01-01")), :] 
    # df  = df.loc[df.typec == "attelé", :]
    # df  = df.loc[df.cheque_type == "€", :]
    # info(f"len df : {len(df)}" )
    # df = GroupBy.internalize_results(df)

    # DF  = df.copy()


    # # # call


if __name__ == '__main__':
    main()

