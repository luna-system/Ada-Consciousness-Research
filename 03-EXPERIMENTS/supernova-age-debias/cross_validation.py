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

# Load data
df = pd.read_csv('data/ztf_dr2_with_colors.csv')
df_valid = df[(df['has_host'] == True) & (df['redshift'] > 0.05)].copy()

# Filter valid data
valid = df_valid['redshift'].notna() & df_valid['x0'].notna() & df_valid['x1'].notna() & df_valid['c'].notna() & df_valid['mass'].notna()
df_valid = df_valid[valid].copy()

z = df_valid['redshift'].values
mB = -2.5 * np.log10(df_valid['x0'].values) + 10.0
x1 = df_valid['x1'].values
c = df_valid['c'].values
mass = df_valid['mass'].values

# Tripp standardization
mass_step = mass - np.nanmedian(mass)
mB_corr = mB + 0.14 * x1 - 3.1 * c - 0.0 * mass_step

# Approximate M
dL_approx = C_LIGHT * z / 70
mu_approx = 5 * np.log10(dL_approx) + 25
M_guess = np.nanmedian(mB_corr - mu_approx)

# Gaussian prior on H0 from SH0ES: H0 ~ N(73.0, 1.4)
H0_prior_mean = 73.0
H0_prior_std = 1.4

def log_prior_h0(H0):
    return -0.5 * ((H0 - H0_prior_mean) / H0_prior_std)**2

def chi2_lcdm(params, z_train, mB_corr_train):
    H0, Om, OL, M = params
    if not (50 < H0 < 100 and 0 < Om < 1 and 0 < OL < 1 and -22 < M < -17):
        return 1e10
    dL = luminosity_distance_lcdm(z_train, H0, Om, OL)
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB_corr_train - M
    residuals = mu_obs - mu_model
    sigma = max(0.05, np.std(residuals))
    chi2 = np.sum(residuals**2 / sigma**2)
    prior_penalty = -2 * log_prior_h0(H0)
    return chi2 + prior_penalty

def chi2_nonaccel(params, z_train, mB_corr_train):
    H0, q0, M = params
    if not (50 < H0 < 100 and 0 < q0 < 5 and -22 < M < -17):
        return 1e10
    dL = luminosity_distance_nonaccel(z_train, H0, q0)
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = mB_corr_train - M
    residuals = mu_obs - mu_model
    sigma = max(0.05, np.std(residuals))
    chi2 = np.sum(residuals**2 / sigma**2)
    prior_penalty = -2 * log_prior_h0(H0)
    return chi2 + prior_penalty

def evaluate_model(params_lcdm, params_nonaccel, z_test, mB_corr_test):
    H0_l, Om_l, OL_l, M_l = params_lcdm
    H0_n, q0_n, M_n = params_nonaccel
    
    # LCDM on test set
    dL_l = luminosity_distance_lcdm(z_test, H0_l, Om_l, OL_l)
    mu_model_l = 5 * np.log10(dL_l) + 25
    mu_obs_l = mB_corr_test - M_l
    residuals_l = mu_obs_l - mu_model_l
    
    # Non-Accel on test set
    dL_n = luminosity_distance_nonaccel(z_test, H0_n, q0_n)
    mu_model_n = 5 * np.log10(dL_n) + 25
    mu_obs_n = mB_corr_test - M_n
    residuals_n = mu_obs_n - mu_model_n
    
    # Use pooled sigma
    sigma_pooled = np.sqrt((np.sum(residuals_l**2) + np.sum(residuals_n**2)) / (2 * len(z_test)))
    
    chi2_lcdm = np.sum(residuals_l**2 / sigma_pooled**2)
    chi2_nonaccel = np.sum(residuals_n**2 / sigma_pooled**2)
    
    return chi2_lcdm, chi2_nonaccel

print("=" * 70)
print("K-FOLD CROSS-VALIDATION BY REDSHIFT")
print("=" * 70)
print(f"Total SNe: {len(z)}")
print()

# K-fold cross-validation
k = 5
z_bins = np.linspace(z.min(), z.max(), k + 1)

results = []

for i in range(k):
    z_low = z_bins[i]
    z_high = z_bins[i + 1]
    
    # Test set: this redshift bin
    test_mask = (z >= z_low) & (z < z_high)
    if i == k - 1:  # Last bin includes upper boundary
        test_mask = (z >= z_low) & (z <= z_high)
    
    train_mask = ~test_mask
    
    z_train = z[train_mask]
    mB_corr_train = mB_corr[train_mask]
    z_test = z[test_mask]
    mB_corr_test = mB_corr[test_mask]
    
    print(f"Fold {i+1}/{k}: z = [{z_low:.3f}, {z_high:.3f}]")
    print(f"  Train: {len(z_train)} SNe, Test: {len(z_test)} SNe")
    
    # Fit models on training set
    result_lcdm = minimize(lambda p: chi2_lcdm(p, z_train, mB_corr_train), 
                          [73.0, 0.3, 0.7, M_guess], method='Nelder-Mead')
    result_nonaccel = minimize(lambda p: chi2_nonaccel(p, z_train, mB_corr_train), 
                              [73.0, 1.0, M_guess], method='Nelder-Mead')
    
    params_lcdm = result_lcdm.x
    params_nonaccel = result_nonaccel.x
    
    # Evaluate on test set
    chi2_lcdm_test, chi2_nonaccel_test = evaluate_model(params_lcdm, params_nonaccel, z_test, mB_corr_test)
    
    print(f"  LCDM params: H0={params_lcdm[0]:.2f}, Om={params_lcdm[1]:.3f}, OL={params_lcdm[2]:.3f}, M={params_lcdm[3]:.3f}")
    print(f"  Non-Accel params: H0={params_nonaccel[0]:.2f}, q0={params_nonaccel[1]:.3f}, M={params_nonaccel[2]:.3f}")
    print(f"  Test chi2: LCDM={chi2_lcdm_test:.1f}, Non-Accel={chi2_nonaccel_test:.1f}")
    print(f"  Winner: {'Non-Accel' if chi2_nonaccel_test < chi2_lcdm_test else 'LCDM'} (Δ={chi2_lcdm_test - chi2_nonaccel_test:.1f})")
    print()
    
    results.append({
        'fold': i + 1,
        'z_low': z_low,
        'z_high': z_high,
        'n_train': len(z_train),
        'n_test': len(z_test),
        'chi2_lcdm': chi2_lcdm_test,
        'chi2_nonaccel': chi2_nonaccel_test,
        'winner': 'Non-Accel' if chi2_nonaccel_test < chi2_lcdm_test else 'LCDM'
    })

# Summary
print("=" * 70)
print("CROSS-VALIDATION SUMMARY")
print("=" * 70)

non_accel_wins = sum(1 for r in results if r['winner'] == 'Non-Accel')
lcdm_wins = sum(1 for r in results if r['winner'] == 'LCDM')

print(f"Non-Accel wins: {non_accel_wins}/{k} folds")
print(f"LCDM wins: {lcdm_wins}/{k} folds")
print()

if non_accel_wins > lcdm_wins:
    print("RESULT: Non-Accel model wins cross-validation!")
else:
    print("RESULT: Mixed results — need further investigation")

print("=" * 70)
