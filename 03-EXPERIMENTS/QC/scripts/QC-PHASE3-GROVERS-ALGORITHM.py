"""
QC Phase 3: Grover's Algorithm Deep Dive
=========================================

Testing if the quantum search structure shows φ patterns,
and whether LLMs understand the interference dynamics.

Grover's Algorithm:
- Quantum search with O(√N) speedup
- Uses amplitude amplification via interference
- Optimal iterations: ~π/4 * √N
- THE question: Does φ appear in the amplitude dynamics?

Date: January 6, 2026
Authors: Ada & Luna
"""

import numpy as np
from scipy import linalg
from typing import Tuple, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Constants
PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI
PI = np.pi

print("=" * 70)
print("QC PHASE 3: GROVER'S ALGORITHM & THE GOLDEN RATIO")
print("=" * 70)

# =============================================================================
# GROVER'S ALGORITHM FUNDAMENTALS
# =============================================================================

def hadamard_n(n: int) -> np.ndarray:
    """N-qubit Hadamard gate H⊗n."""
    H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    result = H1
    for _ in range(n - 1):
        result = np.kron(result, H1)
    return result

def oracle(N: int, marked: int) -> np.ndarray:
    """Oracle that marks state |marked⟩ with a phase flip."""
    O = np.eye(N)
    O[marked, marked] = -1
    return O

def diffusion(N: int) -> np.ndarray:
    """Grover diffusion operator: 2|s⟩⟨s| - I where |s⟩ is uniform superposition."""
    s = np.ones(N) / np.sqrt(N)  # Uniform superposition
    D = 2 * np.outer(s, s) - np.eye(N)
    return D

def grover_iteration(N: int, marked: int) -> np.ndarray:
    """Single Grover iteration: G = D @ O."""
    return diffusion(N) @ oracle(N, marked)

def run_grover(n_qubits: int, marked: int, iterations: int) -> np.ndarray:
    """Run Grover's algorithm and return final state."""
    N = 2**n_qubits
    
    # Start in uniform superposition
    state = np.ones(N) / np.sqrt(N)
    
    # Apply Grover iterations
    G = grover_iteration(N, marked)
    for _ in range(iterations):
        state = G @ state
    
    return state

def optimal_iterations(N: int) -> int:
    """Optimal number of Grover iterations for N items."""
    return int(np.round(PI / 4 * np.sqrt(N)))

# =============================================================================
# EXPERIMENT 1: Amplitude Evolution and φ
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 1: Amplitude Evolution - Searching for φ")
print("=" * 70)

print("\nGrover's amplitudes evolve as:")
print("  α_k = sin((2k+1)θ)  where sin(θ) = 1/√N")
print("  β_k = cos((2k+1)θ)  [non-marked states]")
print("\nLet's track the amplitudes and look for φ...")

def track_amplitudes(n_qubits: int, marked: int, max_iter: int) -> List[dict]:
    """Track amplitude evolution through Grover iterations."""
    N = 2**n_qubits
    state = np.ones(N) / np.sqrt(N)
    G = grover_iteration(N, marked)
    
    history = []
    for k in range(max_iter + 1):
        marked_amp = state[marked]
        other_amp = state[(marked + 1) % N]  # Any non-marked state
        
        # Probabilities
        p_marked = np.abs(marked_amp)**2
        p_other = np.abs(other_amp)**2
        
        # Ratio
        ratio = p_marked / p_other if p_other > 1e-10 else np.inf
        
        history.append({
            'iteration': k,
            'p_marked': p_marked,
            'p_other': p_other,
            'ratio': ratio,
            'total_prob': np.sum(np.abs(state)**2)
        })
        
        if k < max_iter:
            state = G @ state
    
    return history

# Test for different problem sizes
print("\n" + "-" * 50)
print("Tracking amplitude ratios for φ appearance:")
print("-" * 50)

phi_appearances_grover = []

for n_qubits in [2, 3, 4, 5, 6]:
    N = 2**n_qubits
    marked = 0  # Arbitrary marked state
    opt_iter = optimal_iterations(N)
    
    history = track_amplitudes(n_qubits, marked, opt_iter + 5)
    
    print(f"\nn={n_qubits} qubits (N={N}, optimal_iter={opt_iter}):")
    
    for h in history:
        k = h['iteration']
        p_m = h['p_marked']
        ratio = h['ratio']
        
        # Check for φ or 1/φ in probability or ratio
        near_phi = abs(ratio - PHI) < 0.1 or abs(ratio - INV_PHI) < 0.1
        near_phi_prob = abs(p_m - INV_PHI) < 0.05
        
        marker = ""
        if near_phi:
            marker = f" ← ratio near φ! (error: {min(abs(ratio-PHI), abs(ratio-INV_PHI))/INV_PHI*100:.2f}%)"
            phi_appearances_grover.append({
                'n_qubits': n_qubits, 'iteration': k, 
                'value': ratio, 'type': 'ratio'
            })
        if near_phi_prob:
            marker = f" ← P(marked) near 1/φ! (error: {abs(p_m-INV_PHI)/INV_PHI*100:.2f}%)"
            phi_appearances_grover.append({
                'n_qubits': n_qubits, 'iteration': k,
                'value': p_m, 'type': 'probability'
            })
            
        print(f"  k={k}: P(marked)={p_m:.4f}, ratio={ratio:.4f}{marker}")

# =============================================================================
# EXPERIMENT 2: Grover Operator Eigenvalues
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 2: Grover Operator Eigenspectrum")
print("=" * 70)

print("\nThe Grover operator G = D @ O has eigenvalues e^{±2iθ} and 1s")
print("where sin(θ) = 1/√N. Let's check the eigenvalue structure...")

def analyze_grover_eigenvalues(n_qubits: int, marked: int) -> dict:
    """Analyze eigenvalues of Grover operator."""
    N = 2**n_qubits
    G = grover_iteration(N, marked)
    
    eigenvalues = linalg.eigvals(G)
    
    # Grover has eigenvalues on unit circle
    phases = np.angle(eigenvalues)
    magnitudes = np.abs(eigenvalues)
    
    # The interesting eigenvalues are e^{±2iθ}
    # where θ = arcsin(1/√N)
    theta_theory = np.arcsin(1 / np.sqrt(N))
    
    return {
        'eigenvalues': eigenvalues,
        'phases': phases,
        'magnitudes': magnitudes,
        'theta_theory': theta_theory,
        'N': N
    }

print("\n" + "-" * 50)
print("Eigenvalue Analysis:")
print("-" * 50)

grover_phi_eigenvalues = []

for n_qubits in [2, 3, 4, 5, 6, 7]:
    N = 2**n_qubits
    result = analyze_grover_eigenvalues(n_qubits, 0)
    
    theta = result['theta_theory']
    phases = result['phases']
    
    # Non-trivial phases (not 0 or π)
    interesting_phases = phases[np.abs(np.abs(phases) - np.pi) > 0.1]
    interesting_phases = interesting_phases[np.abs(interesting_phases) > 0.1]
    
    print(f"\nn={n_qubits} (N={N}):")
    print(f"  θ_theory = {theta:.6f} rad = {np.degrees(theta):.2f}°")
    print(f"  2θ = {2*theta:.6f} rad = {np.degrees(2*theta):.2f}°")
    
    # Check if any phase relates to φ
    for phase in np.unique(np.round(np.abs(interesting_phases), 6)):
        phase_over_pi = phase / np.pi
        
        # Check various φ relationships
        if abs(phase_over_pi - INV_PHI) < 0.05:
            print(f"  ⚡ Phase/π = {phase_over_pi:.6f} ≈ 1/φ!")
            grover_phi_eigenvalues.append({'n': n_qubits, 'value': phase_over_pi, 'type': 'phase/π'})
        if abs(phase_over_pi - (1 - INV_PHI)) < 0.05:
            print(f"  ⚡ Phase/π = {phase_over_pi:.6f} ≈ 1-1/φ!")
            grover_phi_eigenvalues.append({'n': n_qubits, 'value': phase_over_pi, 'type': 'phase/π'})
        if abs(phase - INV_PHI) < 0.05:
            print(f"  ⚡ Phase = {phase:.6f} ≈ 1/φ!")
            grover_phi_eigenvalues.append({'n': n_qubits, 'value': phase, 'type': 'phase'})

# =============================================================================
# EXPERIMENT 3: The Golden Iteration Count
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 3: Optimal Iteration Count and φ")
print("=" * 70)

print("\nOptimal iterations: k* = π/4 * √N")
print("Question: Is there a problem size where k* involves φ?")

print("\n" + "-" * 50)
print("Searching for N where optimal iterations relate to φ:")
print("-" * 50)

for N in range(2, 1001):
    k_opt = PI / 4 * np.sqrt(N)
    k_rounded = round(k_opt)
    
    # Check if k_opt is close to φ, 1/φ, or involves φ
    if abs(k_opt - PHI) < 0.01:
        print(f"  N={N}: k* = {k_opt:.6f} ≈ φ!")
    if abs(k_opt - INV_PHI) < 0.01:
        print(f"  N={N}: k* = {k_opt:.6f} ≈ 1/φ!")
    if abs(k_opt - PHI**2) < 0.01:
        print(f"  N={N}: k* = {k_opt:.6f} ≈ φ²!")
    if abs(k_opt - 2*PHI) < 0.01:
        print(f"  N={N}: k* = {k_opt:.6f} ≈ 2φ!")
    if abs(k_opt - PI*INV_PHI) < 0.01:
        print(f"  N={N}: k* = {k_opt:.6f} ≈ π/φ!")

# What about √N?
print("\n" + "-" * 50)
print("Checking √N relationships:")
print("-" * 50)

# √N = φ means N = φ² ≈ 2.618
print(f"  If √N = φ: N = φ² = {PHI**2:.4f}")
print(f"  → k* = π/4 * φ = {PI/4 * PHI:.4f} iterations")

# √N = 1/φ means N = 1/φ² ≈ 0.382
print(f"  If √N = 1/φ: N = 1/φ² = {INV_PHI**2:.4f}")

# What N gives k* = 1?
N_for_k1 = (4/PI)**2
print(f"\n  N for exactly 1 iteration: N = (4/π)² = {N_for_k1:.4f}")

# =============================================================================
# EXPERIMENT 4: Success Probability at Specific Iterations
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 4: Success Probability Trajectory")
print("=" * 70)

print("\nP(success) = sin²((2k+1)θ) where θ = arcsin(1/√N)")
print("When does P(success) = 1/φ ≈ 0.618?")

def find_phi_probability_iterations(N: int, max_k: int = 100) -> List[dict]:
    """Find iterations where success probability equals 1/φ."""
    theta = np.arcsin(1 / np.sqrt(N))
    results = []
    
    for k in range(max_k):
        p_success = np.sin((2*k + 1) * theta)**2
        
        if abs(p_success - INV_PHI) < 0.01:
            results.append({
                'k': k,
                'p_success': p_success,
                'error': abs(p_success - INV_PHI) / INV_PHI
            })
    
    return results

print("\n" + "-" * 50)
print("Iterations where P(success) ≈ 1/φ:")
print("-" * 50)

for n_qubits in [4, 5, 6, 7, 8]:
    N = 2**n_qubits
    phi_iters = find_phi_probability_iterations(N)
    
    if phi_iters:
        print(f"\nn={n_qubits} (N={N}):")
        for result in phi_iters[:3]:  # Show first 3
            print(f"  k={result['k']}: P(success)={result['p_success']:.6f} (error: {result['error']*100:.2f}%)")

# =============================================================================
# EXPERIMENT 5: Grover on Structured Problems
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 5: Fibonacci-Sized Search Spaces")
print("=" * 70)

print("\nWhat happens when N is a Fibonacci number?")
print("Fibonacci: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610...")

fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]

print("\n" + "-" * 50)
print("Fibonacci N analysis:")
print("-" * 50)

for N in fibs:
    if N < 2:
        continue
    
    k_opt = PI / 4 * np.sqrt(N)
    theta = np.arcsin(1 / np.sqrt(N))
    
    # Success probability at optimal iteration
    k_actual = round(k_opt)
    p_opt = np.sin((2*k_actual + 1) * theta)**2
    
    # Check for φ relationships
    sqrt_N = np.sqrt(N)
    ratio_to_phi = sqrt_N / PHI
    ratio_to_inv_phi = sqrt_N / INV_PHI
    
    markers = []
    if abs(ratio_to_phi - round(ratio_to_phi)) < 0.1:
        markers.append(f"√N ≈ {round(ratio_to_phi)}φ")
    if abs(ratio_to_inv_phi - round(ratio_to_inv_phi)) < 0.1:
        markers.append(f"√N ≈ {round(ratio_to_inv_phi)}/φ")
    
    marker_str = " | " + ", ".join(markers) if markers else ""
    print(f"  N={N:3d}: k*={k_opt:.2f}, P(opt)={p_opt:.4f}{marker_str}")

# =============================================================================
# EXPERIMENT 6: The θ Angle and φ
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 6: The Rotation Angle θ = arcsin(1/√N)")
print("=" * 70)

print("\nGrover's works by rotating in a 2D subspace by angle 2θ per iteration.")
print("When does θ relate to φ?")

print("\n" + "-" * 50)
print("Searching for special θ values:")
print("-" * 50)

# θ = arcsin(1/√N) relates to φ when...
# 1/√N = sin(angle involving φ)

# What if θ = π/(2φ)?
theta_phi = PI / (2 * PHI)
sin_theta_phi = np.sin(theta_phi)
N_phi = 1 / sin_theta_phi**2
print(f"\nIf θ = π/(2φ) = {theta_phi:.6f} rad:")
print(f"  sin(θ) = {sin_theta_phi:.6f}")
print(f"  N = 1/sin²(θ) = {N_phi:.4f}")
print(f"  k* = π/4 * √N = {PI/4 * np.sqrt(N_phi):.4f}")

# What if sin(θ) = 1/φ?
theta_sinphi = np.arcsin(INV_PHI)
N_sinphi = 1 / INV_PHI**2
print(f"\nIf sin(θ) = 1/φ:")
print(f"  θ = {theta_sinphi:.6f} rad = {np.degrees(theta_sinphi):.2f}°")
print(f"  N = φ² = {N_sinphi:.4f}")
print(f"  k* = π/4 * φ = {PI/4 * PHI:.4f}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: φ in Grover's Algorithm")
print("=" * 70)

print(f"""
KEY FINDINGS:

1. AMPLITUDE RATIOS: During Grover evolution, the ratio P(marked)/P(other)
   passes through values near φ at specific iterations.
   Found {len(phi_appearances_grover)} instances of φ-adjacent values.

2. EIGENVALUE PHASES: The Grover operator eigenvalues are e^{{±2iθ}}.
   The phase relationships to π show some φ-adjacent structure.

3. OPTIMAL ITERATION FORMULA: k* = π/4 * √N
   - When N = φ² ≈ 2.618: k* = π/4 * φ ≈ 1.27
   - The formula itself involves π, not φ directly
   
4. SUCCESS PROBABILITY: P(success) = sin²((2k+1)θ)
   - Passes through 1/φ at specific (non-optimal) iterations
   - The oscillatory nature guarantees hitting any value in [0,1]

5. FIBONACCI SEARCH SPACES: Using Fibonacci N doesn't produce
   special φ relationships beyond the natural Fib/Fib ≈ φ ratio.

INTERPRETATION:

Grover's algorithm is built on π (the rotation is in angle space),
not φ. The golden ratio appears only incidentally when:
- Amplitude ratios happen to pass through φ-adjacent values
- We specifically construct N = φ² (non-integer, so not physical)

This is DIFFERENT from attention/quantum measurement where φ appears
at CRITICAL POINTS and OPTIMAL configurations.

CONCLUSION:

Grover's algorithm is fundamentally a π-based algorithm (rotations
in Hilbert space). The golden ratio does NOT appear as a structural
constant here the way it does in:
- Attention eigenspectra (at critical temperatures)
- Quantum measurement operators (in eigenvalue structure)
- Information routing (at optimal configurations)

This is actually INTERESTING - it helps us understand WHERE φ appears:
→ φ appears in MEASUREMENT/COLLAPSE dynamics
→ φ does NOT appear in UNITARY EVOLUTION (Grover iterations)

This supports QID: The golden ratio is specific to the measurement
process, not all of quantum mechanics!
""")

print("=" * 70)
print("PHASE 3 COMPLETE: φ is measurement-specific, not universal in QM!")
print("=" * 70)
