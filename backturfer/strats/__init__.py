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



