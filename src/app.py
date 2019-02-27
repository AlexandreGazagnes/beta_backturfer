#!/usr/bin/env python3
# coding: utf-8

from src.misc import *


class FormCheck :
    """basic class of funct to manage and clean form"""

    self.__price_min_max = 3000000

    def __check_date_start(d) :
        """check form input for date_start"""

        if not d :
            return 0, False
        else :
            d= pd.Timestamp(d)
            info(d)
            d = timestamp_to_int(d)
            info(d)
            return (d, False)

    def __check_date_stop(d) :
        """check form input for date_stop"""
        if not d :
            return 20000, False
        else :
            d= pd.Timestamp(d)
            info(d)
            d = timestamp_to_int(d)
            info(d)
            return (d, False)

    def __check_date_comp(d1, d2) : 
        pass

    def __check_country(d) : 

        return d, False

    def __check_top(d) : 
        return d, False

    def __check_hippo(d) : 
        d = d.strip().lower()
        return, d, False

    def __check_hippo_comp(country, top, hippo) : 
        return (country, top, hippo), False

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
            return : 0, f"Error : invalid price_min, recieved {d}, expected max {FormCheck.__price_min_max}"

    def check(form) :

        # transform form in normal dict
        form = {i:j for i,j in form.items()}

        # info
        li = [f"{i}:{j}" for i,j in form.items()]
        info("INIT FORM" + "\n".join(li) + "\n\n")

        # error list
        error_list = list()

        # info
        info(f"d_start = {form['date_start']}\n\n")

        form["date_start"], e = FormCheck.__check_date_start(form["date_start"])
        error_list.append(e)
        form["date_stop"], e = FormCheck.__check_date_stop(form["date_stop"])
        error_list.append(e)

        li = [f"{i}:{j}" for i,j in form.items()]
        info("END FORM" + "\n".join(li) + "\n\n")

        # clean error list
        error_list = [i for i in error_list if i]

        return error_list





# INFO:root:ImmutableMultiDict([('date_start', '2018-02-12'),
#     ('date_stop', ''),
#     ('country', 'france'),
#     ('top', '50'),
#     ('hippo', ''),
#     ('quinte', 'all'),
#     ('price_min', '0'),
#     ('price_max', '10 000 000'),
#     ('monte', 'on'),
#     ('attele', 'on'),
#     ('bet_type', 'winning'),
#     ('stratey_type', 'n_winning_cote')])
