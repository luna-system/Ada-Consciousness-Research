"""
Tests for AstroLANNAformer package.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pytest
import torch
import numpy as np
import os

# Set SPS_HOME if available
sps_home = os.environ.get('SPS_HOME', '/home/luna/Code/arf/Ada-Consciousness-Research/03-EXPERIMENTS/supernova-age-debias/fsps')
if os.path.exists(sps_home):
    os.environ['SPS_HOME'] = sps_home

from astro_lannaformer import (
    AstroLANNAformer,
    AstroEmbedding,
    AstroPhysicsLoss,
    SyntheticGalaxyGenerator,
    SyntheticGalaxyDataset,
    create_dataloaders,
)


class TestAstroEmbedding:
    """Test AstroEmbedding module."""
    
    def test_embedding_shape(self):
        """Test output shape is correct."""
        embedding = AstroEmbedding()
        photometry = torch.randn(4, 8)
        redshift = torch.rand(4, 1)
        spectroscopy = torch.randn(4, 100)
        morphology = torch.randn(4, 3)
        
        x = embedding(photometry, redshift, spectroscopy, morphology)
        
        assert x.shape == (4, 4, 16)  # batch, n_features, sedenion_dim
    
    def test_optional_features(self):
        """Test that optional features can be None."""
        embedding = AstroEmbedding()
        photometry = torch.randn(2, 8)
        redshift = torch.rand(2, 1)
        
        x = embedding(photometry, redshift, None, None)
        
        assert x.shape == (2, 2, 16)  # Only photometry + redshift


class TestAstroLANNAformer:
    """Test AstroLANNAformer model."""
    
    def test_forward_pass(self):
        """Test forward pass produces correct outputs."""
        model = AstroLANNAformer()
        photometry = torch.randn(4, 8)
        redshift = torch.rand(4, 1)
        spectroscopy = torch.randn(4, 100)
        morphology = torch.randn(4, 3)
        
        predictions = model(
            photometry, redshift, spectroscopy, morphology,
            return_fusion_weights=True,
        )
        
        assert 'age' in predictions
        assert 'uncertainty' in predictions
        assert 'coevality_score' in predictions
        assert 'young_probability' in predictions
        assert 'fusion_weights' in predictions
        
        assert predictions['age'].shape == (4,)
        assert predictions['uncertainty'].shape == (4,)
    
    def test_age_range(self):
        """Test predicted ages are in valid range."""
        model = AstroLANNAformer()
        photometry = torch.randn(10, 8)
        redshift = torch.rand(10, 1)
        
        predictions = model(photometry, redshift)
        
        assert torch.all(predictions['age'] >= 0.01)
        assert torch.all(predictions['age'] <= 13.8)
    
    def test_uncertainty_positive(self):
        """Test uncertainties are positive."""
        model = AstroLANNAformer()
        photometry = torch.randn(5, 8)
        redshift = torch.rand(5, 1)
        
        predictions = model(photometry, redshift)
        
        assert torch.all(predictions['uncertainty'] > 0)


class TestAstroPhysicsLoss:
    """Test AstroPhysicsLoss."""
    
    def test_loss_computation(self):
        """Test loss computation works."""
        loss_fn = AstroPhysicsLoss()
        
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
        
        assert isinstance(loss, torch.Tensor)
        assert loss.item() > 0
        assert 'age_loss' in components
        assert 'uncertainty_loss' in components


class TestSyntheticGalaxyGenerator:
    """Test SyntheticGalaxyGenerator."""
    
    def test_catalog_generation(self):
        """Test catalog generation."""
        gen = SyntheticGalaxyGenerator(n_galaxies=10, use_fsps=False)
        catalog = gen.generate_catalog()
        
        assert len(catalog) == 10
        assert 'age' in catalog.columns
        assert 'mass' in catalog.columns
        assert 'mag_u' in catalog.columns
    
    def test_age_range(self):
        """Test generated ages are in valid range."""
        gen = SyntheticGalaxyGenerator(n_galaxies=50, use_fsps=False)
        catalog = gen.generate_catalog()
        
        assert catalog['age'].min() >= 0.1
        assert catalog['age'].max() <= 13.8


class TestSyntheticGalaxyDataset:
    """Test SyntheticGalaxyDataset."""
    
    def test_dataset_length(self):
        """Test dataset length matches catalog."""
        gen = SyntheticGalaxyGenerator(n_galaxies=20, use_fsps=False)
        catalog = gen.generate_catalog()
        dataset = SyntheticGalaxyDataset(catalog)
        
        assert len(dataset) == 20
    
    def test_sample_structure(self):
        """Test sample has correct structure."""
        gen = SyntheticGalaxyGenerator(n_galaxies=5, use_fsps=False)
        catalog = gen.generate_catalog()
        dataset = SyntheticGalaxyDataset(catalog)
        
        sample = dataset[0]
        
        assert 'features' in sample
        assert 'targets' in sample
        assert 'photometry' in sample['features']
        assert 'redshift' in sample['features']
        assert 'age' in sample['targets']


class TestDataLoaders:
    """Test DataLoader creation."""
    
    def test_dataloader_creation(self):
        """Test train/val/test split."""
        gen = SyntheticGalaxyGenerator(n_galaxies=100, use_fsps=False)
        catalog = gen.generate_catalog()
        
        train_loader, val_loader, test_loader = create_dataloaders(
            catalog, batch_size=16
        )
        
        assert len(train_loader.dataset) == 80
        assert len(val_loader.dataset) == 10
        assert len(test_loader.dataset) == 10
    
    def test_batch_structure(self):
        """Test batch has correct structure."""
        gen = SyntheticGalaxyGenerator(n_galaxies=32, use_fsps=False)
        catalog = gen.generate_catalog()
        
        train_loader, _, _ = create_dataloaders(catalog, batch_size=16)
        batch = next(iter(train_loader))
        
        assert 'features' in batch
        assert 'targets' in batch
        assert batch['features']['photometry'].shape == (16, 8)
        assert batch['features']['redshift'].shape == (16, 1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
