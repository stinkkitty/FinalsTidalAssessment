#!/usr/bin/env python3

# import the modules you need here
import argparse
import os
import pandas as pd
import numpy as np
import uptide
import pytz
import datetime

def read_tidal_data(filename):
    
    #Make sure file exists
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

        #replace dodgy values with NaN
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
    
    #Convert start and end date to a pandas timestamp
    start_ts = pd.to_datetime(start)
    end_ts = pd.to_datetime(end)
    
    #copy intented section to a separate dataframe
    section_data = data.loc[start_ts:end_ts].copy()
    
    #Check if section exists
    if section_data.empty:
        print('No data found from {start} to {end}')
        return pd.DataFrame(columns=['Sea Level'], index = pd.DatetimeIndex([]))
    
    #Check if data is numeric
    if not pd.api.types.is_numeric_dtype(section_data['Sea Level']):
        section_data["Sea Level"] = pd.to_numeric(section_data['Sea Level'], errors = 'coerce')
        
    #Calculate mean for section
    section_mean = section_data["Sea Level"].mean()
    
    #remove mean
    section_data['Sea Level'] = section_data['Sea Level'] - section_mean
    
    return section_data[["Sea Level"]] 


def join_data(data1, data2):
    
    combined_data = pd.concat([data1, data2])
    
    #Ensure chronological order of data
    combined_data = combined_data.sort_index()
    
    return combined_data[['Sea Level']]


def sea_level_rise(data):
    
                                                     
    return 


def tidal_analysis(data, constituents, start_datetime):
    time_data = data.index.to_numpy()
    sea_level_data = data['Sea Level'].to_numpy()
    tide_obj = uptide.Tides(constituents)
    tide_obj.set_initial_time(start_datetime) #set timezone
    
    amplitudes_radians, phases_radians = uptide.harmonic_analysis(tide_obj, sea_level_data, time_data)
    
    #Convert radians to degrees
    amplitudes_degrees = amplitudes_radians
    phases_degrees = np.degrees(phases_radians)
    
    return amplitudes_degrees, phases_degrees


def get_longest_contiguous_data(data):


    return 




