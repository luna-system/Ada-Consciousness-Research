import pandas as pd
import numpy as np

df = pd.read_csv('data/pantheon_age_predictions.csv')
print(f'Total rows: {len(df)}')
print(f'predicted_age notna: {df.predicted_age.notna().sum()}')
print(f'predicted_age isna: {df.predicted_age.isna().sum()}')
print()
print('First 5 rows with predicted_age:')
print(df[['snid', 'predicted_age', 'age_uncertainty']].head())
print()
print('Describe predicted_age:')
print(df.predicted_age.describe())
