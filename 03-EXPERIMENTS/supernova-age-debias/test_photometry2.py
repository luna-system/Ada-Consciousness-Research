import pandas as pd

df = pd.read_csv('data/pantheon_hosts_with_photometry.csv')
print(f'Total rows: {len(df)}')
print(f'Columns: {list(df.columns)}')
print()

# Check if objID is populated
print(f'With objID: {df.objID.notna().sum()}')
print(f'Without objID: {df.objID.isna().sum()}')
print()

# Show first few rows
print('First 5 rows:')
print(df[['snid', 'objID', 'ra', 'dec']].head())
