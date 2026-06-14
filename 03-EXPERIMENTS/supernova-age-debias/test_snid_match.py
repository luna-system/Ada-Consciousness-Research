import pandas as pd
pred = pd.read_csv('data/pantheon_age_predictions.csv')
pantheon = pd.read_csv('data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat', sep=' ')

print('Prediction snids (first 5):', pred.snid.head().tolist())
print('Pantheon CIDs (first 5):', pantheon.CID.head().tolist())
print()

# Check overlap
pred_snids = set(pred.snid.astype(str).values)
cids = set(pantheon.CID.astype(str).values)
overlap = pred_snids & cids
print(f'Overlap: {len(overlap)}')
print('Examples:', list(overlap)[:5])
