import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_excel('gb3_r1_hun.xlsx')
#print(df)

# Overall look into data
#print(df.info())
#print(df.describe())
#print(df.isnull().sum())
#print(df.isna().sum())

# Changing columns ['Time','Best'] dtype from object to timedelta
# Function to convert mm:ss:sss to timedelta
def convert_to_timedelta(time_str):
    parts = time_str.split(':')
    minutes = int(parts[0])
    seconds = int(parts[1])
    milliseconds = int(parts[2])
    return pd.to_timedelta(minutes * 60 + seconds, unit='s') + pd.to_timedelta(milliseconds, unit='ms')

# Apply conversion function to 'Best' & 'Time' columns
df['Best'] = df['Best'].apply(convert_to_timedelta)
df['Time'] = df['Time'].apply(convert_to_timedelta)

# Result Checking
#print(df['Best'].dtype)
#print(df)
#print(df.loc[0]['Best'] - df.loc[1]['Best'])
# Unfortunetly I need to leave format as it was with '0 days HH:' prefix to execute calculation on it.

# Gap column is not a time dtype, but it's a float64 soo I leave it
#print(df['Gap'])

# MPH column need to be converted into KPH ;)
df['MPH'] = df['MPH'] * 1.609344
df.rename(columns={'MPH': 'KPH'}, inplace=True)
#print(df['KPH'])

