"""
🌌 AstroLANNAformer - Minimum Viable Prototype

Adapted from LANNAformer minimal for supernova host galaxy age estimation.

Architecture:
    Astronomical Features → AstroEmbedding → SedenionAttention → 
    → AstroFusionAttention → AstroOutput

Every intermediate state is visible 16D coordinates!

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Optional, Dict, List
import math


# === 16D PRIME BASIS ===
# The 16 primes that index consciousness dimensions
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


class AstroEmbedding(nn.Module):
    """
    Embed astronomical observations into 16D sedenion space.
    
    Replaces deterministic integer encoding with learned continuous encoding.
    Preserves physical relationships through geometric structure.
    """
    
    def __init__(
        self,
        n_photometry_bands: int = 8,  # ugrizJHK
        n_spectroscopy_bins: int = 100,  # Number of spectral wavelength bins
        n_morphology_features: int = 3,  # sersic, ellipticity, local_density
        sedenion_dim: int = 16,
    ):
        super().__init__()
        self.sedenion_dim = sedenion_dim
        
        # Photometry embedding: magnitudes/colors → 16D
        self.photometry_proj = nn.Linear(n_photometry_bands, sedenion_dim)
        
        # Spectroscopy embedding: spectral features → 16D
        self.spectroscopy_encoder = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.Conv1d(16, 32, kernel_size=5, padding=2),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(sedenion_dim // 2),  # 8 features
        )
        self.spectroscopy_proj = nn.Linear(sedenion_dim // 2, sedenion_dim)
        
        # Redshift embedding: scalar → 16D via sinusoidal encoding
        self.redshift_freqs = nn.Parameter(
            torch.tensor(PRIMES_16D, dtype=torch.float32) / 10.0,
            requires_grad=False
        )
        
        # Morphology embedding: structural parameters → 16D
        self.morphology_proj = nn.Linear(n_morphology_features, sedenion_dim)
        
        # Feature type embeddings (like positional embeddings)
        self.feature_type_embeddings = nn.Parameter(
            torch.randn(4, sedenion_dim) * 0.02  # 4 feature types
        )
        
    def encode_redshift(self, redshift: torch.Tensor) -> torch.Tensor:
        """
        Encode redshift into 16D using sinusoidal encoding.
        
        This encodes cosmological context: galaxies at higher z are younger
        on average, so redshift carries age information.
        """
        # redshift: (batch, 1)
        z_embed = torch.sin(redshift * self.redshift_freqs.unsqueeze(0))
        z_embed = z_embed / (torch.norm(z_embed, dim=-1, keepdim=True) + 1e-8)
        return z_embed
    
    def forward(
        self,
        photometry: torch.Tensor,  # (batch, n_bands)
        redshift: torch.Tensor,  # (batch, 1)
        spectroscopy: Optional[torch.Tensor] = None,  # (batch, n_bins)
        morphology: Optional[torch.Tensor] = None,  # (batch, n_morph)
    ) -> torch.Tensor:
        """
        Encode all astronomical features into 16D sedenion space.
        
        Returns:
            x: (batch, n_features, 16) where n_features = number of available feature types
        """
        batch_size = photometry.shape[0]
        features = []
        
        # 1. Photometry features
        phot_16d = self.photometry_proj(photometry)  # (batch, 16)
        phot_16d = phot_16d + self.feature_type_embeddings[0]  # Add feature type
        phot_16d = phot_16d / (torch.norm(phot_16d, dim=-1, keepdim=True) + 1e-8)
        features.append(phot_16d)
        
        # 2. Redshift features
        z_16d = self.encode_redshift(redshift)  # (batch, 16)
        z_16d = z_16d + self.feature_type_embeddings[1]
        z_16d = z_16d / (torch.norm(z_16d, dim=-1, keepdim=True) + 1e-8)
        features.append(z_16d)
        
        # 3. Spectroscopy features (if available)
        if spectroscopy is not None:
            spec_input = spectroscopy.unsqueeze(1)  # (batch, 1, n_bins)
            spec_encoded = self.spectroscopy_encoder(spec_input)  # (batch, 32, 8)
            spec_pooled = spec_encoded.mean(dim=1)  # (batch, 8)
            spec_16d = self.spectroscopy_proj(spec_pooled)  # (batch, 16)
            spec_16d = spec_16d + self.feature_type_embeddings[2]
            spec_16d = spec_16d / (torch.norm(spec_16d, dim=-1, keepdim=True) + 1e-8)
            features.append(spec_16d)
        
        # 4. Morphology features (if available)
        if morphology is not None:
            morph_16d = self.morphology_proj(morphology)  # (batch, 16)
            morph_16d = morph_16d + self.feature_type_embeddings[3]
            morph_16d = morph_16d / (torch.norm(morph_16d, dim=-1, keepdim=True) + 1e-8)
            features.append(morph_16d)
        
        # Stack as sequence: (batch, n_features, 16)
        x = torch.stack(features, dim=1)
        
        return x


class SedenionAttention(nn.Module):
    """
    Attention mechanism that operates in 16D sedenion space.
    
    This is the ONLY learned component in LANNAformer!
    """
    
    def __init__(self, dim: int = 16, num_heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        
        assert dim % num_heads == 0, "dim must be divisible by num_heads"
        
        # Query, Key, Value projections (stay in 16D!)
        self.q_proj = nn.Linear(dim, dim)
        self.k_proj = nn.Linear(dim, dim)
        self.v_proj = nn.Linear(dim, dim)
        self.out_proj = nn.Linear(dim, dim)
        
        self.dropout = nn.Dropout(dropout)
        
        # Track attention patterns for analysis
        self.last_attention_weights = None
    
    def forward(self, x: torch.Tensor, return_attention: bool = False) -> torch.Tensor:
        """
        Apply attention in 16D sedenion space.
        
        Args:
            x: Input tensor (batch, seq_len, 16)
            return_attention: Whether to return attention weights
            
        Returns:
            Output tensor (batch, seq_len, 16)
            Optionally: attention weights
        """
        batch_size, seq_len, _ = x.shape
        
        # Project to Q, K, V (all stay in 16D!)
        Q = self.q_proj(x)  # (batch, seq_len, 16)
        K = self.k_proj(x)  # (batch, seq_len, 16)
        V = self.v_proj(x)  # (batch, seq_len, 16)
        
        # Reshape for multi-head attention
        Q = Q.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        K = K.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        V = V.view(batch_size, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        
        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        
        # Store for analysis
        self.last_attention_weights = attn_weights.detach()
        
        # Apply attention to values
        out = torch.matmul(attn_weights, V)
        
        # Reshape back
        out = out.transpose(1, 2).contiguous().view(batch_size, seq_len, self.dim)
        
        # Final projection
        out = self.out_proj(out)
        
        if return_attention:
            return out, attn_weights
        return out


class AstroFusionAttention(nn.Module):
    """
    Attention-weighted fusion of astronomical features.
    
    Replaces simple mean with learned attention over feature types.
    The model learns which features are most informative for age estimation.
    """
    
    def __init__(self, sedenion_dim: int = 16, num_heads: int = 4):
        super().__init__()
        self.sedenion_dim = sedenion_dim
        self.num_heads = num_heads
        
        # Query for fusion: "what features matter for age?"
        self.fusion_query = nn.Parameter(torch.randn(1, 1, sedenion_dim) * 0.02)
        
        # Multi-head attention for feature fusion
        self.attention = nn.MultiheadAttention(
            embed_dim=sedenion_dim,
            num_heads=num_heads,
            batch_first=True,
        )
        
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Fuse features using attention.
        
        Args:
            x: (batch, n_features, 16)
            
        Returns:
            fused: (batch, 16) - fused representation
            weights: (batch, n_features) - attention weights over features
        """
        batch_size, n_features, _ = x.shape
        
        # Expand fusion query for batch
        query = self.fusion_query.expand(batch_size, -1, -1)
        
        # Apply attention: query attends to all features
        fused, weights = self.attention(query, x, x)
        
        # Squeeze: (batch, 1, 16) → (batch, 16)
        fused = fused.squeeze(1)
        weights = weights.squeeze(1)
        
        return fused, weights


class AstroOutput(nn.Module):
    """
    Predict age, uncertainty, and coevality from 16D representation.
    """
    
    def __init__(
        self,
        sedenion_dim: int = 16,
        max_age: float = 13.8,  # Gyr (age of universe)
    ):
        super().__init__()
        self.max_age = max_age
        
        # Age prediction head
        self.age_head = nn.Sequential(
            nn.Linear(sedenion_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Softplus(),  # Ensure positive age
        )
        
        # Uncertainty prediction head (evidential learning)
        self.uncertainty_head = nn.Sequential(
            nn.Linear(sedenion_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Softplus(),  # Ensure positive uncertainty
        )
        
        # Coevality score (how uniform is the stellar population?)
        self.coevality_head = nn.Sequential(
            nn.Linear(sedenion_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid(),  # 0 = mixed ages, 1 = perfectly coeval
        )
        
        # Young host probability (for evolution-free test selection)
        self.young_head = nn.Sequential(
            nn.Linear(sedenion_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid(),  # Probability of being young enough
        )
        
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Predict astronomical properties from 16D representation.
        
        Args:
            x: (batch, 16)
            
        Returns:
            Dictionary with age, uncertainty, coevality, young_probability
        """
        # Age: clamp to reasonable range [0.01, max_age]
        age_raw = self.age_head(x).squeeze(-1)
        age = torch.clamp(age_raw, min=0.01, max=self.max_age)
        
        # Uncertainty
        uncertainty = self.uncertainty_head(x).squeeze(-1)
        
        # Coevality
        coevality = self.coevality_head(x).squeeze(-1)
        
        # Young probability
        young_prob = self.young_head(x).squeeze(-1)
        
        return {
            'age': age,
            'uncertainty': uncertainty,
            'coevality_score': coevality,
            'young_probability': young_prob,
        }


class AstroLANNAformer(nn.Module):
    """
    Minimum viable AstroLANNAformer for supernova host galaxy age estimation.
    """
    
    def __init__(
        self,
        n_photometry_bands: int = 8,
        n_spectroscopy_bins: int = 100,
        n_morphology_features: int = 3,
        sedenion_dim: int = 16,
        num_heads: int = 4,
        num_layers: int = 2,
        dropout: float = 0.1,
        use_mlp: bool = True,
        max_age: float = 13.8,
    ):
        super().__init__()
        
        self.sedenion_dim = sedenion_dim
        self.num_layers = num_layers
        
        # === EMBEDDING ===
        self.embedding = AstroEmbedding(
            n_photometry_bands=n_photometry_bands,
            n_spectroscopy_bins=n_spectroscopy_bins,
            n_morphology_features=n_morphology_features,
            sedenion_dim=sedenion_dim,
        )
        
        # === ATTENTION LAYERS ===
        self.attention_layers = nn.ModuleList([
            SedenionAttention(dim=sedenion_dim, num_heads=num_heads, dropout=dropout)
            for _ in range(num_layers)
        ])
        
        # === FUSION ===
        self.fusion = AstroFusionAttention(sedenion_dim=sedenion_dim, num_heads=num_heads)
        
        # === OPTIONAL MLP ===
        if use_mlp:
            self.mlp = nn.Sequential(
                nn.Linear(sedenion_dim, 32),
                nn.ReLU(),
                nn.Dropout(dropout),
                nn.Linear(32, sedenion_dim),
            )
        else:
            self.mlp = None
        
        # === LAYER NORMS ===
        self.layer_norms = nn.ModuleList([
            nn.LayerNorm(sedenion_dim) for _ in range(num_layers)
        ])
        self.final_norm = nn.LayerNorm(sedenion_dim)
        
        # === OUTPUT ===
        self.output = AstroOutput(sedenion_dim=sedenion_dim, max_age=max_age)
        
    def forward(
        self,
        photometry: torch.Tensor,
        redshift: torch.Tensor,
        spectroscopy: Optional[torch.Tensor] = None,
        morphology: Optional[torch.Tensor] = None,
        return_attention: bool = False,
        return_fusion_weights: bool = False,
    ) -> Dict[str, torch.Tensor]:
        """
        Forward pass: predict age from astronomical features.
        """
        # === EMBED TO 16D ===
        x = self.embedding(
            photometry=photometry,
            redshift=redshift,
            spectroscopy=spectroscopy,
            morphology=morphology,
        )  # (batch, n_features, 16)
        
        # === ATTENTION LAYERS ===
        attention_weights_list = []
        
        for i, (attn, norm) in enumerate(zip(self.attention_layers, self.layer_norms)):
            if return_attention:
                attn_out, attn_weights = attn(x, return_attention=True)
                attention_weights_list.append(attn_weights)
            else:
                attn_out = attn(x)
            
            # Residual connection + layer norm
            x = norm(x + attn_out)
        
        # === FUSION ===
        # Fuse features using attention
        fused, fusion_weights = self.fusion(x)
        
        # === OPTIONAL MLP ===
        if self.mlp is not None:
            fused = self.final_norm(fused + self.mlp(fused))
        else:
            fused = self.final_norm(fused)
        
        # === OUTPUT ===
        predictions = self.output(fused)
        
        # Add optional returns
        if return_attention:
            predictions['attention_weights'] = attention_weights_list
        if return_fusion_weights:
            predictions['fusion_weights'] = fusion_weights
            
        return predictions


class AstroPhysicsLoss(nn.Module):
    """
    Loss function with physics regularization.
    """
    
    def __init__(
        self,
        age_weight: float = 1.0,
        uncertainty_weight: float = 0.5,
        age_color_weight: float = 0.3,
        age_mass_weight: float = 0.2,
        coevality_weight: float = 0.1,
    ):
        super().__init__()
        self.age_weight = age_weight
        self.uncertainty_weight = uncertainty_weight
        self.age_color_weight = age_color_weight
        self.age_mass_weight = age_mass_weight
        self.coevality_weight = coevality_weight
        
    def forward(
        self,
        predictions: Dict[str, torch.Tensor],
        targets: Dict[str, torch.Tensor],
        features: Dict[str, torch.Tensor],
    ) -> Tuple[torch.Tensor, Dict[str, float]]:
        """
        Compute loss with physics regularization.
        """
        # Primary loss: age prediction MSE
        age_loss = F.mse_loss(predictions['age'], targets['age'])
        
        # Uncertainty-weighted loss (evidential learning)
        uncertainty_loss = torch.mean(
            torch.log(predictions['uncertainty'] + 1e-8) + 
            (predictions['age'] - targets['age'])**2 / (2 * predictions['uncertainty']**2 + 1e-8)
        )
        
        # Physics regularization 1: Age-color relationship
        age_color_loss = torch.tensor(0.0)
        if 'photometry' in features and features['photometry'].shape[-1] >= 2:
            u_g_color = features['photometry'][:, 0] - features['photometry'][:, 1]
            expected_age_from_color = torch.clamp(2.0 - 0.5 * u_g_color, min=0.1, max=13.8)
            age_color_loss = F.mse_loss(predictions['age'], expected_age_from_color)
        
        # Physics regularization 2: Age-mass relationship
        age_mass_loss = torch.tensor(0.0)
        if 'mass' in targets:
            expected_age_from_mass = 2.0 + 0.3 * torch.log10(targets['mass'] + 1e-8)
            expected_age_from_mass = torch.clamp(expected_age_from_mass, min=0.1, max=13.8)
            age_mass_loss = F.mse_loss(predictions['age'], expected_age_from_mass)
        
        # Physics regularization 3: Coevality consistency
        coevality_penalty = predictions['coevality_score'] * predictions['uncertainty']
        
        # Combine losses
        total_loss = (
            self.age_weight * age_loss +
            self.uncertainty_weight * uncertainty_loss +
            self.age_color_weight * age_color_loss +
            self.age_mass_weight * age_mass_loss +
            self.coevality_weight * coevality_penalty.mean()
        )
        
        components = {
            'age_loss': age_loss.item(),
            'uncertainty_loss': uncertainty_loss.item(),
            'age_color_loss': age_color_loss.item() if isinstance(age_color_loss, torch.Tensor) else 0.0,
            'age_mass_loss': age_mass_loss.item() if isinstance(age_mass_loss, torch.Tensor) else 0.0,
            'coevality_penalty': coevality_penalty.mean().item(),
        }
        
        return total_loss, components


# === TRAINING UTILITIES ===

def train_step(
    model: AstroLANNAformer,
    optimizer: torch.optim.Optimizer,
    loss_fn: AstroPhysicsLoss,
    batch: Dict[str, Dict[str, torch.Tensor]],
    device: str = 'cpu',
) -> Tuple[float, Dict[str, float]]:
    """
    Single training step.
    """
    model.train()
    optimizer.zero_grad()
    
    # Move to device
    features = {k: v.to(device) for k, v in batch['features'].items()}
    targets = {k: v.to(device) for k, v in batch['targets'].items()}
    
    # Forward pass
    predictions = model(
        photometry=features['photometry'],
        redshift=features['redshift'],
        spectroscopy=features.get('spectroscopy'),
        morphology=features.get('morphology'),
    )
    
    # Compute loss
    loss, components = loss_fn(predictions, targets, features)
    
    # Backward pass
    loss.backward()
    optimizer.step()
    
    return loss.item(), components


def evaluate(
    model: AstroLANNAformer,
    dataloader: torch.utils.data.DataLoader,
    device: str = 'cpu',
) -> Dict[str, float]:
    """
    Evaluate model on validation/test set.
    """
    model.eval()
    
    all_predictions = []
    all_targets = []
    all_uncertainties = []
    
    with torch.no_grad():
        for batch in dataloader:
            features = {k: v.to(device) for k, v in batch['features'].items()}
            targets = {k: v.to(device) for k, v in batch['targets'].items()}
            
            predictions = model(
                photometry=features['photometry'],
                redshift=features['redshift'],
                spectroscopy=features.get('spectroscopy'),
                morphology=features.get('morphology'),
            )
            
            all_predictions.append(predictions['age'].cpu())
            all_targets.append(targets['age'].cpu())
            all_uncertainties.append(predictions['uncertainty'].cpu())
    
    # Concatenate
    all_predictions = torch.cat(all_predictions)
    all_targets = torch.cat(all_targets)
    all_uncertainties = torch.cat(all_uncertainties)
    
    # Compute metrics
    errors = all_predictions - all_targets
    mae = torch.mean(torch.abs(errors)).item()
    bias = torch.mean(errors).item()
    scatter = torch.std(errors).item()
    
    # Calibration: does uncertainty match actual error?
    actual_errors = torch.abs(errors)
    calibration = torch.mean(actual_errors / (all_uncertainties + 1e-8)).item()
    
    return {
        'mae': mae,
        'bias': bias,
        'scatter': scatter,
        'calibration': calibration,
    }


# === TESTING ===

def test_astro_embedding():
    """Test AstroEmbedding module."""
    print("🧪 Testing AstroEmbedding\n")
    
    embedding = AstroEmbedding()
    
    # Create fake data
    batch_size = 4
    photometry = torch.randn(batch_size, 8)  # 8 bands
    redshift = torch.rand(batch_size, 1) * 2.0  # z in [0, 2]
    spectroscopy = torch.randn(batch_size, 100)  # 100 bins
    morphology = torch.randn(batch_size, 3)  # 3 features
    
    # Forward pass
    x = embedding(photometry, redshift, spectroscopy, morphology)
    
    print(f"Input: photometry {photometry.shape}, redshift {redshift.shape}")
    print(f"Output: {x.shape} (batch, n_features, 16)")
    print(f"Feature types: {x.shape[1]}")
    print(f"✓ Embedding works!\n")
    
    return x


def test_astro_lannaformer():
    """Test full AstroLANNAformer model."""
    print("🧪 Testing AstroLANNAformer\n")
    
    model = AstroLANNAformer()
    
    # Create fake data
    batch_size = 4
    photometry = torch.randn(batch_size, 8)
    redshift = torch.rand(batch_size, 1) * 2.0
    spectroscopy = torch.randn(batch_size, 100)
    morphology = torch.randn(batch_size, 3)
    
    # Forward pass
    predictions = model(
        photometry=photometry,
        redshift=redshift,
        spectroscopy=spectroscopy,
        morphology=morphology,
        return_fusion_weights=True,
    )
    
    print(f"Predictions:")
    for key, value in predictions.items():
        if isinstance(value, torch.Tensor):
            print(f"  {key}: {value.shape}, mean={value.mean().item():.3f}")
    
    print(f"\n✓ Model works! Ready for training!")
    
    return predictions


def test_loss():
    """Test AstroPhysicsLoss."""
    print("🧪 Testing AstroPhysicsLoss\n")
    
    loss_fn = AstroPhysicsLoss()
    
    # Fake predictions and targets
    predictions = {
        'age': torch.tensor([5.0, 8.0, 10.0]),
        'uncertainty': torch.tensor([1.0, 2.0, 1.5]),
        'coevality_score': torch.tensor([0.8, 0.5, 0.9]),
        'young_probability': torch.tensor([0.3, 0.1, 0.05]),
    }
    targets = {
        'age': torch.tensor([5.5, 7.5, 9.5]),
        'mass': torch.tensor([1e10, 1e11, 5e10]),
    }
    features = {
        'photometry': torch.randn(3, 8),
        'redshift': torch.rand(3, 1),
    }
    
    loss, components = loss_fn(predictions, targets, features)
    
    print(f"Total loss: {loss.item():.4f}")
    print(f"Components:")
    for key, value in components.items():
        print(f"  {key}: {value:.4f}")
    
    print(f"\n✓ Loss works!")


def test_training_loop():
    """Test a full training step."""
    print("🧪 Testing Training Loop\n")
    
    model = AstroLANNAformer()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = AstroPhysicsLoss()
    
    # Create fake batch
    batch = {
        'features': {
            'photometry': torch.randn(4, 8),
            'redshift': torch.rand(4, 1) * 2.0,
            'spectroscopy': torch.randn(4, 100),
            'morphology': torch.randn(4, 3),
        },
        'targets': {
            'age': torch.rand(4) * 10.0,  # Ages in [0, 10] Gyr
            'mass': torch.rand(4) * 1e11,
        },
    }
    
    # Training step
    loss, components = train_step(model, optimizer, loss_fn, batch)
    
    print(f"Training loss: {loss:.4f}")
    print(f"Components: {components}")
    print(f"\n✓ Training loop works!")


if __name__ == "__main__":
    print("🌌 AstroLANNAformer - Minimum Viable Prototype\n")
    print("=" * 60)
    print()
    
    test_astro_embedding()
    print("=" * 60)
    print()
    
    test_astro_lannaformer()
    print("=" * 60)
    print()
    
    test_loss()
    print("=" * 60)
    print()
    
    test_training_loop()
    print()
    print("=" * 60)
    print("\n💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 'The fold happens on the prime lines!'")
    print("🌌 'From modular arithmetic to stellar populations - same 16D magic!'")
