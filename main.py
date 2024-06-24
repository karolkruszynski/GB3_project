import pandas as pd
import numpy as np
df = pd.read_excel('data.xlsx', na_filter=True)
print(df)

# Data Checking
print(df.columns)
print(df.info())
print(df.describe())

print(df['Driver and Team'].unique())