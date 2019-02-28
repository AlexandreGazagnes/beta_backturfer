#!/usr/bin/env python3
# coding: utf-8

from src.misc import *


class FormCheck :
    """basic class of funct to manage and clean form"""

    # consts
    __price_min_max = 5000000
    __price_max_min = 1000


    def __check_date_start(d) :
        """check form input for date_start"""

        if not d : 
            return 0, False
        try : 
            d= pd.Timestamp(d)
        except : 
            return 0, "Error : date_start timestamp conversion, invalid format"
    
        if d >= pd.Timestamp.today()  : 
            return 0, "Error : date_start > Today"

        d = timestamp_to_int(d)

        return (d, False)


    def __check_date_stop(d) :
        """check form input for date_stop"""
        if not d :
            return 30000, False
        try : 
            d= pd.Timestamp(d)
        except : 
            return 0, "Error : date_start timestamp conversion, invalid format"

        if d <= pd.Timestamp("2015-12-31") : 
            return 0, "Error : date_stop to old, data start at 2016-01-01"

        d = timestamp_to_int(d)

        return d, False


    def __check_date_comp(date_start, date_stop) :
        
        if date_stop <= date_start : 
            return 0, 0, "Error : Sorry date_start to close/before date_stop" 

        return date_start, date_stop, False


    def __check_country(d) :

        return d, False


    def __check_hippo(d) :

        d = d.strip().lower()
        
        return d, False


    def __check_hippo_comp(country, hippo) :

        if hippo : 
            country = "monde"

        return country, hippo, False


    def __check_quinte(d) :
        
        return d, False


    def __check_price_min(d) :

        _d = d.strip().replace(" ", "").replace("-", "").replace("€", "").strip()

        if not _d :
            return 0, False

        try :
            _d = int(_d)
        except :
            return "", f"Error : invalid price_min recieved {d}, expected and number"

        if _d < 0 : _d = 0
        if _d > FormCheck.__price_min_max :
            return 0, f"Error : invalid price_min, recieved {d}, expected max {FormCheck.__price_min_max}"

        return _d, False


    def __check_price_max(d) :

        _d = d.strip().replace(" ", "").replace("-", "").replace("€", "").strip()

        if not _d :
            return 50000000, False

        try :
            _d = int(_d)
        except :
            return 0, f"Error : invalid price_max recieved {d}, expected and number"

        if _d <= 0 :
            return 0, f"Error : invalid price_max, recieved {d}, expected max positive value"

        if _d < FormCheck.__price_max_min :
            return 0, f"Error : invalid price_max, recieved {d}, expected min {FormCheck.__price_max_min}"

        return _d, False


    def __check_price_comp(price_min, price_max) : 

        if price_min >= price_max : 
            return 0, 0, f"Error : price min {price_min} >= price_max {price_max}"

        return price_min, price_max , False


    def check(form, verbose=False) :

        # transform form in normal dict
        form = {i:j for i,j in form.items()}

        if verbose : 
            li = [f"{i}:{j}" for i,j in form.items()]
            info("INIT FORM" + "\n".join(li) + "\n\n")

        # error list
        error_list = list()

        # dates
        form["date_start"], e = FormCheck.__check_date_start(form["date_start"])
        error_list.append(e)
        form["date_stop"], e = FormCheck.__check_date_stop(form["date_stop"])
        error_list.append(e)
        form["date_start"], form["date_stop"], e = FormCheck.__check_date_comp(form["date_start"], form["date_stop"])
        error_list.append(e)

        # hippodrome
        form["country"], e = FormCheck.__check_country(form["country"])
        error_list.append(e)
        form["hippo"], e = FormCheck.__check_hippo(form["hippo"])
        error_list.append(e)
        form["country"], form["hippo"], e = FormCheck.__check_hippo_comp(form["country"], form["hippo"]) 
        error_list.append(e)

        # race type
        form["price_min"], e = FormCheck.__check_price_min(form["price_min"])
        error_list.append(e)
        form["price_max"], e = FormCheck.__check_price_max(form["price_max"])
        error_list.append(e)
        form["price_min"], form["price_max"], e = FormCheck.__check_price_comp(form["price_min"], form["price_max"])
        error_list.append(e)

        race_types = ["monté", "attelé", "plat", "haies", "steeple-chase", "steeple-chase cross-country"]
        race_types = [i for i in race_types if i in form.keys()]
        [form.pop(i) for i in race_types if i in form.keys()]
        form["typec"] = race_types


        if verbose : 
            li = [f"{i}:{j}" for i,j in form.items()]
            info("END FORM" + "\n".join(li) + "\n\n")

        # clean error list
        assert len(error_list) == 9
        error_list = [i for i in error_list if i]

        return form, error_list


class App:
    """App class""" 

    def __build_dataframe(df, form) : 

        # errors
        errors = list()

        # dates
        df = df.loc[df.jour >= form["date_start"], :]
        df = df.loc[df.jour <= form["date_stop" ], :]

        info(f" start : {int_to_timestamp(df.jour.min())}")
        info(f" stop  : {int_to_timestamp(df.jour.max())}")

        # hippo
        if form["hippo"] : 

            form["hippo"]  = form["hippo"].strip().lower()
            df["hippo"]    = df.hippo.apply(str.lower)
            df["hippo"]    = df.hippo.apply(str.strip)

            if form["hippo"] not in df.hippo.unique() : 
                errors.append(f"Error : {form['hippo']} not in our hippo database")
                candidates = [i for i in df.hippo.unique() if i[:5] == form["hippo"][:5]]
                candidates = "\n".join(candidates)
                errors.append(f"Error : maybe you should consider {candidates}")
            else  : 
                df = df.loc[df.hippo == form["hippo"], :]
        else : 

            warning("Error NOT IMPLEMENTED")
            pass

        info(f" hippo unique : {df.hippo.unique()}")

        # quinte
        if form["quinte"] == 'all'  : 
            pass
        elif form["quinte"] == "only_quinte" : 
            df = df.loc[df.quinte == 1, :]
        elif form["quinte"] == "only_not_quinte" : 
            df = df.loc[df.quinte == 0, :]
        else : 
            raise ValueError(f"unknown attribute for quite {form['quinte']} ")

        info(f" quinte unique : {df.quinte.unique()}")

        # currency
        if (form["euro_only"] == True) or (form["euro_only"] == "True") : 
            df = df.loc[df.cheque_type == "€", :]
        elif (form["euro_only"] == False) or (form["euro_only"] == "False") : 
            pass
        else : 
            raise ValueError(f"unknown attribute for euro_only {form['euro_only']} ")

        info(f"chque type : {df.cheque_type.unique()}")

        # price
        df = df.loc[df.cheque_val >= form["price_min"], :]
        df = df.loc[df.cheque_val <= form["price_max"], :]

        info(f" cheque min : {df.cheque_val.min()}")
        info(f" cheque max : {df.cheque_val.max()}")


        info(f"typec : {form['typec']}")
        # typec
        ser = df.typec.apply(lambda i : str(i) in form["typec"])
        df = df.loc[ser, :]

        info(f"typec unique : {df.typec.unique()}")

        if len(df) == 0 : 
            errors.append("error len df = 0")

        return df, errors


    def run(df, form, verbose=True): 

        assert isinstance(df, pd.DataFrame)
        assert isinstance(form, dict)

        df, errors  = App.__build_dataframe(df, form)

        if errors : 
            return 0, errors

        if verbose : 
            info(f"len df {len(df)} ")
            info(f"df cols {df.columns} ")
            df.to_csv(f"temp/web_df/{get_an_hash()}.csv", index=False)
            # pk_save(df, get_an_hash(), "temp/web_df/")
        

        return "No errors in App.run", None







