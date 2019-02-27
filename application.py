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
    errors = FormCheck.check(request.form)
    if errors :
        return render_template("index.html", errors=errors)
    else :
        return render_template("turfing.html")
