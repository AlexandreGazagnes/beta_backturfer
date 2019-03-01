#!/usr/bin/env python3
# coding: utf-8


# import 
from src.misc import * 
import requests
from bs4 import BeautifulSoup


# consts
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


# class
class CotePlaced :
    """functions used to scrap and integrade cotepodium in the main dataframe"""

    def __extract_cotes_from_url(url) : 
        """from an url scrap and manage the htm table"""

        # if url is null
        if not url : return np.nan

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

        def scrap_cotepodium(i0=0, i1=10000000) : 

            for n in list_of_comp[i0:i1] :
                if lazy : 
                    if f"comp-{n}.pk" in os.listdir(dest) : 
                        continue
                _df = df.loc[df.comp == n, ["comp", "url"]]
                _df["cotepodium"] = _df.url.apply(CotePodium.__extract_cotes_from_url)
                _df.drop("url", axis=1, inplace=True)
                _df = _df.iloc[0, : ]
                pk_save(_df, f"comp-{n}", dest)


        def join_partials() : 

            filenames = os.listdir(dest)
            filenames = [f for f in filenames if (os.path.isfile(dest + f) and (".pk" in f))]
            filenames = [f.replace(".pk", "") for f in filenames]
            sub_df    = [pk_load(f, dest) for f in filenames]
            sub_df    = pd.DataFrame(sub_df, columns = ["comp", "cotepodium"])
            if clear_temp : 
                pk_clean(dest)

            return sub_df

        # multiprocessing
        list_of_comp = df.comp.unique()
        if cores < 2 : 
            scrap_cotepodium(i0=0, i1=10000000)
        else : 
            chks  = chunks(list_of_comp, cores)
            process_list = [Process(target=scrap_cotepodium, args=chk) for chk in chks]
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
            warning(f"df size in Mo : {sys.getsizeof(new_df) / 1000000}")
            warning(f"timer load df : {round(time.time() - t0, 2)}")
            warning(f"debut {new_df.jour.min()} fin {new_df.jour.max()}")
            warning(new_df.shape)
            warning(new_df.dtypes)

        return new_df 

    @time_it 
    @get_size_of
    def _handle_cotepodium(df) :  
        """ from raw cotepodium, transform in a dict and integrate data in df.results."""

        def f(v) : 
            try :       return {i: j for i,j in zip([np.int8(i)  for i in  v.index] , [np.float32(i)  for i in  v.pmu.values])} 
            except :    return np.nan
        df["cotepodium"] = df.cotepodium.apply(f)


        for i in df.index : 
            r = df.loc[i, "results"]
            r["cotepodium"] = -1.0

            cote_dict = df.loc[i, "cotepodium"]

            if not isinstance(cote_dict, dict) : continue

            for n, val in cote_dict.items() : 
                r.loc[r.numero == n, "cotepodium"] = val 

        return df

    @time_it 
    @get_size_of
    def add(df) : 
        """ scrap and manage cotepodium info"""
    
        df = CotePodium._add_cotes(df, cores=6, dest="temp/scrap/", verbose=True, clear_temp=True, lazy=True) 
        df = CotePodium._handle_cotepodium(df)

        return df





class CoteDuo : 
    pass



class CoteTierce : 
    pass