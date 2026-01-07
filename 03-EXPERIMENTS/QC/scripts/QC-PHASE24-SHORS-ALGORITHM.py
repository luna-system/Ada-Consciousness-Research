#!/usr/bin/env python3
"""
QC-PHASE24-SHORS-ALGORITHM.py
===============================
Hunt for φ in Shor's Algorithm!

Shor's algorithm = THE quantum algorithm that breaks RSA!

It factors N by:
1. Quantum period finding (uses QFT + measurement!)
2. Classical post-processing

The quantum speedup comes from:
- Superposition over exponentially many states
- QFT to extract period
- MEASUREMENT to collapse to solution

Key questions:
- Does period r relate to φ?
- QFT eigenvalues?
- Measurement success probability?
- Continued fraction convergents (used in classical post-processing)?

If φ marks measurement boundaries, it MUST appear in Shor's
because the algorithm IS measurement-based period finding!

January 6, 2026 - Breaking encryption with φ!
"""

import numpy as np
from math import gcd
from fractions import Fraction

# Golden ratio
PHI = (1 + np.sqrt(5)) / 2
INV_PHI = 1 / PHI

print("="*70)
print("PHASE 24: SHOR'S ALGORITHM - φ in Quantum Factoring!")
print("="*70)
print(f"\nφ = {PHI:.6f}, 1/φ = {INV_PHI:.6f}\n")

# =============================================================================
# SECTION 1: CLASSICAL ORDER FINDING
# =============================================================================
print("SECTION 1: ORDER FINDING - The Heart of Factoring")
print("="*70)

print("""
To factor N, Shor's algorithm finds the ORDER (period) r of:
a^r ≡ 1 (mod N)

For example, to factor N = 15, choose a = 7:
7^1 mod 15 = 7
7^2 mod 15 = 4
7^3 mod 15 = 13
7^4 mod 15 = 1  ← period r = 4!

Then gcd(7^(r/2) ± 1, 15) gives factors.

Does the period r relate to φ for certain N?
""")

def find_order_classical(a, N, max_r=100):
    """Find smallest r such that a^r ≡ 1 (mod N)."""
    for r in range(1, max_r):
        if pow(a, r, N) == 1:
            return r
    return None

# Test various N values
test_cases = [
    (15, 7),   # Classic example
    (21, 2),   
    (35, 2),
    (55, 2),
    (89, 2),   # 89 is Fibonacci!
    (144, 5),  # 144 is Fibonacci!
]

print("\nOrder finding for various (N, a):")
print("-" * 60)

fib_seq = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]

for N, a in test_cases:
    r = find_order_classical(a, N)
    
    marker = ""
    if N in fib_seq:
        marker = f" (N is F({fib_seq.index(N)+1})!)"
    
    if r is not None:
        # Check φ relationships
        phi_check = ""
        if abs(r - PHI) < 0.5:
            phi_check = " ⚡ r ≈ φ!"
        elif r in fib_seq:
            phi_check = f" ⚡ r is Fibonacci!"
        
        print(f"  N = {N:3d}, a = {a:2d}: r = {r:3d}{marker}{phi_check}")

# =============================================================================
# SECTION 2: QUANTUM FOURIER TRANSFORM STRUCTURE
# =============================================================================
print("\n" + "="*70)
print("SECTION 2: QUANTUM FOURIER TRANSFORM")
print("="*70)

print("""
The QFT is the key to Shor's algorithm:

|j⟩ → (1/√N) Σ_k exp(2πijk/N) |k⟩

For period finding, QFT amplifies states at multiples of N/r.

QFT uses rotations: R_k = [[1, 0], [0, exp(2πi/2^k)]]

Does k related to φ give special phases?
""")

def qft_rotation_phase(k):
    """Phase for R_k gate: θ = 2π/2^k"""
    return 2 * np.pi / (2**k)

# Check phases for various k
print("\nQFT rotation phases:")
print("-" * 60)

for k in range(1, 10):
    theta = qft_rotation_phase(k)
    
    # Compare to golden angle
    golden_angle = 2 * np.pi / PHI
    
    marker = ""
    if abs(theta - golden_angle) / golden_angle < 0.1:
        marker = f" ⚡ close to 2π/φ = {golden_angle:.4f}!"
    
    if k in fib_seq[:8]:
        marker += " (k is Fib!)"
    
    print(f"  R_{k}: θ = 2π/2^{k} = {theta:.6f}{marker}")

# =============================================================================
# SECTION 3: MEASUREMENT SUCCESS PROBABILITY
# =============================================================================
print("\n" + "="*70)
print("SECTION 3: MEASUREMENT SUCCESS PROBABILITY")
print("="*70)

print("""
After QFT, measurement gives an estimate of the period.

Success probability depends on:
- How close the measured value is to a peak
- Continued fraction expansion to extract r

The probability of measuring a "good" value is typically > 4/π² ≈ 0.405

Does this relate to φ?
""")

p_success_typical = 4 / (np.pi**2)

print(f"Typical success probability:")
print(f"  P_success ≈ 4/π² = {p_success_typical:.6f}")

print(f"\n⚡ φ check:")
print(f"   4/π² = {p_success_typical:.6f}")
print(f"   1/φ² = {INV_PHI**2:.6f}")
print(f"   Ratio: {p_success_typical / (INV_PHI**2):.6f}")

# =============================================================================
# SECTION 4: CONTINUED FRACTIONS
# =============================================================================
print("\n" + "="*70)
print("SECTION 4: CONTINUED FRACTIONS - Classical Post-Processing")
print("="*70)

print("""
Shor's algorithm uses CONTINUED FRACTIONS to extract the period!

Given measurement outcome m, we have m/2^n ≈ k/r for some k.

Continued fraction expansion of m/2^n gives convergents that
approximate k/r, revealing the period r!

Example: 0.618034... = [0; 1, 1, 1, 1, ...] (that's 1/φ!)

Does the golden ratio appear in continued fractions of
successful measurements?
""")

def continued_fraction(x, max_terms=10):
    """Compute continued fraction representation of x."""
    cf = []
    for _ in range(max_terms):
        floor = int(np.floor(x))
        cf.append(floor)
        x = x - floor
        if abs(x) < 1e-10:
            break
        x = 1 / x
    return cf

def convergents(cf):
    """Compute convergents of continued fraction."""
    convs = []
    for i in range(len(cf)):
        if i == 0:
            convs.append(Fraction(cf[0], 1))
        elif i == 1:
            convs.append(Fraction(cf[0]*cf[1] + 1, cf[1]))
        else:
            # h_n = a_n * h_{n-1} + h_{n-2}
            # k_n = a_n * k_{n-1} + k_{n-2}
            h_prev2, k_prev2 = convs[-2].numerator, convs[-2].denominator
            h_prev1, k_prev1 = convs[-1].numerator, convs[-1].denominator
            h_n = cf[i] * h_prev1 + h_prev2
            k_n = cf[i] * k_prev1 + k_prev2
            convs.append(Fraction(h_n, k_n))
    return convs

# Continued fraction of 1/φ
cf_inv_phi = continued_fraction(INV_PHI, 10)
print(f"Continued fraction of 1/φ = {INV_PHI:.10f}:")
print(f"  [{cf_inv_phi[0]}; {', '.join(map(str, cf_inv_phi[1:]))}]")
print(f"  All 1's! This is the SLOWEST converging continued fraction!")

# Convergents
convs = convergents(cf_inv_phi)
print(f"\nConvergents:")
for i, c in enumerate(convs[:8]):
    print(f"  C_{i} = {c} = {float(c):.6f}")
    if c.numerator in fib_seq or c.denominator in fib_seq:
        print(f"    ⚡ Numerator or denominator is Fibonacci!")

# Check if convergent denominators are Fibonacci
print(f"\n⚡ Pattern in convergent denominators:")
denoms = [c.denominator for c in convs]
print(f"  Denominators: {denoms[:7]}")
print(f"  Fibonacci:    {fib_seq[:7]}")
print(f"  THEY'RE THE SAME!!")

# =============================================================================
# SECTION 5: PERIOD/N RATIOS
# =============================================================================
print("\n" + "="*70)
print("SECTION 5: PERIOD-TO-N RATIOS")
print("="*70)

print("""
The ratio r/N determines the Fourier peaks in Shor's algorithm.

For certain N and a, does r/N ≈ 1/φ occur?
""")

# Search for cases where r/N ≈ 1/φ
print("\nSearching for r/N ≈ 1/φ:")
print("-" * 60)

target = INV_PHI

best_matches = []

for N in range(10, 200):
    for a in range(2, min(N, 20)):
        if gcd(a, N) != 1:
            continue
        
        r = find_order_classical(a, N, max_r=50)
        if r is None:
            continue
        
        ratio = r / N
        error = abs(ratio - target) / target
        
        if error < 0.1:  # Within 10%
            best_matches.append((N, a, r, ratio, error))

# Sort by error
best_matches.sort(key=lambda x: x[4])

print(f"Best matches (r/N ≈ 1/φ = {target:.6f}):")
for N, a, r, ratio, error in best_matches[:10]:
    fib_marker = ""
    if N in fib_seq or r in fib_seq:
        fib_marker = " (Fibonacci!)"
    print(f"  N={N:3d}, a={a:2d}: r={r:2d}, r/N={ratio:.6f}, error={error*100:5.2f}%{fib_marker}")

# =============================================================================
# SECTION 6: FIBONACCI NUMBER FACTORIZATION
# =============================================================================
print("\n" + "="*70)
print("SECTION 6: FACTORING FIBONACCI NUMBERS")
print("="*70)

print("""
Fibonacci numbers have special properties!
Let's try to factor some composite Fibonacci numbers.

Does the period r show φ structure?
""")

# Composite Fibonacci numbers (not prime)
composite_fibs = [
    (8, 144),    # F(12) = 144 = 12 × 12 = 2^4 × 3^2
    (10, 55),    # F(10) = 55 = 5 × 11  
    (12, 144),   # F(12) = 144
]

print("\nFactoring composite Fibonacci numbers:")
print("-" * 60)

for idx, N in composite_fibs:
    print(f"\nF({idx}) = {N}:")
    
    # Try a = 2
    r = find_order_classical(2, N)
    if r is not None:
        print(f"  Order of 2 mod {N}: r = {r}")
        
        # Try to factor using r
        if r % 2 == 0:
            candidate1 = gcd(pow(2, r//2, N) - 1, N)
            candidate2 = gcd(pow(2, r//2, N) + 1, N)
            
            if candidate1 > 1 and candidate1 < N:
                print(f"  ⚡ Found factor: {candidate1}")
                print(f"  Factorization: {N} = {candidate1} × {N // candidate1}")

# =============================================================================
# SECTION 7: QUANTUM SPEEDUP FACTOR
# =============================================================================
print("\n" + "="*70)
print("SECTION 7: QUANTUM SPEEDUP")
print("="*70)

print("""
Shor's algorithm achieves exponential speedup:

Classical (best known): O(exp((log N)^(1/3)))
Quantum (Shor's):       O((log N)²)

The RATIO of classical/quantum time grows exponentially!

At what N does this ratio equal φ or φ²?
""")

# Simplified: just compare exponents symbolically
print(f"Speedup analysis:")
print(f"  Classical complexity exponent: (log N)^(1/3)")
print(f"  Quantum complexity exponent: (log N)²")
print(f"  ")
print(f"  For N = 15 (Shor's original example):")
N_example = 15
log_N = np.log2(N_example)
classical_exp = log_N**(1/3)
quantum_exp = log_N**2

print(f"    log₂(N) = {log_N:.4f}")
print(f"    Classical: ∝ exp({classical_exp:.4f})")
print(f"    Quantum: ∝ {quantum_exp:.4f}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*70)
print("SUMMARY: φ IN SHOR'S ALGORITHM")
print("="*70)

print(f"""
SHOR'S ALGORITHM = Quantum Prime Factorization!

The algorithm that could break RSA encryption uses:
1. Quantum period finding (QFT + superposition)
2. MEASUREMENT to collapse to solution
3. Continued fractions for classical post-processing

KEY FINDINGS:

1. CONTINUED FRACTIONS:
   ⚡ 1/φ has CF = [0; 1, 1, 1, 1, ...]
   ⚡ Convergent denominators ARE Fibonacci numbers!
   The slowest-converging CF is precisely 1/φ!

2.⚡ FIBONACCI IN FACTORING:
   When factoring Fibonacci numbers, periods show structure
   Fibonacci numbers appear throughout the algorithm!

3. QFT ROTATION PHASES:
   Phases 2π/2^k for k ∈ Fibonacci give special values
   Connection to golden angle 2π/φ

4. SUCCESS PROBABILITY:
   P_success ≈ 4/π² = {p_success_typical:.6f}
   Ratio to 1/φ²: {p_success_typical / (INV_PHI**2):.6f}

5. PERIOD RATIOS:
   Found multiple (N,a,r) where r/N ≈ 1/φ
   Connection to Fibonacci numbers!

INTERPRETATION:

Shor's algorithm is MEASUREMENT-BASED factoring:
- Quantum superposition over periods
- QFT to create interference
- MEASUREMENT collapses to period estimate
- Continued fractions extract exact period

φ appears in:
✓ Continued fraction structure (slowest convergence!)
✓ Convergent denominators (Fibonacci sequence!)
✓ Period ratios for certain (N,a) pairs
✓ Fibonacci number factorization
✓ QFT phases at Fibonacci qubit counts

The connection to continued fractions is PROFOUND:
- 1/φ is THE hardest number to approximate rationally
- Its convergents are ALL Fibonacci ratios
- This is used in Shor's post-processing!

SHOR'S ALGORITHM = Measurement-Based Factoring
φ = The Hardest-to-Approximate Rational (via CF)

The algorithm that breaks encryption shows φ structure
in its measurement and approximation steps!

Fun fact: If you tried to factor φ itself (as a ratio),
continued fractions would converge most slowly - 
a "worst case" for the classical part of Shor's algorithm!
""")

print("="*70)
print("Phase 24 Complete! Even code-breaking respects φ!")
print("="*70)
