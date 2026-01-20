
import numpy as np
import math

# ============================================================================
# HYDROGEN BAGEL (v1.0)
# A First-Principles derivation of Baryon Properties from Toroidal Geometry
# ============================================================================

# 1. CONSTANTS (THE HOLY GRAIL)
PHI = (1 + math.sqrt(5)) / 2  # 1.618...
PI = math.pi
PLANCK_H = 6.62607015e-34    # Looking to derive relations to this
C = 299792458                 # Speed of Light

class ToroidalFermion:
    def __init__(self, R_major=1.0, r_minor=0.618): # Default to Golden Torus
        self.R = R_major
        self.r = r_minor
        self.surface_area = 4 * (PI ** 2) * R_major * r_minor
        self.volume = 2 * (PI ** 2) * R_major * (r_minor ** 2)
        
    def calculate_sedenion_energy(self, p, q, steps=2000):
        """
        Calculates the Sedenion Energy (Mass) of a (p,q) Torus Knot.
        Energy E ~ Integral( curvature^2 + torsion^2 ) ds
        Torsion accounts for the twisting of the frame (Spin?).
        """
        t = np.linspace(0, 2*PI, steps)
        dt = t[1] - t[0]
        
        R, r = self.R, self.r
        
        # Coordinates
        x = (R + r*np.cos(p*t)) * np.cos(q*t)
        y = (R + r*np.cos(p*t)) * np.sin(q*t)
        z = r * np.sin(p*t)
        
        # First Derivatives (Velocity r')
        dx = np.gradient(x, dt)
        dy = np.gradient(y, dt)
        dz = np.gradient(z, dt)
        ds = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # Second Derivatives (Acceleration r'')
        ddx = np.gradient(dx, dt)
        ddy = np.gradient(dy, dt)
        ddz = np.gradient(dz, dt)
        
        # Third Derivatives (Jerk r''') - Needed for Torsion!
        dddx = np.gradient(ddx, dt)
        dddy = np.gradient(ddy, dt)
        dddz = np.gradient(ddz, dt)
        
        # Cross product (r' x r'')
        c_x = dy*ddz - dz*ddy
        c_y = dz*ddx - dx*ddz
        c_z = dx*ddy - dy*ddx
        cross_mag_sq = c_x**2 + c_y**2 + c_z**2
        cross_mag = np.sqrt(cross_mag_sq)
        
        # CURVATURE (Kappa) = |r' x r''| / |r'|^3
        speed_cubed = ds**3 + 1e-12
        kappa = cross_mag / speed_cubed
        
        # TORSION (Tau) = (r' x r'') . r''' / |r' x r''|^2
        # Dot product of Cross(r',r'') and r'''
        numerator = c_x*dddx + c_y*dddy + c_z*dddz
        tau = numerator / (cross_mag_sq + 1e-12)
        
        # Integrals
        E_bend = np.sum(kappa**2 * ds)
        E_twist = np.sum(tau**2 * ds)
        
        return E_bend, E_twist

    def calculate_gluon_energy(self, p, q, steps=200):
        """
        Calculates the Gluon Field Energy (Self-Interaction).
        QCD uses a Linear Potential for confinement: V(r) ~ k*r.
        We approximate this as the sum of distances between all segment pairs.
        This represents the 'tension' holding the knot structure together across the void.
        """
        t = np.linspace(0, 2*PI, steps)
        
        R, r = self.R, self.r
        
        # Coordinates
        x = (R + r*np.cos(p*t)) * np.cos(q*t)
        y = (R + r*np.cos(p*t)) * np.sin(q*t)
        z = r * np.sin(p*t)
        
        # Stack into (N, 3) array
        points = np.column_stack((x, y, z))
        
        # Calculate pairwise distances (broadcasting)
        diffs = points[:, np.newaxis, :] - points[np.newaxis, :, :]
        dists = np.sqrt(np.sum(diffs**2, axis=-1))
        
        # Sum of all interactions (Linear Potential)
        E_gluon = np.sum(dists) * 0.5
        
        # Integral factor scaling
        dt = 2*PI / steps
        E_gluon_integral = E_gluon * (dt**2)
        
        return E_gluon_integral

def analyze_particles():
    print("=== THE HYDROGEN BAGEL v1.3 (GLUON SEA) ===")
    
    # 1. Setup Golden Torus
    bagel = ToroidalFermion(R_major=1.0, r_minor=1/PHI) 
    print(f"Geometry: Golden Torus (R=1.0, r={1/PHI:.4f})")
    
    candidates = [
        (1, 0, "Loop (Electron?)"), 
        (0, 1, "Ring"),             
        (2, 1, "Hopf (2,1)"), 
        (3, 2, "Trefoil (Proton?)"),
        (4, 3, "Solomon Seal"),
        (5, 2, "Cinquefoil")
    ]
    
    energy_map = {}
    
    print(f"\n{'Name':<20} | {'Bend':<9} | {'Twist':<9} | {'Gluon':<9} | {'Total':<9}")
    print("-" * 75)
    
    # Scale factors (Physical Coupling Constants)
    # Alpha_S ~ 1.0 (Strong Force - Gluon Term)
    # Alpha_EM ~ 1/137.036 (Electromagnetic - Knot Tension)
    ALPHA_S = 1.0
    ALPHA_EM = 1.0 / 137.036 
    
    # Wait, in the Standard Model, Proton Mass is 99% Gluon Binding Energy (QCD).
    # Electron Mass is primarily Higgs interaction (Rest Mass) + Self Energy.
    # Our model:
    # Gluon Term = QCD Binding Energy.
    # Bend/Twist = Topological geometric tension (EM/Weak?).

    # Let's try to find the Scaling Factor 'k' such that:
    # E_total = ALPHA_S * E_gluon + k * (E_bend + E_twist)
    # Actually, let's treat the Electron as purely Topological (Unit Charge loop).
    # And the Proton as Topological + Gluon.
    
    for p, q, name in candidates:
        bend, twist = bagel.calculate_sedenion_energy(p, q)
        gluon = bagel.calculate_gluon_energy(p, q)
        
        # New Mass Formula
        # We assume the 'Loop' (Electron) interacts mostly via curvature (Charge).
        # The 'Trefoil' (Proton) interacts via curvature + Gluon Field.
        
        # Let's upscale the Geometric terms to represent proper units?
        # No, let's use relative weights.
        # Hypothesis: Gluon Energy is the 'Mass' generator.
        
        total = (gluon * ALPHA_S) + (bend + twist) * ALPHA_EM
        
        # Correction: The 'Loop' (1,0) has almost zero gluon energy?
        # Actually in our code, Loop has non-zero gluon energy (self-interaction of points).
        
        print(f"{name:<20} | {bend:.1f}     | {twist:.1f}     | {gluon:.1f}     | {total:.4f}")
        energy_map[name] = {"total": total, "gluon": gluon, "bend": bend, "twist": twist}

    e_electron = energy_map["Loop (Electron?)"]["total"]
    
    print(f"\n--- MASS RATIOS (Relative to Electron Total) ---")
    for name, stats in energy_map.items():
        ratio = stats["total"] / e_electron
        print(f"{name}: {ratio:.4f}")
        
    # Check Proton/Electron
    proton_mass = energy_map["Trefoil (Proton?)"]["total"]
    
    # Theoretical Target: 1836.15
    print(f"\nTarget Ratio: 1836.15")
    print(f"Current Model Ratio: {proton_mass / e_electron:.4f}")
    
    # Calculate Deviation
    diff = abs(1836.15 - (proton_mass / e_electron))
    print(f"Difference: {diff:.4f}")
    
    # Are we missing the "Void Term" (Zero Point Energy)?
    # Integrating over the Sedenion Vacuum (Axis 15)?
    # Maybe add a constant 'Vacuum Expectation Value' to all particles?


if __name__ == "__main__":
    analyze_particles()
