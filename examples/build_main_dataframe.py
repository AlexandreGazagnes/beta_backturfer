#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc         import * 
from src.build        import Build
from src.groupby      import GroupBy
from src.scrap        import CotePodium


# funct
def main()
    df    = Build.create_cachedate_dataframe("pturf_cachedate_2018.csv", "data/")
    df    = GroupBy.create_fancy_dataframe(df)
    df    = CotePodium.create_fancy_cotepodium(df) 
    pk_save(df, "pturf_cachedate_2018_vincennes_groupby_df_only_good_coteprob_cotedirect", "data/")


# main
if __name__ == '__main__':
    main()


