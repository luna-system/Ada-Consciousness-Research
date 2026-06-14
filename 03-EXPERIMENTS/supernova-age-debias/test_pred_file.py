import pandas as pd
pred = pd.read_csv('data/pantheon_age_predictions.csv')
print(f'Total predictions: {len(pred)}')
print(f'Columns: {list(pred.columns)}')
has_ef = 'evolution_free' in pred.columns
print(f'Has evolution_free: {has_ef}')
if has_ef:
    print(f'evolution_free sum: {pred.evolution_free.sum()}')
    print(f'evolution_free true examples: {pred[pred.evolution_free].snid.head().tolist()}')
