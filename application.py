#!/usr/bin/env python3
# coding: utf-8


# import
from src.misc       import *
from src.webapp     import FormCheck, App
from flask          import Flask, render_template, request, session
from flask_session 	import Session
from tempfile 		import mkdtemp


# dataframe
df  = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
hippo = sorted(df.hippo.unique())


# init flask and Session
app = Flask(__name__)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# routes
@app.route("/index")
def index():
	"""index page"""
    return render_template("index.html", today=web_today(), hipo_list=hippo_list)


@app.route("/fancy_index")
def fancy_index():
    """andother index"""
    return render_template("fancy_index.html", today=web_today())


@app.route("/turfing", methods=["POST"])
def turfing():
	"""main app page"""

    form, errors = FormCheck.check(request.form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template("index.html", errors=errors, today=web_today(), hipo_list=hippo_list)
  
    results, errors = App.run(df, form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template("index.html", errors=errors, today=web_today(), hipo_list=hippo_list)

    return render_template("turfing.html", results=results)
