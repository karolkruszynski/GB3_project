import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

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
team_mean_points_df = team_mean_points.reset_index()
team_mean_points_df.columns = ['Team', 'Points for Team']
# Ploting data
plt.figure(figsize=(13,6))
sns.scatterplot(data=team_mean_points_df, x='Points for Team', y='Team', hue='Team')
plt.show()

# Average points per race for the Driver
driver_mean_points = df.groupby(['Driver'])['Points'].mean().sort_values(ascending=False) / 12
# Convert Series na DataFrame
driver_mean_points_df = driver_mean_points.reset_index()
driver_mean_points_df.columns = ['Driver', 'Average Points per Race']
# Ploting data
plt.figure(figsize=(13,6))
sns.barplot(data=driver_mean_points_df, x='Average Points per Race', y='Driver')
plt.show()

# Winning rate for Driver
# Feature Races data
races = ['R01', 'R02', 'R04', 'R05', 'R07', 'R08', 'R10', 'R11']

# If wins add +1 to Winning rate for Driver column
df['Wins in Feature Race'] = df[races].apply(lambda row: (row == 35).sum(), axis=1)
print(df[['Wins in Feature Race', 'Driver', 'Team']].sort_values(ascending=False, by='Wins in Feature Race').head(5))

# Drivers who score point in every race
race_columns = ['R01', 'R02', 'R03', 'R04', 'R05', 'R07', 'R08', 'R09', 'R10', 'R11', 'R12']
# Check if all data in row are greater than 0
df_filtered = df[df[race_columns].gt(0).all(axis=1)]
# Filter drivers by df with gt0
drivers_with_points = df_filtered['Driver'].unique()
print(drivers_with_points)

## WHAT IF?

# What if we count points only for Sprint Races?
df_filtered = df[['R03', 'R09', 'R12', 'Driver']].copy()
df_filtered.fillna(0, inplace=True)
df_filtered['Sprint_Points'] = df_filtered[['R03', 'R09', 'R12']].sum(axis=1)
print(df_filtered[['Driver', 'Sprint_Points']].sort_values(ascending=False, by='Sprint_Points'))

# What if we count points only for Feature Races?
df_filtered2 = df[['R01', 'R02', 'R04', 'R05', 'R07', 'R08', 'R10', 'R11', 'Driver']].copy()
df_filtered2.fillna(0, inplace=True)
df_filtered2['Feature_Points'] = df_filtered2[['R01', 'R02', 'R04', 'R05', 'R07', 'R08', 'R10', 'R11']].sum(axis=1)
print(df_filtered2[['Driver', 'Feature_Points']].sort_values(ascending=False, by='Feature_Points'))

# Plot with Sprint Races and Feature Races side by side for Top10 Drivers

df_filtered_conn = pd.concat([df_filtered['Driver'], df_filtered['Sprint_Points'], df_filtered2['Feature_Points']], axis=1).head(10)
df_melted = pd.melt(df_filtered_conn, id_vars='Driver', var_name='Race_Type', value_name='Points')
# Ploting
plt.figure(figsize=(12, 6))
sns.barplot(data=df_melted, x='Driver', y='Points', hue='Race_Type', dodge=True)
plt.title('Comparison of Sprint Points and Feature Points')
plt.xlabel('Driver')
plt.ylabel('Points')
plt.xticks(rotation=90)
plt.legend(title='Race Type', loc='upper right')
plt.tight_layout()
plt.show()

df.to_excel('gb3_data.xlsx')