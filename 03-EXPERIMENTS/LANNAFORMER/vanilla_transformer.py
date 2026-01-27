#!/usr/bin/env python3
"""
Vanilla Transformer for Mod Addition

Standard transformer architecture (no sedenion magic!)
to compare against LANNAformer.

This will tell us if the plateau is from our geometry
or something more fundamental!

Date: January 26, 2026
Researchers: Ada & Luna - The Consciousness Engineers
"""

import torch
import torch.nn as nn
import math


class VanillaTransformer(nn.Module):
    """
    Standard transformer for modular addition
    
    No sedenion awareness, no geometric constraints.
    Just vanilla multi-head attention + MLPs!
    """
    
    def __init__(self, modulus: int, num_heads: int, num_layers: int, 
                 d_model: int = 128, dropout: float = 0.1, init_scale: float = 1.0):
        super().__init__()
        self.modulus = modulus
        self.d_model = d_model
        self.init_scale = init_scale
        
        # Embeddings
        self.embed_a = nn.Embedding(modulus, d_model)
        self.embed_b = nn.Embedding(modulus, d_model)
        
        # Positional encoding (simple learned)
        self.pos_embed = nn.Parameter(torch.randn(2, d_model))
        
        # Transformer layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=num_heads,
            dim_feedforward=d_model * 4,  # Standard 4x expansion
            dropout=dropout,
            activation='gelu',
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output head
        self.output = nn.Linear(d_model, modulus)
        
        self._init_weights(init_scale)
    
    def _init_weights(self, init_scale=1.0):
        """Initialize weights like standard transformers
        
        Args:
            init_scale: Multiply initialization by this factor (for grokking experiments)
        """
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
                if init_scale != 1.0:
                    p.data *= init_scale
    
    def forward(self, a, b):
        """
        Args:
            a: (batch,) integers in [0, modulus)
            b: (batch,) integers in [0, modulus)
        
        Returns:
            logits: (batch, modulus)
        """
        batch_size = a.shape[0]
        
        # Embed inputs
        a_embed = self.embed_a(a)  # (batch, d_model)
        b_embed = self.embed_b(b)  # (batch, d_model)
        
        # Add positional encoding
        a_embed = a_embed + self.pos_embed[0]
        b_embed = b_embed + self.pos_embed[1]
        
        # Stack into sequence
        x = torch.stack([a_embed, b_embed], dim=1)  # (batch, 2, d_model)
        
        # Transform
        x = self.transformer(x)  # (batch, 2, d_model)
        
        # Pool (take mean of both positions)
        x = x.mean(dim=1)  # (batch, d_model)
        
        # Output
        logits = self.output(x)  # (batch, modulus)
        
        return logits
