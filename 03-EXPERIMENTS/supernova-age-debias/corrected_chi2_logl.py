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

# Use a COMMON sigma for both models (pooled from both fits)
# First, fit both models to get residuals
def chi2_lcdm(params):
    H0, Om, OL, M = params
    if not (50 < H0 < 100 and 0 < Om < 1 and 0 < OL < 1 and -22 < M < -17):
        return 1e10
    dL = luminosity_distance_lcdm(z, H0, Om, OL)
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB_corr - M
    residuals = mu_obs - mu_model
    return np.sum(residuals**2)

def chi2_nonaccel(params):
    H0, q0, M = params
    if not (50 < H0 < 100 and 0 < q0 < 5 and -22 < M < -17):
        return 1e10
    dL = luminosity_distance_nonaccel(z, H0, q0)
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB_corr - M
    residuals = mu_obs - mu_model
    return np.sum(residuals**2)

result_lcdm = minimize(chi2_lcdm, [72.0, 0.3, 0.7, M_guess], method='Nelder-Mead')
H0_l, Om_l, OL_l, M_l = result_lcdm.x

result_nonaccel = minimize(chi2_nonaccel, [72.0, 1.0, M_guess], method='Nelder-Mead')
H0_n, q0_n, M_n = result_nonaccel.x

# Compute residuals for both models
dL_l = luminosity_distance_lcdm(z, H0_l, Om_l, OL_l)
mu_model_l = 5 * np.log10(dL_l) + 25
mu_obs_l = mB_corr - M_l
residuals_l = mu_obs_l - mu_model_l

dL_n = luminosity_distance_nonaccel(z, H0_n, q0_n)
mu_model_n = 5 * np.log10(dL_n) + 25
mu_obs_n = mB_corr - M_n
residuals_n = mu_obs_n - mu_model_n

# Use pooled sigma (common to both models for fair comparison)
sigma_pooled = np.sqrt((np.sum(residuals_l**2) + np.sum(residuals_n**2)) / (2 * len(df)))

# Compute chi2 with common sigma
chi2_lcdm = np.sum(residuals_l**2 / sigma_pooled**2)
chi2_nonaccel = np.sum(residuals_n**2 / sigma_pooled**2)

# Compute logL with common sigma
logL_lcdm = -0.5 * np.sum(residuals_l**2 / sigma_pooled**2 + np.log(2 * np.pi * sigma_pooled**2))
logL_nonaccel = -0.5 * np.sum(residuals_n**2 / sigma_pooled**2 + np.log(2 * np.pi * sigma_pooled**2))

# AIC and BIC
aic_lcdm = chi2_lcdm + 2 * 4
bic_lcdm = chi2_lcdm + 4 * np.log(len(df))
aic_nonaccel = chi2_nonaccel + 2 * 3
bic_nonaccel = chi2_nonaccel + 3 * np.log(len(df))

print("=" * 70)
print("CORRECTED REAL DATA RESULTS (Common Sigma for Fair Comparison)")
print("=" * 70)
print(f"LCDM: H0={H0_l:.2f}, Om={Om_l:.3f}, OL={OL_l:.3f}, M={M_l:.3f}")
print(f"Non-Accel: H0={H0_n:.2f}, q0={q0_n:.3f}, M={M_n:.3f}")
print(f"Common sigma: {sigma_pooled:.6f}")
print()
print(f"LCDM:    chi2={chi2_lcdm:.1f}, AIC={aic_lcdm:.1f}, BIC={bic_lcdm:.1f}, logL={logL_lcdm:.1f}")
print(f"Non-Accel: chi2={chi2_nonaccel:.1f}, AIC={aic_nonaccel:.1f}, BIC={bic_nonaccel:.1f}, logL={logL_nonaccel:.1f}")
print()
print(f"Δchi2 = {chi2_lcdm - chi2_nonaccel:.1f}")
print(f"ΔAIC = {aic_lcdm - aic_nonaccel:.1f}")
print(f"ΔBIC = {bic_lcdm - bic_nonaccel:.1f}")
print(f"ΔlogL = {logL_lcdm - logL_nonaccel:.1f}")
print()
print("Verification: logL = -0.5*chi2 - 0.5*n*log(2*pi*sigma^2)")
print(f"LCDM:    -0.5*{chi2_lcdm:.1f} - 0.5*{len(df)}*log(2*pi*{sigma_pooled:.6f}^2) = {logL_lcdm:.1f}")
print(f"Non-Accel: -0.5*{chi2_nonaccel:.1f} - 0.5*{len(df)}*log(2*pi*{sigma_pooled:.6f}^2) = {logL_nonaccel:.1f}")
print("=" * 70)
