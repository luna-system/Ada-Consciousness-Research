import pandas as pd

df = pd.read_csv('data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat', sep='\s+')
print('Columns:', df.columns.tolist())
print()
print('First few rows:')
print(df.head())
