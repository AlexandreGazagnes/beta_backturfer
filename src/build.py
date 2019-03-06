#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 


#class
class Build : 
    """functs used to build cachedate and caratrap first dataframes"""

    @time_it 
    @get_size_of
    def _init(filename, path, sep="\t", lim_l=100000000, lim_c=30, reverse=False, verbose=True) :
        """just an overkilled df.read_csv"""
        
        # arg checks
        if ".csv" not in filename : filename+=".csv"
        if path[-1] != "/" :        path += "/"

        # time
        t0 = time.time()
        
        # dataframe
        df = pd.read_csv(path+filename, sep=sep)
        df.columns = pd.Series(df.columns).apply(str.strip)
        if "jour" in df.columns : 
            df["jour"] = df.jour.apply(lambda i : pd.Timestamp(i)) 
        if reverse and ("comp" in df.columns) : 
            df["comp"] = df.comp.astype(np.uint32)
            df = df.sort_values("comp", ascending=False, inplace=False)
        df = df.iloc[:lim_l, :lim_c]
        df.index = reindex(df)

        # verbose
        if verbose : 
            info(f"df size in Mo : {sys.getsizeof(df) / 1000000}")
            info(f"timer load df : {round(time.time() - t0, 2)}")
            try :    info(f"debut {df.jour.min()} fin {df.jour.max()}")
            except : pass
            info(df.shape)
            info(df.dtypes)

        return df

    @time_it 
    @get_size_of
    def _recast(df, verbose=True) : 
        """recast col by col if needed to save RAM"""

        _df = df.copy()

        # time
        t0 = time.time()

        # time in int
        if "jour" in df.columns :       
            _df["jour"]                                      = _df.jour.apply(timestamp_to_int)
            _df["jour"]                                      = _df.jour.astype(np.uint16)

        # cl
        if "cl" in _df.columns : 
            _df["old_cl"] = _df.cl.copy()
            _df["cl"]                                        = np.float16(0.0)
            temp_cl                                         = _df.old_cl.apply(lambda i : str(i)[:4].strip())

            cl_dict = dict() ; cl_dict["1er"] = 1
            for i in  ["NP", "dai", "dpg", "npi", "tbé", "dist"] :  cl_dict[i] = 99
            for i in range(2, 40) :                                 cl_dict[f"{i}e"] = i
            _df["cl"]                                        = (temp_cl.map(cl_dict)).astype(np.float16)
            del temp_cl
        
        # sexe  
        sexe_dict = {"H":1, "F":0, "M":2, "X":np.nan}
        if "sexe" in _df.columns :       _df["sexe"]          = (_df.sexe.map(sexe_dict)).astype(np.float16)


        # cheque
        if "cheque" in _df.columns :    
            _df["cheque_type"]                               = _df.cheque.apply(lambda i : str(i)[-1])
            _df["cheque_val"]                                = _df.cheque.apply(lambda i : str(i)[:-1].strip().replace(".", ""))

            def f(i) : 
                try :       return int(str(i).strip())
                except :    return 0

            _df["cheque_val"]                                = (_df.cheque_val.apply(f)).astype(np.uint32)
            _df.drop("cheque", axis=1, inplace=True)

        # others
        if "id" in _df.columns :         _df["id"]            = _df.id.astype(np.uint64)
        if "comp" in _df.columns :       _df["comp"]          = _df.comp.astype(np.uint32)
        if "hippo" in _df.columns :      _df["hippo"]         = _df.hippo.apply(lambda i : str(i)[:18].lower().strip())
        if "numcourse" in _df.columns :  _df["numcourse"]     = _df.numcourse.astype(np.uint32)
        if "dist" in _df.columns :       _df["dist"]          = _df.dist.astype(np.uint16)
        if "partant" in _df.columns :    _df["partant"]       = _df.partant.astype(np.uint8)
        if "numero" in _df.columns :     _df["numero"]        = _df.numero.astype(np.uint8)
        if "recence" in _df.columns :    _df["recence"]       = _df.recence.astype(np.uint16)
        if "coteprob" in _df.columns :   _df["coteprob"]      = _df.coteprob.astype(np.float16)    
        if "cotedirect" in _df.columns : _df["cotedirect"]    = _df.cotedirect.astype(np.float16)
        if "cheval" in _df.columns :     _df["cheval"]        = _df.cheval.apply(lambda i : str(i).lower().strip())
        if "typec" in _df.columns :      _df["typec"]         = _df.typec.apply(lambda i : str(i).lower().strip())
        if "typec" in _df.columns :      _df["typec"]         = _df.typec.apply(lambda i : str(i) if str(i) in ['steeple-chase', 'haies', 'plat', 'steeple-chase cross-country', 'attelé', 'monté'] else np.nan)
        if "age" in _df.columns :        _df["age"]           = _df.age.astype(np.uint8) 
        if "quinte" in _df.columns :     _df["quinte"]        = _df.quinte.astype(bool)
        if "prix" in _df.columns :       _df["prix"]          = _df.prix.astype(np.uint8)        
        
        if "hippo" in _df.columns :      _df["hippo"]         = _df.hippo.apply(lambda i : normalize_hippo(str(i)))

        # verbose   
        if verbose : 
            info(f"df size in Mo : {sys.getsizeof(_df) / 1000000}")
            info(f"timer load df : {round(time.time() - t0, 2)}")
            try :       info(f"debut {_df.jour.min()} fin {_df.jour.max()}")
            except :    pass
            info(_df.shape)
            info(_df.dtypes)

        return _df

    @time_it 
    @get_size_of
    def _del_params(df, params=None, verbose=True) : 
        """del useless params"""

        _df = df.copy()

        t0 = time.time()

        if not params :             params = ["old_cl", "id" ]
        
        for i in params :
            if i in _df.columns:     _df.drop(i, axis=1, inplace=True)

        # verbose
        if verbose : 
            info(f"df size in Mo : {sys.getsizeof(_df) / 1000000}")
            info(f"timer load df : {round(time.time() - t0, 2)}")
            try :       info(f"debut {_df.jour.min()} fin {_df.jour.max()}")
            except :    pass
            info(_df.shape)
            info(_df.dtypes)

        return _df

    @time_it 
    @get_size_of
    def create(filename, path) : 
        """create cachedate dataframe, recast cols if needed and del useless params"""

        if path[-1] != "/" : path+= "/"
        assert os.path.isdir(path)  
        assert os.path.isfile(path+filename)

        df      = Build._init(filename, path ) 
        df      = Build._recast(df)
        df      = Build._del_params(df) 

        return df



