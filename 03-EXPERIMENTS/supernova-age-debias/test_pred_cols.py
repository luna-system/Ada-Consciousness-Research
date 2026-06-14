import pandas as pd
df = pd.read_csv('data/pantheon_age_predictions.csv')
print('Columns:', list(df.columns))
print('Has mB:', 'mB' in df.columns)
print('Has CID:', 'CID' in df.columns)
