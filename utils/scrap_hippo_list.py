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


# ref paths
# path = os.getcwd()
# path = path.split("/")
# path = path[:-1]
# path = "/".join(path) + "/"
# os.chdir(path)
logging.info(os.getcwd())


from src.misc import * 


USER_AGENT  = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
url         = "https://www.boturfers.fr/hippodrome"


# get http response, then html
try : 
    response = requests.get(url, headers=USER_AGENT)
    response.raise_for_status()
    html = response.text
except Exception as e :
    s = f"error request {e} for url {url}"
    warning(s)


# find thead
try : 
    soup = BeautifulSoup(html, 'html.parser') 
    result_block = soup.find_all('table', attrs={'id' : 'liste_hippodromes', 'class': "table table-condensed tablesorter"})
except Exception as e :
    s = f"error request {e} for url {url}"
    warning(s)

if len(result_block) == 1  : 
    cols_raw = str(result_block[0])
else : 
    s = f"error  BS4 len {len(result_block)} for url {url}"
    warning(s)

cols_raw = cols_raw.replace("</table>", "")


# find trow
try : 
    soup = BeautifulSoup(html, 'html.parser') 
    result_block = soup.find_all('tr', attrs={ 'class':"hidden-xs"})
except Exception as e :
    s = f"error request {e} for url {url}"
    warning(s)

for result in result_block : 
    cols_raw += str(result)


# end table
cols_raw+="</table>"


# dataframe
df = pd.read_html(cols_raw)[0]

info(f" df shape : {df.shape}")
info(f" df cols :  {df.columns}")





# dataframe manipulation

df = df.loc[:, ["Hippodrome", 
df = df.sort_values('Classement nombre de courses', axis=1)
df["Hippodrome"] = df.Hippodrome.apply(str.lower)
 