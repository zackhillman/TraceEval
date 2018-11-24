import pandas as pd
import glob
from common.io import file_base, parent_dir, mkdir
import re
import os





def get_proc_data(fpath):
    """Turns the processed data into dataframe from fname
    @:return dataframe of given class"""
    return pd.read_csv(fpath)

if __name__ == "__main__":
    fpath = '/Users/zackhillman/Documents/eece2300/FinalProject/termproject/data/processed/surveys/camd/cine2336/summer/blake_01_summer.csv'

    data_dir = '/Users/zackhillman/Documents/eece2300/FinalProject/termproject/data/raw/surveys-raw/'
    output_dir = '/Users/zackhillman/Documents/eece2300/FinalProject/termproject/data/processed/surveys/'

    df = get_proc_data(fpath)
    test = 1