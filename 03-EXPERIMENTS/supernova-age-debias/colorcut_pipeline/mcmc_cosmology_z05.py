#!/usr/bin/env python3
"""
MCMC Cosmology Analysis with z > 0.05 Cut (Final Run)

Full Bayesian parameter estimation with peculiar velocity correction applied.
Uses sample-specific Tripp parameters for best standardization.

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 14, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import emcee
from scipy.optimize import minimize
import corner
import matplotlib.pyplot as plt

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


def compute_distance_modulus(df, model, params):
    """Compute model distance modulus for given parameters."""
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
    return mu_model


def log_likelihood(params, df, model, alpha, beta, gamma):
    """Log likelihood for cosmological model."""
    df_corr = apply_tripp_standardization(df, alpha, beta, gamma)
    
    mu_model = compute_distance_modulus(df_corr, model, params)
    
    mu_obs = df_corr['mB_corr'].values - params[-1]
    
    residuals = mu_obs - mu_model
    
    sigma = np.std(residuals)
    sigma = max(sigma, 0.05)
    
    logL = -0.5 * np.sum(residuals**2 / sigma**2 + np.log(2 * np.pi * sigma**2))
    
    return logL


def log_prior(params, model):
    """Log prior for parameters."""
    if model == 'lcdm':
        H0, Om, OL, M = params
        if not (50 < H0 < 100 and 0 < Om < 1 and 0 < OL < 1 and -22 < M < -17):
            return -np.inf
        if not (0.5 < Om + OL < 1.5):
            return -np.inf
    elif model == 'nonaccel':
        H0, q0, M = params
        if not (50 < H0 < 100 and 0 < q0 < 5 and -22 < M < -17):
            return -np.inf
    else:
        return -np.inf
    
    return 0.0


def log_probability(params, df, model, alpha, beta, gamma):
    """Total log probability = log prior + log likelihood."""
    lp = log_prior(params, model)
    if not np.isfinite(lp):
        return -np.inf
    
    ll = log_likelihood(params, df, model, alpha, beta, gamma)
    if not np.isfinite(ll):
        return -np.inf
    
    return lp + ll


def run_mcmc(df, model, alpha, beta, gamma, n_walkers=32, n_steps=5000, burn_in=1000):
    """Run MCMC for cosmological model."""
    
    logger.info(f"🌌 Running MCMC for {model} model...")
    logger.info(f"   Standardization: α={alpha:.3f}, β={beta:.3f}, γ={gamma:.4f}")
    logger.info(f"   Walkers: {n_walkers}, Steps: {n_steps}, Burn-in: {burn_in}")
    
    if model == 'lcdm':
        ndim = 4
        initial = [72.0, 0.3, 0.7, -19.8]
        pos = initial + 1e-2 * np.random.randn(n_walkers, ndim)
        pos[:, 0] = np.clip(pos[:, 0], 50, 100)
        pos[:, 1] = np.clip(pos[:, 1], 0.1, 0.9)
        pos[:, 2] = np.clip(pos[:, 2], 0.1, 0.9)
        pos[:, 3] = np.clip(pos[:, 3], -22, -17)
    elif model == 'nonaccel':
        ndim = 3
        initial = [72.0, 1.0, -19.8]
        pos = initial + 1e-2 * np.random.randn(n_walkers, ndim)
        pos[:, 0] = np.clip(pos[:, 0], 50, 100)
        pos[:, 1] = np.clip(pos[:, 1], 0.1, 4.9)
        pos[:, 2] = np.clip(pos[:, 2], -22, -17)
    else:
        raise ValueError(f"Unknown model: {model}")
    
    sampler = emcee.EnsembleSampler(
        n_walkers, ndim, log_probability,
        args=(df, model, alpha, beta, gamma)
    )
    
    logger.info("   Running burn-in...")
    sampler.run_mcmc(pos, burn_in, progress=True)
    sampler.reset()
    
    logger.info("   Running production...")
    sampler.run_mcmc(None, n_steps, progress=True)
    
    samples = sampler.get_chain(flat=True)
    
    logger.info(f"   ✅ MCMC complete! Total samples: {len(samples)}")
    
    if model == 'lcdm':
        labels = ['H0', 'Ωm', 'ΩΛ', 'M']
    else:
        labels = ['H0', 'q0', 'M']
    
    logger.info("   Parameter estimates (median ± std):")
    for i, label in enumerate(labels):
        median = np.median(samples[:, i])
        std = np.std(samples[:, i])
        logger.info(f"     {label} = {median:.3f} ± {std:.3f}")
    
    return sampler, labels


def compute_bayes_factor(sampler_lcdm, sampler_nonaccel, df, alpha, beta, gamma):
    """Compute Bayes factor between ΛCDM and non-accelerating models."""
    
    logL_lcdm = np.max(sampler_lcdm.flatlnprobability)
    logL_nonaccel = np.max(sampler_nonaccel.flatlnprobability)
    
    n = len(df)
    k_lcdm = 4
    k_nonaccel = 3
    
    bic_lcdm = -2 * logL_lcdm + k_lcdm * np.log(n)
    bic_nonaccel = -2 * logL_nonaccel + k_nonaccel * np.log(n)
    
    delta_bic = bic_lcdm - bic_nonaccel
    
    if delta_bic < 0:
        bf = np.exp(-delta_bic / 2)
        winner = 'ΛCDM'
    else:
        bf = np.exp(delta_bic / 2)
        winner = 'Non-Accelerating'
    
    logger.info("📊 Bayesian Model Comparison:")
    logger.info(f"   ΛCDM BIC: {bic_lcdm:.1f}")
    logger.info(f"   Non-Accel BIC: {bic_nonaccel:.1f}")
    logger.info(f"   ΔBIC: {delta_bic:.1f}")
    logger.info(f"   Winner: {winner}")
    logger.info(f"   Bayes Factor: {bf:.1f}")
    
    return delta_bic, bf, winner


def plot_corner(sampler, labels, model_name, output_path):
    """Plot corner plot for MCMC samples."""
    samples = sampler.get_chain(flat=True)
    
    fig = corner.corner(
        samples, labels=labels,
        quantiles=[0.16, 0.5, 0.84],
        show_titles=True, title_kwargs={"fontsize": 12}
    )
    
    fig.suptitle(f'{model_name} Model - MCMC Posteriors (z > 0.05)', fontsize=14)
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"   📊 Corner plot saved to {output_path}")
    plt.close(fig)


def plot_trace(sampler, labels, model_name, output_path):
    """Plot trace plots for MCMC chains."""
    fig, axes = plt.subplots(len(labels), 1, figsize=(10, 2*len(labels)), sharex=True)
    
    if len(labels) == 1:
        axes = [axes]
    
    samples = sampler.get_chain()
    
    for i, label in enumerate(labels):
        ax = axes[i]
        ax.plot(samples[:, :, i], alpha=0.3, color='C0')
        ax.set_ylabel(label)
        ax.set_title(f'{label} trace')
    
    axes[-1].set_xlabel('Step')
    fig.suptitle(f'{model_name} Model - MCMC Traces (z > 0.05)', fontsize=14)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    logger.info(f"   📊 Trace plot saved to {output_path}")
    plt.close(fig)


def run_mcmc_analysis(sample_name, df, alpha, beta, gamma, output_dir='data/mcmc_z05'):
    """Run full MCMC analysis for a sample."""
    
    logger.info(f"\n{'='*70}")
    logger.info(f"🌌 MCMC Analysis (z > 0.05): {sample_name}")
    logger.info(f"{'='*70}")
    
    out_path = Path(output_dir) / sample_name
    out_path.mkdir(parents=True, exist_ok=True)
    
    logger.info("\n📊 Running ΛCDM model...")
    sampler_lcdm, labels_lcdm = run_mcmc(
        df, 'lcdm', alpha, beta, gamma,
        n_walkers=32, n_steps=3000, burn_in=500
    )
    
    logger.info("\n📊 Running Non-Accelerating model...")
    sampler_nonaccel, labels_nonaccel = run_mcmc(
        df, 'nonaccel', alpha, beta, gamma,
        n_walkers=32, n_steps=3000, burn_in=500
    )
    
    logger.info("\n📊 Model Comparison...")
    delta_bic, bf, winner = compute_bayes_factor(
        sampler_lcdm, sampler_nonaccel, df, alpha, beta, gamma
    )
    
    logger.info("\n📊 Generating plots...")
    plot_corner(sampler_lcdm, labels_lcdm, 'ΛCDM', out_path / 'corner_lcdm.png')
    plot_corner(sampler_nonaccel, labels_nonaccel, 'Non-Accelerating', out_path / 'corner_nonaccel.png')
    
    plot_trace(sampler_lcdm, labels_lcdm, 'ΛCDM', out_path / 'trace_lcdm.png')
    plot_trace(sampler_nonaccel, labels_nonaccel, 'Non-Accelerating', out_path / 'trace_nonaccel.png')
    
    np.save(out_path / 'samples_lcdm.npy', sampler_lcdm.get_chain(flat=True))
    np.save(out_path / 'samples_nonaccel.npy', sampler_nonaccel.get_chain(flat=True))
    
    logger.info(f"\n✅ MCMC analysis complete for {sample_name}!")
    logger.info(f"   Results saved to {out_path}")
    
    return {
        'sample': sample_name,
        'n_sne': len(df),
        'delta_bic': delta_bic,
        'bayes_factor': bf,
        'winner': winner,
        'output_dir': str(out_path),
    }


def main():
    """Run MCMC analysis for all samples with z > 0.05."""
    
    logger.info("🌌 Final MCMC Cosmology Analysis (z > 0.05)")
    logger.info("=" * 70)
    
    data_path = Path('data/ztf_dr2/ztfsniadr2_lite/tables')
    hosts = pd.read_csv(data_path / 'globalhost_data.csv')
    sne = pd.read_csv(data_path / 'snia_data.csv')
    df = sne.merge(hosts, on='ztfname', how='inner')
    
    # Apply z > 0.05 cut
    df = df[df['redshift'] > 0.05]
    
    logger.info(f"📊 Loaded {len(df)} ZTF SNe Ia (after z > 0.05 cut)")
    
    tripp_fits = pd.read_csv('data/tripp_parameter_fits.csv')
    tripp_dict = {row['sample']: row for _, row in tripp_fits.iterrows()}
    
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
    
    results = []
    
    for name, info in samples.items():
        sample_df = info['df']
        tripp = info['tripp']
        
        if len(sample_df) < 100:
            logger.warning(f"⚠️ Skipping {name} - too few SNe ({len(sample_df)})")
            continue
        
        result = run_mcmc_analysis(
            name, sample_df,
            tripp['alpha'], tripp['beta'], tripp['gamma']
        )
        results.append(result)
    
    logger.info("\n" + "=" * 70)
    logger.info("📊 FINAL MCMC ANALYSIS SUMMARY (z > 0.05)")
    logger.info("=" * 70)
    logger.info(f"{'Sample':<15} {'N':<8} {'ΔBIC':<12} {'Winner':<20} {'Bayes Factor'}")
    logger.info("-" * 70)
    
    for r in results:
        logger.info(f"{r['sample']:<15} {r['n_sne']:<8} {r['delta_bic']:<12.1f} {r['winner']:<20} {r['bayes_factor']:.1f}")
    
    logger.info("=" * 70)
    logger.info("✅ Final MCMC analysis complete!")
    logger.info("🍩 'Clean data = clean science!'")
    
    summary_df = pd.DataFrame(results)
    summary_df.to_csv('data/mcmc_z05_summary.csv', index=False)
    logger.info("💾 Summary saved to data/mcmc_z05_summary.csv")
    
    return results


if __name__ == "__main__":
    results = main()
