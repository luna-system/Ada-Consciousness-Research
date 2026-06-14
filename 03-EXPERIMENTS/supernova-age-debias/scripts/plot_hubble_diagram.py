"""
Plot Hubble Diagram and Cosmology Results

Visualizes:
- Hubble diagram (distance modulus vs redshift)
- Residuals from best-fit models
- Evolution-free sample selection
- Model comparison

Made with 💜 by Ada & Luna - The Consciousness Engineers
Date: June 13, 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def plot_hubble_diagram(cosmology_results, output_dir='plots'):
    """Plot Hubble diagram with model fits."""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    # Load results
    lcdm = cosmology_results['lcdm']
    nonaccel = cosmology_results['nonaccel']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Panel 1: Hubble Diagram
    ax = axes[0, 0]
    
    z = np.array(lcdm['z'])
    mu_obs = np.array(lcdm['mu_obs'])
    mu_lcdm = np.array(lcdm['mu_model'])
    mu_nonaccel = np.array(nonaccel['mu_model'])
    
    ax.scatter(z, mu_obs, c='blue', alpha=0.6, s=30, label='Evolution-Free SNe Ia')
    
    # Sort for smooth curves
    sort_idx = np.argsort(z)
    z_sorted = z[sort_idx]
    
    # Generate model curves
    z_fine = np.linspace(0.01, max(z), 100)
    
    # ΛCDM curve
    from scipy.integrate import quad
    def E_inv(z):
        return 1.0 / np.sqrt(0.3 * (1 + z)**3 + 0.7)
    
    mu_lcdm_curve = []
    for zi in z_fine:
        integral = quad(E_inv, 0, zi)[0]
        dL = 299792.458 * (1 + zi) * integral / lcdm['H0']
        mu = 5 * np.log10(dL * 1e6 / 10)
        mu_lcdm_curve.append(mu)
    
    # Non-accelerating curve
    mu_nonaccel_curve = []
    for zi in z_fine:
        dL = 299792.458 * zi / nonaccel['H0'] * (1 + (1 - nonaccel['q0']) * zi / 2)
        mu = 5 * np.log10(dL * 1e6 / 10)
        mu_nonaccel_curve.append(mu)
    
    ax.plot(z_fine, mu_lcdm_curve, 'r-', linewidth=2, label=f'ΛCDM (H₀={lcdm["H0"]:.1f})')
    ax.plot(z_fine, mu_nonaccel_curve, 'g--', linewidth=2, label=f'Non-Accel (q₀={nonaccel["q0"]:.2f})')
    
    ax.set_xlabel('Redshift z', fontsize=12)
    ax.set_ylabel('Distance Modulus μ', fontsize=12)
    ax.set_title('Hubble Diagram - Evolution-Free Sample', fontsize=14, fontweight='bold')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    
    # Panel 2: Residuals
    ax = axes[0, 1]
    
    residuals_lcdm = np.array(lcdm['residuals'])
    residuals_nonaccel = np.array(nonaccel['residuals'])
    
    ax.scatter(z, residuals_lcdm, c='red', alpha=0.6, s=30, label='ΛCDM residuals')
    ax.scatter(z, residuals_nonaccel, c='green', alpha=0.6, s=30, label='Non-Accel residuals')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    ax.set_xlabel('Redshift z', fontsize=12)
    ax.set_ylabel('Residuals (mag)', fontsize=12)
    ax.set_title('Hubble Residuals', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Panel 3: Age Distribution
    ax = axes[1, 0]
    
    # Load predictions for age distribution
    predictions_file = 'data/pantheon_age_predictions.csv'
    if Path(predictions_file).exists():
        predictions = pd.read_csv(predictions_file)
        
        if 'predicted_age' in predictions.columns:
            ages = predictions['predicted_age'].dropna()
            
            ax.hist(ages, bins=30, alpha=0.7, color='purple', edgecolor='black')
            ax.axvline(x=2.0, color='red', linestyle='--', linewidth=2, label='Young threshold (2 Gyr)')
            ax.axvline(x=ages.median(), color='blue', linestyle='-', linewidth=2, label=f'Median: {ages.median():.1f} Gyr')
            
            ax.set_xlabel('Predicted Age (Gyr)', fontsize=12)
            ax.set_ylabel('Number of Galaxies', fontsize=12)
            ax.set_title('Host Galaxy Age Distribution', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
    
    # Panel 4: Model Comparison
    ax = axes[1, 1]
    
    comparison = cosmology_results['comparison']
    
    models = ['ΛCDM', 'Non-Accel']
    chi2_vals = [lcdm['chi2'], nonaccel['chi2']]
    rms_vals = [lcdm['rms_residual'], nonaccel['rms_residual']]
    
    x = np.arange(len(models))
    width = 0.35
    
    ax2 = ax.twinx()
    
    bars1 = ax.bar(x - width/2, chi2_vals, width, label='χ²', color='skyblue', alpha=0.8)
    bars2 = ax2.bar(x + width/2, rms_vals, width, label='RMS (mag)', color='salmon', alpha=0.8)
    
    ax.set_xlabel('Model', fontsize=12)
    ax.set_ylabel('χ²', fontsize=12, color='skyblue')
    ax2.set_ylabel('RMS Residual (mag)', fontsize=12, color='salmon')
    ax.set_title('Model Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    
    # Add text with Δχ²
    delta_chi2 = comparison['delta_chi2']
    p_value = comparison['p_value']
    
    ax.text(0.5, 0.95, f'Δχ² = {delta_chi2:.2f}\np = {p_value:.4f}',
            transform=ax.transAxes, ha='center', va='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=11)
    
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/hubble_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"💾 Saved Hubble diagram to {output_dir}/hubble_diagram.png")


def plot_evolution_free_selection(output_dir='plots'):
    """Plot evolution-free sample selection criteria."""
    
    predictions_file = 'data/pantheon_age_predictions.csv'
    if not Path(predictions_file).exists():
        return
    
    predictions = pd.read_csv(predictions_file)
    
    if 'predicted_age' not in predictions.columns:
        return
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Panel 1: Age vs Redshift
    ax = axes[0]
    
    has_age = predictions['predicted_age'].notna()
    
    ax.scatter(predictions.loc[has_age, 'zHD'], predictions.loc[has_age, 'predicted_age'],
               c='blue', alpha=0.5, s=20, label='All hosts')
    
    if 'evolution_free' in predictions.columns:
        evo_free = predictions['evolution_free'] & has_age
        ax.scatter(predictions.loc[evo_free, 'zHD'], predictions.loc[evo_free, 'predicted_age'],
                   c='red', alpha=0.8, s=40, marker='*', label='Evolution-free')
    
    ax.axhline(y=2.0, color='red', linestyle='--', alpha=0.7, label='Age < 2 Gyr')
    ax.set_xlabel('Redshift z', fontsize=12)
    ax.set_ylabel('Predicted Age (Gyr)', fontsize=12)
    ax.set_title('Age vs Redshift', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Panel 2: Sample Composition
    ax = axes[1]
    
    if 'evolution_free' in predictions.columns:
        n_total = has_age.sum()
        n_young = (predictions['predicted_age'] < 2.0).sum()
        n_evolution_free = predictions['evolution_free'].sum()
        
        categories = ['Total\n(with ages)', 'Young\n(< 2 Gyr)', 'Evolution-Free']
        counts = [n_total, n_young, n_evolution_free]
        colors = ['lightblue', 'lightgreen', 'coral']
        
        bars = ax.bar(categories, counts, color=colors, alpha=0.8, edgecolor='black')
        
        # Add count labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(count)}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_ylabel('Number of Galaxies', fontsize=12)
        ax.set_title('Sample Selection', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/evolution_free_selection.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    logger.info(f"💾 Saved selection plot to {output_dir}/evolution_free_selection.png")


def main():
    """Main plotting pipeline."""
    logger.info("🎨 Plotting Hubble Diagram and Results")
    logger.info("=" * 60)
    
    # Load cosmology results
    results_file = 'data/cosmology_results.json'
    
    if not Path(results_file).exists():
        logger.error(f"❌ Cosmology results not found: {results_file}")
        logger.info("   Run fit_cosmology.py first!")
        return 1
    
    with open(results_file) as f:
        cosmology_results = json.load(f)
    
    # Create plots
    plot_hubble_diagram(cosmology_results)
    plot_evolution_free_selection()
    
    logger.info("=" * 60)
    logger.info("✅ Plotting complete!")
    logger.info("🍩 'Beautiful data tells beautiful stories!'")
    
    return 0


if __name__ == "__main__":
    exit(main())
