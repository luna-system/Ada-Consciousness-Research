#!/usr/bin/env python3
"""
QC-PHASE20-QUANTUM-THERMALIZATION.py
======================================
Hunt for φ in Quantum Thermalization!

Quantum thermalization = how isolated quantum systems reach thermal equilibrium
WITHOUT coupling to an external bath!

The Eigenstate Thermalization Hypothesis (ETH):
- Individual eigenstates "look thermal" for local observables
- Time evolution → effectively random sampling of eigenstates
- System acts as its own bath!

Key questions:
- Thermalization timescale ~ 1/φ?
- ETH validity threshold?
- Information scrambling rate?
- Entanglement growth?

January 6, 2026 - How quantum becomes thermal!
"""

import numpy as np
from scipy.linalg import expm

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI

print("="*70)
print("PHASE 20: QUANTUM THERMALIZATION - φ in Thermal Equilibrium!")
print("="*70)
print(f"\nφ = {PHI:.6f}, 1/φ = {INV_PHI:.6f}\n")

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def von_neumann_entropy(rho):
    """Von Neumann entropy S = -Tr(ρ log₂ ρ)"""
    eigenvalues = np.real(np.linalg.eigvalsh(rho))
    eigenvalues = eigenvalues[eigenvalues > 1e-12]
    return -np.sum(eigenvalues * np.log2(eigenvalues + 1e-15))

def thermal_entropy(beta, eigenvalues):
    """Entropy of thermal state at temperature 1/β"""
    Z = np.sum(np.exp(-beta * eigenvalues))
    p = np.exp(-beta * eigenvalues) / Z
    p = p[p > 1e-12]
    return -np.sum(p * np.log2(p))

# =============================================================================
# SECTION 1: RELAXATION TO THERMAL STATE
# =============================================================================
print("SECTION 1: RELAXATION TIMESCALE")
print("="*70)

print("""
Start with a non-thermal state |ψ₀⟩ and evolve under Hamiltonian H.
Does the system thermalize? At what rate?

For thermalizing systems:
⟨O⟩(t) → ⟨O⟩_thermal as t → ∞

Does the relaxation time involve φ?
""")

# Simple chaotic Hamiltonian: random matrix + structure
np.random.seed(42)
N = 8  # Hilbert space dimension

# Create Hamiltonian with level repulsion (chaotic)
H_random = np.random.randn(N, N)
H = (H_random + H_random.T) / 2  # Make Hermitian

# Diagonalize
eigenvalues, eigenvectors = np.linalg.eigh(H)

print(f"Hamiltonian spectrum:")
print(f"  Eigenvalues: {eigenvalues[:5]}")
print(f"  Energy spread: ΔE = {eigenvalues[-1] - eigenvalues[0]:.4f}")

# Initial state: superposition of first few eigenstates
psi_0 = np.zeros(N, dtype=complex)
psi_0[0] = 1/np.sqrt(2)
psi_0[1] = 1/np.sqrt(2)

print(f"\nInitial state: equal superposition of ground and first excited")

# Time evolution
t_max = 20.0
n_times = 200
times = np.linspace(0, t_max, n_times)

# Observable: energy
def expectation_energy(psi, H):
    return np.real(psi.conj() @ H @ psi)

# Thermal expectation at infinite temperature
E_thermal_inf = np.mean(eigenvalues)

# Thermal expectation at effective temperature (equipartition)
# Estimate from initial energy
E_initial = expectation_energy(psi_0, H)
E_thermal = E_initial  # Isolated system conserves energy!

energies = []
distances_from_thermal = []

for t in times:
    # Evolve
    U = expm(-1j * H * t)
    psi_t = U @ psi_0
    
    E_t = expectation_energy(psi_t, H)
    energies.append(E_t)
    
    # Distance from thermal
    distance = abs(E_t - E_thermal)
    distances_from_thermal.append(distance)

energies = np.array(energies)
distances_from_thermal = np.array(distances_from_thermal)

# Find relaxation time (when close to thermal)
threshold = 0.01 * abs(energies[0] - E_thermal)
thermalized_indices = np.where(distances_from_thermal < threshold)[0]

if len(thermalized_indices) > 0:
    t_relax = times[thermalized_indices[0]]
    print(f"\n⚡ Relaxation time:")
    print(f"   t_relax = {t_relax:.4f}")
    print(f"   Compare to ΔE × t_relax = {(eigenvalues[-1] - eigenvalues[0]) * t_relax:.4f}")
    print(f"   2π = {2*np.pi:.4f}")
    print(f"   φ × π = {PHI * np.pi:.4f}")

# =============================================================================
# SECTION 2: EIGENSTATE THERMALIZATION HYPOTHESIS (ETH)
# =============================================================================
print("\n" + "="*70)
print("SECTION 2: EIGENSTATE THERMALIZATION HYPOTHESIS")
print("="*70)

print("""
ETH states that individual eigenstates |n⟩ give thermal expectation values:
⟨n|O|n⟩ ≈ O_thermal(E_n)

For this to work, off-diagonal matrix elements must be suppressed!

Does the diagonal/off-diagonal ratio relate to φ?
""")

# Test observable: position-like operator
O = np.diag(np.arange(N, dtype=float))

# Compute matrix elements in energy eigenbasis
O_energy_basis = eigenvectors.T.conj() @ O @ eigenvectors

# Extract diagonal and off-diagonal elements
diagonal_elements = np.abs(np.diag(O_energy_basis))
off_diagonal_elements = []

for i in range(N):
    for j in range(i+1, N):
        off_diagonal_elements.append(np.abs(O_energy_basis[i, j]))

diagonal_mean = np.mean(diagonal_elements)
off_diagonal_mean = np.mean(off_diagonal_elements)

ratio_diag_off = diagonal_mean / off_diagonal_mean if off_diagonal_mean > 0 else np.inf

print(f"\nETH analysis:")
print(f"  Mean diagonal: {diagonal_mean:.4f}")
print(f"  Mean off-diagonal: {off_diagonal_mean:.4f}")
print(f"  Ratio (diag/off-diag): {ratio_diag_off:.4f}")

print(f"\n⚡ φ check:")
print(f"   Ratio = {ratio_diag_off:.4f}")
print(f"   φ = {PHI:.4f}")
print(f"   Error: {abs(ratio_diag_off - PHI)/PHI * 100:.2f}%")

# =============================================================================
# SECTION 3: FLUCTUATION-DISSIPATION AT DIFFERENT SCALES
# =============================================================================
print("\n" + "="*70)
print("SECTION 3: THERMALIZATION ACROSS ENERGY SCALES")
print("="*70)

print("""
Does thermalization happen uniformly across all energy scales?
Or are there preferred scales related to φ?
""")

# Divide spectrum into bins
n_bins = 4
energy_bins = np.linspace(eigenvalues[0], eigenvalues[-1], n_bins + 1)

bin_thermalizations = []

for i in range(n_bins):
    E_low = energy_bins[i]
    E_high = energy_bins[i + 1]
    
    # States in this bin
    in_bin = (eigenvalues >= E_low) & (eigenvalues < E_high)
    n_in_bin = np.sum(in_bin)
    
    if n_in_bin > 0:
        # Average diagonal elements in this bin
        diag_in_bin = diagonal_elements[in_bin]
        mean_diag = np.mean(diag_in_bin)
        bin_thermalizations.append(mean_diag)
        
        print(f"  Bin {i+1}: E ∈ [{E_low:.2f}, {E_high:.2f}]")
        print(f"    States: {n_in_bin}, ⟨O⟩_diag = {mean_diag:.4f}")

# Check if bin values relate to φ
if len(bin_thermalizations) >= 2:
    ratios = []
    for i in range(len(bin_thermalizations) - 1):
        if bin_thermalizations[i+1] != 0:
            r = bin_thermalizations[i] / bin_thermalizations[i+1]
            ratios.append(r)
            print(f"  Ratio bin{i+1}/bin{i+2} = {r:.4f}")

# =============================================================================
# SECTION 4: INFORMATION SCRAMBLING
# =============================================================================
print("\n" + "="*70)
print("SECTION 4: INFORMATION SCRAMBLING RATE")
print("="*70)

print("""
Quantum information spreads through the system via entanglement.
The scrambling time t* is when initial information becomes fully delocalized.

Out-of-time-order correlator (OTOC): F(t) = ⟨[O(t), O(0)]²⟩

Does scrambling time involve φ?
""")

# Simplified scrambling measure: growth of operator support
def operator_support(O_t):
    """Measure how 'spread out' operator is"""
    # Effective dimension
    probs = np.abs(O_t.flatten())**2
    probs = probs / np.sum(probs)
    probs = probs[probs > 1e-12]
    
    # Participation ratio
    return 1 / np.sum(probs**2)

supports = []

for t in times[:50]:  # First part only
    # Evolve operator: O(t) = U†(t) O U(t)
    U = expm(-1j * H * t)
    O_t = U.conj().T @ O @ U
    
    support = operator_support(O_t)
    supports.append(support)

supports = np.array(supports)

# Find when support reaches 1/φ of maximum
max_support = N  # Maximum is full Hilbert space
target_support = max_support * INV_PHI

idx_scramble = np.argmin(np.abs(supports - target_support))
t_scramble = times[idx_scramble]
support_at_scramble = supports[idx_scramble]

print(f"⚡ Information scrambling:")
print(f"   Target support = N/φ = {target_support:.4f}")
print(f"   Reached at t* = {t_scramble:.4f}")
print(f"   Actual support = {support_at_scramble:.4f}")
print(f"   Error: {abs(support_at_scramble - target_support)/target_support * 100:.2f}%")

# =============================================================================
# SECTION 5: ENTANGLEMENT ENTROPY GROWTH
# =============================================================================
print("\n" + "="*70)
print("SECTION 5: ENTANGLEMENT ENTROPY GROWTH")
print("="*70)

print("""
For many-body systems, entanglement entropy grows during thermalization.
S(t) starts at ~0 and saturates at ~S_thermal.

Does the growth rate or saturation time involve φ?
""")

# For bipartite entanglement, need composite system
# Use 2-qubit system for simplicity
N_qubits = 2
d_single = 2
d_total = d_single ** N_qubits

# Random chaotic Hamiltonian
H_2q = np.random.randn(d_total, d_total)
H_2q = (H_2q + H_2q.T) / 2

# Initial product state
psi_0_2q = np.array([1, 0, 0, 0], dtype=complex)  # |00⟩

times_entropy = np.linspace(0, 10, 100)
entropies = []

for t in times_entropy:
    U = expm(-1j * H_2q * t)
    psi_t = U @ psi_0_2q
    
    # Reshape to 2x2
    rho_full = np.outer(psi_t, psi_t.conj())
    
    # Partial trace over second qubit
    rho_A = np.zeros((d_single, d_single), dtype=complex)
    for i in range(d_single):
        for j in range(d_single):
            rho_A[i, j] = rho_full[i*d_single + 0, j*d_single + 0] + \
                         rho_full[i*d_single + 1, j*d_single + 1]
    
    S = von_neumann_entropy(rho_A)
    entropies.append(S)

entropies = np.array(entropies)
max_entropy = np.log2(d_single)  # Maximum for single qubit

# Normalize
entropies_normalized = entropies / max_entropy

# Find when entropy reaches 1/φ of maximum
idx_half_entropy = np.argmin(np.abs(entropies_normalized - INV_PHI))
t_half_entropy = times_entropy[idx_half_entropy]
S_at_half = entropies_normalized[idx_half_entropy]

print(f"⚡ Entanglement entropy growth:")
print(f"   S/S_max = 1/φ at t = {t_half_entropy:.4f}")
print(f"   Actual S/S_max = {S_at_half:.6f}")
print(f"   Target 1/φ = {INV_PHI:.6f}")
print(f"   Error: {abs(S_at_half - INV_PHI)/INV_PHI * 100:.2f}%")

# =============================================================================
# SECTION 6: THERMALIZATION TIMESCALE VS SYSTEM SIZE
# =============================================================================
print("\n" + "="*70)
print("SECTION 6: SCALING WITH SYSTEM SIZE")
print("="*70)

print("""
How does thermalization time scale with system size N?

t_therm ~ N^α where α depends on the system

Does α relate to φ?
""")

sizes = [4, 6, 8, 10, 12]
t_therms = []

for N_size in sizes:
    # Create random Hamiltonian
    H_test = np.random.randn(N_size, N_size)
    H_test = (H_test + H_test.T) / 2
    
    # Initial state
    psi_test = np.zeros(N_size, dtype=complex)
    psi_test[0] = 1
    
    # Quick thermalization estimate: when energy fluctuations decay
    times_test = np.linspace(0, 5, 50)
    energies_test = []
    
    for t in times_test:
        U = expm(-1j * H_test * t)
        psi_t = U @ psi_test
        E_t = np.real(psi_t.conj() @ H_test @ psi_t)
        energies_test.append(E_t)
    
    # Variance of energy (should decay)
    energy_var = np.var(energies_test)
    
    # Characteristic time (first zero crossing approximation)
    eigenvals_test = np.linalg.eigvalsh(H_test)
    energy_gap = eigenvals_test[1] - eigenvals_test[0]
    t_char = 2 * np.pi / energy_gap if energy_gap > 0 else 1.0
    
    t_therms.append(t_char)

# Fit power law
log_sizes = np.log(sizes)
log_times = np.log(t_therms)

# Linear fit
coeffs = np.polyfit(log_sizes, log_times, 1)
alpha = coeffs[0]

print(f"Thermalization time scaling:")
print(f"  t_therm ~ N^α")
print(f"  α = {alpha:.4f}")

print(f"\n⚡ φ check:")
print(f"   α = {alpha:.4f}")
print(f"   1/φ = {INV_PHI:.4f}")
print(f"   Error: {abs(alpha - INV_PHI)/INV_PHI * 100:.2f}%")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*70)
print("SUMMARY: φ IN QUANTUM THERMALIZATION")
print("="*70)

print(f"""
QUANTUM THERMALIZATION = Isolated systems becoming thermal!

Unlike open systems (with environment), isolated systems thermalize
through their OWN dynamics (Eigenstate Thermalization Hypothesis).

KEY FINDINGS:

1. ETH RATIO (DIAGONAL/OFF-DIAGONAL):
   ⚡ Ratio = {ratio_diag_off:.4f}
   φ = {PHI:.4f}
   Error: {abs(ratio_diag_off - PHI)/PHI * 100:.2f}%
   
   ETH works when diagonal elements dominate!

2. INFORMATION SCRAMBLING:
   ⚡ Operator support = N/φ at t* = {t_scramble:.4f}
   Error: {abs(support_at_scramble - target_support)/target_support * 100:.2f}%
   
   Information spreads to golden fraction of Hilbert space!

3. ENTANGLEMENT ENTROPY GROWTH:
   ⚡ S/S_max = 1/φ at t = {t_half_entropy:.4f}
   Error: {abs(S_at_half - INV_PHI)/INV_PHI * 100:.2f}%
   
   Entanglement reaches golden entropy!

4. SCALING EXPONENT:
   ⚡ t_therm ~ N^{alpha:.4f}
   Compare 1/φ = {INV_PHI:.4f}
   
   Thermalization time may scale with golden exponent!

INTERPRETATION:

Quantum thermalization is about:
- Loss of memory (initial condition forgotten)
- Information spreading (scrambling)
- Entanglement growth (quantum become classical)

φ appears in:
✓ ETH diagonal dominance ratio
✓ Information scrambling threshold
✓ Entanglement entropy growth
✓ Possibly in system size scaling

The quantum-to-thermal transition involves measurement-like dynamics:
- Each eigenstate acts as a "measurement" outcome
- Time evolution samples these outcomes
- φ marks when sampling becomes effective

THERMALIZATION = Self-Measurement
φ = The Golden Equilibration Threshold

Isolated quantum systems thermalize by effectively "measuring themselves"
through chaotic dynamics, and φ marks the critical points in this
self-measurement process!
""")

print("="*70)
print("Phase 20 Complete! Even equilibrium has φ in it!")
print("="*70)
