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
        assert isinstance(N, int)
        assert isinstance(n, int)
        assert isinstance(plateform, str)
        assert plateform in Bet.plateforms

        bet_type = bet_type.lower()
        if "simple" in bet_type : 
            if not ("simple" or "multi") in strat.Class.lower() : 
                raise AttributeError(f"Bet.__init__ : incompatibilty between bet_type {bet_type} and strat {strat}")
        elif "couple" in bet_type : 
            if not ("couple" or "multi") in strat.Class.lower() : 
                raise AttributeError(f"Bet.__init__ : incompatibilty between bet_type {bet_type} and strat {strat}")
        elif "deux_sur_quatre" in bet_type : 
            if not ("couple" or "multi") in strat.Class.lower() : 
                raise AttributeError(f"Bet.__init__ : incompatibilty between bet_type {bet_type} and strat {strat}")
        elif "trio" in bet_type : 
            if not ("trio" or "multi") in strat.Class.lower() : 
                raise AttributeError(f"Bet.__init__ : incompatibilty between bet_type {bet_type} and strat {strat}")
        elif "tierce" in bet_type : 
            if not ("trio" or "multi") in strat.Class.lower() : 
                raise AttributeError(f"Bet.__init__ : incompatibilty between bet_type {bet_type} and strat {strat}")
        elif "quinte" in bet_type : 
            if not ("quinte" or "multi") in strat.Class.lower() : 
                raise AttributeError(f"Bet.__init__ : incompatibilty between bet_type {bet_type} and strat {strat}")
        else : 
            raise AttributeError("Bet.__init__ : unknown error")

        self.bet_type   = bet_type.lower()
        self.strat      = strat
        self.N          = N
        self.n          = n
        self.plateform  = plateform.lower()
        self.bet_min    = Bet.bets_str[bet_type][1]
        self.verbose    = verbose

        if verbose : 
            info(self)


    def run(self, df) : 

        assert isinstance(df, pd.DataFrame)
        assert "comp" in df.columns
        assert "url" in df.columns

        _df = df.copy()

        if "results"  not in _df.columns  : _df = GroupBy.internalize_results(_df)
        if "inscrits" not in _df.columns  : _df["inscrits"] = _df.results.apply(len)

        # _df["bet_autorized"] = self.__define_bet_status(_df)
        # _df["bet_horses"]    = self.__find_bet_horses(_df)
        # _df["win_horses"]    = self.__find_wining_horses(_df)
        # _df["bet_or_not"]    = self.__define_bet_or_not(_df) 
        # _df["good_bet"]      = self.__define_good_bet(_df)
        # _df["cote"]          = self.__find_cote(_df, self.plateform)
        # _df["gains"]         = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized       

        _run = eval(f"Bet.{self.bet_type}")
        _df = _run(df=_df, strat=self.strat, N=self.N, n=self.n, verbose=self.verbose)
        
        return _df 


    def __define_bet_status(self, _df) : 

        if "simple_gagnant" == self.bet_type : 
            # Au SIMPLE, vous devez désigner un cheval parmi les chevaux engagés dans une épreuve.
            #     Si vous le jouez en SIMPLE_GAGNANT ou SIMPLE_GAGNANT_INTERNATIONAL(**) :
            #     vous gagnez s'il arrive premier
            #     Si vous le jouez en SIMPLE_PLACE :
            #      - vous gagnez s'il arrive parmi les 3 premiers à l’arrivée dans une course comptant au minimum 8 chevaux inscrits au programme (*)
            #      - vous gagnez s’il arrive à la première ou à la deuxième place dans une course comptant entre 4 et 7 chevaux inscrits au programme (*)
            #     Si vous le jouez en SIMPLE_PLACE_INTERNATIONAL(**) : Vous gagnez s’il arrive soit parmi les 2 premiers, soit parmi les 3 premiers à l’arrivée(**)
            return [True, ] * len(_df)
        elif "simple_place" == self.bet_type : 
            return _df.inscrits >= 8
        elif "couple" in self.bet_type : 
            # Pour les courses d'au moins 8 partants, au Couplé Gagnant, trouver les deux premiers chevaux de l'arrivée, quel que soit l'ordre.
            # Pour les courses d'au moins 8 partants, au Couplé Placé, trouver deux des trois premiers chevaux de l'arrivée, quel que soit l'ordre.
            # Pour les courses de 4 à 7 partants, au Couplé Ordre, trouver les deux premiers chevaux dans l'ordre exact de l'arrivée.
            return _df.partants >= 8
        elif "trio" in self.bet_type : 
            # Pour les courses d'au moins 8 partants (hors course Quinté+), trouvez les trois premiers chevaux de l'arrivée, quel que soit l'ordre.
            # TRIO_ORDRE
            # Pour les courses des réunions nationales comportant de 4 à 7 partants maximum (hors courses exclusives internet et courses étrangères 
            # en masse commune), trouvez les trois premiers chevaux dans l’ordre exact d’arrivée. 
            return (_df.partants >= 8) * (~_df.quinte) 
        elif "deux" in self.bet_type : 
            # Au DEUX_SUR_QUATRE, vous devez désigner deux chevaux d’une même course parmi les quatre premiers, quel que soit l’ordre d’arrivée. Votre pari est donc 
            # payable si les deux chevaux choisis occupent deux des quatre premières places de l’épreuve.
            # Le 2sur4 est proposé sur toutes les courses d’au moins 10 partants.
            return _df.partants >=10
        elif "tierce" in self.bet_type : 
            # Le Tiercé se joue une fois par jour.
            # Vous devez désigner trois chevaux d’une même course, en précisant leur ordre de classement à l’arrivée.
            #     Si vos trois chevaux sont arrivés aux 3 premières places dans l'ordre indiqué, vous gagnez le rapport "Tiercé dans l'ordre".
            #     Si vous avez trouvé les 3 premiers chevaux de la course mais dans un ordre différent de celui de l'arrivée, vous gagnez le rapport "Tiercé dans le désordre". 
            return _df.quinte
        elif "quinte" in self.bet_type : 
            #  Le  a lieu 1 fois/jour :
            # Au , vous désignez 5 chevaux d'une même course, en précisant leur ordre de classement à l'arrivée.
            return _df.quinte


    def __find_bet_horses(self, _df) : 

        if "simple" in self.bet_type                  : _n_horses = 1
        elif ("couple" or "deux") in self.bet_type    : _n_horses = 2
        elif ("trio" or "tierce") in self.bet_type    : _n_horses = 3
        elif "quinte"            in self.bet_type     : _n_horses = 5
        else : raise AttributeError("Bet.run : something went wrong : 0")
        
        return  _df.results.apply(lambda i : self.strat(i, self.N, _n_horses) )


    def __find_wining_horses(self, _df) : 

        if "simple_gagnant" == self.bet_type          : _n_wining = 1    
        elif "simple_place" == self.bet_type          : _n_wining = 3 
        elif "couple_place" == self.bet_type          : _n_wining = 3 
        elif "couple" in self.bet_type                : _n_wining = 2
        elif "deux" in self.bet_type                  : _n_wining = 4        
        elif ("trio" or "tier") in self.bet_type      : _n_wining = 3  
        elif "quinte"  in self.bet_type               : _n_wining = 5 
        else : raise AttributeError("Bet.run : something went wrong : 1")
        
        return  _df.results.apply(lambda i : Bet.__n_first_nums(i, _n_wining))


    def __define_bet_or_not(self, _df) : 
        
        def f(i) : 
            if not isinstance(i, Iterable) : 
                return True if i > 0 else False
            else :
                return len([_i for _i in i if _i>0]) == len(i)

        return  _df.bet_horses.apply(f)
        

    def __define_good_bet(self, _df) : 

        if "simple_gagnant" == self.bet_type :             
            assert isinstance(_df.win_horses.iloc[0], int) and isinstance(_df.bet_horses.iloc[0], int)
            return _df.bet_horses == _df.win_horses
        elif "simple_place" == self.bet_type : 
            assert (len(_df.win_horses.iloc[0]) == 3) and isinstance(_df.bet_horses.iloc[0], int)
            return _df.apply(lambda i : i.bet_horses in i. win_horses, axis=1)   
        elif "couple_gagnant" == self.bet_type: 
            assert (len(_df.win_horses.iloc[0]) == 3) and (len(_df.bet_horses.iloc[0]) == 2)
            return _df.apply(lambda i :   (i.bet_horses[0] in i.win_horses[0:2]) \
                                        * (i.bet_horses[1] in i.win_horses[0:2]) , axis=1)  
        elif "couple_place" == self.bet_type  : 
            assert (len(_df.win_horses.iloc[0]) == 3) and (len(_df.bet_horses.iloc[0]) == 2)
            return _df.apply(lambda i :   (i.bet_horses[0] in i.win_horses) \
                                        * (i.bet_horses[1] in i.win_horses) , axis=1)   
        elif "couple_ordre" == self.bet_type  :
            assert (len(_df.win_horses.iloc[0]) == 3) and (len(_df.bet_horses.iloc[0]) == 2)
            return _df.apply(lambda i :   (i.bet_horses[0] == i.win_horses[0]) \
                                        * (i.bet_horses[1] == i.win_horses[1]) , axis=1)   
        elif ("trio_ordre" or "tierce_ordre") in self.bet_type: 
            assert (len(_df.win_horses.iloc[0]) == 3) and (len(_df.bet_horses.iloc[0]) == 3)
            return _df.apply(lambda i :   (i.bet_horses[0] == i.win_horses[0]) \
                                        * (i.bet_horses[1] == i.win_horses[1]) \
                                        * (i.bet_horses[2] == i.win_horses[2]) , axis=1)   
        elif ("trio_desordre" or "tierce_desordre") in self.bet_type: 
            assert (len(_df.win_horses.iloc[0]) == 3) and (len(_df.bet_horses.iloc[0]) == 3)
            return _df.apply(lambda i :   (i.bet_horses[0] in i.win_horses) \
                                        * (i.bet_horses[1] in i.win_horses) \
                                        * (i.bet_horses[2] in i.win_horses) , axis=1)
        elif "deux_sur_quatre" == self.bet_type:
            assert (len(_df.win_horses.iloc[0]) == 4) and (len(_df.bet_horses.iloc[0]) == 2)
            return _df.apply(lambda i :   (i.bet_horses[0] in i.win_horses) 
                                        * (i.bet_horses[1] in i.win_horses) , axis=1)
        elif "quinte_ordre" == self.bet_type : 
            assert (len(_df.win_horses.iloc[0]) == 5) and (len(_df.bet_horses.iloc[0]) == 5)
            return _df.apply(lambda i :   (i.bet_horses[0] == i.win_horses[0]) \
                                        * (i.bet_horses[1] == i.win_horses[1]) \
                                        * (i.bet_horses[2] == i.win_horses[2]) \
                                        * (i.bet_horses[3] == i.win_horses[3]) \
                                        * (i.bet_horses[4] == i.win_horses[4]) , axis=1)    
        elif "quinte_desordre" == self.bet_type : 
            assert (len(_df.win_horses.iloc[0]) == 5) and (len(_df.bet_horses.iloc[0]) == 5)
            return _df.apply(lambda i :   (i.bet_horses[0] in i.win_horses) \
                                        * (i.bet_horses[1] in i.win_horses) \
                                        * (i.bet_horses[2] in i.win_horses) \
                                        * (i.bet_horses[3] in i.win_horses) \
                                        * (i.bet_horses[4] in i.win_horses) , axis=1)    
        else : 
            raise AttributeError("something went wrong")    
    

    def __find_cote(self, _df, plateform="pmu") : 

        def check_cote(cote, comp) : 
            try : 
                cote = float(cote)
                assert (cote >=1.0) and (cote <= 10000000.0)
                return cote
            except :
                s = f"Error for comp {comp}, cote {cote}, type {type(cote)}" 
                warning(s)
                return -1.0


        def funct_1(comp, _bet_type, plateform) : 
            _cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote     = _cotes.loc[_cotes.type == _bet_type, plateform]

            return check_cote(cote, comp)


        def funct_2(comp, horse, _bet_type, plateform) : 

            def corected_nums(i) : 
                try :       return int(str(i).strip())
                except :    return i

            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            mask    =     (cotes.type == _bet_type) \
                        * (cotes.numero.apply(corected_nums) == int(horse))
            cote    = cotes.loc[mask , plateform]

            return check_cote(cote, comp)


        def funct_3(comp, horse, _bet_type, plateform) : 
            
            def corrected_nums(i) : 
                if isinstance(i, list):
                    if (len(i) == 2) and isinstance(i[0], int) and isinstance(i[1], int) : 
                        return i
                    else : 
                        raise ValueError("wrong shape for cotes of couple_place : a list but not good")
                elif isinstance(i, str) : 
                    i = i.split("-")
                    assert len(i) == 2
                    i = [ii.strip() for ii in i]
                    i = [int(ii) for ii in i]
                    return i 
                else : 
                    info(type(i))
                    info(i)
                    # raise ValueError("cotes of couple_place : not a list not an str")
                return None

            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cotes    = cotes.loc[cotes.type == "couple_place" , :]
            cotes["numero"] = cotes.numero.apply(corrected_nums)
            # info(cotes.numero)
            # info(f"{horses[0]}, {horses[1]}")
            mask = cotes.numero.apply(lambda i : (horses[0] in i) and (horses[1] in i))
            # info(mask)
            cote = cotes.loc[mask.values, plateform]

            return check_cote(cote, comp)


        if self.bet_type in [   'simple_gagnant', 'couple_gagnant', 'couple_ordre',      
                                'trio_desordre', 'trio_ordre', 'deux_sur_quatre',
                                'tierce_ordre', 'tierce_desordre', 
                                'quinte_ordre','quinte_desordre' ] : 
            return _df.apply(lambda i : funct_1(i.comp, self.bet_type, 
                                        plateform) 
                                        if i.good_bet else -1 )
        elif self.bet_type == "simple_place" : 
            return _df.apply(lambda i : funct_2(i.comp, i.bet_horses, 
                                        self.bet_type, plateform) 
                                        if i.good_bet else -1 )
        elif self.bet_type == "couple_place" : 
            return _df.apply(lambda i : funct_3(i.comp, i.bet_horses, 
                                        self.bet_type, plateform) 
                                        if i.good_bet else -1 )
        else : 
            raise ValueError("something went wrong")



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
    def simple_gagnant(df, strat, N=None, n=1, mise_min=1.5, verbose=True) : 
        """miser sur un cheval gagnant"""

        _df = df.copy()
        _df["bet_autorized"]     = 1
        _df["bet_horse"]         = _df.results.apply(lambda i : strat(i, N) )
        _df["win_horse"]         = _df.results.apply(Bet.__winner_num)
        _df["bet_or_not"]        = _df.bet_horse.apply(lambda i : 1 if i>=1 else 0)
        _df["good_bet"]          = _df.bet_horse == _df.win_horse
        _df["cote"]              = _df.apply(lambda i :  Bet.__winner_cote(i.results) if i.good_bet else -1.0, axis=1) 
        _df["gains"]             = _df.good_bet * _df.cote  * _df.bet_or_not * _df.bet_autorized

        if verbose : 
            info(_df["gains"].describe())

        return _df


    @change_repr
    def simple_place(df, strat, N=None, n=1, mise_min=1.5, verbose=True) : 
        """miser sur un cheavl sur le podium
         - vous gagnez s'il arrive parmi les 3 premiers à l’arrivée dans une course comptant au minimum 8 chevaux inscrits au programme (*)
         - vous gagnez s’il arrive à la première ou à la deuxième place dans une course comptant entre 4 et 7 chevaux inscrits au programme (*)"""

        def corected_nums(i) : 
            try :       return int(str(i).strip())
            except :    return i
        
        _df = df.copy()

        _df["bet_autorized"]     = 1
        _df["bet_horse"]         = _df.results.apply(lambda i : strat(i, N) )
        _df["win_horses"]        = _df.results.apply(Bet.__podium_nums)
        _df["good_bet"]          = _df.apply(lambda i : i.bet_horse in i. win_horses, axis=1)        
        _df["good_bet"]          = _df.good_bet.apply(bool)
        _df["bet_or_not"]        = _df.bet_horse.apply(lambda i : 1 if i>=1 else 0)

        # find podiumcote of bet_horse
        _df["cote"]        = -1.0

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
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        if verbose : 
            info(_df["gains"].describe())

        return _df

    @change_repr
    def couple_place(df, strat, N=None, n=2, mise_min=1.5, verbose=True): 
        """trouver les 2 des 3 premiers chevux  dans le desordre
        Pour les courses d'au moins 8 partants, au Couplé Placé, trouver deux des trois premiers chevaux de l'arrivée, quel que soit l'ordre."""

        def correct_nums(i) : 

            if isinstance(i, list):
                if (len(i) == 2) and isinstance(i[0], int) and isinstance(i[1], int) : 
                    return i
                else : 
                    raise ValueError("wrong shape for cotes of couple_place : a list but not good")
            elif isinstance(i, str) : 
                i = i.split("-")
                assert len(i) == 2
                i = [ii.strip() for ii in i]
                i = [int(ii) for ii in i]
                return i 
            else : 
                info(type(i))
                info(i)
                # raise ValueError("cotes of couple_place : not a list not an str")
            return None

        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=2) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 3))
        _df["good_bet"]         = _df.apply(lambda i : (i.bet_horses[0] in i.win_horses) * (i.bet_horses[1] in i.win_horses) , axis=1)      
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 3 else 0)
        _df["cote"]      = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cotes    = cotes.loc[cotes.type == "couple_place" , :]
            cotes["numero"] = cotes.numero.apply(correct_nums)
            # info(cotes.numero)
            # info(f"{horses[0]}, {horses[1]}")
            mask = cotes.numero.apply(lambda i : (horses[0] in i) and (horses[1] in i))
            # info(mask)
            cote = cotes.loc[mask.values, "pmu"]

            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  

        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df 


    @change_repr
    def couple_gagnant(df, strat, N=None,  n=2, mise_min=1.5,verbose=True): 
        """trouver les 2 premiers dans le desordre
            Pour les courses d'au moins 8 partants, au Couplé Gagnant, trouver les deux premiers chevaux de l'arrivée, quel que soit l'ordre."""

        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=2) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 2))
        _df["good_bet"]         = _df.apply(lambda i : (i.bet_horses[0] in i.win_horses) * (i.bet_horses[1] in i.win_horses) , axis=1)    
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 2 else 0)
        _df["cote"]      = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote    = cotes.loc[cotes.type == "couple_gagnant" , "pmu"]
            
            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df


    @change_repr
    def couple_ordre(df, strat, N=None, n=2, mise_min=1.5, verbose=True): 
        """ trouver dans l'ordre 1 et 2e cheval
        Pour les courses de 4 à 7 partants, au Couplé Ordre, trouver les deux premiers chevaux dans l'ordre exact de l'arrivée."""

        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=2) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 2))
        _df["good_bet"]         = _df.apply(lambda i : (i.bet_horses[0] == i.win_horses[0]) * (i.bet_horses[1] == i.win_horses[1]) , axis=1)    
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 2 else 0)
        _df["cote"]      = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote    = cotes.loc[cotes.type == "couple_gagnant" , "pmu"]
            
            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df


    @change_repr
    def trio_desordre(df, strat, N=None, n=3, mise_min=1.5, verbose=True): 
        """tiercé mais si pas quinte  ???? VERIFIER ???
            Pour les courses d'au moins 8 partants (hors course Quinté+), trouvez les trois premiers chevaux de l'arrivée, quel que soit l'ordre."""

        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=3) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 3))
        _df["good_bet"]         = _df.apply(lambda i :    (i.bet_horses[0] == i.win_horses[0]) \
                                                        * (i.bet_horses[1] == i.win_horses[1]) \
                                                        * (i.bet_horses[2] == i.win_horses[2]) , axis=1)    
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 3 else 0)
        _df["cote"]        = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote    = cotes.loc[cotes.type == "trio_ordre" , "pmu"]
            
            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df


    @change_repr
    def trio_ordre(df, strat, N=None, n=3, mise_min=1.5, verbose=True): 
        """ tiercé mais si pas quinte ???? VERIFIER ???
        Pour les courses des réunions nationales comportant de 4 à 7 partants maximum (hors courses exclusives internet et courses étrangères en masse commune), trouvez les trois premiers chevaux dans l’ordre exact d’arrivée. """

        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=3) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 3))
        _df["good_bet"]         = _df.apply(lambda i :    (i.bet_horses[0] in i.win_horses) \
                                                        * (i.bet_horses[1] in i.win_horses) \
                                                        * (i.bet_horses[2] in i.win_horses) , axis=1)    
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 3 else 0)
        _df["cote"]      = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote    = cotes.loc[cotes.type == "trio_ordre" , "pmu"]
            
            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df



    @change_repr
    def deux_sur_quatre(df, strat, N=None, n=2, mise_min=3, verbose=True): 
        """2 sur les 4 dans le desordre
        vous devez désigner deux chevaux d’une même course parmi les quatre premiers, quel que soit l’ordre d’arrivée. Votre pari est donc payable si les deux chevaux choisis occupent deux des quatre premières places de l’épreuve.
        Le 2sur4 est proposé sur toutes les courses d’au moins 10 partants.²"""
        
        """trouver les 2 premiers dans le desordre
            Pour les courses d'au moins 8 partants, au Couplé Gagnant, trouver les deux premiers chevaux de l'arrivée, quel que soit l'ordre."""

        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=2) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 4))
        _df["good_bet"]         = _df.apply(lambda i : (i.bet_horses[0] in i.win_horses) * (i.bet_horses[1] in i.win_horses) , axis=1)    
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 2 else 0)
        _df["cote"]      = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote    = cotes.loc[cotes.type == "deux_sur_quatre" , "pmu"]
            
            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  

        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df


    @change_repr
    def tierce_ordre(df, strat, N=None, n=3, mise_min=1, verbose=True):
        """tierce ordre
        Si vos trois chevaux sont arrivés aux 3 premières places dans l'ordre indiqué, vous gagnez le rapport "Tiercé dans l'ordre"."""

        return Bet.trio_ordre(df, strat, N=N, n=n, mise_min=mise_min, verbose=verbose)


    @change_repr    
    def tierce_desordre(df, strat, N=None, n=3, mise_min=1, verbose=True):
        """tierce desordre
        Si vous avez trouvé les 3 premiers chevaux de la course mais dans un ordre différent de celui de l'arrivée, vous gagnez le rapport "Tiercé dans le désordre"."""

        return Bet.trio_desordre(df, strat, N=N, n=n, mise_min=mise_min, verbose=verbose)


    @change_repr
    def quinte_desordre(df, strat, N=None, n=5,mise_min=2, verbose=True):
        """ tiercé mais si pas quinte ???? VERIFIER ???
        Pour les courses des réunions nationales comportant de 4 à 7 partants maximum (hors courses exclusives internet et courses étrangères en masse commune), trouvez les trois premiers chevaux dans l’ordre exact d’arrivée. """

        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=5) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 5))
        _df["good_bet"]         = _df.apply(lambda i :    (i.bet_horses[0] in i.win_horses) \
                                                        * (i.bet_horses[1] in i.win_horses) \
                                                        * (i.bet_horses[2] in i.win_horses) \
                                                        * (i.bet_horses[3] in i.win_horses) \
                                                        * (i.bet_horses[4] in i.win_horses) , axis=1)    
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 5 else 0)
        _df["cote"]        = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote    = cotes.loc[cotes.type == "quinte_desordre" , "pmu"]
            
            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df


    @change_repr
    def quinte_ordre(df, strat, N=None, n=5, mise_min=2, verbose=True):
        """ tiercé mais si pas quinte ???? VERIFIER ???
        Pour les courses des réunions nationales comportant de 4 à 7 partants maximum (hors courses exclusives internet et courses étrangères en masse commune), trouvez les trois premiers chevaux dans l’ordre exact d’arrivée. """


        _df = df.copy()

        _df["bet_autorized"]    = 1
        _df["bet_horses"]       = _df.results.apply(lambda i : strat(i, N, n=5) )
        _df["win_horses"]       = _df.results.apply(lambda i : Bet.__n_first_nums(i, 5))
        _df["good_bet"]         = _df.apply(lambda i :    (i.bet_horses[0] == i.win_horses[0]) \
                                                        * (i.bet_horses[1] == i.win_horses[1]) \
                                                        * (i.bet_horses[2] == i.win_horses[2]) \
                                                        * (i.bet_horses[3] == i.win_horses[3]) \
                                                        * (i.bet_horses[4] == i.win_horses[4]) , axis=1)    
        _df["good_bet"]         = _df.good_bet.apply(bool)
        _df["bet_or_not"]       = _df.bet_horses.apply(lambda i : 1 if len(i) == 5 else 0)
        _df["cote"]        = -1.0

        for i in _df.index : 
            if (not _df.loc[i, "good_bet"])  : 
                continue        
            horses   = _df.loc[i, "bet_horses"]
            comp    = _df.loc[i, "comp"]
            cotes   = pk_load(f"comp-{comp}", "data/cotes/")  
            cote    = cotes.loc[cotes.type == "quinte_ordre" , "pmu"]
            
            try : 
                _df.loc[i, "cote"] = float(cote)             
            except : 
                warning(comp)
                warning(cote)
                _df.loc[i, "bet_or_not"] = False
                _df.loc[i, "cote"] = -1.0  


        _df["gains"]             = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized 

        return _df







