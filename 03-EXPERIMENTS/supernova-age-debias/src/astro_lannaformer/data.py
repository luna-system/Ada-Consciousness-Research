"""
Synthetic Galaxy Data Generator for AstroLANNAformer Training - FSPS Version

Generates synthetic galaxy spectra and photometry using REAL FSPS stellar population synthesis.
Creates training data with known ages for self-supervised pretraining.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from typing import Dict, List, Tuple, Optional
import json
import os
from pathlib import Path

# Try to import FSPS
try:
    import fsps
    FSPS_AVAILABLE = True
    print("✅ FSPS available! Using real stellar population synthesis.")
except ImportError:
    FSPS_AVAILABLE = False
    print("⚠️ FSPS not available. Using mock data generator.")

# Try to import torch
try:
    import torch
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️ PyTorch not available. Dataset classes will be limited.")

# Try to import torch
try:
    import torch
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️ PyTorch not available. Dataset classes will be limited.")


class SyntheticGalaxyGenerator:
    """
    Generate synthetic galaxies with known stellar population ages using FSPS.
    
    Uses FSPS (Flexible Stellar Population Synthesis) to generate realistic
    galaxy spectra and photometry across a range of ages, masses, metallicities,
    and star formation histories.
    """
    
    def __init__(
        self,
        n_galaxies: int = 10000,
        seed: int = 42,
        use_fsps: bool = True,
    ):
        self.n_galaxies = n_galaxies
        self.seed = seed
        self.use_fsps = use_fsps and FSPS_AVAILABLE
        
        # Set random seed
        np.random.seed(seed)
        
        # Initialize FSPS if available
        if self.use_fsps:
            self.sp = fsps.StellarPopulation(
                zcontinuous=1,  # Continuous metallicity
                imf_type=1,     # Chabrier IMF
                sfh=1,          # Exponential SFH
                dust_type=2,    # Calzetti dust
            )
            print(f"✅ FSPS initialized for {n_galaxies} galaxies")
        else:
            self.sp = None
            print(f"⚠️ Using mock generator for {n_galaxies} galaxies")
        
        # Photometric bands (SDSS + 2MASS + WISE)
        # Note: FSPS filter names may vary, using common ones
        self.bands = [
            'sdss_u', 'sdss_g', 'sdss_r', 'sdss_i', 'sdss_z',
            'twomass_J', 'twomass_H', 'twomass_Ks',
        ]
        
        # Spectral wavelength grid (simplified)
        self.wavelength_grid = np.linspace(3000, 10000, 1000)  # Angstroms
        
    def generate_galaxy_parameters(self) -> Dict[str, float]:
        """
        Generate random but physically plausible galaxy parameters.
        
        Returns:
            Dictionary with age, mass, metallicity, tau, Av, etc.
        """
        # Age: 0.1 to 13.8 Gyr (uniform in log space for more young galaxies)
        log_age = np.random.uniform(-1, 1.14)  # log10(0.1) to log10(13.8)
        age = 10**log_age
        
        # Mass: 1e8 to 1e12 Msun (uniform in log space)
        log_mass = np.random.uniform(8, 12)
        mass = 10**log_mass
        
        # Metallicity: -2.0 to 0.2 in log10(Z/Zsun)
        logzsol = np.random.uniform(-2.0, 0.2)
        
        # SFH timescale tau: 0.1 to 10 Gyr
        tau = 10**np.random.uniform(-1, 1)
        
        # Dust extinction Av: 0 to 3 mag
        Av = np.random.uniform(0, 3)
        
        # Redshift: 0.01 to 2.0
        redshift = np.random.uniform(0.01, 2.0)
        
        # Morphology parameters
        sersic_index = np.random.uniform(0.5, 6.0)  # 0.5 = disk, 6.0 = bulge
        ellipticity = np.random.uniform(0, 0.7)
        local_density = 10**np.random.uniform(-1, 2)  # Relative density
        
        return {
            'age': age,
            'mass': mass,
            'logzsol': logzsol,
            'tau': tau,
            'Av': Av,
            'redshift': redshift,
            'sersic_index': sersic_index,
            'ellipticity': ellipticity,
            'local_density': local_density,
        }
    
    def generate_fsps_galaxy(self, params: Dict[str, float]) -> Dict[str, np.ndarray]:
        """
        Generate galaxy SED and photometry using REAL FSPS.
        
        Args:
            params: Galaxy parameters from generate_galaxy_parameters()
            
        Returns:
            Dictionary with spectrum, photometry, and derived properties
        """
        if not self.use_fsps:
            return self.generate_mock_galaxy(params)
        
        try:
            # Set FSPS parameters
            self.sp.params['logzsol'] = params['logzsol']
            self.sp.params['tau'] = params['tau']
            self.sp.params['dust2'] = params['Av']
            
            # Generate spectrum
            wave, spec = self.sp.get_spectrum(tage=params['age'])
            
            # Get photometry - try available bands
            try:
                mags = self.sp.get_mags(bands=self.bands, tage=params['age'])
            except KeyError as e:
                # Some bands might not be available, use subset
                available_bands = ['sdss_u', 'sdss_g', 'sdss_r', 'sdss_i', 'sdss_z']
                mags = self.sp.get_mags(bands=available_bands, tage=params['age'])
                # Pad with zeros for missing bands
                mags = np.pad(mags, (0, 8 - len(mags)), mode='constant')
            
            # Interpolate to standard wavelength grid
            spec_interp = np.interp(
                self.wavelength_grid,
                wave,
                spec,
                left=0,
                right=0,
            )
            
            # Add noise to photometry (realistic observational errors)
            photometry_noise = np.random.normal(0, 0.05, len(mags))  # 5% noise
            photometry = mags + photometry_noise
            
            # Add noise to spectrum
            spec_noise = np.random.normal(0, np.max(spec_interp) * 0.02, len(spec_interp))
            spectrum = spec_interp + spec_noise
            
            return {
                'photometry': photometry,
                'spectrum': spectrum,
                'wavelength': self.wavelength_grid,
            }
            
        except Exception as e:
            print(f"⚠️ FSPS error: {e}. Using mock data.")
            return self.generate_mock_galaxy(params)
    
    def generate_mock_galaxy(self, params: Dict[str, float]) -> Dict[str, np.ndarray]:
        """
        Generate mock galaxy data without FSPS.
        
        Uses simple empirical relationships to create plausible data.
        """
        # Photometry: younger = bluer = lower magnitudes in u, g
        age = params['age']
        mass = params['mass']
        Av = params['Av']
        
        # Base magnitudes (arbitrary zero point)
        u = 20.0 + 0.5 * np.log10(mass / 1e10) + 0.3 * age + Av * 1.5
        g = 19.5 + 0.4 * np.log10(mass / 1e10) + 0.2 * age + Av * 1.2
        r = 19.0 + 0.3 * np.log10(mass / 1e10) + 0.15 * age + Av * 0.8
        i = 18.8 + 0.25 * np.log10(mass / 1e10) + 0.1 * age + Av * 0.6
        z = 18.5 + 0.2 * np.log10(mass / 1e10) + 0.08 * age + Av * 0.4
        J = 18.0 + 0.15 * np.log10(mass / 1e10) + 0.05 * age + Av * 0.2
        H = 17.8 + 0.12 * np.log10(mass / 1e10) + 0.03 * age + Av * 0.15
        K = 17.5 + 0.1 * np.log10(mass / 1e10) + 0.02 * age + Av * 0.1
        
        photometry = np.array([u, g, r, i, z, J, H, K])
        
        # Add noise
        photometry += np.random.normal(0, 0.05, 8)
        
        # Spectrum: simple blackbody + emission lines approximation
        wave = self.wavelength_grid
        # Effective temperature decreases with age
        teff = 8000 - 200 * age  # K (very rough!)
        teff = max(teff, 3000)
        
        # Blackbody spectrum (simplified)
        h = 6.626e-27  # erg s
        c = 3e10  # cm/s
        k = 1.38e-16  # erg/K
        
        spec = (2 * h * c**2 / wave**5) / (np.exp(h * c / (wave * k * teff)) - 1)
        spec = spec / np.max(spec)  # Normalize
        
        # Add emission lines for young galaxies
        if age < 2:
            # H-alpha at 6563 Angstroms
            ha_idx = np.argmin(np.abs(wave - 6563))
            spec[ha_idx-5:ha_idx+5] += 0.5 * (2 - age) / 2
            
            # [OIII] at 5007 Angstroms
            oiii_idx = np.argmin(np.abs(wave - 5007))
            spec[oiii_idx-3:oiii_idx+3] += 0.3 * (2 - age) / 2
        
        # Add noise
        spec += np.random.normal(0, 0.02, len(spec))
        
        return {
            'photometry': photometry,
            'spectrum': spec,
            'wavelength': wave,
        }
    
    def generate_catalog(self, save_path: Optional[str] = None) -> pd.DataFrame:
        """
        Generate full synthetic galaxy catalog.
        
        Args:
            save_path: Optional path to save catalog as CSV
            
        Returns:
            DataFrame with galaxy parameters and derived data
        """
        print(f"🌌 Generating {self.n_galaxies} synthetic galaxies...")
        if self.use_fsps:
            print(f"   Using REAL FSPS stellar population synthesis!")
        else:
            print(f"   Using mock generator (no FSPS)")
        
        galaxies = []
        
        for i in range(self.n_galaxies):
            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{self.n_galaxies} galaxies...")
            
            # Generate parameters
            params = self.generate_galaxy_parameters()
            
            # Generate galaxy data
            if self.use_fsps:
                data = self.generate_fsps_galaxy(params)
            else:
                data = self.generate_mock_galaxy(params)
            
            # Combine into record
            galaxy = {
                'galaxy_id': i,
                'age': params['age'],
                'mass': params['mass'],
                'logzsol': params['logzsol'],
                'tau': params['tau'],
                'Av': params['Av'],
                'redshift': params['redshift'],
                'sersic_index': params['sersic_index'],
                'ellipticity': params['ellipticity'],
                'local_density': params['local_density'],
            }
            
            # Add photometry
            for j, band in enumerate(['u', 'g', 'r', 'i', 'z', 'J', 'H', 'K']):
                galaxy[f'mag_{band}'] = data['photometry'][j]
            
            # Add spectrum (store as JSON string for DataFrame compatibility)
            galaxy['spectrum'] = json.dumps(data['spectrum'].tolist())
            
            galaxies.append(galaxy)
        
        # Create DataFrame
        df = pd.DataFrame(galaxies)
        
        # Save if requested
        if save_path:
            df.to_csv(save_path, index=False)
            print(f"💾 Catalog saved to {save_path}")
        
        print(f"✅ Generated {len(df)} galaxies!")
        print(f"   Age range: {df['age'].min():.2f} - {df['age'].max():.2f} Gyr")
        print(f"   Mass range: {df['mass'].min():.2e} - {df['mass'].max():.2e} Msun")
        print(f"   Redshift range: {df['redshift'].min():.3f} - {df['redshift'].max():.3f}")
        
        return df


class SyntheticGalaxyDataset(Dataset):
    """
    PyTorch Dataset for synthetic galaxy training data.
    """
    
    def __init__(
        self,
        catalog: pd.DataFrame,
        use_spectroscopy: bool = True,
        use_morphology: bool = True,
    ):
        self.catalog = catalog
        self.use_spectroscopy = use_spectroscopy
        self.use_morphology = use_morphology
        
        # Pre-parse spectra
        self.spectra = []
        for spec_str in catalog['spectrum']:
            self.spectra.append(np.array(json.loads(spec_str)))
        
    def __len__(self):
        return len(self.catalog)
    
    def __getitem__(self, idx):
        row = self.catalog.iloc[idx]
        
        # Photometry features
        photometry = torch.tensor([
            row['mag_u'], row['mag_g'], row['mag_r'], row['mag_i'],
            row['mag_z'], row['mag_J'], row['mag_H'], row['mag_K'],
        ], dtype=torch.float32)
        
        # Redshift
        redshift = torch.tensor([row['redshift']], dtype=torch.float32)
        
        # Target: age
        age = torch.tensor(row['age'], dtype=torch.float32)
        
        # Target: mass
        mass = torch.tensor(row['mass'], dtype=torch.float32)
        
        # Optional: spectroscopy
        spectroscopy = None
        if self.use_spectroscopy:
            spectroscopy = torch.tensor(self.spectra[idx], dtype=torch.float32)
        
        # Optional: morphology
        morphology = None
        if self.use_morphology:
            morphology = torch.tensor([
                row['sersic_index'],
                row['ellipticity'],
                row['local_density'],
            ], dtype=torch.float32)
        
        return {
            'features': {
                'photometry': photometry,
                'redshift': redshift,
                'spectroscopy': spectroscopy,
                'morphology': morphology,
            },
            'targets': {
                'age': age,
                'mass': mass,
            },
        }


def create_dataloaders(
    catalog: pd.DataFrame,
    batch_size: int = 32,
    train_frac: float = 0.8,
    val_frac: float = 0.1,
    use_spectroscopy: bool = True,
    use_morphology: bool = True,
    num_workers: int = 0,
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Create train/val/test DataLoaders from catalog.
    
    Returns:
        train_loader, val_loader, test_loader
    """
    # Shuffle catalog
    catalog = catalog.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Split
    n_total = len(catalog)
    n_train = int(n_total * train_frac)
    n_val = int(n_total * val_frac)
    
    train_catalog = catalog.iloc[:n_train]
    val_catalog = catalog.iloc[n_train:n_train + n_val]
    test_catalog = catalog.iloc[n_train + n_val:]
    
    # Create datasets
    train_dataset = SyntheticGalaxyDataset(train_catalog, use_spectroscopy, use_morphology)
    val_dataset = SyntheticGalaxyDataset(val_catalog, use_spectroscopy, use_morphology)
    test_dataset = SyntheticGalaxyDataset(test_catalog, use_spectroscopy, use_morphology)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    print(f"📊 DataLoaders created:")
    print(f"   Train: {len(train_dataset)} galaxies")
    print(f"   Val: {len(val_dataset)} galaxies")
    print(f"   Test: {len(test_dataset)} galaxies")
    
    return train_loader, val_loader, test_loader


def test_generator():
    """Test the synthetic galaxy generator."""
    print("🧪 Testing Synthetic Galaxy Generator\n")
    
    # Create generator with FSPS
    gen = SyntheticGalaxyGenerator(n_galaxies=100, use_fsps=True)
    
    # Generate catalog
    catalog = gen.generate_catalog()
    
    print(f"\n📊 Catalog statistics:")
    print(f"   Columns: {list(catalog.columns)}")
    print(f"   Shape: {catalog.shape}")
    print(f"\n   First galaxy:")
    print(catalog.iloc[0])
    
    # Create dataset
    dataset = SyntheticGalaxyDataset(catalog)
    
    print(f"\n📊 Dataset:")
    print(f"   Length: {len(dataset)}")
    
    # Get first sample
    sample = dataset[0]
    print(f"\n   First sample:")
    for key, value in sample['features'].items():
        if value is not None:
            print(f"     {key}: {value.shape}")
    for key, value in sample['targets'].items():
        print(f"     target {key}: {value.shape}")
    
    # Create dataloaders
    train_loader, val_loader, test_loader = create_dataloaders(catalog, batch_size=16)
    
    # Test batch
    batch = next(iter(train_loader))
    print(f"\n📊 Batch:")
    for key, value in batch['features'].items():
        if value is not None:
            print(f"     {key}: {value.shape}")
    
    print(f"\n✅ Generator works!")


if __name__ == "__main__":
    print("🌌 Synthetic Galaxy Data Generator - FSPS Version\n")
    print("=" * 60)
    print()
    
    test_generator()
    
    print()
    print("=" * 60)
    print("\n💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'Real stellar populations for real learning!'")
