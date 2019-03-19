#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc    import *
from backturfer.groupby import GroupBy
from strats             import * 


# class
class Bet : 
    """functions for bet in winning and podium mode
    Bet.winning : you bet one horse will win a race
    Bet.podium :  you bet one horse will be on the podium
    Bet.ordered/unorder tierce : you bet 3 horse on the podium, ordered or not
    Bet.ordered/unorder quinte : you think you are Paco Rabanne, please stop drinking to much beers"""

        #               name             str                min bet 
    bets_str    = {'simple_gagnant':    ('simple gagnant',  1.5, ),
                    'simple_place':     ('simple placé',    1.5, ),
                    'couple_gagnant':   ('couple gagnant',  1.5,),
                    'couple_place':     ('couple placé',    1.5, ),
                    'couple_ordre':     ('couple ordre',    1.5,),
                    'deux_sur_quatre':  ('2 sur 4',         3, ),
                    'trio_ordre':       ('trio ordre',      1.5),
                    'trio_desordre':    ('trio désordre',   1.5),
                    'tierce_ordre':     ('tiercé ordre',    1),
                    'tierce_desordre':  ('tiercé désordre', 1),
                    'quinte_ordre':     ('quinté ordre',    2),
                    'quinte_desordre':  ('quinté désordre', 2)      }


    plateforms  = ['hippodrome', 'web', 'indifferent', 'random']

    strat_comp  = list()


    def give_me_bets() : 
        """give str ref of avialables bets type for user"""

        li = [(j[0].ljust(15, " "), i) for i, j in Bet.bets_str.items()]
        li = [f"{i} : {j}" for i,j in li]
        return "\n".join(li)


    def __init__(self, bet_type, strat, N=0, n=0, plateform='hippodrome', verbose=True) : 

        assert isinstance(bet_type, str) 
        assert bet_type in Bet.bets_str.keys()
        assert isinstance(verbose, bool)
        assert callable(strat)
        assert strat.Class == "SimpleStrats"
        assert isinstance(N, int)
        assert isinstance(n, int)
        assert isinstance(plateform, str)
        assert plateform in Bet.plateforms

        self.bet_type   = bet_type
        self.strat      = strat
        self.N          = N
        self.n          = n
        self.plateform  = plateform
        self.bet_min    = Bet.bets_str[bet_type][1]
        self.verbose    = verbose

        if verbose : 
            info(self)


    def run(self, df) : 

        assert isinstance(df, pd.DataFrame)

        if "results" not in df.columns : 
            df = GroupBy.internalize_results(df)

        _bet = eval(f"Bet.{self.bet_type}")
        info(_bet)

        return _bet(df=df, strat=self.strat, N=self.N, n=self.n, verbose=self.verbose)


    def __winner_num(results) : 
        """find the number of winner of the race"""

        r = results.sort_values("cl", ascending=True, inplace=False)
        
        return r.numero.iloc[0]


    def __winner_cote(results, cote_type="direct") : 
        """find the cote of the winner of the race"""

        r = results.sort_values("cl", ascending=True, inplace=False)
        
        return r[f"cote{cote_type}"].iloc[0]


    def __n_first_nums(results, n=3) : 
        """find the nth first numbers of horses"""

        r = results.sort_values("cl", ascending=True, inplace=False)
        
        return r.numero.iloc[:n].values


    def __n_first_cotes(results, n=3, cote_type="direct") :
        """find the nth first numbers of horses"""

        r = results.sort_values("cl", ascending=True, inplace=False)
        
        return r[f"cote{cote_type}"].iloc[:n].values


    def __podium_nums(results) : 
        
        return Bet.__n_first_nums(results, 3)


    def __podium_cotes(results) : 
        
        return Bet.__n_first_cotes(results, 3)


    @change_repr
    def simple_gagnant(df, strat, N=None, mise_min=1.5, verbose=True) : 
        """miser sur un cheval gagnant"""

        assert isinstance(df, pd.DataFrame)
        assert isinstance(verbose, bool)
        assert callable(strat)
        assert strat.Class == "SimpleStrats"
        if N : assert isinstance(N, int)

        _df = df.copy()

        _df["bet_autorized"]     = 1
        _df["bet_horse"]         = _df.results.apply(lambda i : strat(i, N) )
        _df["win_horse"]         = _df.results.apply(Bet.__winner_num)
        _df["bet_or_not"]        = _df.bet_horse.apply(lambda i : 1 if i>=1 else 0)
        _df["good_bet"]          = _df.bet_horse == _df.win_horse
        _df["horse_cote"]        = _df.apply(lambda i :  Bet.__winner_cote(i.results) if i.good_bet else -1.0, axis=1) 
        _df["gains"]             = _df.good_bet * _df.horse_cote  * _df.bet_or_not * _df.bet_autorized

        if verbose : 
            info(_df["gains"].describe())

        return _df


    @change_repr
    def simple_place(df, strat, N=None, mise_min=1.5, verbose=True) : 
        """miser sur un cheavl sur le podium
         - vous gagnez s'il arrive parmi les 3 premiers à l’arrivée dans une course comptant au minimum 8 chevaux inscrits au programme (*)
         - vous gagnez s’il arrive à la première ou à la deuxième place dans une course comptant entre 4 et 7 chevaux inscrits au programme (*)"""

        assert isinstance(df, pd.DataFrame)
        assert isinstance(verbose, int)
        assert callable(strat)
        assert strat.Class == "SimpleStrats"
        if N : assert isinstance(N, int)

        def corected_nums(i) : 
            try :       return int(str(i).strip())
            except :    return i
        
        _df = df.copy()

        _df["bet_autorized"]     = 1
        _df["bet_horse"]         = _df.results.apply(lambda i : strat(i, N) )
        _df["win_horses"]        = _df.results.apply(Bet.__podium_nums)

        _df["good_bet"]          = _df.apply(lambda i : i.bet_horse in i. win_horses, axis=1)        
        
        _df["bet_or_not"]        = _df.bet_horse.apply(lambda i : 1 if i>=1 else 0)

        # find podiumcote of bet_horse
        _df["horse_cote"]        = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"]) or (not (_df.loc[i, "bet_horse"] >= 1)) : 
                continue
        
            horse   = _df.loc[i, "bet_horse"]
            comp    = _df.loc[i, "comp"]
            # results = _df.loc[i, "results"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            mask    = (cotes.type == "simple_place") * cotes.numero.apply(corected_nums) == int(horse)
            cote    = cotes.loc[mask , "pmu"]
            
            try : 
                _df.loc[i, "horse_cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "horse_cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.horse_cote * _df.bet_or_not * _df.bet_autorized 

        if verbose : 
            info(_df["gains"].describe())

        return _df

    @change_repr
    def couple_place(df, strat, N=None, mise_min=1.5, verbose=True): 
        """trouver les 2 des 3 premiers chevux  dans le desordre
        Pour les courses d'au moins 8 partants, au Couplé Placé, trouver deux des trois premiers chevaux de l'arrivée, quel que soit l'ordre."""

        assert isinstance(df, pd.DataFrame)
        assert isinstance(verbose, int)
        assert callable(strat)
        assert strat.Class == "CoupleStrats"
        if N : assert isinstance(N, int)

        _df = df.copy()

        _df["bet_autorized"]     = 1
        _df["bet_horse"]         = _df.results.apply(lambda i : strat(i, N) )
        _df["win_horses"]        = _df.results.apply(Bet.__podium_nums)

        _df["good_bet"]          = _df.apply(lambda i : i.bet_horse in i. win_horses, axis=1)        
        
        _df["bet_or_not"]        = _df.bet_horse.apply(lambda i : 1 if i>=1 else 0)

        # find podiumcote of bet_horse
        _df["horse_cote"]        = -1.0


        raise NotImplementedError


    # @change_repr
    # def couple_gagnant(df, strat, N=None, mise_min=1.5,verbose=True): 
    #     """trouver les 2 premiers dans le desordre
    #         Pour les courses d'au moins 8 partants, au Couplé Gagnant, trouver les deux premiers chevaux de l'arrivée, quel que soit l'ordre."""
        
    #     raise NotImplementedError


    # @change_repr
    # def couple_ordre(df, strat, N=None, mise_min=1.5, verbose=True): 
    #     """ trouver dans l'ordre 1 et 2e cheval
    #     Pour les courses de 4 à 7 partants, au Couplé Ordre, trouver les deux premiers chevaux dans l'ordre exact de l'arrivée."""

    #     raise NotImplementedError


    # @change_repr
    # def trio_desordre(df, strat, N=None, mise_min=1.5, verbose=True): 
    #     """tiercé mais si pas quinte  ???? VERIFIER ???
    #         Pour les courses d'au moins 8 partants (hors course Quinté+), trouvez les trois premiers chevaux de l'arrivée, quel que soit l'ordre."""

    #     raise NotImplementedError


    # @change_repr
    # def trio_ordre(df, strat, N=None, mise_min=1.5, verbose=True): 
    #     """ tiercé mais si pas quinte ???? VERIFIER ???
    #     Pour les courses des réunions nationales comportant de 4 à 7 partants maximum (hors courses exclusives internet et courses étrangères en masse commune), trouvez les trois premiers chevaux dans l’ordre exact d’arrivée. """

    #     raise NotImplementedError


    # @change_repr
    # def deux_sur_quatre(df, strat, N=None, mise_min=3, verbose=True): 
    #     """2 sur les 4 dans le desordre
    #     vous devez désigner deux chevaux d’une même course parmi les quatre premiers, quel que soit l’ordre d’arrivée. Votre pari est donc payable si les deux chevaux choisis occupent deux des quatre premières places de l’épreuve.
    #     Le 2sur4 est proposé sur toutes les courses d’au moins 10 partants.²"""
        
    #     raise NotImplementedError


    # @change_repr
    # def tierce_ordre(df, strat, N=None, mise_min=1, verbose=True):
    #     """tierce ordre
    #     Si vos trois chevaux sont arrivés aux 3 premières places dans l'ordre indiqué, vous gagnez le rapport "Tiercé dans l'ordre"."""

    #     raise NotImplementedError


    # @change_repr    
    # def tierce_desordre(df, strat, N=None, mise_min=1, verbose=True):
    #     """tierce desordre
    #     Si vous avez trouvé les 3 premiers chevaux de la course mais dans un ordre différent de celui de l'arrivée, vous gagnez le rapport "Tiercé dans le désordre"."""

    #     raise NotImplementedError


    # @change_repr
    # def quinte_ordre(df, strat, N=None, mise_min=2, verbose=True):

    #     raise NotImplementedError


    # @change_repr
    # def quinte_desordre(df, strat, N=None, mise_min=2, verbose=True):

    #     raise NotImplementedError



