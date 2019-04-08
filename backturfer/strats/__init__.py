#!/usr/bin/env python3
# coding: utf-8


from backturfer.strats.multi   import MultiStrats
from backturfer.strats.simple  import SimpleStrats
from backturfer.strats.couple  import CoupleStrats
from backturfer.strats.trio    import TrioStrats
from backturfer.strats.quinte  import QuinteStrats


class Strats() : 


    strats_str = {  # 'MultiStrats'  : MultiStrats.strats_str, 
                    'SimpleStrats' : SimpleStrats.strats_str,
                    'CoupleStrats' : CoupleStrats.strats_str, 
                    'TrioStrats'   : TrioStrats.strats_str, 
                    'QuinteStrats' : QuinteStrats.strats_str,              }


    dummy_1  =  {    "val_1" : "val 1", 
                    "val_2" : "val 2"}

    def dummy_2(i):

        assert isinstance(i, str)

        if i =="a" :  
            return  {    "val_a" : "val a", 
                         "val_b" : "val b"}
        elif i =="A" : 
            return  {    "val_A" : "val A", 
                         "val_B" : "val B"}
        else : 
            raise AttributeError("smthg went wrong")


    def asso(bet_type): 

        bet_type = bet_type.lower()

        if "simple" in bet_type : 
            return Strats.strats_str["SimpleStrats"]
        elif "couple" in bet_type: 
            return Strats.strats_str["CoupleStrats"]
        elif "2" in bet_type: 
            return Strats.strats_str["CoupleStrats"]
        elif "deux" in bet_type: 
            return Strats.strats_str["CoupleStrats"]
        elif "trio" in bet_type : 
            return Strats.strats_str["TrioStrats"]
        elif "tier" in bet_type : 
            return Strats.strats_str["TrioStrats"]
        elif "quint" in bet_type : 
            return Strats.strats_str["QuinteStrats"]
        else : 
            raise AttributeError("someting went wrong")



