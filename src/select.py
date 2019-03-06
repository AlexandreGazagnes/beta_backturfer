#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 


    @get_size_of
    @time_it 
    def select(df, form, verbose=True) : 
        """ """

        assert isinstance(df, pd.DataFrame) 
        assert isinstance(form, dict)

        if not "date_start" in form.keys() :form["date_start"] = 0
        if not "date_stop" in form.keys() : form["date_stop"] = 1000000
        if not "hippo" in form.keys() :     form["hippo"] = None
        if "country" in form.keys() :       
            form["country"] = None
            raise NotImplementedError("no country for now")
        else : 
            form["country"] = None
        if not "quinte" in form.keys() :    form["quinte"] = "all"
        if not "euro_only" in form.keys() : form["euro_only"] = False
        if not "price_min" in form.keys() : form["price_min"] = 0
        if not "price_max" in form.keys() : form["price_max"] = 500000000
        if not "typec" in form.keys() :     form["typec"] = list(df.typec.unique())

        t0 = time.time()

        _df = df.copy()

        # errors
        errors = list()

        for date in [form["date_start"], form["date_stop"]] : 
            if isinstance(date, int) : 
                pass
            elif isinstance(date, str) : 
                try : 
                    date = timestamp_to_int(pd.Timestamp(date))
                except Exception as e: 
                    warning(f"Error date {date} format ")
                    raise e
            elif isinstance(date, pd.Timestamp) : 
                try : 
                    date = timestamp_to_int(date)
                except Exception as e: 
                    warning(f"Error date {date} format ")
                    raise e
            else : 
                raise TypeError(f"unknown type for date {date}")

            assert isinstance(date, int)


        # dates
        _df = _df.loc[_df.jour >= form["date_start"], :]
        _df = _df.loc[_df.jour <= form["date_stop" ], :]


        # hippo
        if form["hippo"] : 

            form["hippo"]  = form["hippo"].strip().lower()
            _df["hippo"]    = _df.hippo.apply(str.lower)
            _df["hippo"]    = _df.hippo.apply(str.strip)

            if form["hippo"] not in _df.hippo.unique() : 
                errors.append(f"Error : {form['hippo']} not in our hippo database")
                candidates = [i for i in _df.hippo.unique() if i[:5] == form["hippo"][:5]]
                candidates = "\n".join(candidates)
                errors.append(f"Error : maybe you should consider {candidates}")
            else  : 
                _df = _df.loc[_df.hippo == form["hippo"], :]
        else : 
            if not form["country"] : 
                pass
            else : 
                raise NotImplementedError("Error NOT IMPLEMENTED country selection")
            

        # quinte
        if form["quinte"] == 'all'  : 
            pass
        elif form["quinte"] in ["only_quinte", 1, "1"] : 
            _df = _df.loc[_df.quinte == 1, :]
        elif form["quinte"] in ["only_not_quinte", 0, "0"] : 
            _df = _df.loc[_df.quinte == 0, :]
        else : 
            raise ValueError(f"unknown attribute for quite {form['quinte']} ")

        # currency
        if (form["euro_only"] == True) or (form["euro_only"] == "True") : 
            _df = _df.loc[_df.cheque_type == "€", :]
        elif (form["euro_only"] == False) or (form["euro_only"] == "False") : 
            pass
        else : 
            raise ValueError(f"unknown attribute for euro_only {form['euro_only']} ")

        # price
        _df = _df.loc[_df.cheque_val >= form["price_min"], :]
        _df = _df.loc[_df.cheque_val <= form["price_max"], :]
        
        # typec
        ser = _df.typec.apply(lambda i : str(i) in form["typec"])
        _df = _df.loc[ser, :]

        if len(_df) == 0 : 
            errors.append("error len _df = 0")
            info("Error, len _df = 0")

        if verbose : 
            info(f"start : {int_to_timestamp(_df.jour.min())}")
            info(f"stop  : {int_to_timestamp(_df.jour.max())}")
            info(f"hippo unique : {_df.hippo.unique()}")
            info(f"quinte unique : {_df.quinte.unique()}")
            info(f"cheque type : {_df.cheque_type.unique()}")
            info(f"cheque min : {_df.cheque_val.min()}")
            info(f"cheque max : {_df.cheque_val.max()}")
            info(f"typec init : {form['typec']}")
            info(f"typec unique : {_df.typec.unique()}")
            info(f"df size in Mo : {sys.getsizeof(_df) / 1000000}")
            info(f"timer load df : {round(time.time() - t0, 2)}")
            try :       info(f"debut {_df.jour.min()} fin {_df.jour.max()}")
            except :    pass
            info(_df.shape)
            info(_df.dtypes)
            info(_df.columns)

            info(form)

        return _df, errors
        


class Selector_() : 

    __valid_keys = ['date_start', 'date_stop', 'hippo', 'country', 'quinte', 'euro_only', 'price_min', 'price_max', 'typec']

    def __init__(self, form=dict()) : 
        
        form = {i: j for i, j in form.items() if i in Selector_.__valid_keys}

        

        self.form = form
 
