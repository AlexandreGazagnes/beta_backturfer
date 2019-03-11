#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 
import requests
from bs4 import BeautifulSoup


# consts
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


# class



class CoteSimplePlace :
    """functions used to scrap and integrade coteplace in the main dataframe"""

    def __extract_cotes_from_url(url) : 
        """from an url scrap and manage the htm table"""

        # if url is null
        if not url : 
            warning("NO URL !!!")
            return np.nan

        if not "https://www.paris-turf.com/" in url :
            if url[0] != "/" : 
                url ="https://www.paris-turf.com/" + url
            else : 
                url = "https://www.paris-turf.com" + url


        url = url.replace("partants-pronostics", "resultats-rapports")

        if  not "resultats-rapports" in url : 
            warning("not resultats-rapports in url")
            warning(f"{url}")
            return np.nan


        # get http response, then html
        try : 
            response = requests.get(url, headers=USER_AGENT)
            response.raise_for_status()
            html = response.text
        except Exception as e :
            s = f"error request {e} for url {url}"
            warning(s)
            return np.nan

        # create and parse our soup obj
        try : 
            soup = BeautifulSoup(html, 'html.parser') 
            result_block = soup.find_all('table', attrs={'class': "table reports first"})
        except Exception as e :
            s = f"error request {e} for url {url}"
            warning(s)
            return np.nan

        # look for just 1 table
        if len(result_block) == 1  : 
            table = result_block[0]
        else : 
            s = f"error  BS4 len {len(result_block)} for url {url}"
            warning(s)
            return np.nan

        # build a good df
        df = pd.read_html(str(table))[0]  
        df.columns = ["horse", "pmu", "pmu.fr", "leturf.fr"]

        # drop winning cote
        df = df.iloc[1:, :]

        # transform df if needed
        df["horse"] = df.horse.apply(lambda i : i.split(" ")[0])
        df.set_index("horse", drop=True, inplace=True) 
        f = lambda i : float(str(i).replace("€", "").strip().replace(",", "."))
        for c in df.columns : 
            df[c] = df[c].apply(f)

        return df


    def __keep_comp_url(df) : 

        return df.loc[:, ]

    @time_it 
    @get_size_of
    def _add_cotes(df, cores=6, dest="temp/scrap/", verbose=True, clear_temp=True, lazy=True) : 
        """for all lines of the dataframe, perform a multiporcess scrap of all urls"""

        assert isinstance(df, pd.DataFrame)
        assert "url" in df.columns
        assert isinstance(cores, int)
        assert (cores >= 1) and (cores <= 8)
        if not os.path.isdir(dest) : 
            os.mkdir(dest)
        assert isinstance(verbose, bool)

        t0 = time.time()

        def scrap_coteplace(i0=0, i1=10000000) : 

            for n in list_of_comp[i0:i1] :
                if lazy : 
                    if f"comp-{n}.pk" in os.listdir(dest) : 
                        continue
                _df = df.loc[df.comp == n, ["comp", "url"]]
                _df["coteplace"] = _df.url.apply(CoteSimplePlace.__extract_cotes_from_url)
                _df.drop("url", axis=1, inplace=True)
                _df = _df.iloc[0, : ]
                pk_save(_df, f"comp-{n}", dest)


        def join_partials() : 

            filenames = os.listdir(dest)
            filenames = [f for f in filenames if (os.path.isfile(dest + f) and (".pk" in f))]
            filenames = [f.replace(".pk", "") for f in filenames]
            sub_df    = [pk_load(f, dest) for f in filenames]
            sub_df    = pd.DataFrame(sub_df, columns = ["comp", "coteplace"])
            if clear_temp : 
                pk_clean(dest)

            return sub_df

        # multiprocessing
        list_of_comp = df.comp.unique()
        if cores < 2 : 
            scrap_coteplace(i0=0, i1=10000000)
        else : 
            chks  = chunks(list_of_comp, cores)
            process_list = [Process(target=scrap_coteplace, args=chk) for chk in chks]
            [i.start() for i in process_list]
            [i.join()  for i in process_list]

        # final
        info("scraping complete")
        _df          = join_partials()
        info("joining_complete")
        new_df       = pd.merge(df, _df, how="left", on=["comp", "comp"])
        info("merging_complete")
        new_df.index = range(len(new_df.index))

        # verbose
        if verbose : 
            info(f"df size in Mo : {sys.getsizeof(new_df) / 1000000}")
            info(f"timer load df : {round(time.time() - t0, 2)}")
            info(f"debut {new_df.jour.min()} fin {new_df.jour.max()}")
            info(new_df.shape)
            info(new_df.dtypes)

        return new_df 

    @time_it 
    @get_size_of
    def _handle_coteplace(df) :  
        """ from raw coteplace, transform in a dict and integrate data in df.results."""

        def f(v) : 
            try :       return {i: j for i,j in zip([np.int8(i)  for i in  v.index] , [np.float32(i)  for i in  v.pmu.values])} 
            except :    return np.nan
        df["coteplace"] = df.coteplace.apply(f)


        for i in df.index : 
            r = df.loc[i, "results"]
            r["coteplace"] = -1.0

            cote_dict = df.loc[i, "coteplace"]

            if not isinstance(cote_dict, dict) : continue

            for n, val in cote_dict.items() : 
                r.loc[r.numero == n, "coteplace"] = val 

        return df

    @time_it 
    @get_size_of
    def add(df) : 
        """ scrap and manage coteplace info"""
    
        df = CoteSimplePlace._add_cotes(df, cores=6, dest="temp/scrap/", verbose=True, clear_temp=True, lazy=True) 
        df = CoteSimplePlace._handle_coteplace(df)

        return df



class CoteSimpleGagnant :

    pass


class AddCote : 


    def __extract_html(url) : 
        """from an url scrap and manage the htm table"""

        # if url is null
        if not url : 
            warning("NO URL !!!")
            return np.nan

        if not isinstance(url, str) : 
            warning('url is not a string')
            warning(url)
            warning(type(url))


        if not "https://www.paris-turf.com/" in url :
            if url[0] != "/" : 
                url ="https://www.paris-turf.com/" + url
            else : 
                url = "https://www.paris-turf.com" + url


        url = url.replace("partants-pronostics", "resultats-rapports")

        if  not "resultats-rapports" in url : 
            warning("not resultats-rapports in url")
            warning(f"{url}")
            return np.nan


        # get http response, then html
        try : 
            response = requests.get(url, headers=USER_AGENT)
            response.raise_for_status()
            html = response.text
        except Exception as e :
            s = f"error request {e} for url {url}"
            warning(s)
            return np.nan


        return html



    def __extract_soup(html, soup_class) : 

        # create and parse our soup obj
        try : 
            soup = BeautifulSoup(html, 'html.parser') 
            result_block = soup.find_all('table', attrs={'class': soup_class})
        except Exception as e :
            s = f"error request {e} for url {url}"
            warning(s)
            return np.nan

        return result_block



    def __extract_simple_gagnant(table) : 


        # build a good df
        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for SIMPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) == 4 : 
            warning("wrong shape for SIMPLE table reports first / len df")
            return np.nan

        gagnant = df.apply(lambda i : ("Gagnant" or "gagnant") in i.numero, axis=1)  
        gagnant = df.loc[gagnant, :] 
        gagnant.index = gagnant.numero.apply(lambda i : int(i.strip().lower().replace(" > gagnant", "").strip()))
        gagnant.drop("numero", axis=1, inplace=True)
        gagnant.index_name="numero"

        for i in gagnant.columns :   
            gagnant[i] = gagnant[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 

        return gagnant


    def __extract_simple_place(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for SIMPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) == 4 : 
            warning("wrong shape for SIMPLE table reports first / len df")
            return np.nan

        place = df.apply(lambda i : ("Placé" or "place" or "Place" or "place") in i.numero, axis=1)  
        place = df.loc[place, :] 
        place.index = place.numero.apply(lambda i : int(i.strip().lower().replace(" > place", "").replace(" > placé", "").strip()))
        place.drop("numero", axis=1, inplace=True)
        place.index_name="numero"

        for i in place.columns :   
            place[i] = place[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 

        return place


    def __extract_couple_gagnant(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 
        
        if not len(df.columns) == 4 : 
            warning("wrong shape for COUPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) == 4 : 
            warning("wrong shape for COUPLE table reports first / len df")
            return np.nan

        gagnant = df.apply(lambda i : ("Gagnant" or "gagnant") in i.numero, axis=1)  
        gagnant = df.loc[gagnant, :] 
        gagnant.index = gagnant.numero.apply(lambda i : i.strip().lower().replace(" > gagnant", "").strip())
        gagnant.drop("numero", axis=1, inplace=True)
        gagnant.index_name="numero"

        for i in gagnant.columns :   
            gagnant[i] = gagnant[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 


        return gagnant


    def __extract_couple_couple_place(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 
        
        if not len(df.columns) == 4 : 
            warning("wrong shape for COUPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) == 4 : 
            warning("wrong shape for COUPLE table reports first / len df")
            return np.nan

        place = df.apply(lambda i : ("Placé" or "place" or "Place" or "place") in i.numero, axis=1)  
        place = df.loc[place, :] 
        place.index = place.numero.apply(lambda i : i.strip().lower().replace(" > place", "").replace(" > placé", "").strip())
        place.drop("numero", axis=1, inplace=True)
        place.index_name="numero"

        for i in place.columns :   
            place[i] = place[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 

        return place



    def __extract_couple_ordre(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 
        
        if not len(df.columns) == 4 : 
            warning("wrong shape for COUPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) == 1 : 
            warning("wrong shape for COUPLE table reports first / len df")
            return np.nan

        ordre = df.copy()
        ordre.index = ordre.numero.apply(lambda i : i.strip().lower().strip())
        ordre.drop("numero", axis=1, inplace=True)
        ordre.index_name="numero"

        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in ordre.columns :   
            ordre[i] = ordre[i].apply(f)

        return ordre




    def __extract_cotes(url)


        html = AddCote.__extract_html(url)

        cotes_dict = {  'simple_gagnant' : np.nan,
                        'simple_place'   : np.nan,
                        'couple_gagnant' : np.nan,
                        'couple_place'   : np.nan,
                        'couple_ordre'   : np.nan, 
                        '2_sur_4'        : np.nan,
                        'tierce_ordre'   : np.nan,
                        'tierce_desordre': np.nan,
                        'quinte_ordre'   : np.nan,
                        'quinte_desordre': np.nan   }       


        # table reports first AKA simple
        # ------------------------------
        result_block = AddCote.__extract_soup(html, soup_class="table reports first")

        # look for just 1 table
        if len(result_block) == 1  : 
            table = result_block[0]
        else : 
            s = f"error  BS4 len {len(result_block)} for url {url}"
            warning(s)
            return np.nan

        cotes_dict['simple_gagnant']    =  AddCote.__extract_simple_gagnant(table)
        cotes_dict['simple_place']      =  AddCote.__extract_simple_place(table)


        # Others 
        # ----------------------------------

        result_block = AddCote.__extract_soup(html, soup_class="table reports")

        # couple
        couple = list()
        for i, j in enumerate(result_block) :  
            r = str(result_block[i]) 
            if ("Couplé" or "couple" or "Couple" or "couplé") in r :  
                    couple.append(r) 

        if len(couple) == 2 :
            if ("Gagnant" or "gagnant") in couple[0] : 
                cotes_dict["couple_gagnant"]  = AddCote.__extract_couple_gagnant(couple[0])
                cotes_dict['couple_place']    = AddCote.__extract_couple_couple_place(couple[0])

            if ("ordre" or "Ordre") in couple[1] : 
                cotes_dict['couple_ordre']    = AddCote.__extract_couple_ordre(couple[1])

        if len(couple) > 2 :    
            warning("Errors???? ")

        if len(couple) == 1 : 
            couple = couple[0]
            if ("ordre" or "Ordre") in couple : 
                cotes_dict['couple_ordre']    = AddCote.__extract_couple_ordre(couple[1])
            else : 
                cotes_dict["couple_gagnant"]  = AddCote.__extract_couple_gagnant(couple[0])
                cotes_dict['couple_place']    = AddCote.__extract_couple_couple_place(couple[0])



# class CoteDeuxSurQuatre : 
    
#     pass


# class CoteTrio : 
    
#     pass



# class CoteTierce : 
    
#     pass


# class CoteQuinte : 
    
#     pass