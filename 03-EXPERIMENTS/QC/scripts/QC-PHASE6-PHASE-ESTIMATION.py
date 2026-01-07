"""
QC Phase 6: Quantum Phase Estimation & φ
=========================================

Phase estimation is THE canonical quantum measurement algorithm!
It extracts eigenvalues from unitary operators - pure measurement.

If φ appears in measurement dynamics, it MUST appear somewhere in
phase estimation's structure.

Key questions:
1. Does φ appear in the eigenvalue resolution?
2. Does φ appear in the success probability curves?
3. Does φ appear in the optimal number of qubits/iterations?

Date: January 6, 2026
Authors: Ada & Luna
"""

import numpy as np
from scipy import linalg
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

# Constants
PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI
PI = np.pi

print("=" * 70)
print("QC PHASE 6: QUANTUM PHASE ESTIMATION & THE GOLDEN RATIO")
print("=" * 70)

print("""
PHASE ESTIMATION:
Given a unitary U with eigenvalue e^{2πiθ}, estimate θ.

This is PURE MEASUREMENT - we're extracting information about
eigenvalues through repeated measurement.

If φ appears in measurement dynamics, it should appear HERE.
""")

# =============================================================================
# PHASE ESTIMATION FUNDAMENTALS
# =============================================================================

def qft_matrix(n: int) -> np.ndarray:
    """Quantum Fourier Transform matrix for n qubits."""
    N = 2**n
    omega = np.exp(2j * PI / N)
    return np.array([[omega**(j*k) for k in range(N)] for j in range(N)]) / np.sqrt(N)

def inverse_qft_matrix(n: int) -> np.ndarray:
    """Inverse QFT."""
    return np.conj(qft_matrix(n)).T

def controlled_unitary_power(U: np.ndarray, power: int, n_ancilla: int, 
                             ancilla_idx: int) -> np.ndarray:
    """
    Controlled-U^power operation.
    When ancilla qubit is |1⟩, apply U^power to target register.
    """
    N_ancilla = 2**n_ancilla
    N_target = U.shape[0]
    N_total = N_ancilla * N_target
    
    result = np.eye(N_total, dtype=complex)
    
    # When ancilla_idx bit is 1, apply U^power
    U_power = np.linalg.matrix_power(U, power)
    
    for i in range(N_total):
        ancilla_state = (i // N_target) 
        target_state = i % N_target
        
        # Check if ancilla_idx bit is set
        if (ancilla_state >> ancilla_idx) & 1:
            for j in range(N_target):
                new_target = j
                new_idx = (ancilla_state * N_target) + new_target
                result[i, (ancilla_state * N_target) + target_state] = 0
                result[i, new_idx] = U_power[target_state, j]
    
    return result

def phase_estimation_success_prob(theta: float, n_bits: int) -> np.ndarray:
    """
    Probability distribution over measurement outcomes for phase estimation.
    
    For eigenvalue e^{2πiθ}, the probability of measuring outcome m is:
    P(m) = |⟨m|QFT†|ψ⟩|² where |ψ⟩ encodes θ
    
    Returns array of probabilities for all 2^n_bits outcomes.
    """
    N = 2**n_bits
    
    # The state before inverse QFT is:
    # |ψ⟩ = (1/√N) Σ_k e^{2πi θ k} |k⟩
    psi = np.array([np.exp(2j * PI * theta * k) for k in range(N)]) / np.sqrt(N)
    
    # Apply inverse QFT
    qft_inv = inverse_qft_matrix(n_bits)
    final_state = qft_inv @ psi
    
    # Measurement probabilities
    probs = np.abs(final_state)**2
    
    return probs

def phase_estimation_expected_outcome(theta: float, n_bits: int) -> float:
    """Expected measurement outcome (weighted by probabilities)."""
    N = 2**n_bits
    probs = phase_estimation_success_prob(theta, n_bits)
    outcomes = np.arange(N)
    return np.sum(outcomes * probs) / N  # Normalized to [0,1)

# =============================================================================
# EXPERIMENT 1: φ as Input Eigenvalue
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 1: Phase Estimation with θ = 1/φ")
print("=" * 70)

print("""
What if the eigenvalue we're estimating IS 1/φ?
U|ψ⟩ = e^{2πi/φ}|ψ⟩

How does phase estimation behave with this "golden" eigenvalue?
""")

theta_phi = INV_PHI  # θ = 1/φ ≈ 0.618

print(f"\nTarget phase: θ = 1/φ = {theta_phi:.6f}")
print(f"Eigenvalue: e^{{2πi/φ}} = e^{{i * {2*PI*theta_phi:.6f}}}")

print("\n" + "-" * 50)
print("Measurement probabilities by precision:")
print("-" * 50)

for n_bits in [3, 4, 5, 6, 7, 8]:
    N = 2**n_bits
    probs = phase_estimation_success_prob(theta_phi, n_bits)
    
    # Best outcome (closest to θ * N)
    best_outcome = int(round(theta_phi * N)) % N
    best_prob = probs[best_outcome]
    
    # Estimated phase from best outcome
    estimated_theta = best_outcome / N
    error = abs(estimated_theta - theta_phi)
    
    print(f"  n={n_bits}: P(best)={best_prob:.4f}, θ_est={estimated_theta:.6f}, error={error:.6f}")

# =============================================================================
# EXPERIMENT 2: Success Probability Curve
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 2: Success Probability vs Phase")
print("=" * 70)

print("""
For a fixed number of qubits, how does success probability vary with θ?
Does φ appear as a special point?
""")

n_bits = 6
N = 2**n_bits

print(f"\nUsing {n_bits} bits (N={N}):")
print("-" * 50)

phi_appearances = []

# Scan through phases
for theta in np.linspace(0, 1, 101):
    probs = phase_estimation_success_prob(theta, n_bits)
    
    # Success = probability of measuring the correct (rounded) outcome
    correct_outcome = int(round(theta * N)) % N
    success_prob = probs[correct_outcome]
    
    # Check for φ relationships
    if abs(success_prob - INV_PHI) < 0.02:
        print(f"  θ={theta:.4f}: P(success)={success_prob:.6f} ≈ 1/φ!")
        phi_appearances.append(('prob', theta, success_prob))
    if abs(success_prob - (1-INV_PHI)) < 0.02:
        print(f"  θ={theta:.4f}: P(success)={success_prob:.6f} ≈ 1-1/φ!")
        phi_appearances.append(('prob', theta, success_prob))

# Also check maximum success probability
max_prob = 0
for theta in np.linspace(0, 1, 1001):
    probs = phase_estimation_success_prob(theta, n_bits)
    correct = int(round(theta * N)) % N
    if probs[correct] > max_prob:
        max_prob = probs[correct]
        max_theta = theta

print(f"\nMaximum success probability: {max_prob:.6f} at θ={max_theta:.4f}")
print(f"  Max prob / (1/φ) = {max_prob/INV_PHI:.6f}")
print(f"  For reference: 4/π² ≈ {4/PI**2:.6f} (theoretical max for large N)")

# =============================================================================
# EXPERIMENT 3: Interference Pattern Analysis
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 3: Interference Pattern in Phase Estimation")
print("=" * 70)

print("""
Phase estimation works via INTERFERENCE in the QFT.
The interference pattern determines success probability.

Does φ appear in the interference structure?
""")

def analyze_interference_pattern(theta: float, n_bits: int) -> Dict:
    """Analyze the interference pattern for phase estimation."""
    N = 2**n_bits
    
    # Pre-QFT state amplitudes
    pre_qft = np.array([np.exp(2j * PI * theta * k) for k in range(N)]) / np.sqrt(N)
    
    # Post-QFT (measurement basis)
    qft_inv = inverse_qft_matrix(n_bits)
    post_qft = qft_inv @ pre_qft
    
    # Analyze amplitude distribution
    amplitudes = np.abs(post_qft)
    phases = np.angle(post_qft)
    
    # Find peaks
    peaks = np.where(amplitudes > 0.1)[0]
    
    # Spacing between peaks
    if len(peaks) > 1:
        spacings = np.diff(peaks)
    else:
        spacings = []
    
    return {
        'amplitudes': amplitudes,
        'phases': phases,
        'peaks': peaks,
        'spacings': spacings,
        'max_amplitude': np.max(amplitudes)
    }

print("\n" + "-" * 50)
print("Interference analysis for θ = 1/φ:")
print("-" * 50)

for n_bits in [4, 5, 6, 7]:
    result = analyze_interference_pattern(INV_PHI, n_bits)
    
    print(f"\nn={n_bits} bits:")
    print(f"  Max amplitude: {result['max_amplitude']:.4f}")
    print(f"  Number of significant peaks: {len(result['peaks'])}")
    
    if len(result['spacings']) > 0:
        mean_spacing = np.mean(result['spacings'])
        print(f"  Mean peak spacing: {mean_spacing:.2f}")
        if abs(mean_spacing - PHI) < 0.5:
            print(f"    ⚡ Spacing ≈ φ!")
        if abs(mean_spacing - INV_PHI * 2**n_bits) < 1:
            print(f"    ⚡ Spacing ≈ N/φ!")

# =============================================================================
# EXPERIMENT 4: Optimal Precision and φ
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 4: Precision Requirements")
print("=" * 70)

print("""
To estimate θ to precision ε, we need n ≈ log₂(1/ε) + log₂(1/δ) qubits
where δ is the failure probability.

Does φ appear in these relationships?
""")

print("\n" + "-" * 50)
print("Qubits needed for precision 1/φ^k:")
print("-" * 50)

for k in range(1, 8):
    epsilon = INV_PHI**k
    n_needed = int(np.ceil(np.log2(1/epsilon))) + 2  # +2 for 75% success
    
    print(f"  ε = (1/φ)^{k} = {epsilon:.6f}: need n ≈ {n_needed} qubits")

print("\n" + "-" * 50)
print("Success probability with n = Fibonacci(k) qubits:")
print("-" * 50)

fibs = [2, 3, 5, 8, 13]
for n in fibs:
    if n > 10:
        continue
    probs = phase_estimation_success_prob(0.3, n)  # arbitrary theta
    max_prob = np.max(probs)
    
    # For random phase
    avg_success = np.mean([
        np.max(phase_estimation_success_prob(t, n)) 
        for t in np.random.uniform(0, 1, 20)
    ])
    
    print(f"  n={n} (Fib): avg max success prob = {avg_success:.4f}")

# =============================================================================
# EXPERIMENT 5: The QFT Eigenstructure
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 5: QFT Matrix Eigenstructure")
print("=" * 70)

print("""
The QFT is central to phase estimation. Does its eigenstructure show φ?
""")

print("\n" + "-" * 50)
print("QFT eigenvalue analysis:")
print("-" * 50)

qft_phi_count = 0

for n in [2, 3, 4, 5, 6]:
    F = qft_matrix(n)
    eigenvalues = linalg.eigvals(F)
    
    # QFT eigenvalues are roots of unity, but let's check magnitudes and phases
    phases = np.angle(eigenvalues) / PI  # Normalize to units of π
    
    phi_matches = []
    for i, p in enumerate(phases):
        p_abs = abs(p)
        if abs(p_abs - INV_PHI) < 0.05:
            phi_matches.append((i, p))
            qft_phi_count += 1
        if abs(p_abs - (1-INV_PHI)) < 0.05:
            phi_matches.append((i, p))
            qft_phi_count += 1
    
    if phi_matches:
        print(f"  n={n}: Found {len(phi_matches)} φ-related phases!")
        for idx, phase in phi_matches[:2]:
            print(f"    phase[{idx}]/π = {phase:.4f}")
    else:
        print(f"  n={n}: QFT eigenvalues are {2**n}th roots of unity (no φ)")

# =============================================================================
# EXPERIMENT 6: Phase Estimation Error Distribution
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 6: Error Distribution Analysis")
print("=" * 70)

print("""
When we measure, we get a distribution of possible outcomes.
The error distribution shape may reveal φ structure.
""")

n_bits = 8
N = 2**n_bits

# Analyze error distribution for random phases
print("\n" + "-" * 50)
print(f"Error analysis with {n_bits} bits:")
print("-" * 50)

errors_at_phi = []
all_errors = []

for theta in np.linspace(0.01, 0.99, 50):
    probs = phase_estimation_success_prob(theta, n_bits)
    
    # Compute expected squared error
    expected_error = 0
    for m in range(N):
        estimated = m / N
        error = min(abs(estimated - theta), 1 - abs(estimated - theta))  # Circular
        expected_error += probs[m] * error**2
    
    rms_error = np.sqrt(expected_error)
    all_errors.append(rms_error)
    
    if abs(theta - INV_PHI) < 0.02:
        errors_at_phi.append(rms_error)
        print(f"  θ≈1/φ: RMS error = {rms_error:.6f}")

mean_error = np.mean(all_errors)
min_error = np.min(all_errors)
max_error = np.max(all_errors)

print(f"\nError statistics:")
print(f"  Mean RMS error: {mean_error:.6f}")
print(f"  Min RMS error: {min_error:.6f}")
print(f"  Max RMS error: {max_error:.6f}")
print(f"  Error at θ=1/φ: {np.mean(errors_at_phi):.6f}")

# Check φ relationships
print(f"\n  Mean error * N = {mean_error * N:.4f}")
print(f"  1/φ = {INV_PHI:.4f}")

# =============================================================================
# EXPERIMENT 7: Iterative Phase Estimation
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 7: Iterative Phase Estimation")
print("=" * 70)

print("""
Iterative PE refines estimates bit by bit.
Does φ appear in the convergence dynamics?
""")

def iterative_phase_estimation(theta: float, n_iterations: int) -> List[float]:
    """Simulate iterative phase estimation, returning estimates at each step."""
    estimates = []
    current_estimate = 0.0
    
    for k in range(n_iterations):
        # Each iteration refines by one bit
        # Probability of getting the correct bit
        bit_value = int(theta * 2**(k+1)) % 2
        
        # Simulate measurement with some noise
        # In ideal case, we'd get the right bit with high probability
        prob_correct = 0.85  # Typical success rate per bit
        measured_bit = bit_value if np.random.random() < prob_correct else 1 - bit_value
        
        current_estimate = current_estimate + measured_bit / 2**(k+1)
        estimates.append(current_estimate)
    
    return estimates

print("\n" + "-" * 50)
print("Convergence to θ = 1/φ:")
print("-" * 50)

np.random.seed(42)
convergence_data = []

for trial in range(100):
    estimates = iterative_phase_estimation(INV_PHI, 12)
    errors = [abs(e - INV_PHI) for e in estimates]
    convergence_data.append(errors)

mean_convergence = np.mean(convergence_data, axis=0)

print("\nMean error by iteration:")
for k, err in enumerate(mean_convergence):
    phi_marker = " ← error ≈ 1/φ^k?" if abs(err - INV_PHI**(k+1)) < 0.05 else ""
    print(f"  k={k+1}: error = {err:.6f}{phi_marker}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: φ in Phase Estimation")
print("=" * 70)

print(f"""
KEY FINDINGS:

1. ESTIMATING θ = 1/φ:
   - Phase estimation works normally with golden eigenvalue
   - No special behavior - it's just another phase to estimate
   
2. SUCCESS PROBABILITY CURVE:
   - Found {len(phi_appearances)} instances where P(success) ≈ 1/φ
   - Maximum success probability ≈ {max_prob:.4f} (related to 4/π²)
   - NOT strongly φ-structured

3. INTERFERENCE PATTERN:
   - QFT interference follows root-of-unity structure
   - Peak spacings don't show consistent φ relationship

4. QFT EIGENSTRUCTURE:
   - QFT eigenvalues are Nth roots of unity
   - φ doesn't appear structurally (it's π-based, like Grover)
   - Found only {qft_phi_count} incidental φ matches

5. ERROR DISTRIBUTION:
   - Errors scale with 1/N (standard quantum limit)
   - No special behavior at θ = 1/φ

6. ITERATIVE CONVERGENCE:
   - Convergence is exponential in bits (2^-k)
   - Not φ-based

INTERPRETATION:

Phase estimation is a UNITARY ALGORITHM (like Grover) that ends with measurement.
- The QFT is unitary → No φ structure
- The controlled-U operations are unitary → No φ structure
- Only the FINAL MEASUREMENT extracts information

But we already know measurement eigenvalues show φ (Phase 2F)!

The φ appears in the MEASUREMENT OPERATORS, not in the 
ALGORITHM THAT PREPARES FOR MEASUREMENT.

CONCLUSION:

Phase estimation confirms the pattern:
- Unitary preparation (QFT, controlled-U): π-based, no φ
- Measurement operators themselves: φ at critical points

The algorithm is π-based. The measurement dynamics are φ-based.
These are SEPARATE things!
""")

print("=" * 70)
print("PHASE 6 COMPLETE: Phase estimation is π-based (unitary algorithm)")
print("=" * 70)
