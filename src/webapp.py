#!/usr/bin/env python3
# coding: utf-8


from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import * 


from src.misc           import *
from src.build          import Build
from src.groupby        import GroupBy
from strats.easy        import Strats 
from src.turfing        import BetRoom, TurfingRoom




class FormCheck :
    """basic class of funct to manage and clean form"""

    # consts
    __price_min_max = 5000000
    __price_max_min = 1000


    def __check_date_start(d) :
        """check form input for date_start"""

        if not d : 
            return 0, False
        try : 
            d= pd.Timestamp(d)
        except : 
            return 0, "Error : date_start timestamp conversion, invalid format"
    
        if d >= pd.Timestamp.today()  : 
            return 0, "Error : date_start > Today"

        d = timestamp_to_int(d)

        return (d, False)


    def __check_date_stop(d) :
        """check form input for date_stop"""
        if not d :
            return 30000, False
        try : 
            d= pd.Timestamp(d)
        except : 
            return 0, "Error : date_start timestamp conversion, invalid format"

        if d <= pd.Timestamp("2015-12-31") : 
            return 0, "Error : date_stop to old, data start at 2016-01-01"

        d = timestamp_to_int(d)

        return d, False


    def __check_date_comp(date_start, date_stop) :
        
        if date_stop <= date_start : 
            return 0, 0, "Error : Sorry date_start to close/before date_stop" 

        return date_start, date_stop, False


    def __check_country(d) :

        return d, False


    def __check_hippo(d) :

        d = d.strip().lower()
        
        return d, False


    def __check_hippo_comp(country, hippo) :

        if hippo : 
            country = "monde"

        return country, hippo, False


    def __check_quinte(d) :
        
        return d, False


    def __check_price_min(d) :

        _d = d.strip().replace(" ", "").replace("-", "").replace("€", "").strip()

        if not _d :
            return 0, False

        try :
            _d = int(_d)
        except :
            return "", f"Error : invalid price_min recieved {d}, expected and number"

        if _d < 0 : _d = 0
        if _d > FormCheck.__price_min_max :
            return 0, f"Error : invalid price_min, recieved {d}, expected max {FormCheck.__price_min_max}"

        return _d, False


    def __check_price_max(d) :

        _d = d.strip().replace(" ", "").replace("-", "").replace("€", "").strip()

        if not _d :
            return 50000000, False

        try :
            _d = int(_d)
        except :
            return 0, f"Error : invalid price_max recieved {d}, expected and number"

        if _d <= 0 :
            return 0, f"Error : invalid price_max, recieved {d}, expected max positive value"

        if _d < FormCheck.__price_max_min :
            return 0, f"Error : invalid price_max, recieved {d}, expected min {FormCheck.__price_max_min}"

        return _d, False


    def __check_price_comp(price_min, price_max) : 

        if price_min >= price_max : 
            return 0, 0, f"Error : price min {price_min} >= price_max {price_max}"

        return price_min, price_max , False


    def check(form, verbose=False) :

        # transform form in normal dict
        form = {i:j for i,j in form.items()}

        if verbose : 
            li = [f"{i}:{j}" for i,j in form.items()]
            info("INIT FORM" + "\n".join(li) + "\n\n")

        # error list
        error_list = list()

        # dates
        form["date_start"], e = FormCheck.__check_date_start(form["date_start"])
        error_list.append(e)
        form["date_stop"], e = FormCheck.__check_date_stop(form["date_stop"])
        error_list.append(e)
        form["date_start"], form["date_stop"], e = FormCheck.__check_date_comp(form["date_start"], form["date_stop"])
        error_list.append(e)

        # hippodrome
        form["country"], e = FormCheck.__check_country(form["country"])
        error_list.append(e)
        form["hippo"], e = FormCheck.__check_hippo(form["hippo"])
        error_list.append(e)
        form["country"], form["hippo"], e = FormCheck.__check_hippo_comp(form["country"], form["hippo"]) 
        error_list.append(e)

        # race type
        form["price_min"], e = FormCheck.__check_price_min(form["price_min"])
        error_list.append(e)
        form["price_max"], e = FormCheck.__check_price_max(form["price_max"])
        error_list.append(e)
        form["price_min"], form["price_max"], e = FormCheck.__check_price_comp(form["price_min"], form["price_max"])
        error_list.append(e)

        race_types = ["monté", "attelé", "plat", "haies", "steeple-chase", "steeple-chase cross-country"]
        race_types = [i for i in race_types if i in form.keys()]
        [form.pop(i) for i in race_types if i in form.keys()]
        form["typec"] = race_types


        if verbose : 
            li = [f"{i}:{j}" for i,j in form.items()]
            info("END FORM" + "\n".join(li) + "\n\n")

        # clean error list
        assert len(error_list) == 9
        error_list = [i for i in error_list if i]

        return form, error_list


class App:
    """App class""" 


    def __bet(df, form, N=0, verbose=True) : 

        bets_obj = {'simple_gagnant': BetRoom.simple_gagnant,
                    'simple_place': BetRoom.simple_place,
                    'couple_gagnant': BetRoom.couple_gagnant,
                    'couple_place': BetRoom.couple_place,
                    'couple_ordre': BetRoom.couple_ordre,
                    'deux_sur_quatre': BetRoom.deux_sur_quatre,
                    'trio_ordre': BetRoom.trio_ordre,
                    'trio_desordre': BetRoom.trio_desordre,
                    'tierce_ordre': BetRoom.tierce_ordre,
                    'tierce_desordre': BetRoom.tierce_desordre,
                    'quinte_ordre': BetRoom.quinte_ordre,
                    'quinte_desordre': BetRoom.quinte_desordre}


        strats_obj = {  'choix_de_la_meilleure_cote': Strats.choix_de_la_meilleure_cote,
                        'choix_de_la__N__meilleure_cote': Strats.choix_de_la__N__meilleure_cote,
                        'choix_aleatoire_parmi_les_inscrits': Strats.choix_aleatoire_parmi_les_inscrits,
                        'choix_aleatoire_parmi_les_partants': Strats.choix_aleatoire_parmi_les_partants,
                        'choix_aleatoire_parmi_les__N__meilleures_cotes': Strats.choix_aleatoire_parmi_les__N__meilleures_cotes,
                        'choix_aleatoire_parmi_les_3_meilleures_cotes': Strats.choix_aleatoire_parmi_les_3_meilleures_cotes,
                        'ne_jamais_parier': Strats.ne_jamais_parier,
                        'pile_ne_pas_jouer_face_jouer_la_meilleure_cote': Strats.pile_ne_pas_jouer_face_jouer_la_meilleure_cote,
                        'choisir_la_pire_cote_inscrite': Strats.choisir_la_pire_cote_inscrite,
                        'choisir_la_pire_cote_partante': Strats.choisir_la_pire_cote_partante}

        bet_key     = form['bet_type']
        strat_key   = form['strategy']
        _N          = int(form['strategy_n'])

        df          = df = GroupBy.internalize_results(df)
        res         = bets_obj[bet_key](df, strats_obj[strat_key], N=_N, verbose=True)

        delta, bet_ratio, _df = delta, bet_ratio, __df  = TurfingRoom.once( df, 
                                            bets_obj[bet_key], 
                                            strats_obj[strat_key], 
                                            N=N, verbose=True)

        return delta, bet_ratio, _df 



    def run(df, form, verbose=True): 

        assert isinstance(df, pd.DataFrame)
        assert isinstance(form, dict)

        df, errors  = Build.select(df, form)

        if errors : 
            return 0, errors

        txt =list()
        txt.append(f"len df         : {len(df)}")
        txt.append(f"start df       : {int_to_timestamp(df.jour.min())}")
        txt.append(f"stop df        : {int_to_timestamp(df.jour.max())}")
        txt.append(f"df.quinte      : {df.quinte.unique()[:10]}")
        txt.append(f"df.hippo       : {df.hippo.unique()[:10]}")
        txt.append(f"df.cheque_max  : {df.cheque_val.max()}")
        txt.append(f"df.cheque_min  : {df.cheque_val.min()}")
        txt.append(f"df.cheque_type : {df.cheque_type.unique()[:10]}")
        txt.append(f"df.typec       : {df.typec.unique()[:10]}")
        txt.append(f"bet type       : {form['bet_type']}")
        txt.append(f"strategy       : {form['strategy']}")
        txt.append(f"n              : {form['strategy_n']}")

        if verbose : 
            df.to_csv(f"temp/web_df/{get_an_hash()}.csv", index=False)    
            info (txt)


        delta, bet_ratio, _df  = App.__bet(df, form, verbose=True)
        txt.append(f"delta: {delta}")
        txt.append(f"bet_ratio: {bet_ratio}")

        return txt, None












class RegistrationForm(FlaskForm): 
    """form for registration"""

    username        = StringField('username', validators=[DataRequired(), Length(min=2, max=20)])
    email           = StringField('email', validators=[DataRequired(), Email()])
    age             = IntegerField("age", validators=[DataRequired(), NumberRange(1, 135)])
    password        = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20)])
    conf_password   = PasswordField('conf_password', validators=[DataRequired(), EqualTo("password")])
    submit          = SubmitField("sign in")



class LoginForm(FlaskForm): 
    """form for login"""

    email           = StringField('email', validators=[DataRequired(), Email()])
    password        = PasswordField('password', validators=[DataRequired, Length(min=8, max=20)])
    remember        = BooleanField("remember me")
    submit          = SubmitField("log in")



class Turfing(FlaskForm): 
    """form for turf"""

    start               = None
    stop                = None
    country             = None 
    specific_hippo      = None 
    quinte              = None 
    cheque_type         = None
    cheque_val          = None
    race_type           = None 





