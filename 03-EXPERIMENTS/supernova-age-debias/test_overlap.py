import pandas as pd
pred = pd.read_csv('data/pantheon_age_predictions.csv')
color = pd.read_csv('data/young_hosts_with_coevality.csv')
print(f'Predictions snids: {len(pred)}')
print(f'Color young snids: {len(color[color.is_young_color])}')
print()
print('Sample prediction snids:', pred.snid.head().tolist())
print('Sample color snids:', color[color.is_young_color].snid.head().tolist())
print()
# Check overlap
pred_snids = set(pred.snid.values)
color_snids = set(color[color.is_young_color].snid.values)
overlap = pred_snids & color_snids
print(f'Overlap: {len(overlap)}')
print('Overlap examples:', list(overlap)[:5])
