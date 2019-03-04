#!/usr/bin/env python3
# coding: utf-8


# import
from src.misc       import *
from src.webapp     import FormCheck, App
from flask          import Flask, render_template, request, session, url_for
from flask_session  import Session
from tempfile       import mkdtemp



# dataframe
df          = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")
index_data  = { "hippo_list": sorted(df.hippo.unique()), 
                "typec_list": df.typec.dropna().value_counts().index, 
                "today"     : web_today()}


# init flask and Session
app = Flask(__name__)
app.config["SESSION_FILE_DIR"]  = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]      = "filesystem"
Session(app)


# routes
@app.route("/home")
@app.route("/index")
@app.route("/")
def index():
    """index page"""

    return render_template( "index.html", index_data=index_data)


@app.route("/fancy_index")
def fancy_index():
    """andother index"""


    return render_template( "index.html", index_data=index_data)


@app.route("/turfing", methods=["POST"])
def turfing():
    """main app page"""

    form, errors = FormCheck.check(request.form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template("index.html", errors=errors, index_data=index_data)
  
    results, errors = App.run(df, form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template("index.html", errors=errors, index_data=index_data)

    return render_template("turfing.html", results=results)


def main() : 
    """main"""

    app.run(debug=True)


if __name__ == '__main__':
    main()
