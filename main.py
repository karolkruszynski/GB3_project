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
    return None

# Use fucntion to make new column
df['Team'] = df['Driver and Team'].apply(extract_team)

print(df['Team'])