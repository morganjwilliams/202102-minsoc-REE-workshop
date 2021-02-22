import pandas as pd
import numpy as np
from pyrolite.geochem.ind import __common_elements__, __common_oxides__ # indexes of elements and oxides which we'll check against

def rename_columns(df):
    """
    Rename the columns which pyrolite can access so we can use the indexing and transformation functions.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with columns you'd like to rename.
    
    Returns
    -------
    pandas.DataFrame
        Dataframe with columns renamed.
    """
    _elements, _oxides = {e.upper(): e for e in __common_elements__}, {o.upper(): o for o in __common_oxides__} # these will serve as lookup tables for our capitalised components
    
    element_columns = {c: _elements[c[:c.find("(PPM")]] for c in df.columns if ("(PPM" in c and c[:c.find("(PPM")]) in _elements} # all of the elemental values are in ppm here
    oxide_columns = {c: _oxides[c[:c.find("(WT%")]] for c in df.columns if ("(WT%" in c and c[:c.find("(WT%")]) in _oxides} # this omits some gas measurements, but gets the major oxides
    isotope_columns = {c: '/'.join([c.title() for c in c.split('_')]) for c in df.pyrochem.list_isotope_ratios if len(c.split('_'))==2}
    
    return df.rename(columns = {**element_columns, **oxide_columns, **isotope_columns})
    
    

def fetch_GEOROC_csv(filepath):
    """
    Fetch a GEOROC csv from a local file or URL.
    
    Parameters
    ----------
    filepath : str | pathlib.Path
        Filepath to a GEOROC csv - can be used to directly fetch a URL thanks to `pandas.read_csv`.
    
    Returns
    -------
    pandas.DataFrame
        Dataframe formatted for `pyrolite`.
    """
    df = pd.read_csv(filepath, encoding='cp1252', skip_blank_lines=False) # get some data from GEOROC directly
    df = df.loc[:np.argmax(df.iloc[:, 0].isnull())-1] # omit the abbreviations and references after the blank line in this file
    df.drop(columns=[c for c in df.columns if 'Unnamed' in c], inplace=True) # drop our redundant column
    df = rename_columns(df)
    df = df.set_index('UNIQUE_ID', drop=True)
    return df