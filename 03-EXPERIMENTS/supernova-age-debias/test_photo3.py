import pandas as pd
df = pd.read_csv('data/pantheon_hosts_with_photometry.csv')
print(f'Total: {len(df)}')
print(f'With dered_r: {df.dered_r.notna().sum()}')
print(f'Without dered_r: {df.dered_r.isna().sum()}')
print()
print('First 3 with photometry:')
print(df[df.dered_r.notna()][['snid', 'dered_u', 'dered_g', 'dered_r', 'zHD']].head(3))
