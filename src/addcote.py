#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 
import requests
from bs4 import BeautifulSoup


# consts
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


# class



# class CoteSimplePlace :
#     """functions used to scrap and integrade coteplace in the main dataframe"""

#     def __extract_cotes_from_url(url) : 
#         """from an url scrap and manage the htm table"""

#         # if url is null
#         if not url : 
#             warning("NO URL !!!")
#             return np.nan

#         if not "https://www.paris-turf.com/" in url :
#             if url[0] != "/" : 
#                 url ="https://www.paris-turf.com/" + url
#             else : 
#                 url = "https://www.paris-turf.com" + url


#         url = url.replace("partants-pronostics", "resultats-rapports")

#         if  not "resultats-rapports" in url : 
#             warning("not resultats-rapports in url")
#             warning(f"{url}")
#             return np.nan


#         # get http response, then html
#         try : 
#             response = requests.get(url, headers=USER_AGENT)
#             response.raise_for_status()
#             html = response.text
#         except Exception as e :
#             s = f"error request {e} for url {url}"
#             warning(s)
#             return np.nan

#         # create and parse our soup obj
#         try : 
#             soup = BeautifulSoup(html, 'html.parser') 
#             result_block = soup.find_all('table', attrs={'class': "table reports first"})
#         except Exception as e :
#             s = f"error request {e} for url {url}"
#             warning(s)
#             return np.nan

#         # look for just 1 table
#         if len(result_block) == 1  : 
#             table = result_block[0]
#         else : 
#             s = f"error  BS4 len {len(result_block)} for url {url}"
#             warning(s)
#             return np.nan

#         # build a good df
#         df = pd.read_html(str(table))[0]  
#         df.columns = ["horse", "pmu", "pmu.fr", "leturf.fr"]

#         # drop winning cote
#         df = df.iloc[1:, :]

#         # transform df if needed
#         df["horse"] = df.horse.apply(lambda i : i.split(" ")[0])
#         df.set_index("horse", drop=True, inplace=True) 
#         f = lambda i : float(str(i).replace("€", "").strip().replace(",", "."))
#         for c in df.columns : 
#             df[c] = df[c].apply(f)

#         return df


#     def __keep_comp_url(df) : 

#         return df.loc[:, ]

#     @time_it 
#     @get_size_of
#     def _add_cotes(df, cores=6, dest="temp/scrap/", verbose=True, clear_temp=True, lazy=True) : 
#         """for all lines of the dataframe, perform a multiporcess scrap of all urls"""

#         assert isinstance(df, pd.DataFrame)
#         assert "url" in df.columns
#         assert isinstance(cores, int)
#         assert (cores >= 1) and (cores <= 8)
#         if not os.path.isdir(dest) : 
#             os.mkdir(dest)
#         assert isinstance(verbose, bool)

#         t0 = time.time()

#         def scrap_coteplace(i0=0, i1=10000000) : 

#             for n in list_of_comp[i0:i1] :
#                 if lazy : 
#                     if f"comp-{n}.pk" in os.listdir(dest) : 
#                         continue
#                 _df = df.loc[df.comp == n, ["comp", "url"]]
#                 _df["coteplace"] = _df.url.apply(CoteSimplePlace.__extract_cotes_from_url)
#                 _df.drop("url", axis=1, inplace=True)
#                 _df = _df.iloc[0, : ]
#                 pk_save(_df, f"comp-{n}", dest)


#         def join_partials() : 

#             filenames = os.listdir(dest)
#             filenames = [f for f in filenames if (os.path.isfile(dest + f) and (".pk" in f))]
#             filenames = [f.replace(".pk", "") for f in filenames]
#             sub_df    = [pk_load(f, dest) for f in filenames]
#             sub_df    = pd.DataFrame(sub_df, columns = ["comp", "coteplace"])
#             if clear_temp : 
#                 pk_clean(dest)

#             return sub_df

#         # multiprocessing
#         list_of_comp = df.comp.unique()
#         if cores < 2 : 
#             scrap_coteplace(i0=0, i1=10000000)
#         else : 
#             chks  = chunks(list_of_comp, cores)
#             process_list = [Process(target=scrap_coteplace, args=chk) for chk in chks]
#             [i.start() for i in process_list]
#             [i.join()  for i in process_list]

#         # final
#         info("scraping complete")
#         _df          = join_partials()
#         info("joining_complete")
#         new_df       = pd.merge(df, _df, how="left", on=["comp", "comp"])
#         info("merging_complete")
#         new_df.index = range(len(new_df.index))

#         # verbose
#         if verbose : 
#             info(f"df size in Mo : {sys.getsizeof(new_df) / 1000000}")
#             info(f"timer load df : {round(time.time() - t0, 2)}")
#             info(f"debut {new_df.jour.min()} fin {new_df.jour.max()}")
#             info(new_df.shape)
#             info(new_df.dtypes)

#         return new_df 

#     @time_it 
#     @get_size_of
#     def _handle_coteplace(df) :  
#         """ from raw coteplace, transform in a dict and integrate data in df.results."""

#         def f(v) : 
#             try :       return {i: j for i,j in zip([np.int8(i)  for i in  v.index] , [np.float32(i)  for i in  v.pmu.values])} 
#             except :    return np.nan
#         df["coteplace"] = df.coteplace.apply(f)


#         for i in df.index : 
#             r = df.loc[i, "results"]
#             r["coteplace"] = -1.0

#             cote_dict = df.loc[i, "coteplace"]

#             if not isinstance(cote_dict, dict) : continue

#             for n, val in cote_dict.items() : 
#                 r.loc[r.numero == n, "coteplace"] = val 

#         return df

#     @time_it 
#     @get_size_of
#     def add(df) : 
#         """ scrap and manage coteplace info"""
    
#         df = CoteSimplePlace._add_cotes(df, cores=6, dest="temp/scrap/", verbose=True, clear_temp=True, lazy=True) 
#         df = CoteSimplePlace._handle_coteplace(df)

#         return df



# class CoteSimpleGagnant :

#     pass


class AddCote : 

    cotes =         [   'simple_gagnant', 'simple_place' , 
                        'couple_gagnant', 'couple_place', 'couple_ordre', 
                        'deux_sur_quatre' ,
                        'tierce_ordre', 'tierce_desordre', 
                        'trio_ordre', 'trio_desordre',
                        'quinte_ordre', 'quinte_desordre'    ]


    html_identifier = { 

                        }



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

        if not len(df) >= 4 : 
            warning("wrong shape for SIMPLE table reports first / len df")
            return np.nan

        gagnant = df.apply(lambda i : ("Gagnant" or "gagnant") in i.numero, axis=1)  
        gagnant = df.loc[gagnant, :] 
        gagnant.index = gagnant.numero.apply(lambda i : int(i.strip().lower().replace(" > gagnant", "").strip()))
        gagnant.drop("numero", axis=1, inplace=True)
        gagnant.index_name="numero"

        for i in gagnant.columns :   
            gagnant[i] = gagnant[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 

        gagnant = gagnant.iloc[:1, :]

        return gagnant


    def __extract_simple_place(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for SIMPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 4 : 
            warning("wrong shape for SIMPLE table reports first / len df")
            return np.nan

        place = df.apply(lambda i : ("Placé" or "place" or "Place" or "place") in i.numero, axis=1)  
        place = df.loc[place, :] 
        place.index = place.numero.apply(lambda i : int(i.strip().lower().replace(" > place", "").replace(" > placé", "").strip()))
        place.drop("numero", axis=1, inplace=True)
        place.index_name="numero"

        for i in place.columns :   
            place[i] = place[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 
        
        place = place.iloc[:3, :]

        return place


    def __extract_couple_gagnant(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 
        
        if not len(df.columns) == 4 : 
            warning("wrong shape for COUPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 4 : 
            warning("wrong shape for COUPLE table reports first / len df")
            return np.nan

        gagnant = df.apply(lambda i : ("Gagnant" or "gagnant") in i.numero, axis=1)  
        gagnant = df.loc[gagnant, :] 

        f = lambda i : "-" in i
        gagnant = gagnant.loc[gagnant.numero.apply(f), :]

        gagnant.index = gagnant.numero.apply(lambda i : i.strip().lower().replace(" > gagnant", "").strip())
        gagnant.drop("numero", axis=1, inplace=True)
        gagnant.index_name="numero"

        for i in gagnant.columns :   
            gagnant[i] = gagnant[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 

        gagnant = gagnant.iloc[:1, :]

        return gagnant


    def __extract_couple_couple_place(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 
        
        if not len(df.columns) == 4 : 
            warning("wrong shape for COUPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 4 : 
            warning("wrong shape for COUPLE table reports first / len df")
            return np.nan

        place = df.apply(lambda i : ("Placé" or "place" or "Place" or "place") in i.numero, axis=1)  
        place = df.loc[place, :] 

        f = lambda i : "-" in i
        place = place.loc[place.numero.apply(f), :]

        place.index = place.numero.apply(lambda i : str(i).strip().lower().replace(" > place", "").replace(" > placé", "").strip())
        place.drop("numero", axis=1, inplace=True)
        place.index_name="numero"

        for i in place.columns :   
            place[i] = place[i].apply(lambda i : np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())) 

        place = place.iloc[:3, :]

        return place


    def __extract_couple_ordre(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 
        
        if not len(df.columns) == 4 : 
            warning("wrong shape for COUPLE table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 1 : 
            warning("wrong shape for COUPLE table reports first / len df")
            return np.nan

        ordre = df.copy()
        f = lambda i : "-" in i
        ordre = ordre.loc[ordre.numero.apply(f), :]


        ordre = df.copy()
        ordre.index = ordre.numero.apply(lambda i : str(i).strip().lower().strip())
        ordre.drop("numero", axis=1, inplace=True)
        ordre.index_name="numero"

        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in ordre.columns :   
            ordre[i] = ordre[i].apply(f)

        ordre = ordre.iloc[:1, :]

        return ordre


    def __extract_trio_desordre(table) : 

        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for Trio table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 1 : 
            warning("wrong shape for Trio table reports first / len df")
            return np.nan

        trio = df.copy()

        f = lambda i : str(i).count("-") == 2
        trio = trio.loc[trio.numero.apply(f), :]

        trio.index = trio.numero.apply(lambda i : str(i).strip().lower().strip())
        trio.drop("numero", axis=1, inplace=True)
        trio.index_name="numero"


        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in trio.columns :   
            trio[i] = trio[i].apply(f)

        trio = trio.iloc[:1, :] 

        return trio


    def __extract_trio_ordre(table) : 

        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for Trio table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 1 : 
            warning("wrong shape for Trio table reports first / len df")
            return np.nan

        trio = df.copy()

        trio.index = trio.numero.apply(lambda i : str(i).strip().lower().strip())
        trio.drop("numero", axis=1, inplace=True)
        trio.index_name="numero"


        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in trio.columns :   
            trio[i] = trio[i].apply(f)

        trio = trio.iloc[:1, :] 

        return trio


    def __extract_deux_sur_quatre(table) : 

        # build a good df
        df = pd.read_html(str(table))[0] 
        
        if not len(df.columns) == 4 : 
            warning("wrong shape for 2 sur 4 table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 1 : 
            warning("wrong shape for 2 sur 4 table reports first / len df")
            return np.nan

        deux_sur_quatre = df.copy()

        f = lambda i : str(i).count("-") == 3
        deux_sur_quatre = deux_sur_quatre.loc[deux_sur_quatre.numero.apply(f), :]

        deux_sur_quatre.index = deux_sur_quatre.numero.apply(lambda i : str(i).strip().lower().strip())
        deux_sur_quatre.drop("numero", axis=1, inplace=True)
        deux_sur_quatre.index_name="numero"

        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in deux_sur_quatre.columns :   
            deux_sur_quatre[i] = deux_sur_quatre[i].apply(f)

        deux_sur_quatre = deux_sur_quatre.iloc[:1, :] 

        return deux_sur_quatre


    def __extract_tierce_ordre(table) : 

        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for Tierce table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) == 2 : 
            warning("wrong shape for Tierce table reports first / len df")
            return np.nan

        tierce = df.copy()
        
        f = lambda i : ("desordre" not in str(i).lower()) and ("désordre" not in str(i).lower())
        tierce = tierce.loc[tierce.numero.apply(f), :]

        f = lambda i : str(i).count("-") == 2
        tierce = tierce.loc[tierce.numero.apply(f), :]

        tierce.index = tierce.numero.apply(lambda i : str(i).strip().lower().strip())
        tierce.drop("numero", axis=1, inplace=True)
        tierce.index_name="numero"


        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in tierce.columns :   
            tierce[i] = tierce[i].apply(f)

        tierce = tierce.iloc[:1, :] 

        return tierce


    def __extract_tierce_desordre(table) : 

        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for Tierce table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) == 2 : 
            warning("wrong shape for Tierce table reports first / len df")
            return np.nan

        tierce = df.copy()
        
        f = lambda i : ("desordre" in str(i).lower()) or ("désordre" in str(i).lower())
        tierce = tierce.loc[tierce.numero.apply(f), :]

        tierce.index = tierce.numero.apply(lambda i : str(i).strip().lower().strip())
        tierce.drop("numero", axis=1, inplace=True)
        tierce.index_name="numero"


        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in tierce.columns :   
            tierce[i] = tierce[i].apply(f)

        tierce = tierce.iloc[:1, :] 

        return tierce


    def __extract_quinte_ordre(table) : 

        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for QUinte table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 2 : 
            warning("wrong shape for QUinte table reports first / len df")
            return np.nan

        quinte = df.copy()
        
        f = lambda i : ("desordre" not in str(i).lower()) and ("désordre" not in str(i).lower()) \
                            and ("bonus" not in str(i).lower()) and ("tirelire" not in str(i).lower())

        quinte = quinte.loc[quinte.numero.apply(f), :]

        f = lambda i : str(i).count("-") == 4
        quinte = quinte.loc[quinte.numero.apply(f), :]

        quinte.index = quinte.numero.apply(lambda i : str(i).strip().lower().strip())
        quinte.drop("numero", axis=1, inplace=True)
        quinte.index_name="numero"


        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in quinte.columns :   
            quinte[i] = quinte[i].apply(f)

        quinte = quinte.iloc[:1, :] 

        return quinte


    def __extract_quinte_desordre(table) : 

        df = pd.read_html(str(table))[0] 

        if not len(df.columns) == 4 : 
            warning("wrong shape for quinte table reports first / len columns")
            return np.nan

        df.columns = ["numero", "pmu", "pmu.fr", "leturf.fr"]

        if not len(df) >= 2 : 
            warning("wrong shape for quinte table reports first / len df")
            return np.nan

        quinte = df.copy()
        
        f = lambda i : ("desordre" in str(i).lower()) or ("désordre" in str(i).lower())
        quinte = quinte.loc[quinte.numero.apply(f), :]

        quinte.index = quinte.numero.apply(lambda i : str(i).strip().lower().strip())
        quinte.drop("numero", axis=1, inplace=True)
        quinte.index_name="numero"


        def f(i) : 
            if isinstance(i, str) : 
                return np.float16(str(i).replace("€", "").replace(" ", "").replace(",", ".").strip())
            else :
                return i
        for i in quinte.columns :   
            quinte[i] = quinte[i].apply(f)

        quinte = quinte.iloc[:1, :] 

        return quinte


    def scrap(url, cotes="all") :
        """give an url srcrap specific cotes and return a df"""

        cotes_dict = {  'simple_gagnant' : None,
                        'simple_place'   : None,
                        'couple_gagnant' : None,
                        'couple_place'   : None,
                        'couple_ordre'   : None, 
                        'trio_desordre'  : None,
                        'trio_ordre'     : None,
                        'deux_sur_quatre': None,
                        'tierce_ordre'   : None,
                        'tierce_desordre': None,
                        'quinte_ordre'   : None,
                        'quinte_desordre': None   }       


        if cotes == "all" : 
            pass

        elif isinstance(cotes, str) : 
            cotes = [cotes]
            cotes = [i for i in cotes if i in AddCote.cotes]
        elif isinstance(cotes, Iterable) : 
            cotes = [i for i in cotes if i in AddCote.cotes]
        else : 
            warning("Error cotes non valid as an argument of AddCotes.scrap")
            return cotes_dict

        if len(cotes) == 0 : 
            warning("Error cotes non valid as an argument of AddCotes.scrap")

        # html
        html = AddCote.__extract_html(url)


        # table reports first AKA simple
        # ------------------------------

        result_block = AddCote.__extract_soup(html, soup_class="table reports first")

        if (("simple_gagnant" or "simple_place") in cotes) or (cotes =="all") :  

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
        if (("couple_gagnant" or  "couple_place" or "couple_ordre") in cotes) or (cotes =="all") :
            couple = list()
            for i, j in enumerate(result_block) :  
                r = str(result_block[i]) 
                if ("Couplé" or "couple" or "Couple" or "couplé") in r :  
                        couple.append(r) 

            if len(couple) > 2 :    
                warning("Errors????")
            
            elif len(couple) == 2 :
                if ("Gagnant" or "gagnant") in couple[0] : 
                    cotes_dict["couple_gagnant"]  = AddCote.__extract_couple_gagnant(couple[0])
                    cotes_dict['couple_place']    = AddCote.__extract_couple_couple_place(couple[0])
                elif ("Gagnant" or "gagnant") in couple[1] : 
                    cotes_dict["couple_gagnant"]  = AddCote.__extract_couple_gagnant(couple[1])
                    cotes_dict['couple_place']    = AddCote.__extract_couple_couple_place(couple[1])
                else : 
                    warning("error  0 couple gagnant in result block")

                if "Ordre" in couple[1] : 
                    cotes_dict['couple_ordre']    = AddCote.__extract_couple_ordre(couple[1])
                elif "Ordre" in couple[0] : 
                    cotes_dict['couple_ordre']    = AddCote.__extract_couple_ordre(couple[0])
                else : 
                    warning("error  0 couple ordre in result block")

            elif len(couple) == 1 : 
                couple = couple[0]
                if ("ordre" or "Ordre") in couple : 
                    cotes_dict['couple_ordre']    = AddCote.__extract_couple_ordre(couple)
                else : 
                    cotes_dict["couple_gagnant"]  = AddCote.__extract_couple_gagnant(couple)
                    cotes_dict['couple_place']    = AddCote.__extract_couple_couple_place(couple)

            del couple


        # trio
        if (("Trio" or "trio") in cotes) or (cotes =="all") :
            trio = list()
            for i, j in enumerate(result_block) :  
                r = str(result_block[i]) 
                if "Trio" in r :  
                        trio.append(r) 


            if len(trio) == 2 : 
                if 'ordre' in trio[0] : 
                    cotes_dict["trio_ordre"] =  AddCote.__extract_trio_ordre(trio[0] )
                    cotes_dict["trio_desordre"]   =  AddCote.__extract_trio_desordre(trio[1])
                elif 'ordre' in trio[1] : 
                    cotes_dict["trio_ordre"] =  AddCote.__extract_trio_ordre(trio[1] )
                    cotes_dict["trio_desordre"]   =  AddCote.__extract_trio_desordre(trio[0])
                else : 
                    warning("error 0 in trio /result_block")

            elif len(trio) == 1  :   
                trio = trio[0]
                if 'ordre' in trio : 
                    cotes_dict["trio_ordre"]        = AddCote.__extract_trio_ordre(trio)
                else : 
                    cotes_dict["trio_desordre"]   =  AddCote.__extract_trio_desordre(trio)
            else :
                    warning("error 1 in trio /result_block")

        del trio


        # deux_sur_quatre
        if (("2_sur_4" or "deux_sur_quatre") in cotes) or (cotes =="all") :
    
            deux_sur_quatre = list()
            for i, j in enumerate(result_block) :  
                r = str(result_block[i]) 
                if "2sur4" in r :  
                        deux_sur_quatre.append(r) 

            if len(deux_sur_quatre) > 1  :   
                warning("errors deux sur quatre in result_block")

            elif len(deux_sur_quatre) == 1 : 
                deux_sur_quatre = deux_sur_quatre[0]
                cotes_dict["deux_sur_quatre"] = AddCote.__extract_deux_sur_quatre(deux_sur_quatre)

        del deux_sur_quatre

        # tierce
        if (("tierce" or "Tiercé" or "tiercé" or "Tiercé") in cotes) or (cotes =="all") :
    
            tierce = list()
            for i, j in enumerate(result_block) :  
                r = str(result_block[i]) 
                if "Tiercé" in r :  
                        tierce.append(r) 

            if len(tierce) > 1  :   
                warning("Errors tierce in result_block")

            elif len(tierce) == 1 : 
                tierce = tierce[0]
                cotes_dict["tierce_ordre"] = AddCote.__extract_tierce_ordre(tierce)
                cotes_dict["tierce_desordre"] = AddCote.__extract_tierce_desordre(tierce)

        del tierce


        # quinte
        if (("quinte" or "quinté" or "Quinté" or "quinté") in cotes) or (cotes =="all") :
            quinte = list()
            for i, j in enumerate(result_block) :  
                r = str(result_block[i]) 
                if "Quinté+" in r :  
                        quinte.append(r) 

            if len(quinte) > 1  :   
                warning("Errors quinte in result_block")

            elif len(quinte) == 1 : 
                quinte = quinte[0]
                cotes_dict["quinte_ordre"] = AddCote.__extract_quinte_ordre(quinte)
                cotes_dict["quinte_desordre"] = AddCote.__extract_quinte_desordre(quinte)

        del quinte


        # handle cotes df /cote dict
        cotes_df = pd.DataFrame(columns = ["numero", "type", "pmu", "pmu.fr", "leturf.fr"])

        for k,v in cotes_dict.items() : 
            if isinstance(v, pd.DataFrame) : 
                df = v.copy()
                df["type"] = str(k)
                df["numero"] = df.index.values
                cotes_df = cotes_df.append(df, ignore_index=True)

        cotes_df = cotes_df[["type", "numero", "pmu", "pmu.fr", "leturf.fr"]]

        return cotes_df




    @time_it 
    @get_size_of
    def add_cotes(df, cotes="all", cores=6, dest="data/cotes/", verbose=True, clear_temp=True, lazy=True) : 
        """for all lines of the dataframe, perform a multiporcess scrap of all urls"""

        assert isinstance(df, pd.DataFrame)
        assert "url" in df.columns
        assert isinstance(cores, int)
        assert (cores >= 1) and (cores <= 8)
        if not os.path.isdir(dest) : 
            os.mkdir(dest)
        assert isinstance(verbose, bool)

        t0 = time.time()


        def scrap_it(i0=0, i1=10000000) : 

            for n in list_of_comp[i0:i1] :
                if lazy : 
                    if f"comp-{n}.pk" in os.listdir(dest) : 
                        continue
                url = df.loc[df.comp == n, "url"]
                _df = AddCote.scrap(url, cotes)
                pk_save(_df, f"comp-{n}", dest)


        # multiprocessing
        list_of_comp = df.comp.unique()
        if cores < 2 : 
            scrap_it(i0=0, i1=10000000)
        else : 
            chks  = chunks(list_of_comp, cores)
            process_list = [Process(target=scrap_it, args=chk) for chk in chks]
            [i.start() for i in process_list]
            [i.join()  for i in process_list]

        # verbose
        if verbose : 
            info(f"df size in Mo : {sys.getsizeof(new_df) / 1000000}")
            info(f"timer load df : {round(time.time() - t0, 2)}")
            info(f"debut {new_df.jour.min()} fin {new_df.jour.max()}")
            info(new_df.shape)
            info(new_df.dtypes)




    # @get_size_of
    # @time_it 
    # def internalize_results(df, path="data/results/", temp="temp/internalize_results/" , cores=6) :

    #     if "results" in df.columns : 
    #         raise ValueError ("results ALREADY in columns")

    #     assert len(df.comp.unique()) == len(df)

    #     _df = df.copy()

    #     def funct(i0=0, i1=10000000) :                 
                
    #         results = []
    #         for comp in tqdm(_df.comp[i0: i1]) : 
    #             results.append([comp, pk_load(str(comp), path)])
            
    #         results = pd.DataFrame(results, columns=["comp", "results"])

    #         info(results.columns)
    #         info(results.head())
            
    #         pk_save(results, str(results.comp[0]), temp)


    #     def temp_merge() : 

    #         sub_df = pd.DataFrame(columns=["comp", "results"])

    #         for n in tqdm(os.listdir(temp)) :

    #             if not ".pk" in n : continue
    #             else : n = n.replace(".pk", "")

    #             r  = pk_load(str(n), temp)
    #             sub_df = sub_df.append(r, ignore_index=True)
    #             os.remove(f"{temp}{n}.pk")

    #         sub_df["comp"] = sub_df.comp.astype(np.uint32)

    #         return sub_df


    #     # multiporcessing
    #     if cores < 2 : 
    #             funct()
    #     else : 
    #         chks  = chunks(_df.comp, cores)
    #         process_list = [Process(target=funct, args=chk) for chk in chks]
    #         [i.start() for i in process_list]
    #         [i.join()  for i in process_list]

    #     # merge
    #     results = temp_merge()

    #     _df = _df.sort_values("comp", axis=0, ascending=True, inplace=False)
    #     _df.index = reindex(_df)

    #     results = results.sort_values("comp", axis=0, ascending=True, inplace=False)
    #     results.index = reindex(results)


    #     assert len(_df) == len(results)
    #     val = _df.comp.values == results.comp.values
    #     assert val.all()


    #     val = _df.index.values == results.index.values
    #     assert val.all()


    #     info(_df.columns)
    #     info(results.columns)

    #     results.columns = ["_comp", "results"]
    #     final_df = pd.concat([_df, results], axis=1, ignore_index=False)
    #     # final_df.columns = list(_df.columns) + list(results.columns) 

    #     info(final_df.loc[:, ["comp", "_comp"]].head())

    #     val = (final_df.comp.values ==final_df["_comp"].values)
    #     assert val.all()                                          

    #     final_df.drop("_comp", axis=1, inplace=True)

    #     assert len(final_df) == len(_df)
    #     assert len(final_df) == len(results)

    #     pk_clean(temp)

    #     return final_df




