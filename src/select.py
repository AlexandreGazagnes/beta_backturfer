#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 


class RaceSelector(dict) : 


    __price_min_max = 5000000
    __price_max_min = 1000
    __typec = [ 'steeple-chase cross-country', 'steeple-chase', 'haies', 'plat', 
                'attelé', 'monté', np.nan]

    __valid_keys = ['date_start', 'date_stop', 'hippo', 'country', 'quinte', 'euro_only', 'price_min', 'price_max', 'typec']

    def __init__(self, form=dict(), hard_check=1, verbose=True) : 

        form = {i: j for i, j in form.items() if i in RaceSelector.__valid_keys}

        if not 'date_start' in form.keys() : form['date_start'] = 0
        if not 'date_stop'  in form.keys() : form['date_stop']  = 1000000
        if not 'hippo'      in form.keys() : form['hippo']      = None
        form['country']     = None
        if not 'quinte'     in form.keys() : form['quinte']     = "all"
        if not 'euro_only'  in form.keys() : form['euro_only']  = False
        if not 'price_min'  in form.keys() : form['price_min']  = 0
        if not 'price_max'  in form.keys() : form['price_max']  = 500000000
        if not 'typec'      in form.keys() : form['typec']      = RaceSelector.__typec

        super().__init__(form)

        errors = list()
        errors.append(self.__check_date_start(hard_check=hard_check))
        errors.append(self.__check_date_stop(hard_check=hard_check))
        errors.append(self.__check_country(hard_check=hard_check))
        errors.append(self.__check_hippo(hard_check=hard_check))
        errors.append(self.__check_quinte(hard_check=hard_check))
        errors.append(self.__check_euro_only(hard_check=hard_check))
        errors.append(self.__check_price_min(hard_check=hard_check))
        errors.append(self.__check_price_max(hard_check=hard_check))
        errors.append(self.__check_typec(hard_check=hard_check))

        self.errors = [i for i in errors if i]

        if  verbose : 
            info("RaceSelector done ! ")



    def __check_date_start(self, hard_check=0) :
        """check form input for date_start"""

        # check type       
        if isinstance(self['date_start'], str) : 
            try : 
                self['date_start'] = self['date_start'].strip().replace("/", "-").replace(":", "-").replace(" ", "")
                self['date_start'] = pd.Timestamp(self['date_start'])
            except Exception as e: 
                warning(f"Error self['date_start'] {self['date_start']}")
                if not hard_check :
                    self['date_start'] = 0
                    return "Error invalid format for date_start; try '2018-12-31 as year-month-day'"
                else        :   
                    raise e

        if isinstance(self['date_start'], pd.Timestamp) : 
            try : 
                self['date_start'] = timestamp_to_int(self['date_start'])
            except Exception as e: 
                warning(f"Error self['date_start'] {self['date_start']}")
                if not hard_check :
                    self['date_start'] = 0
                    return "Error invalid format for date_start; try '2018-12-31 as year-month-day'"
                else        :   
                    raise e

        if not isinstance(self['date_start'], int) : 
                warning(f"Error self['date_start'] {self['date_start']}")
                if not hard_check : 
                    self['date_start'] = 0  
                    return "Error invalid format for date_start; try '2018-12-31 as year-month-day'"
                else        :   
                    raise ValueError("Error invalid format for date_start; try '2018-12-31 as year-month-day'")

        # values
        if self['date_start'] < 0 : 
                warning(f"Error self['date_start'] {self['date_start']}")
                if not hard_check :   
                    self['date_start'] = 0 
                    return "Error invalid value for date_start : neg values not authorized"
                else        :   
                    raise ValueError("Error invalid value for date_start : neg values not authorized")

        if self['date_start'] >= int_today() : 
                warning(f"Error self['date_start'] {self['date_start']}")
                if not hard_check :   
                    self['date_start'] = 0 
                    return "Error invalid value for date_start, date_start > today"
                else        :   
                    raise ValueError("Error invalid value for date_start, date_start > today")

        return None 


    def __check_date_stop(self, hard_check=0) :
        """check form input for date_stop"""

        # check type       
        if isinstance(self['date_stop'], str) : 
            try : 
                self['date_stop'] = self['date_stop'].strip().replace("/", "-").replace(":", "-").replace(" ", "")
                self['date_stop'] = pd.Timestamp(self['date_stop'])
            except Exception as e: 
                warning(f"Error self['date_stop'] {self['date_stop']}")
                if not hard_check :
                    self['date_stop'] = 0
                    return "Error invalid format for date_stop; try '2018-12-31 as year-month-day'"
                else        :   
                    raise e

        if isinstance(self['date_stop'], pd.Timestamp) : 
            try : 
                self['date_stop'] = timestamp_to_int(self['date_stop'])
            except Exception as e: 
                warning(f"Error self['date_stop'] {self['date_stop']}")
                if not hard_check :
                    self['date_stop'] = 0
                    return "Error invalid format for date_stop; try '2018-12-31 as year-month-day'"
                else        :   
                    raise e

        if not isinstance(self['date_stop'], int) : 
                warning(f"Error self['date_stop'] {self['date_stop']}")
                if not hard_check : 
                    self['date_stop'] = 0  
                    return "Error invalid format for date_stop; try '2018-12-31 as year-month-day'"
                else        :   
                    raise ValueError("Error invalid format for date_stop; try '2018-12-31 as year-month-day'")

        # values
        if self['date_stop'] < 0 : 
                warning(f"Error self['date_stop'] {self['date_stop']}")
                if not hard_check :   
                    self['date_stop'] = 0 
                    return "Error invalid value for date_stop : neg values not authorized"
                else        :   
                    raise ValueError("Error invalid value for date_stop : neg values not authorized")

        if self['date_stop'] < self['date_start'] : 
                warning(f"Error self['date_stop'] {self['date_stop']}")
                if not hard_check :   
                    self['date_stop'] = 1000000000 
                    return "Error invalid value for date_stop, date_stop < date_start"
                else        :   
                    raise ValueError("Error invalid value for date_stop, date_stop < date_start")

        return None 


    def __check_country(self, hard_check=0) : 
        """check country"""

        self['country'] = None

        return None


    def __check_hippo(self, hard_check=0) : 
        """check hippo"""

        if not self['hippo'] : 
            return None

        if self['hippo'] : 
            self['country'] = None

        if not isinstance(self['hippo'], str) : 

            warning(f"Error self['hippo'] {self['hippo']}")
            if not hard_check :
                self['hippo'] = None
                return "Error invalid format for hippo, text expected"
            else        :   
                raise ValueError("Error invalid format for hippo, text expected")
        
        self['hippo']   = self['hippo'].strip().lower()
        
        return None


    def __check_hippo_consistancy(self, df, hard_check=0, threshold=3) : 

        if not self['hippo'] : 
            return None

        if self['hippo'] not in list(df.hippo.unique()) : 
            if not hard_check : 
                errors = f"Error : {self['hippo']} not in our hippo database"
                candidates = [i for i in df.hippo.unique() if i[:threshold] == self['hippo'][:threshold]]
                candidates = "\n".join(candidates)
                errors+=(f", maybe you should consider \n{candidates}")
                self['hippo'] = None
                warning(errors)
                return errors
            else : 
                raise ValueError(f"hippo {self['hippo']} not in hippo list")

        return None


    def __check_quinte(self, hard_check=0) : 
        """check quinte"""

        if not self['quinte'] in ["all", 1, 0, "1", "0", True, False, "True", "False", "only_quinte", "only_not_quinte"] : 
            warning(f"error quinte for {self['quinte']}")
            if not hard_check : 
                self['quinte'] = "all"
                return f"error quinte {self['quinte']}"
            else :
                raise ValueError("invalid param for quinte")

        if self['quinte'] in ["1", "0"] :           self['quinte'] = int(self['quinte'])
        if self['quinte'] in ["True", "False"] :    self['quinte'] = bool(self['quinte'])

        return None


    def __check_euro_only(self, hard_check=0) : 
        """check euro"""

        if not self['euro_only'] in [1, 0, "1", "0", True, False, "True", "False"] : 
            warning(f"error euro_only for {self['euro_only']}")
            if not hard_check : 
                self['euro_only'] = False
                return f"error euro_only {self['euro_only']}"
            else :
                raise ValueError("invalid param for euro_only")

        return None


    def __check_price_min(self, hard_check=0) : 

        self['price_min'] = str(self['price_min'])
        self['price_min'] = self['price_min'].strip().replace(" ", "").replace("-", "").replace("€", "").strip()
        
        try : 
            self['price_min'] = int(self['price_min'])
        except Exception as e:
            warning(f"invalid format for price_min {self['price_min']}")
            if not hard_check : 
                self['price_min'] = 0
                return f"error for price_min : impossible to convert in a number"
            else : 
                raise e

        if self['price_min'] < 0 : 
            warning(f"invalid value for price_min {self['price_min']}")
            if not hard_check : 
                self['price_min'] = 0
                return "error for price_min : negative value not allowed"
            else : 
                raise ValueError("error for price_min : negative value not allowed")

        if self['price_min'] > RaceSelector.__price_min_max : 
            warning(f"invalid format for price_min {self['price_min']}")
            if not hard_check : 
                self['price_min'] = 0
                return f"error for price_min : price_min value to big"
            else : 
                raise ValueError("error for price_min : price_min value to big")

        return None


    def __check_price_max(self, hard_check=0) : 

        self['price_max'] = str(self['price_max'])
        self['price_max'] = self['price_max'].strip().replace(" ", "").replace("-", "").replace("€", "").strip()
        
        try : 
            self['price_max'] = int(self['price_max'])
        except Exception as e:
            warning(f"invalid format for price_max {self['price_max']}")
            if not hard_check : 
                self['price_max'] = 0
                return f"error for price_max : impossible to convert in a number"
            else : 
                raise e

        if self['price_max'] < 0 : 
            warning(f"invalid value for price_max {self['price_max']}")
            if not hard_check : 
                self['price_max'] = 500000000
                return f"error for price_max : negative value not allowed"
            else : 
                raise ValueError("error for price_max : negative value not allowed")

        if self['price_max'] < RaceSelector.__price_max_min : 
            warning(f"invalid format for price_max {self['price_max']}")
            if not hard_check : 
                self['price_max'] = 500000000
                return f"error for price_max : value to small than expected, df will be Void"
            else : 
                raise ValueError("error for price_max : value to small than expected, df will be Void")

        if self['price_min'] > self['price_max'] : 
            warning(f"invalid format for price_max {self['price_max']}")
            if not hard_check : 
                self['price_max'] = 500000000
                return f"error for price_max : price_max < price_min"
            else : 
                raise ValueError("error for price_max : price_max < price_min")

        return None


    def __check_price_min_consistancy(self, df, hard_check=0) : 

        if self["price_min"] > df.cheque_val.max() : 
            warning(f"invalid format for price_min {self['price_min']}")
            if not hard_check : 
                self['price_min'] = 0
                return f"error for price_min, after various selections 'price_min' > df.cheque_val.max, df will be Void"
            else : 
                raise ValueError(f"error for price_min, after various selections 'price_min' > df.cheque_val.max, df will be Void")

        return None


    def __check_price_max_consistancy(self, df, hard_check=0) : 

        if self['price_max'] < df.cheque_val.min() : 
            warning(f"invalid format for price_max {self['price_max']}")
            if not hard_check : 
                self['price_max'] = 500000000
                return "error for 'price_max':  after various selections 'price_max' < df.cheque_val.min, df will be Void"
            else : 
                raise ValueError(f"error for 'price_max' : after various selections, 'price_max' < df.cheque_val.min, df will be Void")

        return None


    def __check_typec(self, hard_check=0) : 

        self['typec'] = [str(i).lower().strip() for i in self['typec']]
        self['typec'] = [i for i in self['typec'] if i in RaceSelector.__typec]

        if not len(self['typec']) : 
            warning(f"invalid format for typec {self['typec']}")
            if not hard_check : 
                self['typec'] = RaceSelector.__typec
                return f"error for typec, not in typec list"
            else : 
                raise ValueError(f"invalid format for typec {self['typec']}")

        return None


    def __check_typec_consistancy(self, df, hard_check=0) : 

        self['typec'] = [i for i in self['typec'] if i in list(df.typec.unique())]
        
        if not len(self['typec']) : 
            warning(f"invalid format for typec {self['typec']}")
            if not hard_check : 
                self['typec'] = RaceSelector.__typec
                return f"error for typec : after previous selections, len(typec) = 0, df will be Void"
            else : 
                raise ValueError(f"error for typec : after previous selections, len(typec) = 0, df will be Void")

        return None


    @get_size_of
    @time_it 
    def run(self, df, force_consistancy=True, verbose=True) : 
        """ 
        force_consistancy : return Error if  Raceselector lead to a null dataframe
        ie force to have a not null dataframe
        verbose : print various info"""

        t0 = time.time()
        _df = df.copy()

        # dates
        self.__check_date_start(hard_check=1)
        self.__check_date_stop(hard_check=1)
        # if force_consistancy : 
        #   self.__check_date_start_consistancy(_df, hard_check=1)
        #   self.__check_date_stop_consistancy(_df, hard_check=1)
        _df = _df.loc[_df.jour >= self['date_start'], :]
        _df = _df.loc[_df.jour <= self['date_stop' ], :]

        # hippo and country
        self.__check_country(hard_check=1)
        self.__check_hippo(hard_check=1)
        if force_consistancy : 
            self.__check_hippo_consistancy(_df, hard_check=1)

        if self['hippo'] : 
                _df = _df.loc[_df.hippo == self['hippo'], :]
        else : 
            if not self['country'] :    pass
            else :                      raise NotImplementedError("Error NOT IMPLEMENTED country selection")


        # quinte
        self.__check_quinte(hard_check=1)
        # if force_consistancy : 
            # self.__check_quinte_consistancy(_df, hard_check=1)
        if self['quinte'] in ["only_quinte", 1, "1", True, "True"] : 
            _df = _df.loc[_df.quinte == 1, :]
        if self['quinte'] in ["only_not_quinte", 0, "0", False, "False"] : 
            _df = _df.loc[_df.quinte == 0, :]


        # currency euro_only (alias cheque_type)
        self.__check_euro_only(hard_check=1)
        # if force_consistancy : 
        #           self.__check_euro_only_consistancy(hard_check=1)
        if self['euro_only'] in [True, "True", 1, "1"] : 
            _df = _df.loc[_df.cheque_type == "€", :]
 

        # price
        self.__check_price_min(hard_check=1)
        self.__check_price_max(hard_check=1)
        if  force_consistancy : 
            self.__check_price_min_consistancy(_df, hard_check=1)
            self.__check_price_max_consistancy(_df, hard_check=1)
        _df = _df.loc[_df.cheque_val >= self['price_min'], :]
        _df = _df.loc[_df.cheque_val <= self['price_max'], :]
        
        # typec
        self.__check_typec(hard_check=1)
        if  force_consistancy : 
            self.__check_typec_consistancy(_df, hard_check=1)
        ser = _df.typec.apply(lambda i : str(i) in self['typec'])
        _df = _df.loc[ser, :]

        if verbose : 
            info(f"start            : {int_to_timestamp(_df.jour.min())}")
            info(f"stop             : {int_to_timestamp(_df.jour.max())}")
            info(f"hippo unique     : {_df.hippo.unique()}")
            info(f"quinte unique    : {_df.quinte.unique()}")
            info(f"cheque type      : {_df.cheque_type.unique()}")
            info(f"cheque min       : {_df.cheque_val.min()}")
            info(f"cheque max       : {_df.cheque_val.max()}")
            info(f"typec init       : {self['typec']}")
            info(f"typec unique     : {_df.typec.unique()}")
            info(f"df size in Mo    : {sys.getsizeof(_df) / 1000000}")
            info(f"timer load df    : {round(time.time() - t0, 2)}")
            info(f"df shape         : {_df.shape}")
            info(f"df dtypes        : {_df.dtypes}")
            info(f"df columns       : {_df.columns}")
            info(f"self             : {self}")

        if force_consistancy and not len(_df) :  
            raise ValueError("len df == 0")

        _df.index = reindex(_df)

        return _df
        

