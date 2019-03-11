#!/usr/bin/env python3
# coding: utf-8


from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, SubmitField, IntegerField, BooleanField
from wtforms.validators import * 




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

        race_sel = RaceSelector(form, hard_check=False)

        if race_sel.errors : 
            return errors
        else :
            df = race_sel.perform(df, hard_check=True, force_consistancy=True)

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











