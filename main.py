import pandas as pd
import numpy as np
import re

df = pd.read_excel('data.xlsx', na_filter=True)
print(df)

# Data Checking
print(df.columns)
print(df.info())
print(df.describe())

print(df['Driver and Team'].unique())
print(df['Driver and Team'].values)

# Extract Team
def extract_team(info):
    # Match RegEx [XX]
    match = re.search(r'\[.*?\]', info)
    if match:
        # split string after match and return second half
        return info.split(match.group())[1]
    return np.nan

# Use fucntion to make new column
df['Team'] = df['Driver and Team'].apply(extract_team)

print(df['Team'])
print(df)

# Validation None data for Team column
print(df[df['Team'].isna()])

# For results we modify and insert data manually
dittmann_racing = [19,34,5]
for num in df['Num']:
    if num in dittmann_racing:
        df.loc[[18,22,25],'Team'] = "Chris Dittmann Racing"
    else:
        df.loc[24, 'Team'] = "Fortec Motorsports"

print(df[df['Team'] == 'Dittmann Racing'])

# Changing data in Driver and Team column, to only name for 18,22,24,25 indexes
def extract_name(info):
    # Match RegEx [XX]
    match = re.search(r'\[.*?\]', info)
    if match:
        # split string after match and return first half
        return info.split(match.group())[0]
    return np.nan

# Use function to make new column
df['Driver'] = df['Driver and Team'].apply(extract_name)

# Repair a names for Drivers with NaN
df.loc[18,'Driver'] = "Kanato Le"
df.loc[22, 'Driver'] = "Martinius Stenshorne"
df.loc[25, 'Driver'] = "Javier Sagrera"
df.loc[24, 'Driver'] = "James Wharton"
print(df['Driver'])

# Drop 'Driver and Team' cause we got split columns for Team and Driver separetly
df.drop('Driver and Team', axis=1, inplace=True)
print(df.columns)

# Making points gap to leader column
for driver in df['Driver']:
    leader_points = max(df['Points'])
    df['Points Gap To Leader'] = df['Points'].apply(lambda x: x - leader_points)
print(df['Points Gap To Leader'])

# Drop NA columns for features races
df.dropna(axis=1, how='all', inplace=True)
print(df.columns)

# Checking df after cleaning
print(df.info())
print(df.describe())


# Analysis of driver and team performance

# Average points per race for the Team
team_mean_points = df.groupby(['Team'])['Points'].mean().sort_values(ascending=False)
print(team_mean_points)

# Average points per race for the Driver
driver_mean_points = df.groupby(['Driver'])['Points'].mean().sort_values(ascending=False) / 12
print(driver_mean_points)