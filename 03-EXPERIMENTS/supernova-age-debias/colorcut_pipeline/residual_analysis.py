#!/usr/bin/env python3
"""
Residual Analysis for Supernova Cosmology

Diagnostic plots to identify systematic trends in Hubble residuals.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 14, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib.pyplot as plt
from scipy.optimize import minimize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

C_LIGHT = 299792.458  # km/s


def luminosity_distance_lcdm(z, H0, Om, OL):
    """ΛCDM luminosity distance in Mpc."""
    from scipy.integrate import quad
    
    def integrand(zp):
        return 1.0 / np.sqrt(Om * (1 + zp)**3 + OL)
    
    dL = np.zeros_like(z)
    for i, zi in enumerate(z):
        integral, _ = quad(integrand, 0, zi)
        dL[i] = (C_LIGHT / H0) * (1 + zi) * integral
    
    return dL


def luminosity_distance_nonaccel(z, H0, q0):
    """Non-accelerating luminosity distance (Mattig formula with 1+z)."""
    dL = (C_LIGHT / H0) * z * (1 + z) * (1 + 0.5 * (1 - q0) * z)
    return dL


def apply_tripp_standardization(df, alpha=0.14, beta=3.1, gamma=0.0):
    """Apply Tripp standardization to dataframe."""
    df = df.copy()
    if 'mB' not in df.columns:
        df['mB'] = -2.5 * np.log10(df['x0']) + 10.0
    mass_step = df['mass'] - np.nanmedian(df['mass'])
    df['mB_corr'] = df['mB'] + alpha * df['x1'] - beta * df['c'] - gamma * mass_step
    return df


def compute_residuals(df, model, params, alpha, beta, gamma):
    """Compute Hubble residuals for a given model."""
    df = apply_tripp_standardization(df, alpha, beta, gamma)
    
    z = df['redshift'].values
    
    if model == 'lcdm':
        H0, Om, OL, M = params
        dL = luminosity_distance_lcdm(z, H0, Om, OL)
    elif model == 'nonaccel':
        H0, q0, M = params
        dL = luminosity_distance_nonaccel(z, H0, q0)
    else:
        raise ValueError(f"Unknown model: {model}")
    
    mu_model = 5 * np.log10(dL) + 25
    mu_obs = df['mB_corr'].values - M
    
    residuals = mu_obs - mu_model
    return residuals


def plot_residuals_vs_variable(df, residuals, variable, variable_name, 
                               model_name, output_path, bins=10):
    """Plot residuals vs a given variable with binned statistics."""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Scatter plot
    ax1 = axes[0, 0]
    valid_mask = df[variable].notna() & ~np.isnan(residuals)
    ax1.scatter(df[variable][valid_mask], residuals[valid_mask], alpha=0.3, s=10)
    ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    ax1.set_xlabel(variable_name)
    ax1.set_ylabel('Hubble Residual (mag)')
    ax1.set_title(f'{model_name}: Residuals vs {variable_name}')
    
    # Binned means
    ax2 = axes[0, 1]
    # Create bins
    valid_data = df[variable].dropna()
    if len(valid_data) > 0:
        bin_edges = np.percentile(valid_data, np.linspace(0, 100, bins+1))
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_means = []
        bin_stds = []
        bin_counts = []
        
        for i in range(bins):
            mask = (df[variable] >= bin_edges[i]) & (df[variable] < bin_edges[i+1])
            if i == bins - 1:  # Include right edge for last bin
                mask = (df[variable] >= bin_edges[i]) & (df[variable] <= bin_edges[i+1])
            
            # Also mask valid residuals
            mask = mask & ~np.isnan(residuals)
            
            res_bin = residuals[mask]
            if len(res_bin) > 0:
                bin_means.append(np.mean(res_bin))
                bin_stds.append(np.std(res_bin) / np.sqrt(len(res_bin)))  # SEM
                bin_counts.append(len(res_bin))
            else:
                bin_means.append(np.nan)
                bin_stds.append(np.nan)
                bin_counts.append(0)
        
        bin_means = np.array(bin_means)
        bin_stds = np.array(bin_stds)
        
        valid = ~np.isnan(bin_means)
        if valid.sum() > 0:
            ax2.errorbar(bin_centers[valid], bin_means[valid], yerr=bin_stds[valid], 
                         fmt='o-', capsize=5, color='C0', label='Binned mean ± SEM')
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax2.set_xlabel(variable_name)
        ax2.set_ylabel('Mean Residual (mag)')
        ax2.set_title(f'{model_name}: Binned Residuals vs {variable_name}')
        ax2.legend()
    else:
        ax2.text(0.5, 0.5, 'No valid data', ha='center', va='center', transform=ax2.transAxes)
        ax2.set_title(f'{model_name}: No valid data')
    
    # Histogram of residuals
    ax3 = axes[1, 0]
    # Filter NaN values
    valid_res = residuals[~np.isnan(residuals)]
    if len(valid_res) > 0:
        ax3.hist(valid_res, bins=50, alpha=0.7, edgecolor='black')
        ax3.axvline(x=0, color='red', linestyle='--', alpha=0.5)
        ax3.set_xlabel('Hubble Residual (mag)')
        ax3.set_ylabel('Count')
        ax3.set_title(f'{model_name}: Residual Distribution (σ = {np.std(valid_res):.3f} mag)')
    else:
        ax3.text(0.5, 0.5, 'No valid residuals', ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title(f'{model_name}: No valid residuals')
    
    # Q-Q plot (residuals vs normal)
    ax4 = axes[1, 1]
    valid_res = residuals[~np.isnan(residuals)]
    if len(valid_res) > 0:
        from scipy import stats
        stats.probplot(valid_res, dist="norm", plot=ax4)
        ax4.set_title(f'{model_name}: Q-Q Plot (Normality Test)')
    else:
        ax4.text(0.5, 0.5, 'No valid residuals', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title(f'{model_name}: No valid residuals')
    
    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"   📊 Saved: {output_path}")
    plt.close(fig)


def plot_residuals_summary(df, residuals_lcdm, residuals_nonaccel, 
                           sample_name, output_dir):
    """Create comprehensive residual analysis plots."""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"\n📊 Residual Analysis: {sample_name}")
    logger.info("=" * 70)
    
    # Variables to check
    variables = [
        ('restframe_gz', 'Host Color (g-z)'),
        ('mass', 'Host Mass (log M☉)'),
        ('redshift', 'Redshift'),
        ('x1', 'Stretch (x1)'),
        ('c', 'Color (c)'),
    ]
    
    for var, var_name in variables:
        if var in df.columns and df[var].notna().sum() > 0:
            # ΛCDM
            plot_residuals_vs_variable(
                df, residuals_lcdm, var, var_name,
                f'ΛCDM - {sample_name}',
                output_path / f'residuals_lcdm_vs_{var}.png'
            )
            
            # Non-accelerating
            plot_residuals_vs_variable(
                df, residuals_nonaccel, var, var_name,
                f'Non-Accel - {sample_name}',
                output_path / f'residuals_nonaccel_vs_{var}.png'
            )
    
    # Summary statistics
    logger.info(f"\n📊 Residual Summary:")
    valid_lcdm = residuals_lcdm[~np.isnan(residuals_lcdm)]
    valid_nonaccel = residuals_nonaccel[~np.isnan(residuals_nonaccel)]
    logger.info(f"   ΛCDM:     mean = {np.mean(valid_lcdm):.4f}, σ = {np.std(valid_lcdm):.4f}, N = {len(valid_lcdm)}")
    logger.info(f"   Non-Accel: mean = {np.mean(valid_nonaccel):.4f}, σ = {np.std(valid_nonaccel):.4f}, N = {len(valid_nonaccel)}")
    
    # Shapiro-Wilk test for normality (sample size limit)
    from scipy import stats
    if len(valid_lcdm) > 0 and len(valid_lcdm) < 5000:
        _, p_lcdm = stats.shapiro(valid_lcdm)
        logger.info(f"   Normality (Shapiro-Wilk p-value):")
        logger.info(f"     ΛCDM:     p = {p_lcdm:.4f} {'✅ Normal' if p_lcdm > 0.05 else '❌ Non-normal'}")
    if len(valid_nonaccel) > 0 and len(valid_nonaccel) < 5000:
        _, p_nonaccel = stats.shapiro(valid_nonaccel)
        logger.info(f"     Non-Accel: p = {p_nonaccel:.4f} {'✅ Normal' if p_nonaccel > 0.05 else '❌ Non-normal'}")
    
    logger.info(f"✅ Residual analysis complete for {sample_name}!")


def main():
    """Run residual analysis for all samples."""
    
    logger.info("🌌 Residual Analysis for Supernova Cosmology")
    logger.info("=" * 70)
    
    # Load data
    data_path = Path('data/ztf_dr2/ztfsniadr2_lite/tables')
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia")
    
    # Load fitted Tripp parameters
    tripp_fits = pd.read_csv('data/tripp_parameter_fits.csv')
    tripp_dict = {row['sample']: row for _, row in tripp_fits.iterrows()}
    
    # Best-fit cosmology parameters (from previous analysis)
    # These should be updated with MCMC results when available!
    lcdm_params = {
        'full': [72.37, 0.3, 0.7, -19.842],
        'young': [72.96, 0.3, 0.7, -19.795],
        'old': [72.94, 0.3, 0.7, -19.845],
    }
    
    nonaccel_params = {
        'full': [50.00, 3.264, -20.542],
        'young': [50.00, 1.191, -20.637],
        'old': [50.00, 4.372, -20.512],
    }
    
    # Define samples
    samples = {
        'full': {
            'df': df,
            'tripp': tripp_dict.get('Full Sample', {'alpha': 0.145, 'beta': 3.198, 'gamma': -0.0002})
        },
        'young': {
            'df': df[(df['restframe_gz'] < 1.0) & (df['mass'] < 11.0)],
            'tripp': tripp_dict.get('Young (g-z < 1.0, mass < 11.0)', {'alpha': 0.136, 'beta': 3.215, 'gamma': 0.0})
        },
        'old': {
            'df': df[df['restframe_gz'] > 1.2],
            'tripp': tripp_dict.get('Old (g-z > 1.2)', {'alpha': 0.139, 'beta': 3.076, 'gamma': 0.0001})
        },
    }
    
    # Run residual analysis for each sample
    for name, info in samples.items():
        sample_df = info['df']
        tripp = info['tripp']
        
        if len(sample_df) < 100:
            logger.warning(f"⚠️ Skipping {name} - too few SNe ({len(sample_df)})")
            continue
        
        # Compute residuals
        res_lcdm = compute_residuals(
            sample_df, 'lcdm', lcdm_params[name],
            tripp['alpha'], tripp['beta'], tripp['gamma']
        )
        
        res_nonaccel = compute_residuals(
            sample_df, 'nonaccel', nonaccel_params[name],
            tripp['alpha'], tripp['beta'], tripp['gamma']
        )
        
        # Plot
        plot_residuals_summary(
            sample_df, res_lcdm, res_nonaccel,
            name, f'data/residuals/{name}'
        )
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ Residual analysis complete!")
    logger.info("🍩 'Diagnostics are the soul of good science!'")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
