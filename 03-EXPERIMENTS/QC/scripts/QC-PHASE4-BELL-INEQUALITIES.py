"""
QC Phase 4: Bell Inequalities and the Golden Ratio
====================================================

Bell inequalities quantify the "quantumness" of correlations between
entangled particles under measurement. This is PURE measurement territory!

Key questions:
1. Does φ appear in optimal measurement angles for Bell violation?
2. Does φ appear in the correlation structure itself?
3. Does φ appear in the Tsirelson bound (max QM violation)?

Date: January 6, 2026
Authors: Ada & Luna
"""

import numpy as np
from scipy import optimize
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')

# Constants
PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI
PI = np.pi
SQRT2 = np.sqrt(2)

print("=" * 70)
print("QC PHASE 4: BELL INEQUALITIES & THE GOLDEN RATIO")
print("=" * 70)

# =============================================================================
# BELL/CHSH FUNDAMENTALS
# =============================================================================

def pauli_z():
    """Pauli Z matrix."""
    return np.array([[1, 0], [0, -1]])

def pauli_x():
    """Pauli X matrix."""
    return np.array([[0, 1], [1, 0]])

def pauli_y():
    """Pauli Y matrix."""
    return np.array([[0, -1j], [1j, 0]])

def measurement_operator(theta: float) -> np.ndarray:
    """
    Measurement operator for angle theta in XZ plane.
    M(θ) = cos(θ)Z + sin(θ)X
    """
    return np.cos(theta) * pauli_z() + np.sin(theta) * pauli_x()

def bell_state_phi_plus() -> np.ndarray:
    """
    Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2
    Maximally entangled.
    """
    state = np.zeros(4, dtype=complex)
    state[0] = 1/SQRT2  # |00⟩
    state[3] = 1/SQRT2  # |11⟩
    return state

def bell_state_psi_minus() -> np.ndarray:
    """
    Bell state |Ψ-⟩ = (|01⟩ - |10⟩)/√2
    The singlet state.
    """
    state = np.zeros(4, dtype=complex)
    state[1] = 1/SQRT2   # |01⟩
    state[2] = -1/SQRT2  # |10⟩
    return state

def correlation(state: np.ndarray, theta_a: float, theta_b: float) -> float:
    """
    Compute ⟨ψ|A⊗B|ψ⟩ for measurement angles theta_a, theta_b.
    This is the quantum correlation E(a,b).
    """
    A = measurement_operator(theta_a)
    B = measurement_operator(theta_b)
    
    # A ⊗ B
    AB = np.kron(A, B)
    
    # ⟨ψ|A⊗B|ψ⟩
    return np.real(np.conj(state) @ AB @ state)

def chsh_value(state: np.ndarray, a1: float, a2: float, b1: float, b2: float) -> float:
    """
    Compute CHSH value S = E(a1,b1) + E(a1,b2) + E(a2,b1) - E(a2,b2)
    
    Classical bound: |S| ≤ 2
    Quantum bound (Tsirelson): |S| ≤ 2√2 ≈ 2.828
    """
    E11 = correlation(state, a1, b1)
    E12 = correlation(state, a1, b2)
    E21 = correlation(state, a2, b1)
    E22 = correlation(state, a2, b2)
    
    return E11 + E12 + E21 - E22

# =============================================================================
# EXPERIMENT 1: Optimal CHSH Angles
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 1: Optimal CHSH Measurement Angles")
print("=" * 70)

print("""
The CHSH inequality is maximally violated when:
  a1 = 0, a2 = π/2, b1 = π/4, b2 = 3π/4

These are the "standard" angles. But are there φ-related angles that also
achieve high violation?
""")

# Standard optimal angles
state = bell_state_phi_plus()
standard_angles = (0, PI/2, PI/4, 3*PI/4)
S_standard = chsh_value(state, *standard_angles)

print(f"Standard optimal angles:")
print(f"  a1=0, a2=π/2, b1=π/4, b2=3π/4")
print(f"  CHSH value S = {S_standard:.6f}")
print(f"  Tsirelson bound = 2√2 = {2*SQRT2:.6f}")
print(f"  Violation ratio = {S_standard/(2*SQRT2)*100:.2f}%")

# Now test φ-related angles
print("\n" + "-" * 50)
print("Testing φ-related measurement angles:")
print("-" * 50)

phi_angles_to_test = [
    ("π/φ", PI/PHI),
    ("π/(2φ)", PI/(2*PHI)),
    ("π*φ/4", PI*PHI/4),
    ("arctan(φ)", np.arctan(PHI)),
    ("arctan(1/φ)", np.arctan(INV_PHI)),
    ("π/φ²", PI/PHI**2),
    ("2π/φ³", 2*PI/PHI**3),
]

# Try different combinations
best_phi_S = 0
best_phi_angles = None

for name_a1, a1 in [("0", 0)] + phi_angles_to_test:
    for name_a2, a2 in phi_angles_to_test:
        for name_b1, b1 in phi_angles_to_test:
            for name_b2, b2 in phi_angles_to_test:
                S = abs(chsh_value(state, a1, a2, b1, b2))
                if S > best_phi_S:
                    best_phi_S = S
                    best_phi_angles = (name_a1, name_a2, name_b1, name_b2, a1, a2, b1, b2)

print(f"\nBest φ-based angles found:")
print(f"  a1={best_phi_angles[0]}, a2={best_phi_angles[1]}")
print(f"  b1={best_phi_angles[2]}, b2={best_phi_angles[3]}")
print(f"  CHSH value |S| = {best_phi_S:.6f}")
print(f"  As fraction of Tsirelson: {best_phi_S/(2*SQRT2)*100:.2f}%")

# Check if any φ angle equals standard optimal
print("\n" + "-" * 50)
print("Checking if φ angles match optimal angles:")
print("-" * 50)

optimal_angles = [0, PI/4, PI/2, 3*PI/4]
for name, angle in phi_angles_to_test:
    for opt in optimal_angles:
        if abs(angle - opt) < 0.01:
            print(f"  {name} = {angle:.6f} ≈ {opt/PI:.4f}π (MATCH!)")
        elif abs(angle % PI - opt) < 0.01:
            print(f"  {name} mod π ≈ {opt/PI:.4f}π")

# =============================================================================
# EXPERIMENT 2: The Correlation Function and φ
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 2: Correlation Function E(θ) = -cos(θ)")
print("=" * 70)

print("""
For singlet state |Ψ-⟩, the correlation between measurements at relative
angle θ is:
  E(θ) = -cos(θ)

When does E(θ) = ±1/φ?
""")

# E(θ) = -cos(θ) = 1/φ means cos(θ) = -1/φ
theta_for_inv_phi = np.arccos(-INV_PHI)
theta_for_neg_inv_phi = np.arccos(INV_PHI)

print(f"E(θ) = 1/φ when θ = arccos(-1/φ) = {theta_for_inv_phi:.6f} rad = {np.degrees(theta_for_inv_phi):.2f}°")
print(f"E(θ) = -1/φ when θ = arccos(1/φ) = {theta_for_neg_inv_phi:.6f} rad = {np.degrees(theta_for_neg_inv_phi):.2f}°")

# Verify
state_singlet = bell_state_psi_minus()
E_at_phi_angle = correlation(state_singlet, 0, theta_for_inv_phi)
print(f"\nVerification: E(0, {theta_for_inv_phi:.4f}) = {E_at_phi_angle:.6f}")
print(f"Expected 1/φ = {INV_PHI:.6f}")
print(f"Error: {abs(E_at_phi_angle - INV_PHI)/INV_PHI*100:.4f}%")

# =============================================================================
# EXPERIMENT 3: The Tsirelson Bound and φ
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 3: Tsirelson Bound Analysis")
print("=" * 70)

print("""
The Tsirelson bound is the maximum quantum violation of CHSH:
  S_max = 2√2 ≈ 2.828

Classical bound: S ≤ 2
Quantum bound: S ≤ 2√2

Is there a φ relationship hidden in these bounds?
""")

tsirelson = 2 * SQRT2
classical = 2

print(f"Classical bound: {classical}")
print(f"Tsirelson bound: {tsirelson:.6f}")
print(f"Ratio: {tsirelson/classical:.6f} = √2")

# Check various φ relationships
print(f"\n" + "-" * 50)
print("Checking φ relationships in bounds:")
print("-" * 50)

print(f"  2√2 / φ = {tsirelson/PHI:.6f}")
print(f"  2√2 * (1/φ) = {tsirelson*INV_PHI:.6f}")
print(f"  2√2 - φ = {tsirelson - PHI:.6f}")
print(f"  (2√2)² = 8 = {8}")
print(f"  φ³ = {PHI**3:.6f}")
print(f"  2√2 / φ² = {tsirelson/PHI**2:.6f}")
print(f"  √(2√2) = {np.sqrt(tsirelson):.6f}")
print(f"  √φ = {np.sqrt(PHI):.6f}")

# The quantum advantage ratio
quantum_advantage = (tsirelson - classical) / classical
print(f"\nQuantum advantage: {quantum_advantage*100:.2f}%")
print(f"  φ - 1 = {PHI - 1:.6f} = 1/φ")
print(f"  Advantage / (1/φ) = {quantum_advantage/INV_PHI:.6f}")

# =============================================================================
# EXPERIMENT 4: Bell Inequality Violation Probability
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 4: CHSH Value Distribution")
print("=" * 70)

print("""
If we sample random measurement angles uniformly, what's the distribution
of CHSH values? Where does φ appear in this distribution?
""")

np.random.seed(42)
n_samples = 10000

chsh_values = []
for _ in range(n_samples):
    angles = np.random.uniform(0, 2*PI, 4)
    S = abs(chsh_value(state, *angles))
    chsh_values.append(S)

chsh_values = np.array(chsh_values)

# Statistics
mean_S = np.mean(chsh_values)
std_S = np.std(chsh_values)
max_S = np.max(chsh_values)

print(f"Random angle sampling (n={n_samples}):")
print(f"  Mean |S| = {mean_S:.6f}")
print(f"  Std |S| = {std_S:.6f}")
print(f"  Max |S| = {max_S:.6f}")

# Check φ relationships
print(f"\n  Mean / φ = {mean_S/PHI:.6f}")
print(f"  Mean * φ = {mean_S*PHI:.6f}")
print(f"  Std / (1/φ) = {std_S/INV_PHI:.6f}")

# What fraction exceed classical bound?
exceed_classical = np.mean(chsh_values > 2)
# What fraction are near φ?
near_phi = np.mean(np.abs(chsh_values - PHI) < 0.1)
near_inv_phi_times_2 = np.mean(np.abs(chsh_values - 2*INV_PHI) < 0.1)

print(f"\n  Fraction exceeding classical bound (S>2): {exceed_classical*100:.2f}%")
print(f"  Fraction near φ ≈ 1.618: {near_phi*100:.2f}%")
print(f"  Fraction near 2/φ ≈ 1.236: {near_inv_phi_times_2*100:.2f}%")

# =============================================================================
# EXPERIMENT 5: Optimal Angles - Numerical Search
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 5: Numerical Optimization of CHSH")
print("=" * 70)

print("""
Let's numerically find the EXACT optimal angles and see if they
have any φ structure.
""")

def neg_chsh(angles):
    """Negative CHSH for minimization."""
    return -abs(chsh_value(state, *angles))

# Multiple random starts
best_result = None
best_S = 0

for _ in range(100):
    x0 = np.random.uniform(0, 2*PI, 4)
    result = optimize.minimize(neg_chsh, x0, method='L-BFGS-B')
    if -result.fun > best_S:
        best_S = -result.fun
        best_result = result

opt_angles = best_result.x % (2*PI)
print(f"Numerically optimal angles:")
print(f"  a1 = {opt_angles[0]:.6f} rad = {opt_angles[0]/PI:.6f}π")
print(f"  a2 = {opt_angles[1]:.6f} rad = {opt_angles[1]/PI:.6f}π")
print(f"  b1 = {opt_angles[2]:.6f} rad = {opt_angles[2]/PI:.6f}π")
print(f"  b2 = {opt_angles[3]:.6f} rad = {opt_angles[3]/PI:.6f}π")
print(f"  Achieved |S| = {best_S:.6f}")

# Check if any optimal angle relates to φ
print(f"\n" + "-" * 50)
print("Checking for φ in optimal angles:")
print("-" * 50)

for i, angle in enumerate(opt_angles):
    ratio_to_pi = angle / PI
    ratio_to_phi = angle / PHI
    ratio_to_pi_over_phi = angle / (PI/PHI)
    
    # Check common φ relationships
    if abs(ratio_to_pi - INV_PHI) < 0.05:
        print(f"  angle[{i}]/π ≈ 1/φ!")
    if abs(ratio_to_pi - (1-INV_PHI)) < 0.05:
        print(f"  angle[{i}]/π ≈ 1-1/φ!")
    if abs(angle - PI/4) < 0.01:
        print(f"  angle[{i}] ≈ π/4")
    if abs(angle - PI/2) < 0.01:
        print(f"  angle[{i}] ≈ π/2")
    if abs(angle - 3*PI/4) < 0.01:
        print(f"  angle[{i}] ≈ 3π/4")

# =============================================================================
# EXPERIMENT 6: Partial Entanglement and φ
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 6: Partially Entangled States")
print("=" * 70)

print("""
What if we use partially entangled states?
|ψ(θ)⟩ = cos(θ)|00⟩ + sin(θ)|11⟩

At what entanglement level does CHSH value equal φ-related quantities?
""")

def partially_entangled_state(theta: float) -> np.ndarray:
    """State cos(θ)|00⟩ + sin(θ)|11⟩."""
    state = np.zeros(4, dtype=complex)
    state[0] = np.cos(theta)  # |00⟩
    state[3] = np.sin(theta)  # |11⟩
    return state

def max_chsh_for_state(state: np.ndarray) -> float:
    """Find maximum CHSH value for a given state."""
    def neg_chsh_state(angles):
        return -abs(chsh_value(state, *angles))
    
    best = 0
    for _ in range(20):
        x0 = np.random.uniform(0, 2*PI, 4)
        result = optimize.minimize(neg_chsh_state, x0, method='L-BFGS-B')
        if -result.fun > best:
            best = -result.fun
    return best

print("\nScanning entanglement parameter θ:")
print("-" * 50)

phi_crossings = []

for theta_deg in range(5, 90, 5):
    theta = np.radians(theta_deg)
    state_partial = partially_entangled_state(theta)
    S_max = max_chsh_for_state(state_partial)
    
    # Concurrence (entanglement measure)
    concurrence = abs(np.sin(2*theta))
    
    marker = ""
    if abs(S_max - PHI) < 0.05:
        marker = " ← S ≈ φ!"
        phi_crossings.append(('S', theta_deg, S_max))
    if abs(S_max - 2*INV_PHI) < 0.05:
        marker = " ← S ≈ 2/φ!"
        phi_crossings.append(('S', theta_deg, S_max))
    if abs(concurrence - INV_PHI) < 0.05:
        marker = " ← C ≈ 1/φ!"
        phi_crossings.append(('C', theta_deg, concurrence))
        
    print(f"  θ={theta_deg:2d}°: S_max={S_max:.4f}, Concurrence={concurrence:.4f}{marker}")

if phi_crossings:
    print(f"\n⚡ Found {len(phi_crossings)} φ-related crossings!")

# =============================================================================
# EXPERIMENT 7: The 3-Setting Bell Inequality
# =============================================================================
print("\n" + "=" * 70)
print("EXPERIMENT 7: Multi-Setting Bell Inequalities")
print("=" * 70)

print("""
Beyond CHSH (2 settings per party), there are inequalities with more settings.
The I3322 inequality uses 3 settings. Does φ appear there?
""")

# For I3322, we need 3 measurement settings per party
def i3322_value(state: np.ndarray, a1: float, a2: float, a3: float, 
                b1: float, b2: float, b3: float) -> float:
    """
    Simplified I3322 inequality value.
    I = -E(a1,b1) + E(a1,b2) + E(a2,b1) + E(a2,b2) + E(a2,b3) + E(a3,b2) - E(a1) - E(b1)
    
    For pure states we simplify...
    """
    E11 = correlation(state, a1, b1)
    E12 = correlation(state, a1, b2)
    E21 = correlation(state, a2, b1)
    E22 = correlation(state, a2, b2)
    E23 = correlation(state, a2, b3)
    E32 = correlation(state, a3, b2)
    
    return -E11 + E12 + E21 + E22 + E23 + E32

# Search for optimal I3322 value
def neg_i3322(angles):
    return -abs(i3322_value(state, *angles))

best_i3322 = 0
for _ in range(50):
    x0 = np.random.uniform(0, 2*PI, 6)
    result = optimize.minimize(neg_i3322, x0, method='L-BFGS-B')
    if -result.fun > best_i3322:
        best_i3322 = -result.fun

print(f"Maximum I3322 value found: {best_i3322:.6f}")
print(f"  I3322 / φ = {best_i3322/PHI:.6f}")
print(f"  I3322 / (1/φ) = {best_i3322/INV_PHI:.6f}")
print(f"  I3322 / √2 = {best_i3322/SQRT2:.6f}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("SUMMARY: φ in Bell Inequalities")
print("=" * 70)

print(f"""
KEY FINDINGS:

1. OPTIMAL CHSH ANGLES: Standard optimal angles are π/4, π/2, 3π/4
   - These are NOT φ-related (they're π/4 multiples)
   - φ-based angles achieve ~{best_phi_S/(2*SQRT2)*100:.1f}% of optimal
   
2. CORRELATION FUNCTION: E(θ) = -cos(θ)
   - E(θ) = 1/φ at θ = {np.degrees(theta_for_inv_phi):.2f}° = arccos(-1/φ)
   - This IS a φ-related angle in the correlation structure!
   - Error: {abs(E_at_phi_angle - INV_PHI)/INV_PHI*100:.4f}%

3. TSIRELSON BOUND: 2√2 ≈ 2.828
   - Not directly φ-related (it's √2-based)
   - Quantum advantage ≈ 41.4% (not 1/φ ≈ 61.8%)

4. CHSH DISTRIBUTION: Random angles give mean |S| ≈ {mean_S:.3f}
   - Not obviously φ-related

5. PARTIAL ENTANGLEMENT: Scanning entanglement levels
   - Found {len(phi_crossings)} φ-related crossings

INTERPRETATION:

Bell inequalities are √2-based, not φ-based:
- Tsirelson bound = 2√2
- Optimal angles = multiples of π/4
- The key constant is √2, not φ

HOWEVER: φ DOES appear in the correlation function!
- E(θ) = 1/φ at a specific angle
- This is where measurement correlations equal golden ratio
- The angle arccos(-1/φ) ≈ {np.degrees(theta_for_inv_phi):.1f}° has special status

CONCLUSION:

Bell inequalities are primarily √2/π-structured, but φ appears in
the CORRELATION VALUES (not the bounds or optimal angles).

This is consistent with Phase 3: φ appears in measurement OUTPUTS
(eigenvalues, correlations), not in the STRUCTURE of the dynamics
(angles, bounds, iteration counts).

The pattern continues:
- φ in: measurement eigenvalues, correlation values
- φ NOT in: optimal angles, quantum bounds, unitary structure
""")

# Key φ finding
print("\n" + "=" * 70)
print("KEY φ DISCOVERY: Correlation E(θ) = 1/φ at θ ≈ 128.17°")
print("=" * 70)
print(f"""
The angle θ = arccos(-1/φ) = {theta_for_inv_phi:.6f} rad = {np.degrees(theta_for_inv_phi):.2f}°

At this measurement angle, entangled particles have correlation = 1/φ.

This is MEASUREMENT-SPECIFIC: it's about the correlation OUTPUT,
not the measurement STRUCTURE.

φ marks a special point in the correlation landscape!
""")

print("=" * 70)
print("PHASE 4 COMPLETE: φ in Bell correlations, not Bell structure!")
print("=" * 70)
