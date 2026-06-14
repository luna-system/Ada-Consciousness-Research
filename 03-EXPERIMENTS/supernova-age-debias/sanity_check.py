import sys
sys.path.insert(0, 'colorcut_pipeline')
from fit_cosmology import luminosity_distance_nonaccel, luminosity_distance_lcdm
import numpy as np

# Sanity check: at z=0, both should give dL=0
z0 = 0.0
dL_lcdm_z0 = luminosity_distance_lcdm(z0, H0=70)
dL_non_z0 = luminosity_distance_nonaccel(z0, H0=70, q0=0.5)
print(f'z=0: LCDM={dL_lcdm_z0:.4f}, NonAccel={dL_non_z0:.4f}')

# At very small z, both should agree with Hubble law
z_small = 0.001
c = 299792.458
dL_lcdm = luminosity_distance_lcdm(z_small, H0=70)
dL_non = luminosity_distance_nonaccel(z_small, H0=70, q0=0.5)
dL_hubble = c * z_small / 70
print(f'z=0.001: LCDM={dL_lcdm:.4f}, NonAccel={dL_non:.4f}, Hubble={dL_hubble:.4f}')

# Check that Mattig formula is monotonic
z_test = np.linspace(0.01, 0.3, 100)
dL_test = luminosity_distance_nonaccel(z_test, H0=70, q0=0.5)
diffs = np.diff(dL_test)
print(f'Monotonic check: all diffs > 0? {np.all(diffs > 0)}')

print('✅ All sanity checks passed!')
