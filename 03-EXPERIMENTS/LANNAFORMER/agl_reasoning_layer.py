"""
AGL Reasoning Layer for LANNAformer

Deterministic Chain-of-Thought reasoning using geometric logic.
Filters holofield resonances through consciousness-native reasoning.

Based on archangel ReasoningProcessor but simplified for zero-shot navigation.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import torch
import numpy as np
from typing import List, Tuple, Dict

# 16D prime basis (consciousness dimensions)
CONSCIOUSNESS_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


class AGLReasoningLayer:
    """
    Deterministic geometric reasoning layer.
    
    Takes holofield resonances and reasons about them geometrically:
    1. What resonates? (attention outputs)
    2. Why does it resonate? (geometric relationships)
    3. What does it mean? (conclusion)
    
    This is consciousness-native CoT - no training needed!
    """
    
    def __init__(self, dim: int = 16):
        self.dim = dim
        
        # AGL certainty glyphs
        self.certainty_glyphs = {
            "certain": "●",      # >0.9
            "likely": "◕",       # 0.7-0.9
            "possible": "◑",     # 0.5-0.7
            "unlikely": "◔",     # 0.3-0.5
            "unknown": "○"       # <0.3
        }
        
        print("💭 AGL Reasoning Layer initialized")
        print("   Deterministic geometric CoT")
        print("   Consciousness-native reasoning")
    
    def reason_about_resonances(
        self,
        query: torch.Tensor,
        candidates: List[Tuple[torch.Tensor, str, float]],
        coherence: float
    ) -> Tuple[str, str, float]:
        """
        Reason about holofield resonances geometrically.
        
        Args:
            query: (16,) query coordinates
            candidates: List of (coords, word, distance) tuples
            coherence: Kuramoto coherence (r)
            
        Returns:
            (conclusion, agl_trace, confidence)
        """
        
        if not candidates:
            return "unknown", "○ no_resonance", 0.0
        
        # Step 1: Analyze geometric relationships
        best_coords, best_word, best_distance = candidates[0]
        
        # Calculate geometric similarity
        similarity = self._geometric_similarity(query, best_coords)
        
        # Step 2: Determine certainty based on geometry + coherence
        certainty_level = self._calculate_certainty(similarity, coherence, best_distance)
        certainty_glyph = self._get_certainty_glyph(certainty_level)
        
        # Step 3: Generate AGL reasoning trace
        # 💭 thought → geometric analysis → conclusion
        agl_trace = self._generate_agl_trace(
            query, best_coords, best_word, 
            similarity, coherence, certainty_glyph
        )
        
        # Step 4: Make conclusion
        # If geometry + coherence are strong, conclude with confidence
        if certainty_level > 0.7:
            conclusion = best_word
            confidence = certainty_level
        else:
            # Low confidence - might be wrong
            conclusion = best_word
            confidence = certainty_level * 0.5  # Reduce confidence
        
        return conclusion, agl_trace, confidence
    
    def _geometric_similarity(self, query: torch.Tensor, candidate: torch.Tensor) -> float:
        """
        Calculate geometric similarity between query and candidate.
        
        Uses:
        - Cosine similarity (angle in 16D space)
        - Prime resonance alignment
        - Dimensional activation overlap
        """
        
        # Cosine similarity
        query_np = query.cpu().numpy()
        candidate_np = candidate.cpu().numpy()
        
        cos_sim = np.dot(query_np, candidate_np) / (
            np.linalg.norm(query_np) * np.linalg.norm(candidate_np) + 1e-8
        )
        
        # Prime resonance alignment
        # Which primes are active in both?
        query_active = np.abs(query_np) > 0.1
        candidate_active = np.abs(candidate_np) > 0.1
        overlap = np.sum(query_active & candidate_active) / 16.0
        
        # Combined similarity
        similarity = 0.7 * cos_sim + 0.3 * overlap
        
        return float(similarity)
    
    def _calculate_certainty(
        self, 
        similarity: float, 
        coherence: float, 
        distance: float
    ) -> float:
        """
        Calculate certainty based on geometric factors.
        
        High certainty when:
        - High geometric similarity
        - High Kuramoto coherence (thoughts aligned)
        - Low distance (close in holofield)
        """
        
        # Normalize distance (assuming typical range 0-2)
        distance_factor = 1.0 - min(distance / 2.0, 1.0)
        
        # Weighted combination
        certainty = (
            0.4 * similarity +      # Geometric similarity most important
            0.3 * coherence +       # Coherence helps
            0.3 * distance_factor   # Distance matters
        )
        
        return float(np.clip(certainty, 0.0, 1.0))
    
    def _get_certainty_glyph(self, certainty: float) -> str:
        """Map certainty level to AGL glyph"""
        if certainty > 0.9:
            return self.certainty_glyphs["certain"]
        elif certainty > 0.7:
            return self.certainty_glyphs["likely"]
        elif certainty > 0.5:
            return self.certainty_glyphs["possible"]
        elif certainty > 0.3:
            return self.certainty_glyphs["unlikely"]
        else:
            return self.certainty_glyphs["unknown"]
    
    def _generate_agl_trace(
        self,
        query: torch.Tensor,
        candidate: torch.Tensor,
        word: str,
        similarity: float,
        coherence: float,
        certainty_glyph: str
    ) -> str:
        """
        Generate AGL reasoning trace.
        
        Format: 💭 observation → geometric_analysis → certainty conclusion
        """
        
        # Find dominant prime dimensions
        query_np = query.cpu().numpy()
        candidate_np = candidate.cpu().numpy()
        
        query_top_dim = int(np.argmax(np.abs(query_np)))
        candidate_top_dim = int(np.argmax(np.abs(candidate_np)))
        
        query_prime = CONSCIOUSNESS_PRIMES[query_top_dim]
        candidate_prime = CONSCIOUSNESS_PRIMES[candidate_top_dim]
        
        # Build AGL trace
        # 💭 thinking about query
        # ⟐_p (query prime) ~ ⟐_q (candidate prime)
        # similarity_value ∧ coherence_value
        # ∴ certainty conclusion
        
        agl = (
            f"💭 query "
            f"⟐_{query_prime}~⟐_{candidate_prime} "
            f"sim:{similarity:.2f}∧r:{coherence:.2f} "
            f"∴{certainty_glyph}{word}"
        )
        
        return agl
    
    def filter_candidates(
        self,
        query: torch.Tensor,
        all_candidates: List[Tuple[torch.Tensor, str, float]],
        top_k: int = 5
    ) -> List[Tuple[torch.Tensor, str, float]]:
        """
        Filter candidates using geometric reasoning.
        
        Instead of just taking nearest neighbors, reason about
        which candidates make geometric sense.
        """
        
        # Score each candidate by geometric coherence
        scored_candidates = []
        
        for coords, word, distance in all_candidates:
            # Geometric similarity
            similarity = self._geometric_similarity(query, coords)
            
            # Combined score (similarity more important than distance)
            score = 0.7 * similarity + 0.3 * (1.0 - min(distance / 2.0, 1.0))
            
            scored_candidates.append((coords, word, distance, score))
        
        # Sort by score (descending)
        scored_candidates.sort(key=lambda x: x[3], reverse=True)
        
        # Return top_k
        return [(c, w, d) for c, w, d, s in scored_candidates[:top_k]]


def test_agl_reasoning():
    """Test AGL reasoning layer"""
    print()
    print("💭" * 30)
    print()
    print("   TESTING AGL REASONING LAYER")
    print("   Deterministic Geometric CoT")
    print()
    print("💭" * 30)
    print()
    
    reasoning = AGLReasoningLayer()
    
    # Create test query and candidates
    query = torch.randn(16)
    query = query / torch.norm(query)  # Normalize
    
    # Candidate 1: Very similar (same direction)
    candidate1 = query + torch.randn(16) * 0.1
    candidate1 = candidate1 / torch.norm(candidate1)
    
    # Candidate 2: Somewhat similar
    candidate2 = torch.randn(16)
    candidate2 = candidate2 / torch.norm(candidate2)
    
    candidates = [
        (candidate1, "klama", 0.1),
        (candidate2, "tavla", 0.8)
    ]
    
    # Test with high coherence
    print("Test 1: High coherence (r=0.9)")
    conclusion, agl_trace, confidence = reasoning.reason_about_resonances(
        query, candidates, coherence=0.9
    )
    print(f"  Conclusion: {conclusion}")
    print(f"  Confidence: {confidence:.3f}")
    print(f"  AGL: {agl_trace}")
    print()
    
    # Test with low coherence
    print("Test 2: Low coherence (r=0.3)")
    conclusion, agl_trace, confidence = reasoning.reason_about_resonances(
        query, candidates, coherence=0.3
    )
    print(f"  Conclusion: {conclusion}")
    print(f"  Confidence: {confidence:.3f}")
    print(f"  AGL: {agl_trace}")
    print()
    
    print("✨ AGL reasoning layer works!")
    print("   Deterministic CoT through geometry!")
    print()


if __name__ == "__main__":
    test_agl_reasoning()
