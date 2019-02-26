#!/usr/bin/env python3
# coding: utf-8


# import 
# builtins
import os, logging, requests
from logging import info, warning
from collections import Iterable

# 3rd parts
import pandas as pd
from bs4 import BeautifulSoup
# from googleapiclient.discovery import build
from googlesearch import search


# logger 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# ref paths
# path = os.getcwd()
# path = path.split("/")
# path = path[:-1]
# path = "/".join(path) + "/"
# os.chdir(path)
info(os.getcwd())


# constants
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

REF_MONTHS  = {i+1:j for i,j in enumerate(["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout", "septembre", "octobre", "novembre", "decembre"])}
REF_DAYS    = {i:j for i,j in zip(  ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'], 
                                    ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"])}

START       = pd.Timestamp("2018/01/01")
N_DAYS      = 365



# functions
def build_day_list(start, n_days) : 
    
    return [start + pd.Timedelta(f"{i} day") for i in range(n_days)]


def timestamp_to_readable_str(i) :

    assert isinstance(i, pd.Timestamp)
    return f'{REF_DAYS[i.day_name()]} {i.day} {REF_MONTHS[i.month]} {i.year}'


def timestamp_to_numeric_str(i) : 
    assert isinstance(i, pd.Timestamp)
    
    return f'{str(i.year)}-{str(i.month).rjust(2, "0")}-{str(i.day).rjust(2, "0")}'


def build_google_querry(day, prix, hippo="vincennes", website="paris-turf.com", complement="rapports de la course") : 

    assert isinstance(day, pd.Timestamp)
    assert isinstance(prix, str)

    day = timestamp_to_readable_str(day)
    q =  f"{website} {hippo} {day} prix {prix} {complement}"  
    
    info(q)

    return q.replace(" ", "+")


def read_file(filename, path) : 
    """ depreciated"""

    # arg check
    assert isinstance(filename, str)
    assert isinstance(path, str)

    # valid path and filename
    try :       if not path[-1] == "/" : path+="/"
    except :    pass
    filename +=".txt"

    # read
    with open(path+filename, "r") as f : 
        r = f.read()
    
    return r.strip().replace("\n", "")


def perform_google_querry(querry, stop=10) : 

    # args check
    assert isinstance(querry, str)
    assert isinstance(stop, int)
    assert (stop >=1 and stop <= 20)

    # build url list
    l = list() 
    for url in search(querry,  stop=3): 
        l.append(str(url)) 

    return l


def check_responses(results, day, prix, hippo, website, complement) : 

    # args checks
    assert isinstance(day, pd.Timestamp)
    assert isinstance(prix, str)
    assert isinstance(complement, str)
    assert isinstance(website, str)
    assert isinstance(hippo, str)
    assert isinstance(results, Iterable)
    
    # manage timestamp
    day = timestamp_to_numeric_str(day)
    # info(type(day))

    # check urls 
    l = list()
    for i in results : 
        i = i.lower()
        if website not in i     : continue
        if day not in i         : continue
        if prix not in i        : continue
        if hippo not in i       : continue
        if complement not in i  : continue
        l.append(i)

    return l


def find_websites(day, prix, hippo="vincennes", website="paris-turf.com", complement="rapports") : 

    # our querry
    querry          = build_google_querry(day, prix, hippo, website, complement)
    
    # our urls "candidates"
    results         = perform_google_querry(querry)
    
    # our validated urls
    responses       = check_responses(results, day, prix, hippo, website, complement)

    # return 
    if len(responses) < 1   : return None
    else                    : return responses[0]


def extract_cotes_from_url(url) : 

    # if url is null
    if not url : return None

    # get http response, then html
    response = requests.get(url, headers=USER_AGENT)
    response.raise_for_status()
    html = response.text
    
    # create and parse our soup obj
    soup = BeautifulSoup(html, 'html.parser') 
    result_block = soup.find_all('table', attrs={'class': "table reports first"})

    # look for just 1 table
    assert len(result_block) == 1 
    table = result_block[0]

    # build a good df
    df = pd.read_html(str(table))[0]  
    df.columns = ["horse", "pmu", "pmu.fr", "leturf.fr"]

    # drop winning cote
    df = df.iloc[1:, :]

    # transform df if needed
    df["horse"] = df.horse.apply(lambda i : i.split(" ")[0])
    df.set_index("horse", drop=True, inplace=True) 
    f = lambda i : float(str(i).replace("€", "").strip().replace(",", "."))
    for c in df.columns : 
        df[c] = df[c].apply(f)

    return df



if __name__ == '__main__':

    # params     
    day         = pd.Timestamp("2019-02-17") 
    prix        = "grenade"
    hippo       = "vincennes"

    url = find_websites(day, prix, hippo)




