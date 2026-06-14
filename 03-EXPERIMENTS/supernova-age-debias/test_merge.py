import pandas as pd
pred = pd.read_csv('data/pantheon_age_predictions.csv')
pantheon = pd.read_csv('data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat', sep=' ')

# Try merge
merged = pred.merge(
    pantheon[['CID', 'mB', 'MU_SH0ES', 'MU_SH0ES_ERR_DIAG']],
    left_on='snid',
    right_on='CID',
    how='left'
)

print(f'Merged: {len(merged)}')
print(f'mB notna: {merged.mB.notna().sum()}')
print(f'Columns: {list(merged.columns)}')

# Check a specific example
print()
print('Example 2001az:')
print(merged[merged.snid == '2001az'][['snid', 'CID', 'mB', 'MU_SH0ES']])
