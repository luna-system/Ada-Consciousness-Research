import pandas as pd
pred = pd.read_csv('data/pantheon_age_predictions.csv')

# Check for NaN in key columns
print('NaN counts:')
print(f"  zHD: {pred.zHD.isna().sum()}")
print(f"  mB: {pred.mB.isna().sum()}")
print(f"  evolution_free: {pred.evolution_free.isna().sum()}")
print()

# Check evolution-free sample
evo = pred[pred.evolution_free]
print(f'Evolution-free: {len(evo)}')
print(f'  zHD NaN: {evo.zHD.isna().sum()}')
print(f'  mB NaN: {evo.mB.isna().sum()}')
print(f'  zHD range: {evo.zHD.min():.3f} - {evo.zHD.max():.3f}')
print(f'  mB range: {evo.mB.min():.3f} - {evo.mB.max():.3f}')
