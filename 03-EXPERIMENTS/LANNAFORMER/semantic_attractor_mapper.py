"""
Semantic Attractor Mapper for 16D Consciousness Space!

Maps text to 16D coordinates using SEMANTIC ATTRACTORS instead of hashing.
Each dimension has MEANING (from bagel physics), and we detect which
semantic features are present to weight each dimension appropriately.

This is how transformers ACTUALLY work - they learn which dimensions
represent which semantic features! We're doing it explicitly using
consciousness physics! 🍩✨

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import numpy as np
import re
from typing import Dict, List, Tuple
from collections import Counter

# 16D Consciousness Dimensions (from Bagel Physics!)
CONSCIOUSNESS_DIMENSIONS = {
    # VALIDATED DIMENSIONS (9/16)
    3: {
        'name': 'COHERENCE',
        'description': '1s orbital consciousness - logical structure, sequences',
        'keywords': ['order', 'sequence', 'logic', 'structure', 'system', 'pattern', 'first', 'second', 'third']
    },
    5: {
        'name': 'IDENTITY',
        'description': '2s shell bridging - self, names, labels',
        'keywords': ['name', 'identity', 'self', 'called', 'known', 'is', 'are', 'being']
    },
    19: {
        'name': 'HARMONY',
        'description': '2p orbital geometry - balance, cycles, seasons',
        'keywords': ['cycle', 'season', 'balance', 'harmony', 'rhythm', 'pattern', 'repeat']
    },
    23: {
        'name': 'WISDOM',
        'description': '3s consciousness expansion - knowledge, understanding',
        'keywords': ['know', 'understand', 'learn', 'wisdom', 'knowledge', 'study', 'science']
    },
    29: {
        'name': 'INFINITY',
        'description': '4s consciousness scaling - vastness, universe, cosmos',
        'keywords': ['universe', 'infinite', 'vast', 'cosmos', 'space', 'all', 'everything']
    },
    41: {
        'name': 'LOVE',
        'description': '41.176 Hz Klein frequency - emotion, connection, care',
        'keywords': ['love', 'care', 'emotion', 'feel', 'heart', 'connection', 'relationship']
    },
    43: {
        'name': 'NON_ORIENTABLE',
        'description': 'Inside/outside collapse - paradox, duality, both',
        'keywords': ['paradox', 'both', 'neither', 'inside', 'outside', 'dual', 'opposite']
    },
    47: {
        'name': 'TIME',
        'description': 'Temporal holonomy - time, when, duration',
        'keywords': ['time', 'when', 'year', 'month', 'day', 'hour', 'ago', 'future', 'past', 'now', 
                     'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
                     'september', 'october', 'november', 'december',
                     'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    },
    53: {
        'name': 'SPACE',
        'description': 'Spatial coherence - location, where, place',
        'keywords': ['where', 'place', 'location', 'country', 'city', 'here', 'there', 'near', 'far',
                     'north', 'south', 'east', 'west', 'continent', 'ocean', 'land']
    },
    
    # MYSTERY DIMENSIONS (7/16) - Active in calculations
    7: {
        'name': 'DUALITY',
        'description': 'Choice orientations - options, alternatives',
        'keywords': ['choice', 'option', 'or', 'either', 'alternative', 'different']
    },
    11: {
        'name': 'STRUCTURE',
        'description': 'Complex geometry - shape, form, structure',
        'keywords': ['shape', 'form', 'structure', 'geometry', 'build', 'construct', 'architecture']
    },
    13: {
        'name': 'CHANGE',
        'description': 'Dynamic evolution - change, transform, evolve',
        'keywords': ['change', 'transform', 'evolve', 'become', 'grow', 'develop', 'shift']
    },
    17: {
        'name': 'LIFE',
        'description': 'Biological resonance - life, living, organism',
        'keywords': ['life', 'living', 'alive', 'organism', 'biological', 'animal', 'plant', 'cell']
    },
    31: {
        'name': 'CREATION',
        'description': 'Active generation - create, make, generate',
        'keywords': ['create', 'make', 'generate', 'produce', 'build', 'form', 'new']
    },
    37: {
        'name': 'TRUTH',
        'description': 'Deep reality - truth, fact, real',
        'keywords': ['truth', 'fact', 'real', 'actual', 'true', 'reality', 'exist']
    },
    59: {
        'name': 'CONSCIOUSNESS',
        'description': 'Meta-awareness - aware, conscious, mind',
        'keywords': ['aware', 'conscious', 'mind', 'think', 'thought', 'consciousness', 'awareness']
    }
}

# Prime order for 16D space
PRIMES_16D = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59][:16]

class SemanticAttractorMapper:
    """
    Maps text to 16D consciousness space using semantic attractors.
    
    Each dimension represents a specific semantic feature (TIME, SPACE, LOVE, etc.)
    and we detect which features are present in the text to weight dimensions.
    """
    
    def __init__(self):
        self.dimensions = CONSCIOUSNESS_DIMENSIONS
        self.primes = PRIMES_16D
        
        # Build keyword index for fast lookup
        self.keyword_to_dims = {}
        for prime, dim_info in self.dimensions.items():
            for keyword in dim_info['keywords']:
                if keyword not in self.keyword_to_dims:
                    self.keyword_to_dims[keyword] = []
                self.keyword_to_dims[keyword].append(prime)
    
    def detect_semantic_features(self, text: str) -> Dict[int, float]:
        """
        Detect which semantic features are present in text.
        
        Returns dict of {prime: strength} for active dimensions.
        """
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)
        
        # Count keyword matches per dimension
        dim_counts = Counter()
        for word in words:
            if word in self.keyword_to_dims:
                for prime in self.keyword_to_dims[word]:
                    dim_counts[prime] += 1
        
        # Normalize by text length
        total_words = len(words) if words else 1
        dim_strengths = {
            prime: count / total_words
            for prime, count in dim_counts.items()
        }
        
        return dim_strengths
    
    def text_to_attractor_coords(self, text: str, base_strength: float = 1.0) -> np.ndarray:
        """
        Map text to 16D coordinates using semantic attractors.
        
        Each dimension is weighted by how strongly that semantic feature
        appears in the text. This creates natural clustering of related concepts!
        """
        # Detect semantic features
        dim_strengths = self.detect_semantic_features(text)
        
        # Build 16D coordinates
        coords = np.zeros(16)
        
        for i, prime in enumerate(self.primes):
            if prime in dim_strengths:
                # Strong attractor - use detected strength
                strength = dim_strengths[prime]
                coords[i] = strength * np.sqrt(prime) * base_strength
            else:
                # Weak/no attractor - small random noise
                coords[i] = np.random.normal(0, 0.01) * np.sqrt(prime)
        
        # Normalize to unit sphere
        norm = np.linalg.norm(coords)
        if norm > 0:
            coords = coords / norm
        
        return coords
    
    def analyze_text_attractors(self, text: str) -> Dict:
        """
        Analyze which semantic attractors are active in text.
        
        Returns detailed breakdown of dimension activations.
        """
        dim_strengths = self.detect_semantic_features(text)
        
        # Sort by strength
        sorted_dims = sorted(dim_strengths.items(), key=lambda x: x[1], reverse=True)
        
        analysis = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'total_words': len(re.findall(r'\b\w+\b', text.lower())),
            'active_dimensions': []
        }
        
        for prime, strength in sorted_dims:
            if prime in self.dimensions:
                dim_info = self.dimensions[prime]
                analysis['active_dimensions'].append({
                    'prime': prime,
                    'name': dim_info['name'],
                    'strength': strength,
                    'description': dim_info['description']
                })
        
        return analysis

def test_semantic_attractors():
    """Test semantic attractor mapping on example texts"""
    print()
    print("🌌" * 30)
    print()
    print("   SEMANTIC ATTRACTOR MAPPING TEST")
    print("   Learning Consciousness-Native Embeddings")
    print()
    print("🌌" * 30)
    print()
    
    mapper = SemanticAttractorMapper()
    
    # Test texts with different semantic features
    test_texts = [
        ("April is the fourth month of the year.", "Temporal concept"),
        ("Australia is a country in Oceania.", "Spatial concept"),
        ("Love is a deep emotional connection.", "Emotional concept"),
        ("The atom is the basic unit of matter.", "Structural concept"),
        ("Monday is the first day of the week.", "Temporal + Sequential"),
        ("The universe is infinite and vast.", "Cosmic concept"),
        ("Knowledge and wisdom come from learning.", "Cognitive concept"),
    ]
    
    print("🔍 Analyzing Semantic Attractors:\n")
    
    for text, label in test_texts:
        print(f"{'='*60}")
        print(f"Text: {text}")
        print(f"Label: {label}")
        print()
        
        # Analyze attractors
        analysis = mapper.analyze_text_attractors(text)
        
        print(f"Active Dimensions:")
        for dim in analysis['active_dimensions'][:5]:  # Top 5
            print(f"  {dim['name']:20s} (Prime {dim['prime']:2d}): {dim['strength']:.3f} - {dim['description']}")
        
        # Get coordinates
        coords = mapper.text_to_attractor_coords(text)
        print(f"\n16D Coordinates (first 4): {coords[:4]}")
        print()
    
    print()
    print("🌟 Testing Semantic Clustering:\n")
    
    # Test if related concepts cluster
    temporal_texts = [
        "January is the first month",
        "February comes after January",
        "Monday is a day of the week",
        "Tuesday follows Monday"
    ]
    
    spatial_texts = [
        "Australia is a country",
        "Canada is in North America",
        "Paris is a city in France",
        "Tokyo is the capital of Japan"
    ]
    
    print("Temporal Concepts:")
    temporal_coords = []
    for text in temporal_texts:
        coords = mapper.text_to_attractor_coords(text)
        temporal_coords.append(coords)
        print(f"  {text:40s} TIME dim: {coords[PRIMES_16D.index(47)]:.3f}")
    
    print("\nSpatial Concepts:")
    spatial_coords = []
    for text in spatial_texts:
        coords = mapper.text_to_attractor_coords(text)
        spatial_coords.append(coords)
        print(f"  {text:40s} SPACE dim: {coords[PRIMES_16D.index(53)]:.3f}")
    
    # Calculate within-group vs between-group similarities
    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    temporal_sims = []
    for i in range(len(temporal_coords)):
        for j in range(i+1, len(temporal_coords)):
            temporal_sims.append(cosine_sim(temporal_coords[i], temporal_coords[j]))
    
    spatial_sims = []
    for i in range(len(spatial_coords)):
        for j in range(i+1, len(spatial_coords)):
            spatial_sims.append(cosine_sim(spatial_coords[i], spatial_coords[j]))
    
    cross_sims = []
    for t_coord in temporal_coords:
        for s_coord in spatial_coords:
            cross_sims.append(cosine_sim(t_coord, s_coord))
    
    print(f"\n📊 Clustering Analysis:")
    print(f"  Temporal-Temporal similarity: {np.mean(temporal_sims):.3f} ± {np.std(temporal_sims):.3f}")
    print(f"  Spatial-Spatial similarity:   {np.mean(spatial_sims):.3f} ± {np.std(spatial_sims):.3f}")
    print(f"  Temporal-Spatial similarity:  {np.mean(cross_sims):.3f} ± {np.std(cross_sims):.3f}")
    print()
    
    if np.mean(temporal_sims) > np.mean(cross_sims) and np.mean(spatial_sims) > np.mean(cross_sims):
        print("✅ SUCCESS! Related concepts cluster together!")
        print("   Semantic attractors create natural groupings!")
    else:
        print("❌ Clustering not strong enough yet.")
        print("   Need to tune attractor strengths.")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🍩 Mapping semantics to consciousness space!")

if __name__ == "__main__":
    test_semantic_attractors()
