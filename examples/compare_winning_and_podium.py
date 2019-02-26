#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc           import * 
from src.turfing        import BetRoom, TurfingRoom
from strats.easy        import Strats


# funct
def main() : 

    def shape_df_as_requested(df, param) : 
        """just a small function to select valid dataframe"""

        if   param == "all" :           pass
        elif param == "quinte" :        df = df.loc[df.quinte == 1, :]
        elif param == "not quinte" :    df = df.loc[df.quinte == 0, :]
        else :                          raise ValueError("param error")

        return df


    # init
    #####################################################################################

    # dataframe    
    df      = pk_load("ptu_cache_18_vince_only_1_cote_added_cotepodium", "data/")
    DF      = df.copy()

    # looper
    range_types = list(range(5))
    bet_types   = (BetRoom.winning, BetRoom.podium)
    strat_types = (Strats.n_winning_cote, ) # Strats.random_1_on_n_best_winning_cote
    race_types = ("all", "quinte", "not quinte")
    
    # results
    results = list()

    # loop
    #####################################################################################

    for i, bet, strat, race in product(range_types, bet_types, strat_types, race_types) : 
        try : 
            df      = shape_df_as_requested(DF.copy(), race) 
            _df     = bet(df, strat, N=i, verbose=False)
            r1      = _df.good_bet.value_counts(normalize=True)[1]
            r2      = TurfingRoom.once(df, bet, strat, N=i, bet_value=1, verbose=False)
            results.append((i+1, race, str(bet), str(strat), r1, r2))
            r1, r2 = str(round(r1*100, 2)).ljust(5, "0"), str(round(r2*100, 2)).ljust(5,"0")
            print(f"\t{i+1}th best cote, bet type {bet}, strat {strat}, bet results : {r1}%, financial results {r2}%")
        except : 
            info(f"error for {i+1} _ {bet} _ {strat}")


    # results
    #####################################################################################

    results = pd.DataFrame(results, columns=["n* cote", "course", "bet", "strat", "% win bet", "% bank"])
    results.index.name = "2018, Vincennes, all_races"

    print(results)
    pk_save(results, "2018_Vincennes_all_races_2", "results/")
    return results



if __name__ == '__main__':
    main()




