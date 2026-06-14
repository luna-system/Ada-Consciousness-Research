import pandas as pd
pred = pd.read_csv('data/pantheon_age_predictions.csv')
print(f'Columns: {list(pred.columns)}')
print(f'Has mB: {"mB" in pred.columns}')
print(f'Has MU_SH0ES: {"MU_SH0ES" in pred.columns}')
if 'mB' in pred.columns:
    print(f'mB NaN: {pred.mB.isna().sum()}')
    print(f'mB not NaN: {pred.mB.notna().sum()}')
