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

# Apply conversion function to 'Best' column
df['Best'] = df['Best'].apply(convert_to_timedelta)
#df['Best'] = df['Best'].astype(str).str[7:]  # Slice to remove '0 days ' prefix
print(df.loc[0]['Best'] - df.loc[1]['Best'])

# Format timedelta column for display
# Format timedelta column for display

print(df['Best'].dtype)
print(df)