#!/usr/bin/env python3
# coding: utf-8


###############################################################################
#       BETA_BACKTURFER
###############################################################################


if __name__ == '__main__':
    # import 
    from backturfer import *
    # from strats     import *


    # loading dataframe
    df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")


    # dataframe selection
    form        = { 'date_start': '2017-01-01',
                    'date_stop': '2019-04-01',
                    'country': 'france',
                    'hippo': '',
                    'quinte': 'all',
                    'euro_only': 'True',
                    'price_min': '',
                    'price_max': '',
                    'bet_type': 'simple_gagnant',
                    'strategy': 'strat_a',
                    'strategy_n': '0',
                    'plateform': 'hippodrome',
                    'stratey_param': '',
                    'bet_value_type': 'fixed'}


    race_sel    = RaceSelector(form)
    df          = race_sel(df)
    df          = GroupBy.internalize_results(df)


    # comp = 1016312
    # cotes = pk_load(f"comp-{comp}", "data/cotes/")  



    # strat = SimpleStrats.choix_de_la_meilleure_cote
    # bt = "simple_place"
    # bet = Bet(bt, strat) 
    # _ = bet.run(df.copy())

    # bt = "simple_place"
    # bet = Bet(bt, SimpleStrats.choix_de_la_meilleure_cote) 
    # _ = bet.run(df.copy())


    # bt = "simple_place"
    # bet = Bet(bt, CoupleStrats.choix_des_2_meilleures_cotes) 
    # _ = bet.run(df.copy())




# bets = [    ("simple_place",     SimpleStrats.choix_de_la_meilleure_cote),
#             ("simple_gagnant",   SimpleStrats.choix_de_la_meilleure_cote),
#             ("couple_ordre",     CoupleStrats.choix_des_2_meilleures_cotes),
#             ("couple_gagnant",   CoupleStrats.choix_des_2_meilleures_cotes),
#             ("couple_place",     CoupleStrats.choix_des_2_meilleures_cotes),
#             ("deux_sur_quatre",  CoupleStrats.choix_des_2_meilleures_cotes),
#             ("trio_ordre",       TrioStrats.choix_des_3_meilleures_cotes),
#             ("trio_desordre",    TrioStrats.choix_des_3_meilleures_cotes),
#             ("trio_ordre",       TrioStrats.choix_des_3_meilleures_cotes),
#             ("trio_desordre",    TrioStrats.choix_des_3_meilleures_cotes),
#             ("quinte_ordre",     QuinteStrats.choix_des_5_meilleures_cotes),
#             ("quinte_desordre",  QuinteStrats.choix_des_5_meilleures_cotes) ]

# for bt, st in bets : 

#     debug(f"bet {bt} strat {st}")
#     bet = Bet(bt, st)
#     _ = bet.run(df.copy())






# AddCote.add_cotes(df, cotes="all", cores=6, dest="data/cotes/", lazy=True)



# # # bet
# bet = Bet("simple_place", Strats.choix_de_la_meilleure_cote)
# info(bet)
# info(bet.__dict__)

# _df = bet(df)
# # # bets and turf
# # info("just Bet")

# _df = Bet.simple_gagnant(       df, 
#                                 Strats.choix_de_la_meilleure_cote)

# info("Trurfing Room Once")
# delta, bet_ratio, __df  = TurfingRoom.once( df, 
#                                             BetRoom.simple_gagnant, 
#                                             Strats.choix_de_la_meilleure_cote, 
#                                             N=0)





# DF  = df.copy()

# def main() : 

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

