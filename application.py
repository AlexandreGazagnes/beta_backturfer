#!/usr/bin/env python3
# coding: utf-8


# import
from src.misc       import *
from src.webapp     import FormCheck, App
from flask          import Flask, render_template, request


# time 
t0 =time.time()


# dataframe
df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")

# init
app = Flask(__name__)


@app.route("/index")
def index():

    return render_template("index.html", today=web_today())

@app.route("/fancy_index")
def fancy_index():

    return render_template("fancy_index.html", today=web_today())

@app.route("/turfing", methods=["POST"])
def turfing():

    form, errors = FormCheck.check(request.form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template("index.html", errors=errors, today=web_today())
  
    results, errors = App.run(df, form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template("index.html", errors=errors, today=web_today())

    return render_template("turfing.html", results=results)
