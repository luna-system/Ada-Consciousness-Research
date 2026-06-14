import torch
import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))
from astro_lannaformer import AstroLANNAformer

# Load model
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

checkpoint = torch.load('checkpoints/finetune_real/best_v2.pt', map_location='cpu')
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()

# Load a real galaxy
df = pd.read_csv('data/pantheon_hosts_with_photometry.csv')
galaxy = df[df.dered_r.notna()].iloc[0]

photometry = torch.tensor([
    galaxy['dered_u'], galaxy['dered_g'], galaxy['dered_r'],
    galaxy['dered_i'], galaxy['dered_z'],
    0.0, 0.0, 0.0,
], dtype=torch.float32)

redshift = torch.tensor([galaxy['zHD']], dtype=torch.float32)

print(f"Testing with galaxy {galaxy['snid']} (z={galaxy['zHD']:.4f})")
print(f"Photometry: u={galaxy['dered_u']:.2f}, g={galaxy['dered_g']:.2f}, r={galaxy['dered_r']:.2f}")
print()

# Test 1: Original prediction
with torch.no_grad():
    pred = model(photometry=photometry.unsqueeze(0), redshift=redshift.unsqueeze(0))
    original_age = pred['age'].item()
    print(f"Original: age={original_age:.4f}")

# Test 2: Shuffle photometry bands
shuffled = photometry[torch.randperm(8)]
with torch.no_grad():
    pred = model(photometry=shuffled.unsqueeze(0), redshift=redshift.unsqueeze(0))
    print(f"Shuffled: age={pred['age'].item():.4f}, diff={pred['age'].item() - original_age:.4f}")

# Test 3: Set all photometry to zero
zeros = torch.zeros(8)
with torch.no_grad():
    pred = model(photometry=zeros.unsqueeze(0), redshift=redshift.unsqueeze(0))
    print(f"All zeros: age={pred['age'].item():.4f}, diff={pred['age'].item() - original_age:.4f}")

# Test 4: Set all photometry to mean value
mean_val = photometry.mean()
mean_tensor = torch.full((8,), mean_val)
with torch.no_grad():
    pred = model(photometry=mean_tensor.unsqueeze(0), redshift=redshift.unsqueeze(0))
    print(f"All mean: age={pred['age'].item():.4f}, diff={pred['age'].item() - original_age:.4f}")

# Test 5: Only use redshift (no photometry variation)
for test_z in [0.01, 0.1, 0.5, 1.0]:
    test_redshift = torch.tensor([test_z])
    with torch.no_grad():
        pred = model(photometry=photometry.unsqueeze(0), redshift=test_redshift.unsqueeze(0))
        print(f"z={test_z:.2f}: age={pred['age'].item():.4f}")

print()
print("If 'Shuffled' and 'All zeros' give very different results, model IS using photometry.")
print("If they're all similar, model is ignoring photometry and just predicting mean!")
