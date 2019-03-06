#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 


# class
class GroupBy : 
    """functions used to enhance the first dataFrame with an new level of data. see group_by_courses"""

    @time_it 
    @get_size_of
    def _group_by_courses(df, cores=1, dest="temp/grouped_races/", verbose=True, clear_temp=True) : 
        """perform a groupby action on a basic dataframe and return a new dataframe with meta data as cols + "results"""

        # check agrs
        assert isinstance(df, pd.DataFrame)
        assert isinstance(cores, int)
        assert (cores >=1) and (cores <=8)
        assert isinstance(verbose, bool)
        if not os.path.isdir(dest) : 
            os.mkdir(dest)

        # here meta params for one  race
        cols = ["comp", "jour", "hippo", "numcourse", "partant", "typec", "cheque_val", "cheque_type"]
        cols = [i for i in cols if i in df.columns]

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
            info(f"df size in Mo : {sys.getsizeof(new_df) / 1000000}")
            info(f"timer load df : {round(time.time() - t0, 2)}")
            info(f"debut {new_df.jour.min()} fin {new_df.jour.max()}")
            info(new_df.shape)
            info(new_df.dtypes)

        return new_df


    @time_it 
    @get_size_of
    def _recast_dataframe(df) :

        _df = df.copy()

        if "jour" in _df.columns:        _df["jour"]          = _df.jour.astype(np.uint16)
        if "id" in _df.columns :         _df["id"]            = _df.id.astype(np.uint64)
        if "comp" in _df.columns :       _df["comp"]          = _df.comp.astype(np.uint32)
        if "hippo" in _df.columns :      _df["hippo"]         = _df.hippo.apply(lambda i : str(i)[:18].lower().strip())
        if "numcourse" in _df.columns :  _df["numcourse"]     = _df.numcourse.astype(np.uint32)
        if "dist" in _df.columns :       _df["dist"]          = _df.dist.astype(np.uint16)
        if "partant" in _df.columns :    _df["partant"]       = _df.partant.astype(np.uint8)
        if "typec" in _df.columns :      _df["typec"]         = _df.typec.apply(lambda i : str(i).lower().strip())
        if "typec" in _df.columns :      _df["typec"]         = _df.typec.apply(lambda i : str(i) if str(i) in ['steeple-chase', 'haies', 'plat', 'steeple-chase cross-country', 'attelé', 'monté'] else np.nan)
        if "quinte" in _df.columns :     _df["quinte"]        = _df.quinte.astype(bool)
        if "prix" in _df.columns :       _df["prix"]          = _df.prix.astype(np.uint8)        
 
        return _df 


    def __cote_score(results, cote_type) :

        assert isinstance(cote_type, str)
        assert cote_type in ["prob", "direct"]

        return round(sum(results[f"cote{cote_type}"] > 0.0) /  len(results[f"cote{cote_type}"]), 2)


    def _compute_cote_score(df, cote_type) : 
        """compute and add cotedirect/coteprob score based on the .isna() rate. 
        ie 1 : very good, 0 : very bad"""

        _df = df.copy()

        assert isinstance(cote_type, str)
        assert cote_type in ["prob", "direct"]

        _df[f"cote{cote_type}_score"] = _df.results.apply(lambda i : GroupBy.__cote_score(i,  cote_type))

        return _df


    def __sort_by_cl(results) :

        return results.sort_values("cl", ascending=True, inplace=False)


    def _compute_sort_by_cl(df) : 
        """sort by cl on a df"""

        _df = df.copy()

        results = _df.results
        sorted_results = results.apply(lambda i : GroupBy.__sort_by_cl(i))
        _df["results"] = sorted_results 

        return _df


    def _select_only_valuable_races(df, n=0.99) : 
        """based on on a grouped by df, compute and select only good races, with coteprob and cotedirect >= n"""

        _df = df.copy()

        _df = _df.loc[_df.hippo == "vincennes"]
        _df = GroupBy.compute_cote_score(_df, "prob")
        _df = GroupBy.compute_cote_score(_df, "direct")
        _df = _df.loc[_df.cotedirect_score >n, :]
        _df = _df.loc[_df.coteprob_score >n, :]
        _df.index = reindex(_df)

        return _df

    @time_it 
    @get_size_of
    def _merge_cache_carac(cache, carac) : 

        assert isinstance(cache, pd.DataFrame)
        assert isinstance(carac, pd.DataFrame)

        _cache = cache.copy()
        _carac = carac.copy()

        comp_cache = _cache.comp
        comp_carac = _carac.comp

        if comp_cache.shape[0] != comp_cache.unique().shape[0] : 
            info("error mismatch len cache key")
            k = comp_cache.value_counts()
            k = [i for i in k[k>1].index.values]
            info(f"please check after cachetrap.comp = {k}")

            for i in k  : 
                idx_drop = comp_cache[comp_cache == i].index
                if len(idx_drop)>1 : 
                    idx_drop = idx_drop[1:]
                    _cache = _cache.drop(idx_drop, axis=0, inplace=False)
                else : 
                    pass

        if comp_carac.shape[0] != comp_carac.unique().shape[0] : 
            info("error mismatch len carac key")
            k = comp_carac.value_counts()
            k = [i for i in k[k>1].index.values]
            info(f"please check after caractrap.comp = {k}")

            for i in k  : 
                idx_drop = comp_carac[comp_carac == i].index
                if len(idx_drop)>1 : 
                    idx_drop = idx_drop[1:]
                    _carac = _carac.drop(idx_drop, axis=0, inplace=False)
                else : 
                    pass

        assert "comp" in _cache.columns
        assert "comp" in _carac.columns

        _cache.sort_values("comp", axis=0, ascending=True, inplace=True)
        _carac.sort_values("comp", axis=0, ascending=True, inplace=True)

        assert len(_cache) == len(_carac)
        val = _cache.comp.values == _carac.comp.values
        assert val.all()

        _df = pd.concat([_cache, _carac], axis=1, ignore_index=True)

        funct = lambda i : i if i!="comp" else "_comp"
        _df.columns = list(_cache.columns) + list(map(funct, _carac.columns)) 

        val = (_df.comp ==_df["_comp"])
        assert val.all()                                          

        _df.drop("_comp", axis=1, inplace=True)

        # assert len(_df) == len(carac)
        # assert len(_df) == len(cache)

        # depreciated because to slow...
        # df = pd.merge(  cache, carac, how="left", on='comp', 
        #                 suffixes=('_cache', '_carac'), validate="1:1")

        return _df


    @time_it 
    @get_size_of
    def externalize_results(df, path="data/results/") : 
        """drop results and save it locally"""

        if  not "results" in df.columns : 
            raise ValueError ("results not in columns")

        assert len(df.comp.unique()) == len(df)


        def funct(i0=0, i1=10000000) : 

            for i in tqdm(df.index[i0:i1]) : 
                comp    = df.loc[i, "comp"]
                results = df.loc[i, "results"]
                pk_save(results, str(comp), path)

            return None


        # multiporcessing
        if cores < 2 : 
                funct()
        else : 
            chks  = chunks(df.index, cores)
            process_list = [Process(target=funct, args=chk) for chk in chks]
            [i.start() for i in process_list]
            [i.join()  for i in process_list]


        # drop df
        _df = df.drop("results", axis=1, inplace=False)
        
        return _df


    @time_it 
    @get_size_of
    def __old_internalize_results(df, path="data/results/") : 
        """load results from local path"""

        if "results" in df.columns : 
            raise ValueError ("results ALREADY in columns")

        assert len(df.comp.unique()) == len(df)

        _df = df.copy()

        results_list = list()
        for i in tqdm(_df.index) : 
            comp    = _df.loc[i, "comp"]
            results = pk_load(str(comp), path)
            results_list.append(results)

        _df["results"] = results_list
        
        return _df


    @get_size_of
    @time_it 
    def internalize_results(df, path="data/results/", temp="temp/internalize_results/" , cores=6) :

        if "results" in df.columns : 
            raise ValueError ("results ALREADY in columns")

        assert len(df.comp.unique()) == len(df)

        _df = df.copy()

        def funct(i0=0, i1=10000000) :                 
                
            results = []
            for comp in tqdm(_df.comp[i0: i1]) : 
                results.append([comp, pk_load(str(comp), path)])
            
            results = pd.DataFrame(results, columns=["comp", "results"])

            info(results.columns)
            info(results.head())
            
            pk_save(results, str(results.comp[0]), temp)


        def temp_merge() : 

            sub_df = pd.DataFrame(columns=["comp", "results"])

            for n in tqdm(os.listdir(temp)) :

                if not ".pk" in n : continue
                else : n = n.replace(".pk", "")

                r  = pk_load(str(n), temp)
                sub_df = sub_df.append(r, ignore_index=True)
                os.remove(f"{temp}{n}.pk")

            sub_df["comp"] = sub_df.comp.astype(np.uint32)

            return sub_df


        # multiporcessing
        if cores < 2 : 
                funct()
        else : 
            chks  = chunks(_df.comp, cores)
            process_list = [Process(target=funct, args=chk) for chk in chks]
            [i.start() for i in process_list]
            [i.join()  for i in process_list]

        # merge
        results = temp_merge()

        _df = _df.sort_values("comp", axis=0, ascending=True, inplace=False)
        _df.index = reindex(_df)

        results = results.sort_values("comp", axis=0, ascending=True, inplace=False)
        results.index = reindex(results)


        assert len(_df) == len(results)
        val = _df.comp.values == results.comp.values
        assert val.all()


        val = _df.index.values == results.index.values
        assert val.all()


        info(_df.columns)
        info(results.columns)

        results.columns = ["_comp", "results"]
        final_df = pd.concat([_df, results], axis=1, ignore_index=False)
        # final_df.columns = list(_df.columns) + list(results.columns) 

        info(final_df.loc[:, ["comp", "_comp"]].head())

        val = (final_df.comp.values ==final_df["_comp"].values)
        assert val.all()                                          

        final_df.drop("_comp", axis=1, inplace=True)

        assert len(final_df) == len(_df)
        assert len(final_df) == len(results)

        pk_clean(temp)

        return final_df





    @time_it 
    @get_size_of
    def create_merged_dataframe(cache, carac) : 
        """from a basic cache dataframe, perform a groupby races and merge with carac"""
        
        cache = GroupBy._group_by_courses(cache, cores=6, dest="temp/grouped_races/", verbose=True, clear_temp=True)
        cache = GroupBy._recast_dataframe(cache)
        df    = GroupBy._merge_cache_carac(cache, carac)
        df    = GroupBy.externalize_results(df)

        return df



