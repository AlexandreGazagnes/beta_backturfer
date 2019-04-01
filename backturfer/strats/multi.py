#!/usr/bin/env python3
# coding: utf-8


# import 
from backturfer.misc import *

# class
class MultiStrats : 

    _type       = "strats"
    _subtype    = "multi"

    strats_str  = { 'choix_des__N__meilleures_cotes'      : 'choix des N meilleures_cotes',
                    'choix_aleatoire_parmi_les_inscrits'  : 'choix aléatoire parmi les inscrits',
                    'choix_aleatoire_parmi_les_partants'  : 'choix aléatoire parmi les partants',  
                    'choix_aleatoire_parmi_les__N__meilleures_cotes' : 'choix alétoire parmi les N meilleures cotes', 
                    'ne_jamais_parier' : 'ne_jamais_parier',
                    'choix_aleatoire_entre_les__N__et__M__meilleures_cotes': 'choix_aleatoire entre les N et M  meilleures_cotes',
                    'choix_des__N__pires_cotes_inscrites': 'choix_des__N__pires_cotes_inscrites', 
                    'choix_des_N__pires_cotes_partantes': , 'choix_des_N__pires_cotes_partantes'   }


    @change_repr
    def choix_des__N__meilleures_cotes(results, N, n, cote_type='direct') : 
        """chose the horse with nth best cote"""

        assert isinstance(results, pd.DataFrame)
        len_r = len(results) 
        if not isinstance(int(N), int):  raise ValueError("N should be an int")
        if not isinstance(int(n), int):  raise ValueError("n should be an int")
        if (N>len_r):               raise AttributeError(f"N >= n chevaux : {N} >= {len_r}")
        if (n>len_r):               raise AttributeError(f"n >= n chevaux : {n} >= {len_r}")
        if (n>5) or(n<1) :          raise AttributeError(f"invalid n : {n}")
        if (n>1) and ((n+N)>len_r): raise AttributeError(f"invalid n+N > {n}+{N} > {len_r} ")

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

        if n==1             : return r.numero.iloc[N]
        elif n > 1 and n <6 : return list(r.numero.iloc[N:n+N])
        else                : raise ValueError("choix_des_N__meilleures_cotes")


    @change_repr
    def choix_aleatoire_parmi_les_inscrits(results, N, n, cote_type="direct") : 
        """chose one horse random"""
        N=1

        assert isinstance(results, pd.DataFrame)
        len_r = len(results) 
        if not isinstance(int(N), int):  raise ValueError("N should be an int")
        if not isinstance(int(n), int):  raise ValueError("n should be an int")
        if (N>len_r):               raise AttributeError(f"N >= n chevaux : {N} >= {len_r}")
        if (n>len_r):               raise AttributeError(f"n >= n chevaux : {n} >= {len_r}")
        if (n>5) or(n<1) :          raise AttributeError(f"invalid n : {n}")
        if (n>1) and ((n+N)>len_r): raise AttributeError(f"invalid n+N > {n}+{N} > {len_r} ")

        r = np.random.choice(results.numero, size=n, replace=False)
        if len(r) == 1 : r = r[0]

        return r


    @change_repr
    def choix_aleatoire_parmi_les_partants(results, N, n, cote_type="direct") : 
        """chose one horse random"""

        assert isinstance(results, pd.DataFrame)
        len_r = len(results) 
        if not isinstance(int(N), int):  raise ValueError("N should be an int")
        if not isinstance(int(n), int):  raise ValueError("n should be an int")
        if (N>len_r):               raise AttributeError(f"N >= n chevaux : {N} >= {len_r}")
        if (n>len_r):               raise AttributeError(f"n >= n chevaux : {n} >= {len_r}")
        if (n>5) or(n<1) :          raise AttributeError(f"invalid n : {n}")
        if (n>1) and ((n+N)>len_r): raise AttributeError(f"invalid n+N > {n}+{N} > {len_r} ")

        _results = results.loc[results.partant == True, :]
        r = np.random.choice(_results.numero, size=n, replace=False)
        if len(r) == 1 : 
            r = r[0]

        return r


    @change_repr
    def choix_aleatoire_parmi_les__N__meilleures_cotes(results, N, n, cote_type="direct") : 
        """chose the horse with nth best cote"""

        assert isinstance(results, pd.DataFrame)
        len_r = len(results) 
        if not isinstance(int(N), int):  raise ValueError("N should be an int")
        if not isinstance(int(n), int):  raise ValueError("n should be an int")
        if (N>len_r):               raise AttributeError(f"N >= n chevaux : {N} >= {len_r}")
        if (n>len_r):               raise AttributeError(f"n >= n chevaux : {n} >= {len_r}")
        if (n>5) or(n<1) :          raise AttributeError(f"invalid n : {n}")
        if (n>1) and ((n+N)>len_r): raise AttributeError(f"invalid n+N > {n}+{N} > {len_r} ")

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

        r = np.random.choice(results.numero.iloc[:N], size=n, replace=False)
        if len(r) == 1 : r = r[0]
        
        return r

    @change_repr
    def choix_aleatoire_entre_les__N__et__M__meilleures_cotes(results, N, M, n cote_type="direct") : 
        raise NotImplementedError


    @change_repr
    def ne_jamais_parier(results, N=None, n=None, cote_type="None") : 
        """just go to the hippo, no bets, just enjoy races and stalk beautiful ladies"""

        return -1

    @change_repr
    def choix_des__N__pires_cotes_inscrites(results, N, n, cote_type="direct") : 
        """chose the horse with best cote)"""

        assert isinstance(results, pd.DataFrame)
        len_r = len(results) 
        if not isinstance(int(N), int):  raise ValueError("N should be an int")
        if not isinstance(int(n), int):  raise ValueError("n should be an int")
        if (N>len_r):               raise AttributeError(f"N >= n chevaux : {N} >= {len_r}")
        if (n>len_r):               raise AttributeError(f"n >= n chevaux : {n} >= {len_r}")
        if (n>5) or(n<1) :          raise AttributeError(f"invalid n : {n}")
        if (n>1) and ((n+N)>len_r): raise AttributeError(f"invalid n+N > {n}+{N} > {len_r} ")

        r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

        if n==1             : return r.numero.iloc[N]
        elif n > 1 and n <6 : return list(r.numero.iloc[N:n+N])
        else                : raise ValueError("choix_des_N__pires_cotes")


    @change_repr
    def choix_des_N__pires_cotes_partantes(results, N, n, cote_type="direct")  : 
        """chose the horse with best cote)"""

        raise NotImplementedError




    # @change_repr
    # def choix_de_la_meilleure_cote(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""
    #     return MultiStrats.choix_des_N__meilleures_cotes(results, 0, 1, cote_type)


    # @change_repr
    # def choix_des_2_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""
    #     return MultiStrats.choix_des_N__meilleures_cotes(results, 0, 2, cote_type)


    # @change_repr
    # def choix_des_3_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""
    #     return MultiStrats.choix_des_N__meilleures_cotes(results, 0, 3, cote_type)


    # @change_repr
    # def choix_des_5_meilleures_cotes(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""

    #     return MultiStrats.choix_des_N__meilleures_cotes(results, 0, 5, cote_type)


    # @change_repr
    # def choix_aleatoire_un_inscrit(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""
    #     return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 1, cote_type)


    # @change_repr
    # def choix_aleatoire_2_inscrits(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""
    #     return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 2, cote_type)


    # @change_repr
    # def choix_aleatoire_3_inscrits(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""
    #     return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 3, cote_type)


    # @change_repr
    # def choix_aleatoire_5_inscrits(results, N=None, n=None, cote_type="direct") : 
    #     """chose the horse with best cote"""
    #     return MultiStrats.choix_aleatoire_parmi_les_inscrits(results, 0, 5, cote_type)


    # __strat_types = ["choix_des_N__meilleures_cotes", ]
    # __cote_types = ["direct", "prob"]
 

    # def __init__(self, strat_type, N=0, n=1, cote_type="direct") : 

    #     assert isinstance(N, int)
    #     assert isinstance(n, int)
    #     assert cote_type in self.__cote_types
    #     if not strat_type == "choix_de_la__N__meilleure_cote" :
    #         raise NotImplentedError("please be patient young padawan....")

    #     self.strat_type = strat_type
    #     self.N = N
    #     self.n = n
    #     self.Class = f"MultiStrats.{self.strat_type}"

    # def __call__(self, results, N, n) : 

    #     if self.strat_type == "choix_de_la__N__meilleure_cote" : 
    #         if N >= len(results) : 
    #             info("N sup >= nb chevaux")
    #             return -1

    #         r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

    #         return r.numero.iloc[N]


    # def __repr__(self) : 
    #     return f"MultiStrats.{self.strat_type}"


    # @change_repr
    # def choix_de_la__N__meilleure_cote(results, N, n=0, cote_type="direct") : 
    #     """chose the horse with nth best cote"""
        
    #     if not isinstance(N, int) : 
    #         raise ValueError("N should be an int")

    #     if N >= len(results) : 
    #         info("N sup >= nb chevaux")
    #         return -1

    #     r = results.sort_values(f"cote{cote_type}", ascending=True, inplace=False)

    #     return r.numero.iloc[N]

