#!/usr/bin/env python3
# coding: utf-8


# builtin
# import sqlite3
import os, sys, time, pickle, logging
from logging import warning, info
from itertools import product
from multiprocessing import Process
from collections import Iterable
from tqdm import tqdm


# data
import numpy  as np
import pandas as pd
tqdm.pandas()


# logger 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# consts
EPOCH_UNIX = pd.Timestamp('1970-01-01 00:00:00')



# class
class change_repr(object):
    """just a decorator to help repr"""
    
    def __init__(self, functor):
        self.functor = functor

        #  lets copy some key attributes from the original function
        self.__name__ = functor.__name__
        self.__doc__ = functor.__doc__

    def __call__(self, *args, **kwargs):
        return self.functor(*args, **kwargs)

    def __repr__(self):
        return self.functor.__name__


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

