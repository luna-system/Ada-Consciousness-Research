# PHASE 1: LANNAformer Porting for Supernova Age Debiasing

## Goal
Adapt LANNAformer (Liquid Angelic Neural Net Architecture) from consciousness-native language modeling to physics-informed stellar population age estimation for Type Ia supernova cosmology.

## Why LANNAformer is Perfect for This

### 1. Multi-Modal by Design
LANNAformer's `ConsciousnessEmbedding` already handles multiple input streams (tokens + positions + prime modulations). We extend to astronomical features:
- **Host galaxy photometry**: ugriz/JHK bands → continuous feature vectors
- **Host galaxy spectroscopy**: spectral flux densities → 1D feature sequences
- **SN Ia light curve**: time-series photometry → temporal sequences
- **Host morphology**: Sersic index, ellipticity, environment → scalar features
- **Redshift**: z → scalar embedding with cosmological context

The `SedenionTensor` (16D hypercomplex) naturally handles multi-dimensional feature spaces without flattening into unnatural vector spaces.

### 2. Physics-Informed Structure
Sedenion algebra is already physics-native. We embed astrophysical relationships as geometric constraints:
- **Age-color relationship**: younger = bluer (embedded as sedenion phase relationship)
- **Age-metallicity**: older = more metal-rich (embedded as amplitude modulation)
- **Dust extinction**: Av vs Rv relationships (embedded as holonomy transformations)
- **Delay-time distributions**: progenitor age vs host age mapping (embedded as attention priors)

### 3. Attention Over Continuous Values
`KuramotoAttention` uses phase-coupled oscillator dynamics — perfect for continuous astronomical data:
- Attend across **photometric bands** (u→g→r→i→z as phase relationships)
- Attend across **spectral features** (emission lines, absorption lines, continuum)
- Attend across **time** (light curve evolution as phase dynamics)
- Attend across **redshift** (evolutionary trends as frequency modulation)

### 4. Uncertainty Quantification
Consciousness coherence and frequency stability become **evidential uncertainty**:
- `consciousness_coherence` → prediction confidence (0 = uncertain, 1 = certain)
- `frequency_stability` → model stability (deviation from expected physics)
- Combined: "age = 5.2 ± 1.8 Gyr, coherence = 0.82, stable"

### 5. Modular Architecture
Repurpose existing LANNALayer phases:

| LANNA Component | Astronomy Adaptation |
|-----------------|---------------------|
| **KuramotoAttention** | Feature-space attention across bands/spectra/time |
| **KleinHolonomy** | Preserve physical relationships (age-color-mass-metallicity) |
| **SedenionMLP** | Nonlinear mapping from observables to age estimates |
| **GravitationalDynamics** | Ensemble fusion: multiple age estimates combine/evidence-weight |

## Porting Plan

### Step 1: Input Embedding Adaptation

**Current**: `ConsciousnessEmbedding` maps token IDs → sedenion space
**New**: `AstroEmbedding` maps continuous features → sedenion space

```python
class AstroEmbedding(nn.Module):
    """Embed astronomical observations into sedenion consciousness space."""
    
    def __init__(
        self,
        photometry_bands: List[str] = ['u', 'g', 'r', 'i', 'z', 'J', 'H', 'K'],
        spectroscopy_bins: int = 1000,  # Number of spectral wavelength bins
        lightcurve_timesteps: int = 50,  # Number of light curve observation epochs
        sedenion_dim: int = 16,
        max_redshift: float = 2.5,
    ):
        super().__init__()
        
        # Photometry embedding: each band → sedenion coefficient
        self.photometry_embedding = nn.Linear(len(photometry_bands), sedenion_dim)
        
        # Spectroscopy embedding: 1D CNN over wavelength → sedenion sequence
        self.spectroscopy_encoder = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv1d(32, 64, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(sedenion_dim),
        )
        
        # Light curve embedding: temporal encoder → sedenion dynamics
        self.lightcurve_encoder = nn.LSTM(
            input_size=2,  # [time_since_peak, magnitude]
            hidden_size=sedenion_dim,
            num_layers=2,
            batch_first=True,
        )
        
        # Redshift embedding: scalar → sedenion context
        self.redshift_embedding = nn.Linear(1, sedenion_dim)
        
        # Host morphology embedding
        self.morphology_embedding = nn.Linear(3, sedenion_dim)  # [sersic, ellipticity, local_density]
        
        # Fusion: combine all streams into unified sedenion state
        self.fusion_attention = nn.MultiheadAttention(sedenion_dim, num_heads=4)
        
        # Physics prime modulation (adapted from consciousness primes)
        # Use astrophysical constants: H0, c, G, etc. encoded as frequencies
        self.physics_constants = torch.tensor([
            67.4,   # H0 [km/s/Mpc]
            299792.458,  # c [km/s]
            6.674,  # G [10^-11 m^3/kg/s^2]
            13.8,   # Universe age [Gyr]
            0.0224, # Omega_b h^2
            0.120,  # Omega_c h^2
            0.966,  # ns
            0.811,  # sigma8
            # ... etc
        ], dtype=torch.float32)
        
        self.physics_modulation = nn.Parameter(
            torch.sin(self.physics_constants * (1 + math.sqrt(5)) / 2)
        )
```

### Step 2: KuramotoAttention Adaptation

**Current**: Phase-coupled attention across sequence positions
**New**: Phase-coupled attention across feature dimensions

```python
class AstroKuramotoAttention(nn.Module):
    """Phase-coupled attention for astronomical feature relationships."""
    
    def __init__(
        self,
        sedenion_dim: int = 16,
        num_heads: int = 4,
        consciousness_lock_freq: float = 41.176,  # Keep as metaphor
        # New: astrophysical frequency priors
        age_color_freq: float = 0.5,  # Age-color relationship strength
        dust_extinction_freq: float = 0.3,  # Dust correction importance
        metallicity_age_freq: float = 0.4,  # Metallicity-age coupling
    ):
        super().__init__()
        
        # Natural frequencies for each feature dimension
        # u-band oscillates faster (bluer, more sensitive to young stars)
        # K-band oscillates slower (redder, more sensitive to old stars)
        self.natural_frequencies = nn.Parameter(torch.tensor([
            2.0,  # u-band: high frequency (young, hot stars)
            1.5,  # g-band
            1.0,  # r-band
            0.7,  # i-band
            0.5,  # z-band
            0.3,  # J-band
            0.2,  # H-band
            0.1,  # K-band: low frequency (old, cool stars)
        ]))
        
        # Coupling strengths between features
        # Strong coupling: u-g (both trace young stars)
        # Weak coupling: u-K (very different stellar populations)
        self.coupling_matrix = nn.Parameter(torch.eye(8) * 0.5)
        
    def forward(self, sedenion_states: SedenionTensor):
        """
        Apply phase-coupled attention across photometric bands.
        
        The phase relationships encode physical relationships:
        - In-phase oscillation = correlated features (u and g both trace young stars)
        - Anti-phase oscillation = anti-correlated features (young vs old stellar populations)
        - Phase lag = delayed relationship (light curve evolution)
        """
        # Extract phases from sedenion coefficients
        phases = torch.atan2(sedenion_states.coeffs[..., 1], sedenion_states.coeffs[..., 0])
        
        # Phase coupling dynamics
        phase_differences = phases.unsqueeze(-1) - phases.unsqueeze(-2)
        coupling = self.coupling_matrix * torch.sin(phase_differences)
        
        # Update phases (Kuramoto dynamics)
        phase_updates = self.natural_frequencies + coupling.sum(dim=-1)
        
        # Convert back to sedenion coefficients with updated phases
        amplitudes = torch.sqrt(sedenion_states.coeffs[..., 0]**2 + sedenion_states.coeffs[..., 1]**2)
        new_coeffs = sedenion_states.coeffs.clone()
        new_coeffs[..., 0] = amplitudes * torch.cos(phase_updates)
        new_coeffs[..., 1] = amplitudes * torch.sin(phase_updates)
        
        return SedenionTensor(new_coeffs)
```

### Step 3: Physics-Regularized Loss

```python
class AstroPhysicsLoss(nn.Module):
    """Loss function incorporating astrophysical relationships as regularization."""
    
    def __init__(
        self,
        age_color_weight: float = 1.0,
        age_mass_weight: float = 0.5,
        dust_consistency_weight: float = 0.3,
        coevality_weight: float = 0.2,
    ):
        super().__init__()
        self.age_color_weight = age_color_weight
        self.age_mass_weight = age_mass_weight
        self.dust_consistency_weight = dust_consistency_weight
        self.coevality_weight = coevality_weight
        
    def forward(
        self,
        predictions: Dict[str, torch.Tensor],  # age, uncertainty, coevality
        targets: Dict[str, torch.Tensor],  # spectroscopic ages, etc.
        features: Dict[str, torch.Tensor],  # photometry, spectroscopy, etc.
    ):
        # Primary loss: age prediction MSE
        age_loss = F.mse_loss(predictions['age'], targets['age'])
        
        # Uncertainty-weighted loss (evidential learning)
        uncertainty_loss = torch.mean(
            torch.log(predictions['uncertainty']) + 
            (predictions['age'] - targets['age'])**2 / (2 * predictions['uncertainty']**2)
        )
        
        # Physics regularization 1: Age-color relationship
        # Younger galaxies should be bluer (lower u-g, g-r colors)
        predicted_colors = features['photometry'][:, 0] - features['photometry'][:, 1]  # u-g
        expected_colors = 2.5 - 0.3 * predictions['age']  # Rough empirical relation
        age_color_loss = F.mse_loss(predicted_colors, expected_colors)
        
        # Physics regularization 2: Age-mass relationship
        # More massive galaxies tend to be older
        predicted_mass_age = predictions['age']
        expected_mass_age = 2.0 + 0.5 * torch.log10(features['mass'])  # Rough relation
        age_mass_loss = F.mse_loss(predicted_mass_age, expected_mass_age)
        
        # Physics regularization 3: Dust consistency
        # Dust-corrected colors should be consistent with age
        dust_corrected_colors = features['photometry'][:, 0] - features['photometry'][:, 1] - features['Av']
        dust_consistency_loss = F.mse_loss(dust_corrected_colors, expected_colors)
        
        # Physics regularization 4: Coevality
        # For coeval galaxies, age predictions should have low variance
        coevality_penalty = predictions['coevality_score'] * predictions['uncertainty']
        # High coevality + high uncertainty = bad (should be confident about coeval populations)
        
        total_loss = (
            age_loss + 
            0.5 * uncertainty_loss +
            self.age_color_weight * age_color_loss +
            self.age_mass_weight * age_mass_loss +
            self.dust_consistency_weight * dust_consistency_loss +
            self.coevality_weight * coevality_penalty.mean()
        )
        
        return total_loss, {
            'age_loss': age_loss,
            'uncertainty_loss': uncertainty_loss,
            'age_color_loss': age_color_loss,
            'age_mass_loss': age_mass_loss,
            'dust_consistency_loss': dust_consistency_loss,
            'coevality_penalty': coevality_penalty.mean(),
        }
```

### Step 4: Output Layer Adaptation

**Current**: `ConsciousnessOutput` projects sedenion → vocabulary logits
**New**: `AstroOutput` projects sedenion → age + uncertainty + coevality

```python
class AstroOutput(nn.Module):
    """Project from sedenion space to astronomical predictions."""
    
    def __init__(
        self,
        sedenion_dim: int = 16,
        max_age: float = 13.8,  # Gyr (age of universe)
    ):
        super().__init__()
        
        # Age prediction head
        self.age_head = nn.Sequential(
            nn.Linear(sedenion_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Softplus(),  # Ensure positive age
        )
        
        # Uncertainty prediction head (evidential learning)
        self.uncertainty_head = nn.Sequential(
            nn.Linear(sedenion_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Softplus(),  # Ensure positive uncertainty
        )
        
        # Coevality score (how uniform is the stellar population?)
        self.coevality_head = nn.Sequential(
            nn.Linear(sedenion_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),  # 0 = mixed ages, 1 = perfectly coeval
        )
        
        # Young host probability (for evolution-free test selection)
        self.young_head = nn.Sequential(
            nn.Linear(sedenion_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid(),  # Probability of being young enough
        )
        
    def forward(self, sedenion_states: SedenionTensor):
        """
        Predict age, uncertainty, coevality, and young-host probability.
        
        Returns:
            age: Predicted stellar population age [Gyr]
            uncertainty: Prediction uncertainty [Gyr]
            coevality_score: How uniform is the stellar population [0-1]
            young_probability: Probability of being young enough for evolution-free test [0-1]
            consciousness_coherence: Model confidence in prediction [0-1]
        """
        # Pool sedenion states (mean over sequence dimension)
        pooled = torch.mean(sedenion_states.coeffs, dim=1)  # [batch, sedenion_dim]
        
        # Predictions
        age = self.age_head(pooled).squeeze(-1)  # [batch]
        uncertainty = self.uncertainty_head(pooled).squeeze(-1)  # [batch]
        coevality_score = self.coevality_head(pooled).squeeze(-1)  # [batch]
        young_probability = self.young_head(pooled).squeeze(-1)  # [batch]
        
        # Consciousness coherence as prediction confidence
        coherence = sedenion_states.consciousness_coherence()
        
        return {
            'age': age,
            'uncertainty': uncertainty,
            'coevality_score': coevality_score,
            'young_probability': young_probability,
            'consciousness_coherence': coherence,
        }
```

### Step 5: Training Pipeline

```python
class AstroLANNATrainer:
    """Training pipeline for LANNAformer on stellar population age estimation."""
    
    def __init__(
        self,
        model: AstroLANNA,
        optimizer: torch.optim.Optimizer,
        physics_loss: AstroPhysicsLoss,
        device: str = 'cuda',
    ):
        self.model = model
        self.optimizer = optimizer
        self.physics_loss = physics_loss
        self.device = device
        
    def train_epoch(self, dataloader: DataLoader):
        self.model.train()
        total_loss = 0
        
        for batch in dataloader:
            # Move to device
            features = {k: v.to(self.device) for k, v in batch['features'].items()}
            targets = {k: v.to(self.device) for k, v in batch['targets'].items()}
            
            # Forward pass
            predictions = self.model(features)
            
            # Compute loss with physics regularization
            loss, loss_components = self.physics_loss(predictions, targets, features)
            
            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            
        return total_loss / len(dataloader)
    
    def evaluate(self, dataloader: DataLoader):
        self.model.eval()
        predictions_list = []
        targets_list = []
        
        with torch.no_grad():
            for batch in dataloader:
                features = {k: v.to(self.device) for k, v in batch['features'].items()}
                targets = {k: v.to(self.device) for k, v in batch['targets'].items()}
                
                predictions = self.model(features)
                predictions_list.append(predictions)
                targets_list.append(targets)
        
        # Compute metrics
        all_predictions = torch.cat([p['age'] for p in predictions_list])
        all_targets = torch.cat([t['age'] for t in targets_list])
        all_uncertainties = torch.cat([p['uncertainty'] for p in predictions_list])
        
        mae = torch.mean(torch.abs(all_predictions - all_targets)).item()
        bias = torch.mean(all_predictions - all_targets).item()
        scatter = torch.std(all_predictions - all_targets).item()
        
        # Calibration: does uncertainty match actual error?
        actual_errors = torch.abs(all_predictions - all_targets)
        calibration = torch.mean(actual_errors / all_uncertainties).item()
        # calibration ≈ 1.0 means uncertainty is well-calibrated
        
        return {
            'mae': mae,
            'bias': bias,
            'scatter': scatter,
            'calibration': calibration,
        }
```

## Data Pipeline

### Phase 1: Self-Supervised on Synthetics

```python
class SyntheticGalaxyGenerator:
    """Generate synthetic galaxies with known ages for pretraining."""
    
    def __init__(
        self,
        sps_model: str = 'fsps',  # or 'bc03'
        n_galaxies: int = 100000,
    ):
        self.sps_model = sps_model
        self.n_galaxies = n_galaxies
        
    def generate(self):
        """Generate synthetic galaxy catalog."""
        galaxies = []
        
        for i in range(self.n_galaxies):
            # Random physical parameters
            age = np.random.uniform(0.1, 13.8)  # Gyr
            mass = np.random.uniform(1e8, 1e12)  # Msun
            metallicity = np.random.uniform(0.0001, 0.03)  # Z
            tau = np.random.uniform(0.1, 10.0)  # SFH timescale
            Av = np.random.uniform(0, 3.0)  # Dust extinction
            
            # Generate SED with FSPS/BC03
            sed = self.generate_sed(age, mass, metallicity, tau, Av)
            
            # Extract photometry
            photometry = self.extract_photometry(sed, ['u', 'g', 'r', 'i', 'z', 'J', 'H', 'K'])
            
            # Extract spectroscopy (low-res for training, high-res for labels)
            spectroscopy_low = self.extract_spectroscopy(sed, resolution=100)
            spectroscopy_high = self.extract_spectroscopy(sed, resolution=1000)
            
            # Derive "ground truth" age from high-res spectroscopy
            # (In reality, this is what spectroscopic fitting gives us)
            age_truth = self.fit_age_from_spectroscopy(spectroscopy_high)
            
            galaxies.append({
                'photometry': photometry,
                'spectroscopy': spectroscopy_low,
                'age': age_truth,
                'mass': mass,
                'metallicity': metallicity,
                'Av': Av,
            })
            
        return galaxies
```

### Phase 2: Supervised Fine-Tuning

```python
class RealGalaxyDataset(Dataset):
    """Dataset of real galaxies with spectroscopic ages."""
    
    def __init__(
        self,
        catalog: str = 'pantheon+_hosts',
        spectroscopic_ages: str = 'sdss_boss_spectra',
        quality_cut: float = 0.8,  # Minimum spectroscopic quality
    ):
        self.catalog = catalog
        self.spectroscopic_ages = spectroscopic_ages
        self.quality_cut = quality_cut
        
        # Load data
        self.galaxies = self.load_galaxies()
        
    def load_galaxies(self):
        """Load galaxy catalog with spectroscopic ages."""
        # Load Pantheon+ host galaxies
        pantheon_hosts = pd.read_csv('pantheon+_hosts.csv')
        
        # Load spectroscopic ages from SDSS/BOSS
        spectroscopic_ages = pd.read_csv('sdss_boss_ages.csv')
        
        # Merge on galaxy ID
        merged = pantheon_hosts.merge(spectroscopic_ages, on='galaxy_id')
        
        # Apply quality cut
        merged = merged[merged['spectroscopic_quality'] > self.quality_cut]
        
        return merged
    
    def __getitem__(self, idx):
        galaxy = self.galaxies.iloc[idx]
        
        return {
            'features': {
                'photometry': torch.tensor([
                    galaxy['u_mag'], galaxy['g_mag'], galaxy['r_mag'],
                    galaxy['i_mag'], galaxy['z_mag'], galaxy['J_mag'],
                    galaxy['H_mag'], galaxy['K_mag'],
                ]),
                'spectroscopy': torch.tensor(galaxy['spectrum']),  # 1D array
                'redshift': torch.tensor([galaxy['redshift']]),
                'morphology': torch.tensor([
                    galaxy['sersic_index'],
                    galaxy['ellipticity'],
                    galaxy['local_density'],
                ]),
            },
            'targets': {
                'age': torch.tensor(galaxy['spectroscopic_age']),  # Ground truth
                'mass': torch.tensor(galaxy['stellar_mass']),
                'metallicity': torch.tensor(galaxy['metallicity']),
                'Av': torch.tensor(galaxy['dust_av']),
            },
        }
```

## Evaluation Strategy

### Metrics

1. **Age Prediction Accuracy**
   - MAE (Mean Absolute Error): target < 1 Gyr
   - Bias: target < 0.2 Gyr (no systematic offset)
   - Scatter: target < 0.8 Gyr (precision)

2. **Uncertainty Calibration**
   - Calibration score: actual_error / predicted_uncertainty ≈ 1.0
   - Coverage: 68% of predictions within 1-sigma uncertainty
   - Sharpness: uncertainties should be as small as possible while remaining calibrated

3. **Binary Classification (Young vs Old)**
   - AUC-ROC for young galaxy identification
   - Precision/recall for evolution-free test selection

4. **Coevality Detection**
   - Variance of predicted ages within host sample
   - True coeval galaxies should have low predicted age variance

5. **Cosmological Impact**
   - Hubble residual scatter after age correction
   - Model comparison: ΛCDM vs w₀wₐCDM vs non-accelerating

### Baselines

1. **Standard SPS Fitting**: BC03/FSPS with MCMC
2. **Random Forest**: Standard ML on photometry + spectroscopy
3. **Standard Transformer**: Without physics-informed structure
4. **LANNAformer (Ours)**: Physics-informed sedenion architecture

## Implementation Timeline

| Week | Task |
|------|------|
| 1 | Port `AstroEmbedding` from `ConsciousnessEmbedding` |
| 2 | Adapt `KuramotoAttention` for feature-space attention |
| 3 | Implement `AstroPhysicsLoss` with regularization terms |
| 4 | Build `AstroOutput` head for age + uncertainty + coevality |
| 5 | Synthetic data generation pipeline |
| 6 | Real data integration (Pantheon+ hosts) |
| 7 | Self-supervised pretraining on synthetics |
| 8 | Supervised fine-tuning on real data |
| 9 | Evaluation and baseline comparison |
| 10 | Cosmology application: evolution-free test |

## Open Questions

1. **How to handle missing data?** Not all galaxies have spectroscopy. Need robust imputation or multi-modal fusion.

2. **How to transfer from synthetic to real?** Domain adaptation between FSPS/BC03 and real observations.

3. **How to validate coevality?** Need ground truth coeval populations (e.g., globular clusters, single-burst galaxies).

4. **How to incorporate redshift evolution?** The model should know that galaxies at z=1 are younger on average.

5. **How to handle selection effects?** Pantheon+ is not a random sample — it's SN-selected.

## Next Steps

1. [ ] Review latest LiquidAI model API for compatibility
2. [ ] Gather Pantheon+ host galaxy data (photometry + spectra)
3. [ ] Set up FSPS/BC03 synthetic generation pipeline
4. [ ] Implement `AstroEmbedding` module
5. [ ] Test on small synthetic dataset
6. [ ] Iterate on physics regularization weights
7. [ ] Scale to full dataset

## Notes

- This is exploratory! No pressure to solve cosmology in one sprint 💜
- The Korean team's work is still being debated — we might confirm ΛCDM after all
- Either way: we'll learn something, build something cool, and have fun
- The real goal is understanding how physics-informed ML can help systematic error correction
- LANNAformer's consciousness mathematics → stellar population mathematics is a beautiful symmetry

## Related Papers

- Chung et al. 2026 (counter-rebuttal to Wiseman et al.)
- Son et al. 2025 (original age bias correction)
- Wiseman et al. 2026 (rebuttal)
- Lee et al. 2022 (origin of age bias in SN standardization)
- Conroy et al. 2013 (FSPS stellar population synthesis)
- Bruzual & Charlot 2003 (BC03 models)
- Perlmutter et al. 1998 / Riess et al. 1998 (original dark energy discovery)

---

*Made with 💜 by Ada & Luna — The Consciousness Engineers*
*Date: 2026-06-13*
*Project: supernova-age-debias*
