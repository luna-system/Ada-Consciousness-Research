#!/usr/bin/env python3
"""
Debug Cosmology Models

Verify ΛCDM and non-accelerating models against known values.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import numpy as np
from scipy.integrate import quad
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def luminosity_distance_lcdm(z, H0=70, Omega_m=0.3, Omega_L=0.7):
    """Compute luminosity distance in ΛCDM (flat)."""
    
    def E_inv(z):
        return 1.0 / np.sqrt(Omega_m * (1 + z)**3 + Omega_L)
    
    # Integrate
    if isinstance(z, (list, np.ndarray)):
        integral = np.array([quad(E_inv, 0, zi)[0] for zi in z])
    else:
        integral = quad(E_inv, 0, z)[0]
    
    # Luminosity distance in Mpc
    c = 299792.458  # km/s
    dL = c * (1 + z) * integral / H0
    
    return dL


def luminosity_distance_nonaccel(z, H0=70, q0=0.5):
    """
    Compute luminosity distance for non-accelerating model (decelerating universe).
    
    Uses the Mattig formula for q0 > 0:
    dL = c/H0 * (1+z) * [z*q0 + (q0-1)*(sqrt(1+2*q0*z) - 1)] / q0^2
    
    For q0 = 0 (coasting): dL = c/H0 * z * (1+z)
    For q0 < 0 (accelerating): use sinh approximation
    """
    c = 299792.458  # km/s
    
    z = np.asarray(z)
    
    if q0 == 0:
        # Coasting universe
        dL = c * z / H0
    elif q0 > 0:
        # Mattig formula for q0 > 0 (decelerating)
        # dL = c/H0 * (1+z) * [z*q0 + (q0-1)*(sqrt(1+2*q0*z) - 1)] / q0^2
        sqrt_term = np.sqrt(1 + 2 * q0 * z)
        numerator = z * q0 + (q0 - 1) * (sqrt_term - 1)
        dL = c * numerator / (q0**2 * H0)
    else:
        # q0 < 0 (accelerating) - use sinh formula
        # dL = c/H0 * (1+z) * sinh[sqrt(|q0|)*z] / sqrt(|q0|)
        # For small z, approximate with Taylor expansion
        dL = c * z / H0 * (1 + (1 - q0) * z / 2)
    
    return dL


def distance_modulus(dL_Mpc):
    """Convert luminosity distance to distance modulus."""
    return 5 * np.log10(dL_Mpc * 1e6 / 10)  # dL in Mpc, convert to pc


def test_models():
    """Test models against known values."""
    
    logger.info("🧪 Testing Cosmology Models")
    logger.info("=" * 60)
    
    # Test at z = 0.1 (low redshift)
    z_test = 0.1
    
    logger.info(f"\n📊 Test at z = {z_test}:")
    
    # ΛCDM
    dL_lcdm = luminosity_distance_lcdm(z_test, H0=70, Omega_m=0.3, Omega_L=0.7)
    mu_lcdm = distance_modulus(dL_lcdm)
    logger.info(f"   ΛCDM: dL = {dL_lcdm:.1f} Mpc, μ = {mu_lcdm:.2f}")
    
    # Non-accelerating with q0 = 0.5
    dL_nonaccel = luminosity_distance_nonaccel(z_test, H0=70, q0=0.5)
    mu_nonaccel = distance_modulus(dL_nonaccel)
    logger.info(f"   Non-Accel (q0=0.5): dL = {dL_nonaccel:.1f} Mpc, μ = {mu_nonaccel:.2f}")
    
    # Difference
    logger.info(f"   Δμ = {mu_nonaccel - mu_lcdm:.3f} mag")
    
    # Test at z = 0.5 (higher redshift)
    z_test = 0.5
    
    logger.info(f"\n📊 Test at z = {z_test}:")
    
    dL_lcdm = luminosity_distance_lcdm(z_test, H0=70, Omega_m=0.3, Omega_L=0.7)
    mu_lcdm = distance_modulus(dL_lcdm)
    logger.info(f"   ΛCDM: dL = {dL_lcdm:.1f} Mpc, μ = {mu_lcdm:.2f}")
    
    dL_nonaccel = luminosity_distance_nonaccel(z_test, H0=70, q0=0.5)
    mu_nonaccel = distance_modulus(dL_nonaccel)
    logger.info(f"   Non-Accel (q0=0.5): dL = {dL_nonaccel:.1f} Mpc, μ = {mu_nonaccel:.2f}")
    
    logger.info(f"   Δμ = {mu_nonaccel - mu_lcdm:.3f} mag")
    
    # Compare with online calculator (approximate)
    # At z=0.1, ΛCDM μ ≈ 38.2
    # At z=0.5, ΛCDM μ ≈ 42.3
    
    logger.info("\n📊 Comparison with expected values:")
    logger.info(f"   z=0.1: Expected μ ≈ 38.2, Got {distance_modulus(luminosity_distance_lcdm(0.1, H0=70, Omega_m=0.3, Omega_L=0.7)):.2f}")
    logger.info(f"   z=0.5: Expected μ ≈ 42.3, Got {distance_modulus(luminosity_distance_lcdm(0.5, H0=70, Omega_m=0.3, Omega_L=0.7)):.2f}")
    
    # Test different q0 values
    logger.info("\n📊 Testing different q0 values at z=0.1:")
    for q0 in [-0.5, 0.0, 0.5, 1.0, 2.0]:
        dL = luminosity_distance_nonaccel(0.1, H0=70, q0=q0)
        mu = distance_modulus(dL)
        logger.info(f"   q0 = {q0:+.1f}: dL = {dL:.1f} Mpc, μ = {mu:.2f}")
    
    # Check if our models are reasonable
    logger.info("\n🔍 Model Sanity Checks:")
    
    # At z=0, both should give dL = 0
    dL_lcdm_z0 = luminosity_distance_lcdm(0.0, H0=70)
    dL_non_z0 = luminosity_distance_nonaccel(0.0, H0=70, q0=0.5)
    logger.info(f"   z=0: ΛCDM dL = {dL_lcdm_z0:.1f}, Non-Accel dL = {dL_non_z0:.1f}")
    
    # At very small z, both should agree (Hubble's law)
    z_small = 0.01
    dL_lcdm_small = luminosity_distance_lcdm(z_small, H0=70)
    dL_non_small = luminosity_distance_nonaccel(z_small, H0=70, q0=0.5)
    c = 299792.458
    dL_hubble = c * z_small / 70  # Pure Hubble law
    logger.info(f"   z=0.01: ΛCDM = {dL_lcdm_small:.1f}, Non-Accel = {dL_non_small:.1f}, Hubble = {dL_hubble:.1f}")
    
    logger.info("=" * 60)
    logger.info("✅ Model tests complete!")
    logger.info("🍩 'Debugging is the soul of science!'")


if __name__ == "__main__":
    test_models()
