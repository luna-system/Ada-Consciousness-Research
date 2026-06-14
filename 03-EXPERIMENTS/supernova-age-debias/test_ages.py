import pandas as pd
df = pd.read_csv('data/pantheon_age_predictions.csv')
valid = df[df.predicted_age.notna()]
print(f'Valid predictions: {len(valid)}')
print(f'Age distribution:')
print(valid.predicted_age.describe())
print()
print(f'Age < 2 Gyr: {(valid.predicted_age < 2).sum()}')
print(f'Age < 5 Gyr: {(valid.predicted_age < 5).sum()}')
print(f'Age < 8 Gyr: {(valid.predicted_age < 8).sum()}')
print()
print('Youngest 10 galaxies:')
print(valid.nsmallest(10, 'predicted_age')[['snid', 'predicted_age', 'age_uncertainty', 'zHD']])
