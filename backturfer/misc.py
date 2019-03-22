#!/usr/bin/env python3
# coding: utf-8


# builtin
# import sqlite3
import os, sys, time, pickle, logging, string, secrets
from logging import warning, info, debug
from itertools import product
from multiprocessing import Process, cpu_count
from collections import Iterable, OrderedDict
from tqdm import tqdm
from pprint import pprint

# import dask
# from dask import dataframe as dd
# from dask.distributed import Client
# from dask.multiprocessing import get
# from multiprocessing import cpu_count


# dask_client = Client()


# data
import numpy  as np
import pandas as pd
tqdm.pandas()

# visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()



# logger 
logger = logging.getLogger()
logger.setLevel(logging.WARNING)


# consts
EPOCH_UNIX = pd.Timestamp('1970-01-01 00:00:00')
N_CORES    = cpu_count()


# decorators

class change_repr(object):
    """just a decorator to help repr"""
    
    def __init__(self, functor):

        self.functor     = functor
        self.__name__    = functor.__name__
        self.__doc__     = functor.__doc__
        self.Class       = str(functor).split(" ")[1].split(".")[0]


    def __call__(self, *args, **kwargs):
        return self.functor(*args, **kwargs)


    def __repr__(self):
        return self.functor.__name__


    def __str__(self):
        return self.functor.__name__


def time_size(funct) : 

    def timer_sizer(*param, **params) :  
        """internal funct of time it decorator"""
        
        t0  = time.time() 
        d   = funct(*param, **params) 
        t1  = round(time.time() - t0, 2)
        s   = str(funct)
        s   = s.split("at")
        s   = s[0].strip()
        
        info(f"{s} done in {t1} secondes")
        s   = round(sys.getsizeof(d) / 1000000, 4)
        info(f"data {s} Mo")

        return d 

    return timer_sizer


def time_it(funct) :  
    """time it decorator"""

    def timer(*param, **params) :  
        """internal funct of time it decorator"""
        
        t0 = time.time() 
        d = funct(*param, **params) 
        t1 = round(time.time() - t0, 2)
        s = str(funct)
        s = s.split("at")
        s = s[0].strip()
        info(f"{s} done in {t1} secondes") 

        return d 

    return timer 


def get_size_of(funct) : 

    def get_size(*param, **params) : 

        d = funct(*param, **params)
        s = round(sys.getsizeof(d) / 1000000, 4)
        info(f"data {s} Mo")

        return d

    return get_size
    

# functs
def gsf(i) : 
    """get size of in Mo"""
    s = sys.getsizeof(i) / 1000000
    s = round(s, 2)
    return f'{s} Mo'



def pk_save(data, filename, path) : 

    filename = str(path+filename+".pk")
    with open(filename, 'wb') as f :
        pk = pickle.Pickler(f)
        pk.dump(data)


def pk_load(filename, path) : 

    filename = str(path+filename+".pk")
    with open(filename, 'rb') as f :
        pk = pickle.Unpickler(f)
        return pk.load()


def _clean(path, ext) : 

    files = [f for f in os.listdir(path) if os.path.isfile(path + f)]
    _ = [os.remove(path+i) for i in files if ext in i]


def pk_clean(path) : 
 
    _clean(path, ".pk")


def get_min_max_of(d) : 
    try : 
        D = np.iinfo(d)
        return(D.min, D.max)
    except : 
        D = np.finfo(d)
        return(D.min, D.max)


def get_epoch_unix() :  
    
    return pd.Timestamp('1970-01-01 00:00:00')


def timestamp_to_int(d) : 
    
    return int((d - EPOCH_UNIX).days)


def int_to_timestamp(n) : 
    
    return EPOCH_UNIX + pd.Timedelta(f"{n} days")


def chunks(l, n) : 
    from math import ceil
    numbs =  [ceil(i) for i in np.linspace(0,len(l)+1, n+1)]    
    pairs = list()
    for i, val in enumerate(numbs) : 
        try : 
            pairs.append((numbs[i], numbs[i+1]))
        except : 
            return pairs


def timestamp_to_str(t) : 

    return f'{str(t.year)}-{str(t.month).rjust(2, "0")}-{str(t.day).rjust(2, "0")}'


def reindex(df) : 

    return range(len(df.index))


def web_today() : 
    
    t = pd.Timestamp.today()
    y, m, d = str(t.year), str(t.month).rjust(2, "0") , str(t.day).rjust(2, "0")
    t = f"{y}-{m}-{d}"

    return t 


def int_today() : 
    
    t = pd.Timestamp.today()

    return timestamp_to_int(t)


def get_an_hash(l=20) : 
    """ return a very good random string"""

    return secrets.token_hex()


def force_pseudo_ascii(txt) : 

    for char in list("àâ") : 
        txt = txt.replace(char, "a")

    for char in list("éèêë") : 
        txt = txt.replace(char, "e")

    for char in list("ïî") : 
        txt = txt.replace(char, "i")
    
    for char in list("ôó") : 
        txt = txt.replace(char, "o")

    for char in list("ùü") : 
        txt = txt.replace(char, "u") 

    return txt


def normalize_hippo(txt) : 
    
    txt = txt.lower()
    # txt = txt.replace("-", "")
    txt = txt.replace("  ", " ")
    txt = txt.replace("  ", " ")
    txt = force_pseudo_ascii(txt)
    txt = txt.strip()

    return txt


def random_df(l=10, c=["a", "b", "c"]) : 

    arr = np.random.randint(0, 100, (l, len(c)))

    return pd.DataFrame(arr, columns=c)


