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



try : 
    soup = BeautifulSoup(html, 'html.parser') 
    result_block = soup.find_all('table', attrs={'class': "table table-condensed tablesorter"})
except Exception as e :
    s = f"error request {e} for url {url}"
    warning(s)



# look for just 1 table
if len(result_block) == 1  : 
    table = result_block[0]
else : 
    s = f"error  BS4 len {len(result_block)} for url {url}"
    warning(s)




cols = pd.read_html(str(table))[0].columns