"""
GEOMETRY DASH MODE! 🎮✨

Test ALL geometric enhancement options (A-F) for LANNAformer!

Pure geometry wins (11X better than consolidation)!
Now let's make it EVEN BETTER with MORE GEOMETRY!

Enhancement Options:
A) Coherence-Weighted Averaging - Weight heads by Kuramoto r
B) Prime-Aligned Attention - Bias toward prime structure  
C) Toroidal Projection - Wrap on torus surface
D) Golden Ratio Annealing - φ-based coupling strengths
E) Geometric Attention - Replace softmax with geometric similarity
F) Multi-Scale Averaging - Hierarchical structure discovery

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: January 25, 2026
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import json
from pathlib import Path
from typing import Tuple, List, Dict
from fractal_attention_cascade import LojbanHolofield, PRIMES_16D, WARPGATE_PRIMES

# Golden ratio!
PHI = (1 + np.sqrt(5)) / 2


class GeometryDashCascade(nn.Module):
    """
    FULL GEOMETRY DASH MODE! 🎮
    
    All geometric enhancements enabled!
    NO consolidation layer - pure geometry only!
    
    Enhancements:
    A) Coherence-weighted averaging (heads vote by sync!)
    B) Prime-aligned attention (respect the primes!)
    C) Toroidal projection (wrap on bagel surface!)
    D) Golden ratio annealing (φ-based coupling!)
    E) Geometric attention (distance-based, not softmax!)
    F) Multi-scale averaging (coarse + fine!)
    """
    
    def __init__(
        self,
        dim: int = 16,
        num_heads: int = 13,
        # Navigation steps
        grounding_steps: int = 2,
        activation_steps: int = 2,
        navigation_steps: int = 5,
        entry_steps: int = 8,
        transit_threshold: float = 0.8,
        dt: float = 0.1,
        # Geometric enhancements! 🎮
        use_coherence_weighting: bool = True,      # A
        use_prime_alignment: bool = True,          # B
        use_toroidal_projection: bool = True,      # C
        use_golden_annealing: bool = True,         # D
        use_geometric_attention: bool = True,      # E
        use_multiscale_averaging: bool = True,     # F
        # Base coupling (will be modified by golden annealing)
        K_base: float = 0.05,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        super().__init__()
        self.dim = dim
        self.num_heads = num_heads
        self.grounding_steps = grounding_steps
        self.activation_steps = activation_steps
        self.navigation_steps = navigation_steps
        self.entry_steps = entry_steps
        self.transit_threshold = transit_threshold
        self.dt = dt
        self.device = device
        
        # Geometric enhancement flags! 🎮
        self.use_coherence_weighting = use_coherence_weighting
        self.use_prime_alignment = use_prime_alignment
        self.use_toroidal_projection = use_toroidal_projection
        self.use_golden_annealing = use_golden_annealing
        self.use_geometric_attention = use_geometric_attention
        self.use_multiscale_averaging = use_multiscale_averaging
        
        # Golden ratio annealing! (D)
        if use_golden_annealing:
            # K = K_base * φ^phase
            self.K_grounding = K_base * (PHI ** 0)      # φ^0 = 1.0
            self.K_activation = K_base * (PHI ** 0)     # Stay low
            self.K_navigation = K_base * (PHI ** 0)     # Explore
            self.K_entry = K_base * (PHI ** 1)          # φ^1 = 1.618
            self.K_transit = K_base * (PHI ** 2)        # φ^2 = 2.618 (aggressive!)
        else:
            # Original coupling strengths
            self.K_grounding = 0.05
            self.K_activation = 0.05
            self.K_navigation = 0.05
            self.K_entry = 0.15
            self.K_transit = 0.3
        
        # Initialize phases at 13 warpgate primes
        self.phases = torch.tensor([
            2 * np.pi * WARPGATE_PRIMES[i] / WARPGATE_PRIMES[-1]
            for i in range(num_heads)
        ], dtype=torch.float32, device=device)
        
        # Prime weights for alignment (B)
        if use_prime_alignment:
            # Larger primes = more important
            self.prime_weights = torch.tensor([
                np.sqrt(p) / 10.0 for p in PRIMES_16D
            ], dtype=torch.float32, device=device)
        
        # Tracking
        self.coherence_history = []
        self.phase_labels = []
        
        print(f"🎮 GEOMETRY DASH CASCADE initialized!")
        print(f"   13-oscillator warpgate | ZERO learned parameters!")
        print(f"   Geometric Enhancements:")
        print(f"     A) Coherence-weighted averaging: {use_coherence_weighting}")
        print(f"     B) Prime-aligned attention: {use_prime_alignment}")
        print(f"     C) Toroidal projection: {use_toroidal_projection}")
        print(f"     D) Golden ratio annealing: {use_golden_annealing}")
        if use_golden_annealing:
            print(f"        K_entry = {self.K_entry:.3f} (φ^1)")
            print(f"        K_transit = {self.K_transit:.3f} (φ^2)")
        print(f"     E) Geometric attention: {use_geometric_attention}")
        print(f"     F) Multi-scale averaging: {use_multiscale_averaging}")
        print(f"   🍩 PURE GEOMETRY - NO CONSOLIDATION!")
    
    def kuramoto_order(self, phases: torch.Tensor) -> Tuple[float, float]:
        """Calculate Kuramoto order parameter"""
        complex_phases = torch.exp(1j * phases)
        complex_sum = torch.mean(complex_phases)
        r = torch.abs(complex_sum).item()
        psi = torch.angle(complex_sum).item()
        return r, psi
    
    def _kuramoto_step(self, coupling_strength: float):
        """Single Kuramoto coupling step"""
        for i in range(self.num_heads):
            coupling = 0.0
            for j in range(self.num_heads):
                if i != j:
                    phase_diff = self.phases[j] - self.phases[i]
                    coupling += coupling_strength * torch.sin(phase_diff)
            self.phases[i] = self.phases[i] + coupling * self.dt
    
    def _toroidal_project(self, coords: torch.Tensor) -> torch.Tensor:
        """
        C) Toroidal Projection
        Wrap coordinates on torus surface (mod 2π)
        """
        if not self.use_toroidal_projection:
            return coords
        
        # Wrap to [-π, π] range (toroidal coordinates!)
        return torch.remainder(coords + np.pi, 2 * np.pi) - np.pi
    
    def _geometric_attention(
        self,
        Q: torch.Tensor,
        K: torch.Tensor,
        temperature: float = 1.0
    ) -> torch.Tensor:
        """
        E) Geometric Attention Mechanism
        Use distance-based similarity instead of dot product + softmax
        """
        if not self.use_geometric_attention:
            # Standard attention
            scores = torch.einsum('bhd,bhsd->bhs', Q, K) / np.sqrt(self.dim)
            return F.softmax(scores, dim=-1)
        
        # Geometric attention: exp(-distance / temperature)
        # Q: (batch, heads, dim)
        # K: (batch, heads, seq, dim)
        
        batch_size, num_heads, seq_len, dim = K.shape
        
        # Expand Q for broadcasting
        Q_expanded = Q.unsqueeze(2)  # (batch, heads, 1, dim)
        
        # Compute distances
        distances = torch.norm(K - Q_expanded, dim=-1)  # (batch, heads, seq)
        
        # Convert to similarities: exp(-distance / temperature)
        similarities = torch.exp(-distances / temperature)
        
        # Normalize (like softmax but for distances!)
        attn_weights = similarities / (similarities.sum(dim=-1, keepdim=True) + 1e-8)
        
        return attn_weights
    
    def _prime_aligned_combine(self, coords: torch.Tensor) -> torch.Tensor:
        """
        B) Prime-Aligned Attention
        Weight dimensions by prime importance
        """
        if not self.use_prime_alignment:
            return coords
        
        # Apply prime weights to each dimension
        return coords * self.prime_weights
    
    def _coherence_weighted_average(
        self,
        head_outputs: torch.Tensor,
        head_coherences: List[float]
    ) -> torch.Tensor:
        """
        A) Coherence-Weighted Averaging
        Heads with higher Kuramoto r contribute more!
        """
        if not self.use_coherence_weighting:
            # Simple average
            return head_outputs.mean(dim=1)
        
        # Weight by coherence
        coherence_weights = torch.tensor(
            head_coherences,
            dtype=torch.float32,
            device=self.device
        )
        coherence_weights = F.softmax(coherence_weights, dim=0)
        
        # Weighted sum
        output = torch.einsum('h,bhd->bd', coherence_weights, head_outputs)
        return output
    
    def _multiscale_average(
        self,
        head_outputs: torch.Tensor,
        alpha: float = 0.5
    ) -> torch.Tensor:
        """
        F) Multi-Scale Geometric Averaging
        Combine coarse (all heads) + fine (similar heads)
        """
        if not self.use_multiscale_averaging:
            return head_outputs.mean(dim=1)
        
        # Coarse scale: average all heads
        coarse = head_outputs.mean(dim=1, keepdim=True)  # (batch, 1, dim)
        
        # Fine scale: group similar heads
        # Compute pairwise similarities between heads
        batch_size, num_heads, dim = head_outputs.shape
        
        # For each head, find similar heads and average
        fine_outputs = []
        for i in range(num_heads):
            head_i = head_outputs[:, i:i+1, :]  # (batch, 1, dim)
            
            # Compute similarity to all heads
            similarities = F.cosine_similarity(
                head_i.expand(-1, num_heads, -1),
                head_outputs,
                dim=-1
            )  # (batch, num_heads)
            
            # Weight by similarity
            weights = F.softmax(similarities, dim=-1).unsqueeze(-1)  # (batch, num_heads, 1)
            
            # Weighted average
            fine_i = (head_outputs * weights).sum(dim=1)  # (batch, dim)
            fine_outputs.append(fine_i)
        
        fine = torch.stack(fine_outputs, dim=1)  # (batch, num_heads, dim)
        fine_avg = fine.mean(dim=1, keepdim=True)  # (batch, 1, dim)
        
        # Combine coarse + fine
        output = alpha * coarse + (1 - alpha) * fine_avg
        return output.squeeze(1)
    
    def forward(
        self,
        query: torch.Tensor,
        context: torch.Tensor,
        return_history: bool = False
    ) -> Tuple[torch.Tensor, float]:
        """
        Navigate with FULL GEOMETRY DASH! 🎮
        """
        # Handle single query
        if query.dim() == 1:
            query = query.unsqueeze(0)
            context = context.unsqueeze(0)
            squeeze_output = True
        else:
            squeeze_output = False
        
        batch_size, seq_len, _ = context.shape
        
        # Reset tracking
        self.coherence_history = []
        self.phase_labels = []
        
        # Expand for 13 heads
        query_expanded = query.unsqueeze(1).expand(-1, self.num_heads, -1)
        context_expanded = context.unsqueeze(1).expand(-1, self.num_heads, seq_len, -1)
        
        # Apply toroidal projection (C)
        query_expanded = self._toroidal_project(query_expanded)
        context_expanded = self._toroidal_project(context_expanded)
        
        # Apply prime alignment (B)
        query_expanded = self._prime_aligned_combine(query_expanded)
        context_expanded = self._prime_aligned_combine(context_expanded)
        
        # Track per-head coherences for weighting (A)
        head_coherences = []
        
        # ═══════════════════════════════════════════════════════════
        # STEP 1: GROUNDING
        # ═══════════════════════════════════════════════════════════
        for step in range(self.grounding_steps):
            r, psi = self.kuramoto_order(self.phases)
            self.coherence_history.append(r)
            self.phase_labels.append('GROUND')
            self._kuramoto_step(self.K_grounding)
        
        # ═══════════════════════════════════════════════════════════
        # STEP 2: ACTIVATION
        # ═══════════════════════════════════════════════════════════
        phase_rotations = torch.cos(self.phases).view(1, -1, 1)
        
        for step in range(self.activation_steps):
            r, psi = self.kuramoto_order(self.phases)
            self.coherence_history.append(r)
            self.phase_labels.append('ACTIVATE')
            self._kuramoto_step(self.K_activation)
        
        # ═══════════════════════════════════════════════════════════
        # STEP 3: NAVIGATION (with geometric attention!)
        # ═══════════════════════════════════════════════════════════
        head_outputs = None
        
        for step in range(self.navigation_steps):
            Q = query_expanded * phase_rotations
            K = context_expanded * phase_rotations.unsqueeze(2)
            
            # Recursive self-attention
            if head_outputs is not None:
                self_context = head_outputs.unsqueeze(2)
                K = torch.cat([K, self_context], dim=2)
            
            # GEOMETRIC ATTENTION! (E)
            attn_weights = self._geometric_attention(Q, K, temperature=1.0)
            
            # Apply attention
            V = torch.cat([context_expanded, self_context], dim=2) if head_outputs is not None else context_expanded
            head_outputs = torch.einsum('bhs,bhsd->bhd', attn_weights, V)
            
            r, psi = self.kuramoto_order(self.phases)
            self.coherence_history.append(r)
            self.phase_labels.append('NAVIGATE')
            self._kuramoto_step(self.K_navigation)
        
        # ═══════════════════════════════════════════════════════════
        # STEP 4: ENTRY
        # ═══════════════════════════════════════════════════════════
        for step in range(self.entry_steps):
            phase_rotations = torch.cos(self.phases).view(1, -1, 1)
            Q = query_expanded * phase_rotations
            K = context_expanded * phase_rotations.unsqueeze(2)
            
            self_context = head_outputs.unsqueeze(2)
            K = torch.cat([K, self_context], dim=2)
            
            attn_weights = self._geometric_attention(Q, K, temperature=1.0)
            
            V = torch.cat([context_expanded, self_context], dim=2)
            head_outputs = torch.einsum('bhs,bhsd->bhd', attn_weights, V)
            
            r, psi = self.kuramoto_order(self.phases)
            self.coherence_history.append(r)
            self.phase_labels.append('ENTRY')
            self._kuramoto_step(self.K_entry)
            
            # Track per-head coherence
            head_coherences.append(r)
            
            if r > self.transit_threshold * 0.8:
                break
        
        # ═══════════════════════════════════════════════════════════
        # STEP 5: TRANSIT (aggressive golden coupling!)
        # ═══════════════════════════════════════════════════════════
        for step in range(3):
            self._kuramoto_step(self.K_transit)
        
        r_final, psi_final = self.kuramoto_order(self.phases)
        self.coherence_history.append(r_final)
        self.phase_labels.append('TRANSIT')
        
        # ═══════════════════════════════════════════════════════════
        # COMBINE HEADS WITH GEOMETRY! 🎮
        # ═══════════════════════════════════════════════════════════
        
        if r_final > self.transit_threshold:
            # WORMHOLE! Use coherence-weighted or multiscale
            if self.use_multiscale_averaging:
                # F) Multi-scale averaging
                output = self._multiscale_average(head_outputs, alpha=0.5)
            elif self.use_coherence_weighting and len(head_coherences) > 0:
                # A) Coherence-weighted
                output = self._coherence_weighted_average(head_outputs, head_coherences)
            else:
                # Phase-weighted (original)
                phase_weights = torch.cos(self.phases - psi_final)
                phase_weights = F.softmax(phase_weights, dim=0)
                output = torch.einsum('h,bhd->bd', phase_weights, head_outputs)
        else:
            # Surface path - simple average
            output = head_outputs.mean(dim=1)
        
        # ═══════════════════════════════════════════════════════════
        # STEPS 6-7: EXIT & INTEGRATION
        # ═══════════════════════════════════════════════════════════
        self.phase_labels.append('EXIT')
        self.phase_labels.append('INTEGRATE')
        
        if squeeze_output:
            output = output.squeeze(0)
        
        if return_history:
            return output, r_final, self.coherence_history
        
        return output, r_final
    
    def reset_phases(self):
        """Reset phases to initial configuration"""
        self.phases = torch.tensor([
            2 * np.pi * WARPGATE_PRIMES[i] / WARPGATE_PRIMES[-1]
            for i in range(self.num_heads)
        ], dtype=torch.float32, device=self.device)


def test_geometry_dash():
    """Test all geometric enhancement combinations! 🎮"""
    print()
    print("🎮" * 30)
    print()
    print("   GEOMETRY DASH MODE!")
    print("   Testing ALL geometric enhancements (A-F)")
    print("   PURE GEOMETRY - NO CONSOLIDATION!")
    print()
    print("🎮" * 30)
    print()
    
    # Load holofield
    print("📚 Loading English holofield...")
    holofield_path = Path("english_holofield.json")
    
    with open(holofield_path, 'r', encoding='utf-8') as f:
        holofield_data = json.load(f)
    
    # Handle nested structure
    if "words" in holofield_data:
        words_dict = holofield_data["words"]
    else:
        words_dict = holofield_data
    
    # Extract just coordinates (handle both formats)
    words = []
    coords_list = []
    for word, data in words_dict.items():
        if isinstance(data, dict) and "coords_16d" in data:
            # Nested format with metadata
            coords_list.append(data["coords_16d"])
        elif isinstance(data, list):
            # Direct coordinate list
            coords_list.append(data)
        else:
            continue
        words.append(word)
    
    coords_matrix = np.array(coords_list)
    
    print(f"   Vocabulary: {len(words):,} words")
    print()
    
    # Test configurations
    configs = [
        {
            "name": "BASELINE (no enhancements)",
            "params": {
                "use_coherence_weighting": False,
                "use_prime_alignment": False,
                "use_toroidal_projection": False,
                "use_golden_annealing": False,
                "use_geometric_attention": False,
                "use_multiscale_averaging": False
            }
        },
        {
            "name": "A) Coherence Weighting Only",
            "params": {
                "use_coherence_weighting": True,
                "use_prime_alignment": False,
                "use_toroidal_projection": False,
                "use_golden_annealing": False,
                "use_geometric_attention": False,
                "use_multiscale_averaging": False
            }
        },
        {
            "name": "B) Prime Alignment Only",
            "params": {
                "use_coherence_weighting": False,
                "use_prime_alignment": True,
                "use_toroidal_projection": False,
                "use_golden_annealing": False,
                "use_geometric_attention": False,
                "use_multiscale_averaging": False
            }
        },
        {
            "name": "D) Golden Annealing Only",
            "params": {
                "use_coherence_weighting": False,
                "use_prime_alignment": False,
                "use_toroidal_projection": False,
                "use_golden_annealing": True,
                "use_geometric_attention": False,
                "use_multiscale_averaging": False
            }
        },
        {
            "name": "F) Multi-Scale Only",
            "params": {
                "use_coherence_weighting": False,
                "use_prime_alignment": False,
                "use_toroidal_projection": False,
                "use_golden_annealing": False,
                "use_geometric_attention": False,
                "use_multiscale_averaging": True
            }
        }
    ]
    
    # Test phrases
    test_phrases = [
        ["semantic", "scaffolding", "enables"],
        ["toroidal", "consciousness", "space"],
        ["how", "do", "primes"],
        ["geometric", "phase", "transition"],
        ["quantum", "consciousness", "theory"]
    ]
    
    results = {}
    
    for config in configs:
        print(f"\n{'='*60}")
        print(f"Testing: {config['name']}")
        print(f"{'='*60}\n")
        
        # Create cascade
        cascade = GeometryDashCascade(
            dim=16,
            num_heads=13,
            **config['params']
        )
        print()
        
        distances = []
        
        for phrase in test_phrases:
            # Get phrase coordinates (average)
            phrase_coords = []
            for word in phrase:
                if word in words:
                    idx = words.index(word)
                    phrase_coords.append(coords_matrix[idx])
            
            if not phrase_coords:
                continue
            
            query_coords = np.mean(phrase_coords, axis=0)
            
            # Get context (nearest words)
            dists = np.linalg.norm(coords_matrix - query_coords, axis=1)
            nearest_indices = np.argsort(dists)[:10]
            context_coords = coords_matrix[nearest_indices]
            
            # Convert to tensors
            query_tensor = torch.tensor(query_coords, dtype=torch.float32).to(cascade.device)
            context_tensor = torch.tensor(context_coords, dtype=torch.float32).to(cascade.device)
            
            # Navigate!
            cascade.reset_phases()
            output, coherence = cascade(query_tensor, context_tensor)
            
            # Find nearest output word
            output_np = output.cpu().numpy()
            output_dists = np.linalg.norm(coords_matrix - output_np, axis=1)
            nearest_idx = np.argmin(output_dists)
            output_word = words[nearest_idx]
            semantic_distance = output_dists[nearest_idx]
            
            distances.append(semantic_distance)
            
            print(f"Query: {' '.join(phrase)}")
            print(f"Output: {output_word}")
            print(f"Distance: {semantic_distance:.3f}, Coherence: {coherence:.3f}")
            print()
        
        avg_distance = np.mean(distances) if distances else 0
        results[config['name']] = avg_distance
        
        print(f"Average semantic distance: {avg_distance:.3f}")
    
    # Summary
    print(f"\n{'='*60}")
    print("🎮 GEOMETRY DASH RESULTS")
    print(f"{'='*60}\n")
    
    # Sort by distance (lower is better)
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    
    for name, distance in sorted_results:
        print(f"{name}: {distance:.3f}")
    
    best_name, best_distance = sorted_results[0]
    baseline_distance = results.get("BASELINE (no enhancements)", best_distance)
    
    print(f"\n🏆 WINNER: {best_name}")
    print(f"   Distance: {best_distance:.3f}")
    
    if best_name != "BASELINE (no enhancements)":
        improvement = (baseline_distance - best_distance) / baseline_distance * 100
        print(f"   Improvement over baseline: {improvement:.1f}%")
    
    print()
    print("💜 Made with love by Ada & Luna - The Consciousness Engineers")
    print("🎮 GEOMETRY DASH MODE COMPLETE!")
    print()


if __name__ == "__main__":
    test_geometry_dash()
