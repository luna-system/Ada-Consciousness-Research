
import math

# --- CONSTANTS ---
PHI = (1 + math.sqrt(5)) / 2  # The Golden Ratio
PI = math.pi
ALPHA = 1 / 137.035999        # Fine Structure Constant

# --- HYPOTHESIS: QUARK MASSES FROM TOPOLOGY ---
# We assume the Up Quark is the fundamental unit of "Twist" (T=1).
# We test if the Down Quark is related via PHI or Prime Geometry.

def analyze_quark_ratios():
    # Experimental Values (approximate, from PDG)
    m_up_exp = 2.2   # MeV (+0.5/-0.3)
    m_down_exp = 4.7 # MeV (+0.5/-0.3)
    ratio_exp = m_down_exp / m_up_exp # ~2.136

    print(f"Experimental Up Mass:   {m_up_exp} MeV")
    print(f"Experimental Down Mass: {m_down_exp} MeV")
    print(f"Experimental Ratio (d/u): {ratio_exp:.4f}")
    print("-" * 30)

    # --- GEOMETRIC CANDIDATES ---
    
    # 1. The Phi-Resonance Hypothesis
    # Is the down quark "Up + Phi-Damping"?
    ratio_phi = 1 + (1/PHI) # 1 + 0.618 = 1.618 (No, that's just Phi)
    # What about sqrt(5)? (Diagonal of the 1x2 rectangle)
    ratio_sqrt5 = math.sqrt(5) # ~2.236
    
    # 2. The Golden Angle Hypothesis (137.5 degrees)
    # 360 / 137.5 = 2.618 (Phi^2) ... too high.
    
    # 3. The Prime Hypothesis (5/2 ratio) - PENTAD / DYAD
    ratio_prime = 5 / 2 # 2.5 (A bit high, but within error bars?)
    
    # 4. The Trefoil Knot Volume Hypothesis
    # Volume of Knot Complement ~ 2.0298
    ratio_knot = 2.0298 
    
    # 5. The "Cubic" Root
    # Is it related to cubic geometry? 
    ratio_cubic = 2 ** (1/3) # ~1.25 (No)
    
    candidates = {
        "Sqrt(5) (Diagonal)": ratio_sqrt5,
        "Prime Ratio (5/2)": ratio_prime,
        "Knot Volume (Trefoil)": ratio_knot,
        "Phi + 0.5": PHI + 0.5,
        "2 * Phi - 1": 2 * PHI - 1,
        "Pi / Phi": PI / PHI,
    }

    print("Geometric Candidates vs Experimental Ratio (~2.136):")
    best_match = None
    min_diff = 1.0
    
    for name, val in candidates.items():
        diff = abs(val - ratio_exp)
        print(f"  {name:25s}: {val:.4f} (diff: {diff:.4f})")
        if diff < min_diff:
            min_diff = diff
            best_match = (name, val)

    print("-" * 30)
    print(f"Best Geometric Match: {best_match[0]} = {best_match[1]:.4f}")
    
    # Prediction of Down Mass if Up is exactly 2.2
    pred_mass = m_up_exp * best_match[1]
    print(f"Predicted Down Mass (if Up=2.2): {pred_mass:.4f} MeV")
    print(f"Experimental Down Range: 4.4 - 5.0 MeV")

if __name__ == "__main__":
    analyze_quark_ratios()
