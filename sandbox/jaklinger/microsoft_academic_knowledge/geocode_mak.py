import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzy_proc
from os.path import join as pjoin

'''Combine fuzzy scores from different scorers'''
class ComboFuzzer:
    def __init__(self,fuzzers):
        self.fuzzers = fuzzers
        # Define the normalisation variable in advance
        # Note: defined as inverse for speed
        self.norm = 1/np.sqrt(len(fuzzers))
    
    def combo_fuzz(self,target,candidate):
        _score = 0
        for _fuzz in self.fuzzers:
            _raw_score = (_fuzz(target,candidate)/100)
            _score += _raw_score**2
        return np.sqrt(_score)*self.norm

'''
Get the Lat/Lon from GRID data by fuzzy matching institute names
'''
class LatLonGetter:
    def __init__(self,grid_path,scorer):
        self.scorer = scorer
        # Read the GRID data
        grid_full = pd.read_csv(pjoin(grid_path,"grid.csv"),low_memory=False)
        grid_address = pd.read_csv(pjoin(grid_path,"full_tables/addresses.csv"),low_memory=False)
        grid_alias = pd.read_csv(pjoin(grid_path,"full_tables/aliases.csv"),low_memory=False)
        # Join the dataframes
        grid_df = grid_full.join(grid_address.set_index(keys=["grid_id"]),on="ID")
        grid_df = grid_df.join(grid_alias.set_index(keys=["grid_id"]),on="ID")
        grid_df = grid_df[["Name","lat","lng","ID","alias"]]
        
        # Find the null aliases
        self.df = grid_df
        null_alias = pd.isnull(self.df.alias)
        not_null = self.df.loc[~null_alias]
        # Now generate the list of names + not null aliases
        alias_names = list(not_null.alias.values)
        std_names = list(grid_df.Name.values)
        self.all_possible_values = std_names + alias_names
        self.lower_possible_values = [x.lower() for x in
                                      self.all_possible_values]
        self.fuzzy_matches = {}

    def get_latlon(self,mak_name):
        assert mak_name != ""
        # Super-fast check to see if there is an exact match
        try:
            idx = self.lower_possible_values.index(mak_name)
            match = self.all_possible_values[idx]
            score = 1.
        # Otherwise, fuzzy match
        except ValueError:
            # If already done a fuzzy match for this
            if mak_name in self.fuzzy_matches:
                match,score = self.fuzzy_matches[mak_name]
            # Otherwise, do the fuzzy match
            else:
                results = fuzzy_proc.extract(mak_name,self.all_possible_values)
                filtered = [r for r,s in results if s > 50]
                match,score = fuzzy_proc.extractOne(query=mak_name,
                                                    choices=filtered,
                                                    scorer=self.scorer)
        self.fuzzy_matches[mak_name] = (match,score)

        # Check whether the match was a Name or alias
        condition = self.df.Name == match
        if condition.sum() == 0:
            condition = self.df.alias == match

        _df = self.df.loc[condition]
        # Get the lat/lon
        lat = _df["lat"].values[0]
        lon = _df["lng"].values[0]
        return (lat,lon,match,score)
    
    def process_latlons(self,mak_institutes):
        isnull = pd.isnull(mak_institutes)
        if type(isnull) is bool:
            if isnull:
                return []
        elif all(isnull):
            return []
        results = []
        for mak_name in mak_institutes:
            results.append(self.get_latlon(mak_name))
        return results

'''
Wrapper method: just pass a list of institutes from MAK
and the path to the GRID data.
'''
def lat_lon_from_mak_names(mak_institutes,grid_path):
    cf = ComboFuzzer([fuzz.token_sort_ratio,fuzz.partial_ratio])
    llg = LatLonGetter(grid_path=grid_path,scorer=cf.combo_fuzz)    
    return llg.process_latlons(mak_institutes)

if __name__ == "__main__":
    mak_institutes = ["united arab emirates university","university of sharjah","masdar institute of science and technology",
                      "university of washington","american university of sharjah","khalifa university",
                      "petroleum institute","new york university abu dhabi","zayed university",
                      "max planck society","university of milan","national research council"]
    # Change this for your own local path
    grid_path = "~/Downloads/grid20170810/"
    lat_lon_score = lat_lon_from_mak_names(mak_institutes,grid_path)
    for inst,(lat,lon,score) in zip(mak_institutes,lat_lon_score):
        print(inst,lat,lon,score)
