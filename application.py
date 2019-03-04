#!/usr/bin/env python3
# coding: utf-8


# import

from flask          import Flask, render_template, request, session, url_for, flash, redirect
from flask_session  import Session
from tempfile       import mkdtemp


from src.misc       import *
from src.webapp     import FormCheck, App, RegistrationForm, LoginForm
from src.turfing    import BetRoom, TurfingRoom
from strats.easy    import Strats


# dataframe
df          = pk_load("WITHOUT_RESULTS_pturf_grouped_and_merged_cache_carac_2016-2019_OK", "data/")


# init flask and Session
app = Flask(__name__)
app.config["SESSION_FILE_DIR"]  = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"]      = "filesystem"
app.config["SECRET_KEY"]        = "10e5cc248f27ad663a6a19a424067b8ff9217916fe87a1a1209c7b1f2ef56cc8"
Session(app)


# default values for index
index_data  = { "hippo_list"    : sorted(df.hippo.unique()), 
                "typec_list"    : df.typec.dropna().value_counts().index, 
                "today"         : web_today(),
                "date_start"    : "2017-01-01", # timestamp_to_str(int_to_timestamp(df.jour.min()))
                "bet_list"      : BetRoom.bets_str,
                "strat_list"    : Strats.strats  }


# routes
@app.route("/index", methods=["GET", "POST"])
@app.route("/",methods=["GET", "POST"])
def index():
    """index page"""

    return render_template("index.html", index_data=index_data)


@app.route("/turfing", methods=["POST"])
def turfing():
    """main app page"""

    form, errors = FormCheck.check(request.form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template("index.html", errors=errors, index_data=index_data)
  
    results, errors = App.run(df, form, verbose=True)
    info(f"ERRRORS = {errors}")
    if errors : return render_template( "index.html", 
                                        errors=errors, 
                                        index_data=index_data)

    return render_template("turfing.html", title="results", results=results)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """register page"""

    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    """login page """

    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'azertyaz':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)


# main
def main() : 
    """main"""

    app.run(debug=True)



# called as main
if __name__ == '__main__':
    main()
