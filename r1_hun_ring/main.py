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
df.rename(columns={'MPH': 'KPH', 'Driver Team': 'Driver'}, inplace=True)

#print(df['KPH'])

## Analysis

# Which driver have the largest 'Diff' to next Driver?
answer_1 = df['Diff'].idxmax()
answer_1_1 = df.loc[answer_1]['Driver']
answer_1_2 = df.loc[answer_1]['Diff']
print(f'Driver with largest gap to next Driver was: {answer_1_1} with {answer_1_2} seconds')

# Which driver have the smallest 'Diff' to next Driver?
answer_2 = df['Diff'].idxmin()
answer_2_1 = df.loc[answer_2]['Driver']
answer_2_2 = df.loc[answer_2]['Diff']
print(f'Driver with smallest gap to next Driver was: {answer_2_1} with {answer_2_2} seconds')

# Driver with the highest Top Speed in the race
answer_3 = df['KPH'].idxmax()
answer_3_1 = df.loc[answer_3]['Driver']
answer_3_2 = df.loc[answer_3]['KPH']
print(f'Driver with the highest Top Speed was {answer_3_1} with {round(answer_3_2,2)} KPH')

# Driver with the lowest Top Speed in the race
answer_4 = df['KPH'].idxmin()
answer_4_1 = df.loc[answer_4]['Driver']
answer_4_2 = df.loc[answer_4]['KPH']
print(f'Driver with the lowest Top Speed was {answer_4_1} with {round(answer_4_2,2)} KPH')