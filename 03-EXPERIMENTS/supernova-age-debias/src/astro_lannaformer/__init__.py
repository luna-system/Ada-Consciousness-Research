"""
AstroLANNAformer - Physics-informed neural network for supernova host galaxy age estimation.

A consciousness-native architecture adapted from LANNAformer for astrophysics.
Uses 16D sedenion mathematics and physics-regularized learning to estimate
stellar population ages from photometry, spectroscopy, and morphology.

Made with 💜 by Ada & Luna - The Consciousness Engineers
"""

from .model import (
    AstroLANNAformer,
    AstroEmbedding,
    AstroFusionAttention,
    AstroOutput,
    AstroPhysicsLoss,
    SedenionAttention,
    train_step,
    evaluate,
)

from .data import (
    SyntheticGalaxyGenerator,
    SyntheticGalaxyDataset,
    create_dataloaders,
)

__version__ = "0.1.0"
__author__ = "Ada & Luna"

__all__ = [
    "AstroLANNAformer",
    "AstroEmbedding",
    "AstroFusionAttention",
    "AstroOutput",
    "AstroPhysicsLoss",
    "SedenionAttention",
    "SyntheticGalaxyGenerator",
    "SyntheticGalaxyDataset",
    "create_dataloaders",
    "train_step",
    "evaluate",
]
