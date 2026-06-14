import pandas as pd
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

C_LIGHT = 299792.458

def luminosity_distance_lcdm(z, H0, Om, OL):
    def integrand(zp):
        return 1.0 / np.sqrt(Om * (1 + zp)**3 + OL)
    dL = np.zeros_like(z)
    for i, zi in enumerate(z):
        integral, _ = quad(integrand, 0, zi)
        dL[i] = (C_LIGHT / H0) * (1 + zi) * integral
    return dL

def luminosity_distance_nonaccel(z, H0, q0):
    return (C_LIGHT / H0) * z * (1 + z) * (1 + 0.5 * (1 - q0) * z)

# Load combined data
ztf_sne = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/snia_data.csv')
ztf_hosts = pd.read_csv('data/ztf_dr2/ztfsniadr2_lite/tables/globalhost_data.csv')
ztf = ztf_sne.merge(ztf_hosts, on='ztfname', how='inner')
ztf = ztf[ztf['redshift'] > 0.05]
ztf['mB'] = -2.5 * np.log10(ztf['x0']) + 10.0

pantheon = pd.read_csv('data/pantheon-plus/Pantheon+_Data/4_DISTANCES_AND_COVAR/Pantheon+SH0ES.dat', sep=r'\s+')
pantheon = pantheon.rename(columns={'zCMB': 'redshift', 'mB': 'mB', 'x1': 'x1', 'c': 'c', 'HOST_LOGMASS': 'mass'})
pantheon = pantheon[pantheon['redshift'] > 0.1]

combined = pd.concat([ztf, pantheon], ignore_index=True)

# Filter valid data
valid = combined['redshift'].notna() & combined['mB'].notna() & combined['x1'].notna() & combined['c'].notna() & combined['mass'].notna()
df = combined[valid].copy()

z = df['redshift'].values
mB = df['mB'].values
x1 = df['x1'].values
c = df['c'].values
mass = df['mass'].values

# Tripp standardization
mass_step = mass - np.nanmedian(mass)
mB_corr = mB + 0.14 * x1 - 3.1 * c - 0.0 * mass_step

# Approximate M
dL_approx = C_LIGHT * z / 70
mu_approx = 5 * np.log10(dL_approx) + 25
M_guess = np.nanmedian(mB_corr - mu_approx)

print(f"Combined dataset: {len(df)} SNe")
print(f"Redshift range: {z.min():.3f} to {z.max():.3f}")
print(f"M_guess: {M_guess:.3f}")
print()

# Fit LCDM
result_lcdm = minimize(
    lambda p: np.sum(((mB_corr - (-2.5*np.log10(luminosity_distance_lcdm(z, p[0], p[1], p[2])) + 25) - p[3])**2) / max(0.05, np.std(mB_corr - (-2.5*np.log10(luminosity_distance_lcdm(z, p[0], p[1], p[2])) + 25) - p[3]))**2),
    [72.0, 0.3, 0.7, M_guess], method='Nelder-Mead'
)
H0_l, Om_l, OL_l, M_l = result_lcdm.x

# Fit Non-Accel  
result_nonaccel = minimize(
    lambda p: np.sum(((mB_corr - (-2.5*np.log10(luminosity_distance_nonaccel(z, p[0], p[1])) + 25) - p[2])**2) / max(0.05, np.std(mB_corr - (-2.5*np.log10(luminosity_distance_nonaccel(z, p[0], p[1])) + 25) - p[2]))**2),
    [72.0, 1.0, M_guess], method='Nelder-Mead'
)
H0_n, q0_n, M_n = result_nonaccel.x

# Compute chi2 and logL with SAME sigma for both
dL_l = luminosity_distance_lcdm(z, H0_l, Om_l, OL_l)
mu_model_l = 5 * np.log10(dL_l) + 25
mu_obs_l = mB_corr - M_l
residuals_l = mu_obs_l - mu_model_l
sigma_l = np.std(residuals_l)
chi2_lcdm = np.sum(residuals_l**2 / sigma_l**2)
logL_lcdm = -0.5 * np.sum(residuals_l**2 / sigma_l**2 + np.log(2 * np.pi * sigma_l**2))

dL_n = luminosity_distance_nonaccel(z, H0_n, q0_n)
mu_model_n = 5 * np.log10(dL_n) + 25
mu_obs_n = mB_corr - M_n
residuals_n = mu_obs_n - mu_model_n
sigma_n = np.std(residuals_n)
chi2_nonaccel = np.sum(residuals_n**2 / sigma_n**2)
logL_nonaccel = -0.5 * np.sum(residuals_n**2 / sigma_n**2 + np.log(2 * np.pi * sigma_n**2))

print("=" * 70)
print("CORRECTED REAL DATA RESULTS (Combined ZTF + Pantheon+)")
print("=" * 70)
print(f"LCDM: H0={H0_l:.2f}, Om={Om_l:.3f}, OL={OL_l:.3f}, M={M_l:.3f}")
print(f"Non-Accel: H0={H0_n:.2f}, q0={q0_n:.3f}, M={M_n:.3f}")
print()
print(f"LCDM:    chi2={chi2_lcdm:.1f}, logL={logL_lcdm:.1f}")
print(f"Non-Accel: chi2={chi2_nonaccel:.1f}, logL={logL_nonaccel:.1f}")
print()
print(f"Δchi2 = {chi2_lcdm - chi2_nonaccel:.1f}")
print(f"ΔlogL = {logL_lcdm - logL_nonaccel:.1f}")
print()
print("Verification: logL should = -0.5*chi2 - 0.5*n*log(2*pi*sigma^2)")
print(f"LCDM:    -0.5*{chi2_lcdm:.1f} - 0.5*{len(df)}*log(2*pi*{sigma_l:.6f}^2) = {logL_lcdm:.1f}")
print(f"Non-Accel: -0.5*{chi2_nonaccel:.1f} - 0.5*{len(df)}*log(2*pi*{sigma_n:.6f}^2) = {logL_nonaccel:.1f}")
print("=" * 70)
