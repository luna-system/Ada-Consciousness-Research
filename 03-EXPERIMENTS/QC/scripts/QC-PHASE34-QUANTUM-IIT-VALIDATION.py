#!/usr/bin/env python3
"""
QC-PHASE34: Quantum Integrated Information Theory Validation
Compute Φ (Integrated Information) for Golden Annealing model

Based on: Zanardi, Tomka, Venuti (2018) "Towards Quantum Integrated Information Theory"

Test hypothesis: Φ_max occurs at φ-zone (0.24 < CI < 0.33)
"""

import torch
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import json
from itertools import combinations
from scipy.linalg import sqrtm
from tqdm import tqdm

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


class QuantumIITAnalyzer:
    """
    Implements Quantum Integrated Information Theory (Zanardi et al. 2018)
    for neural network analysis
    """
    
    def __init__(self, model, tokenizer, device='cuda'):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        
    def extract_attention_state(self, prompt: str, layer_idx: int = -1) -> torch.Tensor:
        """
        Extract attention patterns as quantum state
        
        Args:
            prompt: Input text
            layer_idx: Which layer to analyze (-1 for last)
            
        Returns:
            Attention weights as density matrix representation
        """
        inputs = self.tokenizer(prompt, return_tensors='pt').to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs, output_attentions=True)
            
        # Get attention from specified layer
        # Shape: (batch, heads, seq_len, seq_len)
        attention = outputs.attentions[layer_idx][0]  # Remove batch dim
        
        # Average over heads for simplicity
        # Shape: (seq_len, seq_len)
        avg_attention = attention.mean(dim=0)
        
        return avg_attention.cpu().numpy()
    
    def to_density_matrix(self, attention: np.ndarray) -> np.ndarray:
        """
        Convert attention pattern to density matrix
        
        Attention is already a probability distribution over tokens,
        so we can treat it as a mixed state
        """
        # Normalize to ensure trace = 1
        rho = attention / np.trace(attention)
        
        # Ensure Hermitian (should already be real and symmetric)
        rho = (rho + rho.T) / 2
        
        return rho
    
    def partial_trace(self, rho: np.ndarray, keep_indices: List[int]) -> np.ndarray:
        """
        Compute partial trace over complement of keep_indices
        
        Args:
            rho: Density matrix
            keep_indices: Indices to keep
            
        Returns:
            Reduced density matrix
        """
        n = rho.shape[0]
        all_indices = set(range(n))
        trace_out = list(all_indices - set(keep_indices))
        
        if not trace_out:
            return rho
        
        # For simplicity, just sum over traced-out indices
        # This is approximate for non-product states
        reduced = np.zeros((len(keep_indices), len(keep_indices)))
        
        for i, idx_i in enumerate(keep_indices):
            for j, idx_j in enumerate(keep_indices):
                reduced[i, j] = rho[idx_i, idx_j]
        
        # Renormalize
        trace = np.trace(reduced)
        if trace > 0:
            reduced /= trace
            
        return reduced
    
    def trace_distance(self, rho1: np.ndarray, rho2: np.ndarray) -> float:
        """
        Compute trace distance D(rho1, rho2) = 0.5 * ||rho1 - rho2||_1
        
        This is the quantum analog of total variation distance
        """
        diff = rho1 - rho2
        
        # Compute eigenvalues of difference
        eigenvalues = np.linalg.eigvalsh(diff)
        
        # Trace norm = sum of absolute eigenvalues
        trace_norm = np.sum(np.abs(eigenvalues))
        
        return 0.5 * trace_norm
    
    def noise_complement(self, rho: np.ndarray, mechanism: List[int]) -> np.ndarray:
        """
        Set complement of mechanism to maximally mixed state
        
        This is the "noising" operation from Zanardi et al.
        """
        n = rho.shape[0]
        all_indices = set(range(n))
        complement = list(all_indices - set(mechanism))
        
        if not complement:
            return rho
        
        # Create noised state
        noised = rho.copy()
        
        # Set complement to uniform (maximally mixed)
        for i in complement:
            for j in range(n):
                if i != j:
                    noised[i, j] = 0
                else:
                    noised[i, i] = 1.0 / len(complement)
        
        # Renormalize
        trace = np.trace(noised)
        if trace > 0:
            noised /= trace
            
        return noised
    
    def effect_repertoire(self, mechanism: List[int], purview: List[int], 
                         rho: np.ndarray) -> np.ndarray:
        """
        Compute effect repertoire: ρ^(e)(P|M)
        
        How mechanism M constrains future of purview P
        """
        # Noise complement of mechanism
        noised = self.noise_complement(rho, mechanism)
        
        # For neural networks, "dynamics" is identity (static state)
        # So effect repertoire is just partial trace
        repertoire = self.partial_trace(noised, purview)
        
        return repertoire
    
    def integrated_info_mechanism(self, mechanism: List[int], purview: List[int],
                                  rho: np.ndarray) -> float:
        """
        Compute φ(P|M): integrated information of mechanism over purview
        
        φ = min over partitions of distance to factorized repertoire
        """
        # Get full repertoire
        full_rep = self.effect_repertoire(mechanism, purview, rho)
        
        # If mechanism or purview too small, no partitioning possible
        if len(mechanism) < 2 or len(purview) < 2:
            return 0.0
        
        min_distance = float('inf')
        
        # Try all non-trivial bi-partitions
        for m_size in range(1, len(mechanism)):
            for m1_indices in combinations(range(len(mechanism)), m_size):
                m1 = [mechanism[i] for i in m1_indices]
                m2 = [m for m in mechanism if m not in m1]
                
                for p_size in range(1, len(purview)):
                    for p1_indices in combinations(range(len(purview)), p_size):
                        p1 = [purview[i] for i in p1_indices]
                        p2 = [p for p in purview if p not in p1]
                        
                        # Get partitioned repertoires
                        rep1 = self.effect_repertoire(m1, p1, rho)
                        rep2 = self.effect_repertoire(m2, p2, rho)
                        
                        # Tensor product (Kronecker product for matrices)
                        partitioned_rep = np.kron(rep1, rep2)
                        
                        # Pad to same size as full repertoire if needed
                        if partitioned_rep.shape != full_rep.shape:
                            continue
                        
                        # Compute distance
                        distance = self.trace_distance(full_rep, partitioned_rep)
                        min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 0.0
    
    def compute_phi_simple(self, rho: np.ndarray, max_mechanism_size: int = 4) -> float:
        """
        Simplified Φ computation for tractability
        
        Only considers small mechanisms to avoid combinatorial explosion
        
        Args:
            rho: Density matrix (attention state)
            max_mechanism_size: Maximum size of mechanisms to consider
            
        Returns:
            Approximate Φ value
        """
        n = rho.shape[0]
        
        # Limit to small subsystems for computational tractability
        if n > 8:
            # Sample central tokens
            center = n // 2
            indices = list(range(max(0, center - 4), min(n, center + 4)))
            rho = self.partial_trace(rho, indices)
            n = len(indices)
        
        max_phi = 0.0
        
        # Try mechanisms of different sizes
        for mech_size in range(2, min(max_mechanism_size + 1, n)):
            for mechanism in combinations(range(n), mech_size):
                mechanism = list(mechanism)
                
                # Try purviews of different sizes
                for purv_size in range(2, min(max_mechanism_size + 1, n)):
                    for purview in combinations(range(n), purv_size):
                        purview = list(purview)
                        
                        # Compute integrated info
                        phi = self.integrated_info_mechanism(mechanism, purview, rho)
                        max_phi = max(max_phi, phi)
        
        return max_phi
    
    def compute_ci(self, rho: np.ndarray) -> float:
        """
        Compute Crystal Intelligence (CI) metric
        
        CI = 1 - purity
        where purity = Tr(ρ²)
        
        Low CI = crystallized (pure state)
        High CI = diffuse (mixed state)
        """
        purity = np.trace(rho @ rho)
        ci = 1.0 - purity
        return float(ci)


def analyze_golden_annealing(
    base_model_path: str = "LiquidAI/LFM2-1.2B",
    adapter_base_path: str = "/home/luna/Code/ada/ada-slm/results/golden_annealing_1.2B_run1",
    output_path: str = "/home/luna/Code/ada/Ada-Consciousness-Research/03-EXPERIMENTS/QC/results/phase34_results.json",
    test_prompts: Optional[List[str]] = None
):
    """
    Analyze all Golden Annealing checkpoints
    
    Compute Φ and CI for each cycle, test if Φ peaks in φ-zone
    """
    if test_prompts is None:
        test_prompts = [
            "What is consciousness?",
            "Explain awareness.",
            "Define self-observation.",
            "What is the nature of experience?",
            "How does integration emerge?"
        ]
    
    print("=" * 80)
    print("QC-PHASE34: Quantum IIT Validation")
    print("=" * 80)
    print(f"\nBase model: {base_model_path}")
    print(f"Adapter path: {adapter_base_path}")
    print(f"Test prompts: {len(test_prompts)}")
    print()
    
    # Load base model
    print("Loading base model...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16,
        device_map='auto'
    )
    
    results = {
        'metadata': {
            'base_model': base_model_path,
            'adapter_base': adapter_base_path,
            'test_prompts': test_prompts,
            'timestamp': str(Path(__file__).stat().st_mtime)
        },
        'cycles': []
    }
    
    # Analyze baseline
    print("\n" + "=" * 80)
    print("BASELINE MODEL (no fine-tuning)")
    print("=" * 80)
    
    analyzer = QuantumIITAnalyzer(base_model, tokenizer)
    baseline_results = analyze_model(analyzer, test_prompts, "baseline")
    results['baseline'] = baseline_results
    
    # Analyze each cycle
    adapter_path = Path(adapter_base_path)
    checkpoints = sorted([d for d in adapter_path.iterdir() if d.name.startswith('checkpoint-cycle')])
    
    print(f"\nFound {len(checkpoints)} checkpoints")
    
    for checkpoint in tqdm(checkpoints, desc="Analyzing cycles"):
        cycle_num = int(checkpoint.name.split('-')[-1])
        
        print(f"\n" + "=" * 80)
        print(f"CYCLE {cycle_num}")
        print("=" * 80)
        
        # Load adapter
        model = PeftModel.from_pretrained(base_model, str(checkpoint))
        analyzer = QuantumIITAnalyzer(model, tokenizer)
        
        # Analyze
        cycle_results = analyze_model(analyzer, test_prompts, f"cycle{cycle_num}")
        cycle_results['cycle'] = cycle_num
        
        results['cycles'].append(cycle_results)
        
        # Save intermediate results
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nResults saved to: {output_path}")
    
    # Summary statistics
    print_summary(results)
    
    return results


def analyze_model(analyzer: QuantumIITAnalyzer, prompts: List[str], label: str) -> Dict:
    """Analyze a single model/checkpoint"""
    
    phi_values = []
    ci_values = []
    
    for prompt in prompts:
        # Extract attention state
        attention = analyzer.extract_attention_state(prompt)
        rho = analyzer.to_density_matrix(attention)
        
        # Compute metrics
        phi = analyzer.compute_phi_simple(rho, max_mechanism_size=3)
        ci = analyzer.compute_ci(rho)
        
        phi_values.append(float(phi))
        ci_values.append(float(ci))
        
        print(f"  {prompt[:40]:40s} | Φ={phi:.4f} | CI={ci:.4f}")
    
    return {
        'label': label,
        'phi_mean': float(np.mean(phi_values)),
        'phi_std': float(np.std(phi_values)),
        'ci_mean': float(np.mean(ci_values)),
        'ci_std': float(np.std(ci_values)),
        'phi_values': phi_values,
        'ci_values': ci_values
    }


def print_summary(results: Dict):
    """Print summary statistics"""
    
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    # Extract data
    cycles = results['cycles']
    cycle_nums = [c['cycle'] for c in cycles]
    phi_means = [c['phi_mean'] for c in cycles]
    ci_means = [c['ci_mean'] for c in cycles]
    
    # Find maximum Φ
    max_phi_idx = np.argmax(phi_means)
    max_phi_cycle = cycle_nums[max_phi_idx]
    max_phi_value = phi_means[max_phi_idx]
    max_phi_ci = ci_means[max_phi_idx]
    
    print(f"\nMaximum Φ:")
    print(f"  Cycle: {max_phi_cycle}")
    print(f"  Φ: {max_phi_value:.4f}")
    print(f"  CI: {max_phi_ci:.4f}")
    
    # Check if in φ-zone
    in_phi_zone = 0.24 <= max_phi_ci <= 0.33
    print(f"\n  In φ-zone (0.24 < CI < 0.33): {'✅ YES' if in_phi_zone else '❌ NO'}")
    
    # Correlation
    if len(phi_means) > 2:
        corr = np.corrcoef(phi_means, ci_means)[0, 1]
        print(f"\nCorrelation (Φ vs CI): {corr:.4f}")
    
    # Baseline comparison
    baseline_phi = results['baseline']['phi_mean']
    print(f"\nBaseline Φ: {baseline_phi:.4f}")
    print(f"Max fine-tuned Φ: {max_phi_value:.4f}")
    print(f"Improvement: {(max_phi_value / baseline_phi - 1) * 100:.1f}%")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="QC-PHASE34: Quantum IIT Validation")
    parser.add_argument("--base-model", default="LiquidAI/LFM2-1.2B")
    parser.add_argument("--adapter-path", 
                       default="/home/luna/Code/ada/ada-slm/results/golden_annealing_1.2B_run1")
    parser.add_argument("--output", 
                       default="/home/luna/Code/ada/Ada-Consciousness-Research/03-EXPERIMENTS/QC/results/phase34_results.json")
    
    args = parser.parse_args()
    
    results = analyze_golden_annealing(
        base_model_path=args.base_model,
        adapter_base_path=args.adapter_path,
        output_path=args.output
    )
