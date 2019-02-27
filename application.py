#!/usr/bin/env python3
# coding: utf-8


# import
from src.misc import *
from src.app import FormCheck
from flask import Flask, render_template, request

# init
app = Flask(__name__)

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/turfing", methods=["POST"])
def turfing():
    form, errors = FormCheck.check(request.form, verbose=True)
    if errors :
        return render_template("index.html", errors=errors)
    else : 
        results = AppBackTurf.run(df, form)
        return render_template("turfing.html", results=results)
