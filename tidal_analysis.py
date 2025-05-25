#!/usr/bin/env python3

# import the modules you need here
import argparse
import os
import pandas as pd
import numpy as np

def read_tidal_data(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file '{filename}' was not found")
    
    try:
        df = pd.read_csv(
            filename,
            sep=r'\s+',
            skiprows=12,
            names=["Cycle", "Date", "Time", "ASLVBG02", "Residual"],
            na_values=['nan', 'Nan', 'None', '']
            )
        
        df["Date_Time"] = pd.to_datetime(df["Date"] + " " + df["Time"])
        df.set_index("Date_Time", inplace=True)
        
        df["ASLVBG02"] = df["ASLVBG02"].astype(str).str.extract(r"([-+]?[0-9]*\.?[0-9]+)").astype(float)

        df["ASLVBG02"] = df["ASLVBG02"].replace(-99.0, np.nan)       
    
    except Exception as e:
        raise ValueError(f"Error parsing tidal data from '{filename}': {e}")
   
    df = df.rename(columns={'ASLVBG02': 'Sea Level'})
    df = df[['Sea Level']]
    
    return df
    
def extract_single_year_remove_mean(year, data):
    
    #Check if the sea level and time data exists
    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Input DataFrame must have a DatetimeIndex.")
    if 'Sea Level' not in data.columns:
        raise ValueError("Input DataFrame must have a 'Sea Level' column.")
        
    #extract data for target year to a separate dataframe
    year_data = data[data.index.year == year].copy()
    
    #check that year data exists
    if year_data.empty:
        print(f"No data found for year {year}")
        return pd.DataFrame(columns=['Sea Level'], index=pd.DatetimeIndex([]))

    annual_mean = year_data["Sea Level"].mean()
    
    #remove mean from year data
    year_data['Sea Level'] = year_data['Sea Level'] - annual_mean
    
    return year_data[['Sea Level']]

def extract_section_remove_mean(start, end, data):


    return 


def join_data(data1, data2):

    return 



def sea_level_rise(data):

                                                     
    return 

def tidal_analysis(data, constituents, start_datetime):


    return 

def get_longest_contiguous_data(data):


    return 




