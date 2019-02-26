#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 


# class
class GroupBy : 
    """functions used to enhance the first dataFrame with an new level of data. see group_by_courses"""


    def group_by_courses(df, cores=1, dest="temp/grouped_races/", verbose=True, clear_temp=True) : 
        """perform a groupby action on a basic dataframe and return a new dataframe with meta data as cols + "results"""

        # check agrs
        assert isinstance(df, pd.DataFrame)
        assert isinstance(cores, int)
        assert (cores >=1) and (cores <=8)
        assert isinstance(verbose, bool)
        if not os.path.isdir(dest) : 
            os.mkdir(dest)

        # here meta params for one  race
        cols = ["comp", "numcourse", "jour", "hippo", "dist", "partant", "typec", "cheque_val", "cheque_type"]
        for i in cols :  assert i in df.columns

        # time
        t0 = time.time()

        # global index
        list_of_races = df.numcourse.unique()

        # functions
        def group_races(i0=0, i1=1000000000) : 

            for n in list_of_races[i0:i1] : 
                sub_df = df.loc[df.numcourse == n, :]
                pk_save(sub_df, str(n), dest)

        def check_races(i0=0, i1=1000000000) :  

            for n in list_of_races[i0:i1] : 
                sub_df  = pk_load(str(n), dest)

                # check same meta data
                ok = True
                for i in cols: 
                    if not len(sub_df[i].unique()) == 1 : 
                        if i == "dist" :    pass          # allow dist
                        else :              ok = False    # if not dist error

                # 
                # add some other sanity checks
                # 

                if not ok : 
                    warning(sub_df)
                    os.remove(f"{dest}{n}.pk")

        def reshape_races(i0=0, i1=1000000000) :  

            for n in list_of_races[i0:i1] : 
                if not os.path.isfile(f"{dest}{n}.pk") : continue
                sub_df  = pk_load(str(n), dest)

                # here are results of the race
                results = sub_df.drop(cols, axis=1, inplace=False)
                
                # here meta params and results
                ser = [sub_df[i].iloc[0] for i in cols ] + [results, ]
                ser = pd.Series(ser, index=cols+["results"])

                # save
                pk_save(ser, str(n), dest)

        def merge_races(i0=0, i1=1000000000) : 

            new_df = pd.DataFrame(columns=cols+["results",])

            for n in list_of_races[i0:i1] : 
                if not os.path.isfile(f"{dest}{n}.pk") : continue
                ser  = pk_load(str(n), dest)
                new_df = new_df.append(ser, ignore_index=True)
                os.remove(f"{dest}{n}.pk")

            pk_save(new_df, str(list_of_races[i0]), dest)
            
        def final_merge() : 

            new_df = pd.DataFrame(columns=cols+["results",])

            for n in tqdm(os.listdir(dest)) : 
                if not ".pk" in n : continue
                else : n = n.replace(".pk", "")

                ser  = pk_load(str(n), dest)
                new_df = new_df.append(ser, ignore_index=True)
                if clear_temp : 
                    os.remove(f"{dest}{n}.pk")

            return new_df

        # multiprocessing
        functions_list = [group_races, check_races, reshape_races, merge_races]
        if cores < 2 : 
            [funct() for funct in tqdm(functions_list)]

        else : 
            chks  = chunks(list_of_races, cores)
            for funct in tqdm(functions_list) : 
                process_list = [Process(target=funct, args=chk) for chk in chks]
                [i.start() for i in process_list]
                [i.join()  for i in process_list]

        # final
        info("grouping complete")
        new_df          = final_merge()
        info("merging complete")
        new_df          = new_df.iloc[1:-1, :]
        new_df.index    = range(len(new_df.index))

        # verbose
        if verbose : 
            warning(f"df size in Mo : {sys.getsizeof(new_df) / 1000000}")
            warning(f"timer load df : {round(time.time() - t0, 2)}")
            warning(f"debut {new_df.jour.min()} fin {new_df.jour.max()}")
            warning(new_df.shape)
            warning(new_df.dtypes)

        return new_df


    def __cote_score(results, cote_type) :

        assert isinstance(cote_type, str)
        assert cote_type in ["prob", "direct"]

        return round(sum(results[f"cote{cote_type}"] > 0.0) /  len(results[f"cote{cote_type}"]), 2)


    def compute_cote_score(df, cote_type) : 
        """compute and add cotedirect/coteprob score based on the .isna() rate. 
        ie 1 : very good, 0 : very bad"""

        assert isinstance(cote_type, str)
        assert cote_type in ["prob", "direct"]

        df[f"cote{cote_type}_score"] = df.results.apply(lambda i : GroupBy.__cote_score(i,  cote_type))

        return df


    def __sort_by_cl(results) :

        return results.sort_values("cl", ascending=True, inplace=False)


    def compute_sort_by_cl(df) : 
        """sort by cl on a df"""

        results = df.results
        sorted_results = results.apply(lambda i : GroupBy.__sort_by_cl(i))
        df["sorted_results"] = sorted_results 

        return df


    def select_only_valuable_races(df, n=0.99) : 
        """based on on a grouped by df, compute and select only good races, with coteprob and cotedirect >= n"""

        df = df.loc[df.hippo == "vincennes"]
        df = GroupBy.compute_cote_score(df, "prob")
        df = GroupBy.compute_cote_score(df, "direct")
        df = df.loc[df.cotedirect_score >n, :]
        df = df.loc[df.coteprob_score >n, :]
        df.index = reindex(df)

        return df


    def create_fancy_dataframe(df) : 
        """from a basic dataframe, perform a groupby races and then a selection to keep only valuable races"""
        
        df = GroupBy.group_by_courses(df, cores=6, dest="temp/grouped_races/", verbose=True, clear_temp=True)
        df = GroupBy.select_only_valuable_races(df)
        return df



