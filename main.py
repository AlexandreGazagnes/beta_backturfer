#!/usr/bin/env python3
# coding: utf-8


###############################################################################
#       BETA_BACKTURFER
###############################################################################


# import 
from backturfer import *
from strats     import *


# loading dataframe
df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")


# dataframe selection
form        = { 'date_start': "2017-01-01", 
                'quinte'    : 1, 
                'euro_only' : True, 
                'typec'     : ['attelé', 'monté', "plat"]  }

race_sel    = RaceSelector(form)
df          = race_sel(df)
df          = GroupBy.internalize_results(df)


# # couple gagnant
# bet = Bet("couple_gagnant", CoupleStrats.choix_des_2_meilleures_cotes)
# df_couple_gagnant = bet.run(df.copy())
# print(df_couple_gagnant.good_bet.value_counts(normalize=True))


# # couple ordre
# bet = Bet("couple_ordre", CoupleStrats.choix_des_2_meilleures_cotes)
# df_couple_ordre = bet.run(df.copy())
# print(df_couple_ordre.good_bet.value_counts(normalize=True))


# # couple place
# bet = Bet("couple_place", CoupleStrats.choix_des_2_meilleures_cotes)
# df_couple_place = bet.run(df.copy())
# print(df_couple_place.good_bet.value_counts(normalize=True))


# # deux sur quatre
# bet = Bet("deux_sur_quatre", CoupleStrats.choix_des_2_meilleures_cotes)
# df_2_sur_4 = bet.run(df.copy())
# print(df_2_sur_4.good_bet.value_counts(normalize=True))


# bet = Bet("trio_ordre", TrioStrats.choix_des_3_meilleures_cotes)
# df_trio_ordre = bet.run(df.copy())
# print(df_trio_ordre.good_bet.value_counts(normalize=True))


bet = Bet("quinte_desordre", QuinteStrats.choix_des_5_meilleures_cotes)
df_quinte_desordre = bet.run(df.copy())
print(df_quinte_desordre.good_bet.value_counts(normalize=True))

_df = df_quinte_desordre.copy()
goods = _df.loc[_df.good_bet, :]



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


