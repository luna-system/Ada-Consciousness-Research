import torch
import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
from astro_lannaformer import AstroLANNAformer

# Load NEW mixed model
model = AstroLANNAformer(
    n_photometry_bands=8,
    n_spectroscopy_bins=100,
    n_morphology_features=3,
    sedenion_dim=16,
    num_heads=8,
    num_layers=4,
    dropout=0.1,
    use_mlp=True,
    max_age=13.8,
)

checkpoint = torch.load('checkpoints/mixed_training/best.pt', map_location='cpu')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

print("Testing NEW mixed model:")
print("=" * 50)

# Test with different photometry inputs
test_cases = [
    ('bright', torch.tensor([15.0, 14.0, 13.0, 12.5, 12.0, 0.0, 0.0, 0.0], dtype=torch.float32)),
    ('faint', torch.tensor([25.0, 24.0, 23.0, 22.5, 22.0, 0.0, 0.0, 0.0], dtype=torch.float32)),
    ('blue', torch.tensor([18.0, 17.0, 18.0, 19.0, 20.0, 0.0, 0.0, 0.0], dtype=torch.float32)),
    ('red', torch.tensor([20.0, 19.0, 18.0, 17.0, 16.0, 0.0, 0.0, 0.0], dtype=torch.float32)),
    ('all_zeros', torch.zeros(8, dtype=torch.float32)),
]

for name, photometry in test_cases:
    with torch.no_grad():
        pred = model(
            photometry=photometry.unsqueeze(0),
            redshift=torch.tensor([0.1], dtype=torch.float32).unsqueeze(0),
        )
        print(f"  {name}: age={pred['age'].item():.4f}, unc={pred['uncertainty'].item():.4f}")

# Test with actual galaxies
df = pd.read_csv('data/pantheon_hosts_with_photometry.csv')
valid = df[df.dered_r.notna()].head(5)

print("\nActual galaxies:")
for _, row in valid.iterrows():
    photometry = torch.tensor([
        row['dered_u'], row['dered_g'], row['dered_r'],
        row['dered_i'], row['dered_z'],
        0.0, 0.0, 0.0,
    ], dtype=torch.float32)
    with torch.no_grad():
        pred = model(
            photometry=photometry.unsqueeze(0),
            redshift=torch.tensor([row['zHD']], dtype=torch.float32).unsqueeze(0),
        )
        print(f"  {row['snid']}: age={pred['age'].item():.4f}, unc={pred['uncertainty'].item():.4f}")
