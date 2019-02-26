 #!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 


#class
class Build : 
    """functs used to build cachedate and caratrap first dataframes"""

    def create_dataframe(filename, path, lim_l=100000000, lim_c=22, reverse=False, verbose=True) :
        """just an overkilled df.read_csv"""
        
        # arg checks
        if ".csv" not in filename : filename+=".csv"
        if path[-1] != "/" :        path += "/"

        # time
        t0 = time.time()
        
        # dataframe
        df = pd.read_csv(path+filename)
        df.columns = pd.Series(df.columns).apply(str.strip)
        df["jour"] = df.jour.apply(lambda i : pd.Timestamp(i)) 
        if reverse : 
            df = df.sort_values("numcourse", ascending=False, inplace=False)
        df = df.iloc[:lim_l, :lim_c]
        df.index = range(len(df.index))

        # verbose
        if verbose : 
            warning(f"df size in Mo : {sys.getsizeof(df) / 1000000}")
            warning(f"timer load df : {round(time.time() - t0, 2)}")
            warning(f"debut {df.jour.min()} fin {df.jour.max()}")
            warning(df.shape)
            warning(df.dtypes)

        return df


    def recast_cachedate_if_needed(df, verbose=True) : 
        """recast col by col if needed to save RAM"""

        # time
        t0 = time.time()

        # time in int
        if "jour" in df.columns :       
            df["jour"]                                      = df.jour.apply(timestamp_to_int)
            df["jour"]                                      = df.jour.astype(np.uint16)

        # cl
        df["old_cl"] = df.cl.copy()
        if "cl" in df.columns : 
            df["cl"]                                        = np.float16(0.0)
            temp_cl                                         = df.old_cl.apply(lambda i : str(i)[:4].strip())

            cl_dict = dict() ; cl_dict["1er"] = 1
            for i in  ["NP", "dai", "dpg", "npi", "tbé", "dist"] :  cl_dict[i] = 99
            for i in range(2, 40) :                                 cl_dict[f"{i}e"] = i
            df["cl"]                                        = (temp_cl.map(cl_dict)).astype(np.float16)
            del temp_cl
        
        # sexe  
        sexe_dict = {"H":1, "F":0, "M":2, "X":np.nan}
        if "sexe" in df.columns :       df["sexe"]          = (df.sexe.map(sexe_dict)).astype(np.float16)


        # cheque
        if "cheque" in df.columns :    
            df["cheque_type"]                               = df.cheque.apply(lambda i : str(i)[-1])
            df["cheque_val"]                                = df.cheque.apply(lambda i : str(i)[:-1].strip().replace(".", ""))

            def f(i) : 
                try :       return int(str(i).strip())
                except :    return 0

            df["cheque_val"]                                = (df.cheque_val.apply(f)).astype(np.uint32)
            df.drop("cheque", axis=1, inplace=True)

        # others
        if "id" in df.columns :         df["id"]            = df.id.astype(np.uint64)
        if "comp" in df.columns :       df["comp"]          = df.comp.astype(np.uint32)
        if "hippo" in df.columns :      df["hippo"]         = df.hippo.apply(lambda i : str(i)[:10].lower().strip())
        if "numcourse" in df.columns :  df["numcourse"]     = df.numcourse.astype(np.uint32)
        if "dist" in df.columns :       df["dist"]          = df.dist.astype(np.uint16)
        if "partant" in df.columns :    df["partant"]       = df.partant.astype(np.uint8)
        if "numero" in df.columns :     df["numero"]        = df.numero.astype(np.uint8)
        if "recence" in df.columns :    df["recence"]       = df.recence.astype(np.uint16)
        if "coteprob" in df.columns :   df["coteprob"]      = df.coteprob.astype(np.float16)    
        if "cotedirect" in df.columns : df["cotedirect"]    = df.cotedirect.astype(np.float16)
        if "cheval" in df.columns :     df["cheval"]        = df.cheval.apply(lambda i : str(i).lower())
        if "typec" in df.columns :      df["typec"]         = df.typec.apply(lambda i : str(i) if str(i) in ['Steeple-chase', 'Haies', 'Plat', 'Steeple-chase cross-country', 'Attelé', 'Monté'] else np.nan)
        if "age" in df.columns :        df["age"]           = df.age.astype(np.uint8) 

        # verbose
        if verbose : 
            warning(f"df size in Mo : {sys.getsizeof(df) / 1000000}")
            warning(f"timer load df : {round(time.time() - t0, 2)}")
            warning(f"debut {df.jour.min()} fin {df.jour.max()}")
            warning(df.shape)
            warning(df.dtypes)

        return df


    def del_useless_params_cachedate(df, params=None, verbose=True) : 
        """del useless params"""

        t0 = time.time()

        if not params :             params = ["sexe", "old_cl", "id", "recence", "cheque", "ecurie", "age", "distpoids"]
        
        for i in params :
            if i in df.columns:     df.drop(i, axis=1, inplace=True)

        # verbose
        if verbose : 
            warning(f"df size in Mo : {sys.getsizeof(df) / 1000000}")
            warning(f"timer load df : {round(time.time() - t0, 2)}")
            warning(f"debut {df.jour.min()} fin {df.jour.max()}")
            warning(df.shape)
            warning(df.dtypes)

        return df


    def create_cachedate_dataframe(filename, path) : 
        """create cachedate dataframe, recast cols if needed and del useless params"""

        if path[-1] != "/" : path+= "/"
        assert os.path.isdir(path)  
        assert os.path.isfile(path+filename)

        df      = Build.create_dataframe(filename, path ) 
        df      = Build.recast_cachedate_if_needed(df)
        df      = Build.del_useless_params_cachedate(df) 

        return df


