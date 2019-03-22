#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc    import *
from backturfer.model   import *
from backturfer.strats  import * 


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


    plateforms  = ['pmu', 'pmu.fr', 'leturf.fr']

    strat_comp  = list()


    def give_me_bets() : 
        """give str ref of avialables bets type for user"""

        li = [(j[0].ljust(15, " "), i) for i, j in Bet.bets_str.items()]
        li = [f"{i} : {j}" for i,j in li]
        return "\n".join(li)


    def __init__(self, bet_type, strat, N=0, n=0, plateform='pmu', verbose=True) : 

        assert isinstance(bet_type, str) 
        assert bet_type in Bet.bets_str.keys()
        assert isinstance(verbose, bool)
        assert callable(strat)
        assert isinstance(N, int)
        assert isinstance(n, int)
        assert isinstance(plateform, str)
        assert plateform in Bet.plateforms

        bet_type     = bet_type.lower()
        _strat_class = strat.Class.lower()

        if not "multi" in _strat_class : 

            check_dict = {  "simple":"simple", 
                            "couple":"couple", "deux_sur_quatre":"couple", 
                            "tierce":"trio", "trio":"trio", 
                            "quinte" : "quinte"}

            key = [i for i in check_dict.keys() if i in bet_type]
            debug(key)
            key = key[0]

            if (not check_dict[key] in _strat_class) : 
                    raise AttributeError(f"Bet.__init__ : incompatibilty between bet_type {bet_type} and strat {strat}")

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

        _df["bet_autorized"] = self.__define_bet_status(_df)
        _df["bet_horses"]    = self.__find_bet_horses(_df)
        _df["win_horses"]    = self.__find_wining_horses(_df)
        _df["bet_or_not"]    = self.__define_bet_or_not(_df) 
        _df["good_bet"]      = self.__define_good_bet(_df)
        _df["cote"]          = self.__find_cote(_df, self.plateform)
        _df["gains"]         = _df.good_bet * _df.cote * _df.bet_or_not * _df.bet_autorized       

        # _run = eval(f"Bet.{self.bet_type}")
        # _df = _run(df=_df, strat=self.strat, N=self.N, n=self.n, verbose=self.verbose)
        
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
            return _df.partant_cache >= 8
        elif "trio" in self.bet_type : 
            # Pour les courses d'au moins 8 partants (hors course Quinté+), trouvez les trois premiers chevaux de l'arrivée, quel que soit l'ordre.
            # TRIO_ORDRE
            # Pour les courses des réunions nationales comportant de 4 à 7 partants maximum (hors courses exclusives internet et courses étrangères 
            # en masse commune), trouvez les trois premiers chevaux dans l’ordre exact d’arrivée. 
            return (_df.partant_cache >= 8) * (~_df.quinte) 
        elif "deux" in self.bet_type : 
            # Au DEUX_SUR_QUATRE, vous devez désigner deux chevaux d’une même course parmi les quatre premiers, quel que soit l’ordre d’arrivée. Votre pari est donc 
            # payable si les deux chevaux choisis occupent deux des quatre premières places de l’épreuve.
            # Le 2sur4 est proposé sur toutes les courses d’au moins 10 partants.
            return _df.partant_cache >=10
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

        _bt = self.bet_type
        debug(f"bet type {_bt}")
        debug(f"bet type {type(_bt)}")
        if "simple" in _bt                          : _n_horses = 1
        elif ("couple" in _bt) or ("deux" in _bt)   : _n_horses = 2
        elif ("trio" in _bt) or ("tierce" in _bt)   : _n_horses = 3
        elif "quinte"  in _bt                       : _n_horses = 5
        else : raise AttributeError("Bet.run : something went wrong : 0")
        
        return  _df.results.apply(lambda i : self.strat(i, self.N, _n_horses) )


    def __find_wining_horses(self, _df) : 

        _bt = self.bet_type
        if "simple_gagnant" == _bt              : _n_wining = 1    
        elif "simple_place" == _bt              : _n_wining = 3 
        elif "couple_place" == _bt              : _n_wining = 3 
        elif "couple" in _bt                    : _n_wining = 2
        elif "deux" in _bt                      : _n_wining = 4        
        elif ("trio" in _bt) or("tier" in _bt)  : _n_wining = 3  
        elif "quinte"  in _bt                   : _n_wining = 5 
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
            debug(f"type win_horses {type(_df.win_horses.iloc[0])}")
            debug(f"type bet_horses {type(_df.bet_horses.iloc[0])}")            
            assert isinstance(int(_df.win_horses.iloc[0]), int) and isinstance(int(_df.bet_horses.iloc[0]), int)
            return _df.bet_horses == _df.win_horses
        elif "simple_place" == self.bet_type : 
            debug(f"len win_horses {len(_df.win_horses.iloc[0])}")
            debug(f"type bet_horses {type(_df.bet_horses.iloc[0])}")
            assert (len(_df.win_horses.iloc[0]) == 3) and isinstance(int(_df.bet_horses.iloc[0]), int)
            return _df.apply(lambda i : i.bet_horses in i. win_horses, axis=1)   
        elif "couple_gagnant" == self.bet_type: 
            # debug(f"len win_horses {len(_df.win_horses.iloc[0])}")
            # debug(f"len bet_horses {len(_df.bet_horses.iloc[0])}")
            assert (len(_df.win_horses.iloc[0]) == 2) and (len(_df.bet_horses.iloc[0]) == 2)
            return _df.apply(lambda i :   (i.bet_horses[0] in i.win_horses[:2]) \
                                        * (i.bet_horses[1] in i.win_horses[:2]) , axis=1)  
        elif "couple_place" == self.bet_type  : 
            assert (len(_df.win_horses.iloc[0]) == 3) and (len(_df.bet_horses.iloc[0]) == 2)
            return _df.apply(lambda i :   (i.bet_horses[0] in i.win_horses) \
                                        * (i.bet_horses[1] in i.win_horses) , axis=1)   
        elif "couple_ordre" == self.bet_type  :
            debug(f"len win_horses {len(_df.win_horses.iloc[0])}")
            debug(f"len bet_horses {len(_df.bet_horses.iloc[0])}")
            assert (len(_df.win_horses.iloc[0]) == 2) and (len(_df.bet_horses.iloc[0]) == 2)
            return _df.apply(lambda i :   (i.bet_horses[0] == i.win_horses[0]) \
                                        * (i.bet_horses[1] == i.win_horses[1]) , axis=1)   
        elif ("trio_ordre" in self.bet_type) or ("tierce_ordre" in self.bet_type): 
            assert (len(_df.win_horses.iloc[0]) == 3) and (len(_df.bet_horses.iloc[0]) == 3)
            return _df.apply(lambda i :   (i.bet_horses[0] == i.win_horses[0]) \
                                        * (i.bet_horses[1] == i.win_horses[1]) \
                                        * (i.bet_horses[2] == i.win_horses[2]) , axis=1)   
        elif ("trio_desordre"in self.bet_type) or ("tierce_desordre" in self.bet_type): 
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
            debug(f"plateform {plateform}")
            debug(f"_cotes.type {_cotes.type}")
            debug(f"_bet_type {_bet_type}")
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


        def funct_3(comp, horses, _bet_type, plateform) : 
            
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
            debug(f"list cols : {_df.columns}")
            return _df.apply(lambda i : funct_1(i.comp, self.bet_type, 
                                        plateform) 
                                        if i.good_bet else -1, axis=1 )
        elif self.bet_type == "simple_place" : 
            return _df.apply(lambda i : funct_2(i.comp, i.bet_horses, 
                                        self.bet_type, plateform) 
                                        if i.good_bet else -1, axis=1)
        elif self.bet_type == "couple_place" : 
            return _df.apply(lambda i : funct_3(i.comp, i.bet_horses, 
                                        self.bet_type, plateform) 
                                        if i.good_bet else -1, axis=1)
        else : 
            raise ValueError("something went wrong")



    # def __winner_num(results) : 
    #     """find the number of winner of the race"""

    #     r = results.sort_values("cl", ascending=True, inplace=False)
        
    #     return r.numero.iloc[0]


    # def __winner_cote(results, cote_type="direct") : 
    #     """find the cote of the winner of the race"""

    #     r = results.sort_values("cl", ascending=True, inplace=False)
        
    #     return r[f"cote{cote_type}"].iloc[0]


    def __n_first_nums(results, n=3) : 
        """find the nth first numbers of horses"""

        r = results.sort_values("cl", ascending=True, inplace=False)
        
        return r.numero.iloc[:n].values


    def __n_first_cotes(results, n=3, cote_type="direct") :
        """find the nth first numbers of horses"""

        r = results.sort_values("cl", ascending=True, inplace=False)
        
        return r[f"cote{cote_type}"].iloc[:n].values
