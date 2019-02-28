#!/usr/bin/env python3
# coding: utf-8


# import
from src.misc       import *
from src.webapp     import FormCheck, App
from flask          import Flask, render_template, request


# time 
t0 =time.time()


# dataframe
df  = pk_load("pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
info(f"df, loaded : {round(time.time() - t0, 2)}")
t0 =time.time()

# init
app = Flask(__name__)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/turfing", methods=["POST"])
def turfing():
    form, errors = FormCheck.check(request.form, verbose=True)
    
    info(f"ERRRORS = {errors}")

    if errors :
        return render_template("index.html", errors=errors)
  
    results, errors = App.run(df, form, verbose=True)
    if errors : 
        return render_template("index.html", errors=errors)

    return render_template("turfing.html", results=results)
